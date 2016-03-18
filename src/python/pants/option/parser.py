# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import copy
import os
import re
import traceback
import warnings
from collections import defaultdict

import six

from pants.base.deprecated import check_deprecated_semver, deprecated_conditional
from pants.base.revision import Revision
from pants.option.arg_splitter import GLOBAL_SCOPE, GLOBAL_SCOPE_CONFIG_SECTION
from pants.option.custom_types import (ListValueComponent, dict_option, file_option, list_option,
                                       target_list_option, target_option)
from pants.option.errors import (BooleanOptionImplicitVal, BooleanOptionNameWithNo,
                                 BooleanOptionType, DeprecatedOptionError, FrozenRegistration,
                                 ImplicitValIsNone, InvalidAction, InvalidKwarg, InvalidMemberType,
                                 MemberTypeNotAllowed, NoOptionNames, OptionNameDash,
                                 OptionNameDoubleDash, ParseError, RecursiveSubsystemOption,
                                 Shadowing)
from pants.option.option_util import is_boolean_option, is_list_option
from pants.option.ranked_value import RankedValue
from pants.option.scope import ScopeInfo
from pants.version import PANTS_SEMVER


class Parser(object):
  """An argument parser in a hierarchy.

  Each node in the hierarchy is a 'scope': the root is the global scope, and the parent of
  a node is the scope it's immediately contained in. E.g., the 'compile.java' scope is
  a child of the 'compile' scope, which is a child of the global scope.

  Options registered on a parser are also registered transitively on all the scopes it encloses.
  Registration must be in outside-in order: we forbid registering options on an outer scope if
  we've already registered an option on one of its inner scopes. This is to ensure that
  re-registering the same option name on an inner scope correctly replaces the identically-named
  option from the outer scope.
  """

  class BooleanConversionError(ParseError):
    """Indicates a value other than 'True' or 'False' when attempting to parse a bool."""

  class FromfileError(ParseError):
    """Indicates a problem reading a value @fromfile."""

  @staticmethod
  def str_to_bool(s):
    if isinstance(s, six.string_types):
      if s.lower() == 'true':
        return True
      elif s.lower() == 'false':
        return False
      else:
        raise Parser.BooleanConversionError('Got "{0}". Expected "True" or "False".'.format(s))
    if s is True:
      return True
    elif s is False:
      return False
    else:
      raise Parser.BooleanConversionError('Got {0}. Expected True or False.'.format(s))

  def __init__(self, env, config, scope_info, parent_parser, option_tracker):
    """Create a Parser instance.

    :param env: a dict of environment variables.
    :param :class:`pants.option.config.Config` config: data from a config file.
    :param scope_info: the scope this parser acts for.
    :param parent_parser: the parser for the scope immediately enclosing this one, or
                          None if this is the global scope.
    :param option_tracker: the option tracker to record where option values came from.
    """
    self._env = env
    self._config = config
    self._scope_info = scope_info
    self._scope = self._scope_info.scope
    self._option_tracker = option_tracker

    # If True, no more registration is allowed on this parser.
    self._frozen = False

    # All option args registered with this parser.  Used to prevent shadowing args in inner scopes.
    self._known_args = set()

    # List of (args, kwargs) registration pairs, exactly as captured at registration time.
    self._option_registrations = []

    # A Parser instance, or None for the global scope parser.
    self._parent_parser = parent_parser

    # List of Parser instances.
    self._child_parsers = []

    if self._parent_parser:
      self._parent_parser._register_child_parser(self)

  @property
  def scope(self):
    return self._scope

  def walk(self, callback):
    """Invoke callback on this parser and its descendants, in depth-first order."""
    callback(self)
    for child in self._child_parsers:
      child.walk(callback)

  def _create_flag_value_map(self, flags):
    """Returns a map of flag -> list of values, based on the given flag strings.

    None signals no value given (e.g., -x, --foo).
    The value is a list because the user may specify the same flag multiple times, and that's
    sometimes OK (e.g., when appending to list-valued options).
    """
    flag_value_map = defaultdict(list)
    for flag in flags:
      key, has_equals_sign, flag_val = flag.partition('=')
      if not has_equals_sign:
        if not flag.startswith('--'):  # '-xfoo' style.
          key = flag[0:2]
          flag_val = flag[2:]
        if not flag_val:
          # Either a short option with no value or a long option with no equals sign.
          # Important so we can distinguish between no value ('--foo') and setting to an empty
          # string ('--foo='), for options with an implicit_value.
          flag_val = None
      flag_value_map[key].append(flag_val)
    return flag_value_map

  def parse_args(self, flags, namespace):
    """Set values for this parser's options on the namespace object."""
    flag_value_map = self._create_flag_value_map(flags)

    for args, kwargs in self._unnormalized_option_registrations_iter():
      self._validate(args, kwargs)
      dest = kwargs.get('dest') or self._select_dest(args)
      is_bool = is_boolean_option(kwargs)

      def consume_flag(flag):
        self._check_deprecated(dest, kwargs)
        del flag_value_map[flag]

      # Compute the values provided on the command line for this option.  Note that there may be
      # multiple values, for any combination of the following reasons:
      #   - The user used the same flag multiple times.
      #   - The user specified a boolean flag (--foo) and its inverse (--no-foo).
      #   - The option has multiple names, and the user used more than one of them.
      #
      # We also check if the option is deprecated, but we only do so if the option is explicitly
      # specified as a command-line flag, so we don't spam users with deprecated option values
      # specified in config, which isn't something they control.
      implicit_value = kwargs.get('implicit_value')
      flag_vals = []

      def add_flag_val(v):
        if v is None:
          if implicit_value is None:
            raise ParseError('Missing value for command line flag {} in {}'.format(
              arg, self._scope_str()))
          else:
            flag_vals.append(implicit_value)
        else:
          flag_vals.append(v)

      for arg in args:
        if is_bool:
          if arg in flag_value_map:
            flag_vals.append('true' if kwargs['action'] == 'store_true' else 'false')
            consume_flag(arg)
          elif self._inverse_arg(arg) in flag_value_map:
            flag_vals.append('false' if kwargs['action'] == 'store_true' else 'true')
            consume_flag(self._inverse_arg(arg))
        else:
          if arg in flag_value_map:
            for v in flag_value_map[arg]:
              add_flag_val(v)
            consume_flag(arg)

      # Get the value for this option, falling back to defaults as needed.
      try:
        val = self._compute_value(dest, kwargs, flag_vals)
      except ParseError as e:
        # Reraise a new exception with context on the option being processed at the time of error.
        # Note that other exception types can be raised here that are caught by ParseError (e.g.
        # BooleanConversionError), hence we reference the original exception type as type(e).
        raise type(e)(
          'Error computing value for {} in {} (may also be from PANTS_* environment variables).'
          '\nCaused by:\n{}'.format(', '.join(args), self._scope_str(), traceback.format_exc())
        )

      setattr(namespace, dest, val)

    # See if there are any unconsumed flags remaining.
    if flag_value_map:
      raise ParseError('Unrecognized command line flags on {}: {}'.format(
        self._scope_str(), ', '.join(flag_value_map.keys())))

    return namespace

  def option_registrations_iter(self):
    """Returns an iterator over the normalized registration arguments of each option in this parser.

    Useful for generating help and other documentation.

    Each yielded item is an (args, kwargs) pair, as passed to register(), except that kwargs
    will be normalized in the following ways:
      - It will always have 'dest' explicitly set.
      - It will always have 'default' explicitly set, and the value will be a RankedValue.
      - For recursive options, the original registrar will also have 'recursive_root' set.

    Note that recursive options we inherit from a parent will also be yielded here, with
    the correctly-scoped default value.
    """
    def normalize_kwargs(args, orig_kwargs):
      nkwargs = copy.copy(orig_kwargs)
      dest = nkwargs.get('dest') or self._select_dest(args)
      nkwargs['dest'] = dest
      if not ('default' in nkwargs and isinstance(nkwargs['default'], RankedValue)):
        nkwargs['default'] = self._compute_value(dest, nkwargs, [])
      return nkwargs

    # First yield any recursive options we inherit from our parent.
    if self._parent_parser:
      for args, kwargs in self._parent_parser._recursive_option_registration_args():
        yield args, normalize_kwargs(args, kwargs)

    # Then yield our directly-registered options.
    # This must come after yielding inherited recursive options, so we can detect shadowing.
    for args, kwargs in self._option_registrations:
      normalized_kwargs = normalize_kwargs(args, kwargs)
      if 'recursive' in normalized_kwargs:
        # If we're the original registrar, make sure we can distinguish that.
        normalized_kwargs['recursive_root'] = True
      yield args, normalized_kwargs

  def _unnormalized_option_registrations_iter(self):
    """Returns an iterator over the raw registration arguments of each option in this parser.

    Each yielded item is an (args, kwargs) pair, exactly as passed to register().

    Note that recursive options we inherit from a parent will also be yielded here.
    """
    # First yield any recursive options we inherit from our parent.
    if self._parent_parser:
      for args, kwargs in self._parent_parser._recursive_option_registration_args():
        yield args, kwargs
    # Then yield our directly-registered options.
    for args, kwargs in self._option_registrations:
      if 'recursive' in kwargs and self._scope_info.category == ScopeInfo.SUBSYSTEM:
        raise RecursiveSubsystemOption(self.scope, args[0])
      yield args, kwargs

  def _recursive_option_registration_args(self):
    """Yield args, kwargs pairs for just our recursive options.

    Includes all the options we inherit recursively from our ancestors.
    """
    if self._parent_parser:
      for args, kwargs in self._parent_parser._recursive_option_registration_args():
        yield args, kwargs
    for args, kwargs in self._option_registrations:
      # Note that all subsystem options are implicitly recursive: a subscope of a subsystem
      # scope is another (optionable-specific) instance of the same subsystem, so it needs
      # all the same options.
      if self._scope_info.category == ScopeInfo.SUBSYSTEM or 'recursive' in kwargs:
        yield args, kwargs

  def register(self, *args, **kwargs):
    """Register an option."""
    if self._frozen:
      raise FrozenRegistration(self.scope, args[0])

    # Prevent further registration in enclosing scopes.
    ancestor = self._parent_parser
    while ancestor:
      ancestor._freeze()
      ancestor = ancestor._parent_parser

    # Temporary munging to effectively turn action='append' options into list options,
    # for uniform handling.  From here on, action='append' is an error.
    # TODO: Remove after action='append' deprecation.
    if kwargs.get('action') == 'append':
      if 'type' in kwargs:
        kwargs['member_type'] = kwargs['type']
      kwargs['type'] = list_option
      del kwargs['action']

    # Temporary munging to effectively turn type='target_list_option' options into list options,
    # with member type 'target_option', for uniform handling.
    # TODO: Remove after target_list_option deprecation.
    if kwargs.get('type') == target_list_option:
      kwargs['type'] = list_option
      kwargs['member_type'] = target_option
      deprecated_conditional(lambda: True, '0.0.80',
                             'target_list_option is deprecated for option {} in scope {}. '
                             'Use type=list_option, member_type=target_option.'.format(
                               args[0], self.scope
                             ))

    # Record the args. We'll do the underlying parsing on-demand.
    self._option_registrations.append((args, kwargs))
    if self._parent_parser:
      for arg in args:
        existing_scope = self._parent_parser._existing_scope(arg)
        if existing_scope is not None:
          raise Shadowing(self.scope, arg, outer_scope=self._scope_str(existing_scope))
    self._known_args.update(args)

  def _check_deprecated(self, dest, kwargs):
    """Checks option for deprecation and issues a warning/error if necessary."""
    deprecated_ver = kwargs.get('deprecated_version', None)
    if deprecated_ver is not None:
      msg = (
        "Option '{dest}' in {scope} is deprecated and removed in version {removal_version}. {hint}"
      ).format(dest=dest,
               scope=self._scope_str(),
               removal_version=deprecated_ver,
               hint=kwargs.get('deprecated_hint', ''))

      if PANTS_SEMVER >= Revision.semver(deprecated_ver):
        # Once we've hit the deprecated_version, raise an error instead of warning. This allows for
        # more actionable options hinting to continue beyond the deprecation period until removal.
        raise DeprecatedOptionError(msg)
      else:
        # Out of range stacklevel to suppress printing src line.
        warnings.warn('*** {}'.format(msg), DeprecationWarning, stacklevel=9999)

  _allowed_registration_kwargs = {
    'type', 'member_type', 'action', 'choices', 'dest', 'default', 'implicit_value', 'metavar',
    'help', 'advanced', 'recursive', 'recursive_root', 'registering_class',
    'fingerprint', 'deprecated_version', 'deprecated_hint', 'removal_version', 'fromfile'
  }

  # TODO: Get rid of action entirely.  Replace with type=bool.
  _allowed_actions = {
    'store', 'store_true', 'store_false'
  }

  _allowed_member_types = {
    str, int, float, tuple, dict_option, file_option, target_option
  }

  def _validate(self, args, kwargs):
    """Validate option registration arguments."""
    def error(exception_type, arg_name=None, **msg_kwargs):
      if arg_name is None:
        arg_name = args[0] if args else '<unknown>'
      raise exception_type(self.scope, arg_name, **msg_kwargs)

    if not args:
      error(NoOptionNames)
    # validate args.
    for arg in args:
      if not arg.startswith('-'):
        error(OptionNameDash, arg_name=arg)
      if not arg.startswith('--') and len(arg) > 2:
        error(OptionNameDoubleDash, arg_name=arg)

    # Validate kwargs.
    if kwargs.get('action', 'store') not in self._allowed_actions:
      error(InvalidAction, action=kwargs['action'])

    if is_boolean_option(kwargs) and 'type' in kwargs:
      error(BooleanOptionType)

    if 'implicit_value' in kwargs:
      if is_boolean_option(kwargs):
        error(BooleanOptionImplicitVal)
      elif kwargs['implicit_value'] is None:
        error(ImplicitValIsNone)

    if 'member_type' in kwargs and kwargs.get('type', str) != list_option:
      error(MemberTypeNotAllowed, type_=kwargs.get('type', str))

    if kwargs.get('member_type', str) not in self._allowed_member_types:
      error(InvalidMemberType, member_type=kwargs.get('member_type', str))

    for kwarg in kwargs:
      if kwarg not in self._allowed_registration_kwargs:
        error(InvalidKwarg, kwarg=kwarg)

    deprecated_ver = kwargs.get('deprecated_version')
    if deprecated_ver is not None:
      check_deprecated_semver(deprecated_ver, check_expired=False)

  def _existing_scope(self, arg):
    if arg in self._known_args:
      return self._scope
    elif self._parent_parser:
      return self._parent_parser._existing_scope(arg)
    else:
      return None

  _ENV_SANITIZER_RE = re.compile(r'[.-]')

  def _select_dest(self, args):
    """Select the dest name for the option.

    '--foo-bar' -> 'foo_bar' and '-x' -> 'x'.
    """
    arg = next((a for a in args if a.startswith('--')), args[0])
    return arg.lstrip('-').replace('-', '_')

  def _compute_value(self, dest, kwargs, flag_val_strs):
    """Compute the value to use for an option.

    The source of the default value is chosen according to the ranking in RankedValue.
    """
    # Helper function to convert a string to a value of the option's type.
    def to_value_type(val_str):
      if val_str is None:
        return None
      elif is_boolean_option(kwargs):
        return self.str_to_bool(val_str)
      else:
        return kwargs.get('type', str)(val_str)

    # Helper function to expand a fromfile=True value string, if needed.
    def expand(val_str):
      if is_fromfile and val_str and val_str.startswith('@'):
        if val_str.startswith('@@'):   # Support a literal @ for fromfile values via @@.
          return val_str[1:]
        else:
          fromfile = val_str[1:]
          try:
            with open(fromfile) as fp:
              return fp.read().strip()
          except IOError as e:
            raise self.FromfileError('Failed to read {} in {} from file {}: {}'.format(
                dest, self._scope_str(), fromfile, e))
      else:
        return val_str

    # Validate that fromfile=True is only applied to option types that allow it.
    # TODO: Why? Seems like this should always work. It may be silly to have a boolean
    # literal in a file, but I don't see why we should go out of our way to prevent it.
    is_fromfile = kwargs.get('fromfile', False)
    action = kwargs.get('action')
    if is_fromfile and action:
      raise ParseError('Cannot fromfile {} with an action ({}) in scope {}'
                       .format(dest, action, self._scope))

    # Get value from config files, and capture details about its derivation.
    config_details = None
    config_section = GLOBAL_SCOPE_CONFIG_SECTION if self._scope == GLOBAL_SCOPE else self._scope
    config_val_str = expand(self._config.get(config_section, dest, default=None))
    config_source_file = self._config.get_source_for_option(config_section, dest)
    if config_source_file is not None:
      config_source_file = os.path.relpath(config_source_file)
      config_details = 'in {}'.format(config_source_file)

    # Get value from environment, and capture details about its derivation.
    udest = dest.upper()
    if self._scope == GLOBAL_SCOPE:
      # For convenience, we allow three forms of env var for global scope options.
      # The fully-specified env var is PANTS_GLOBAL_FOO, which is uniform with PANTS_<SCOPE>_FOO
      # for all the other scopes.  However we also allow simply PANTS_FOO. And if the option name
      # itself starts with 'pants-' then we also allow simply FOO. E.g., PANTS_WORKDIR instead of
      # PANTS_PANTS_WORKDIR or PANTS_GLOBAL_PANTS_WORKDIR. We take the first specified value we
      # find, in this order: PANTS_GLOBAL_FOO, PANTS_FOO, FOO.
      env_vars = ['PANTS_DEFAULT_{0}'.format(udest),  # Temporary, until deprecation is complete.
                  'PANTS_GLOBAL_{0}'.format(udest), 'PANTS_{0}'.format(udest)]
      if udest.startswith('PANTS_'):
        env_vars.append(udest)
    else:
      sanitized_env_var_scope = self._ENV_SANITIZER_RE.sub('_', self._scope.upper())
      env_vars = ['PANTS_{0}_{1}'.format(sanitized_env_var_scope, udest)]

    env_val_str = None
    env_details = None
    if self._env:
      for env_var in env_vars:
        if env_var in self._env:
          deprecated_conditional(lambda: env_var == 'PANTS_DEFAULT_{0}'.format(udest), '0.0.80',
                                 'Use PANTS_GLOBAL_{0} instead of PANTS_DEFAULT_{0}'.format(udest))
          env_val_str = expand(self._env.get(env_var))
          env_details = 'from env var {}'.format(env_var)
          break

    # Get value from cmd-line flags.
    flag_vals = [to_value_type(expand(x)) for x in flag_val_strs]
    if is_list_option(kwargs):
      # Note: It's important to set flag_val to None if no flags were specified, so we can
      # distinguish between no flags set vs. explicit setting of the value to [].
      flag_val = ListValueComponent.merge(flag_vals) if flag_vals else None
    elif len(flag_vals) > 1:
      raise ParseError('Multiple cmd line flags specified for option {} in {}'.format(
          dest, self._scope_str()))
    elif len(flag_vals) == 1:
      flag_val = flag_vals[0]
    else:
      flag_val = None

    # Rank all available values.
    # Note that some of these values may already be of the value type, but type conversion
    # is idempotent, so this is OK.
    values_to_rank = [to_value_type(x) for x in
                      [flag_val, env_val_str, config_val_str, kwargs.get('default'), None]]
    # Note that ranked_vals will always have at least one element, and no elements will be None.
    ranked_vals = list(reversed(list(RankedValue.prioritized_iter(*values_to_rank))))

    # Record info about the derivation of each of the values.
    for ranked_val in ranked_vals:
      if ranked_val.rank == RankedValue.CONFIG:
        details = config_details
      elif ranked_val.rank == RankedValue.ENVIRONMENT:
        details = env_details
      else:
        details = None
      self._option_tracker.record_option(scope=self._scope,
                                         option=dest,
                                         value=ranked_val.value,
                                         rank=ranked_val.rank,
                                         deprecation_version=kwargs.get('deprecated_version'),
                                         details=details)

    # Helper function to check various validity constraints on final option values.
    def check(val):
      if val is not None:
        choices = kwargs.get('choices')
        if choices is not None and val not in choices:
          raise ParseError('{} is not an allowed value for option {} in {}. '
                           'Must be one of: {}'.format(val, dest, self._scope_str(), choices))
        elif kwargs.get('type') == file_option and not os.path.isfile(val):
          raise ParseError('File value {} for option {} in {} does not exist.'.format(
              val, dest, self._scope_str()))

    # Generate the final value from all available values, and check that it (or its members,
    # if a list) are in the set of allowed choices.
    if is_list_option(kwargs):
      merged_rank = ranked_vals[-1].rank
      merged_val = ListValueComponent.merge(
          [rv.value for rv in ranked_vals if rv.value is not None]).val
      merged_val = [kwargs.get('member_type', str)(x) for x in merged_val]
      map(check, merged_val)
      ret = RankedValue(merged_rank, merged_val)
    else:
      ret = ranked_vals[-1]
      check(ret.value)

    # All done!
    return ret

  def _inverse_arg(self, arg):
    if arg.startswith('--'):
      if arg.startswith('--no-'):
        raise BooleanOptionNameWithNo(self.scope, arg)
      return '--no-{}'.format(arg[2:])
    else:
      return None

  def _register_child_parser(self, child):
    self._child_parsers.append(child)

  def _freeze(self):
    self._frozen = True

  def _scope_str(self, scope=None):
    scope = scope or self.scope
    return 'global scope' if scope == GLOBAL_SCOPE else "scope '{}'".format(scope)

  def __str__(self):
    return 'Parser({})'.format(self._scope)
