# vim:fileencoding=UTF-8 
#
# Copyright © 2016, 2019 Stan Livitski
#     
#    Licensed under the Apache License, Version 2.0 with modifications,
#  (the "License"); you may not use this file except in compliance
#  with the License. You may obtain a copy of the License at
#
#   https://raw.githubusercontent.com/StanLivitski/EPyColl/master/LICENSE
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
    Helpers for obtaining information about callable
    objects and have the same code run different types of callables.

    Key elements
    ------------
    prepare_call : A function that unwraps a callable, if necessary,
        and tells whether the resulting object requires the ``self``
        argument to be called.
    call : Calls the target object, prepending ``self``
        argument if necessary.
"""

import version

version.requirePythonVersion(3, 3)

def call(callable_, globals_, self, *args, **kwargs):
    """
    Calls the target object, prepending ``self`` argument to
    the argument list if necessary.
    
    Parameters
    ----------
    callable_ : callable
        Reference to a function or method object or wrapper.
    globals_ : dict
        The dictionary of the module defining the target callable,
        or the local dictionary for the scope in which the target callable's
        container is defined.
    self : object | None
        The value to be passed as ``self`` argument, if
        required by the target.
    args : collections.Iterable
        Any positional arguments, excluding ``self``.
    kwargs : collections.Mapping
        Any keyword arguments, excluding ``self``.

    Returns
    -------
    object | None
        Any value returned by the call.

    Raises
    ------
    TypeError
        If the argument is not callable or has unknown type.
    BaseException
        Any exception thrown by the call.

    See Also
    --------    
    prepare_call : processes the callable before making the call
    """

    target, selfNeeded = prepare_call(callable_, globals_)
    _args = [ self ] if selfNeeded else []
    _args.extend(args)
    return target(*_args, **kwargs)

def prepare_call(callable_, globals_):
    """
    Unwrap method decorators applied to ``callable_`` and
    tell whether the resulting object requires the ``self``
    argument to be called.
    
    Dereferences ``@staticmethod`` and ``@classmethod`` decorators
    and returns a flag telling whether explicit ``self`` argument
    is required. This method may be used when preparing class
    definitions (e.g. decorating methods) as well as at runtime.
    
    Parameters
    ----------
    callable_ : callable
        Reference to a function or method object or wrapper.
    globals_ : dict
        The dictionary of the module defining the target callable,
        or the local dictionary for the scope in which the target callable's
        container is defined. If the container has not yet been defined
        (e.g. when processing a decorator) this mapping should also contain
        its future qualified name mapped to the ``object`` type value.

    Returns
    -------
    callable
        Dereferenced callable object.
    boolean
        A flag telling whether explicit ``self`` argument must
        be on the argument list.

    Raises
    ------
    TypeError
        If the argument is not callable or has unknown type.

    """

    bindable = None
    if not callable(callable_) and hasattr(callable_, '__func__'):
        if isinstance(callable_, staticmethod):
            bindable = False
        callable_ = callable_.__func__
    if not callable(callable_):
        raise TypeError('Argument of type %s is not callable' % type(callable_).__name__)
    if hasattr(callable_, '__self__'):
        bindable = False
    if bindable is None:
        prefix = callable_.__qualname__[:-len(callable_.__name__)]
        if prefix:
            assert '.' == prefix[-1]
            prefix = prefix[:-1]
            try:
                bindable = isinstance(eval(prefix, globals_), type)
            except:
                bindable = False
        else:
            bindable = False
    return callable_, bindable
