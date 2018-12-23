# vim:fileencoding=UTF-8 
#
# Copyright © 2015, 2018 Stan Livitski
#     
# Published under MIT License. See `LICENSE` file at the
# root of this repository for details.
#
"""
    Helpers that provide Python version information and runtime
    version control to other modules. 
    
    Helper functions that provide Python version information
    to the callers and allow other modules to declare the runtime
    versions they are compatible with.

    Key elements
    ------------
    requirePythonVersion : A function that checks Python's version
    against supplied constraints.
"""

import sys

def _inBoundaries(value, bounds):
    """
    Tell if an integer value is within a range.
       
    Parameters
    ----------
    value : int
        A value to be tested.
    bounds : int | tuple(int, int)
        Low boundary of the range, or a tuple of the form (low, high+1).

    Returns
    -------
    boolean
        Whether or not the value fell within the range
    """

    if type(bounds) is tuple:
        assert 2 == len(bounds)
        return bounds[0] <= value < bounds[1]
    else:
        assert type(bounds) is int
        return bounds <= value
    
"""
A tuple with major and minor version numbers of the Python environment
represented as integers.
"""

def requirePythonVersion(major, minor = None, legend = "The caller"):
    """
    Checks the Python runtime version against constraints provided
    by the caller.
    
    Checks the Python runtime version against constraints provided
    by the caller and raises an exception if the check fails. On
    success, returns nothing. 
    
    Parameters
    ----------
    major : int | tuple(int, int)
        Lowest major Python version supported by the caller, or
        a tuple of the form (lowest, highest+1).
    minor : int | tuple(int, int)
        Lowest minor Python version supported by the caller, or
        a tuple of the form (lowest, highest+1). If omitted, zero
        is assumed.
    legend : str
        A string describing the client to be included in error
        message.

    Raises
    ------
    Unsupported
        If the runtime version is not supported by the caller.

    See Also
    --------    
    Python : Python runtime version information known to this module

    Examples
    --------
    >>> requirePythonVersion(0)
    >>> requirePythonVersion(0, 0)
    >>> requirePythonVersion(999999999) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    .
    Unsupported: The caller requires major Python version 999999999 or newer, running ...
    >>> requirePythonVersion(1, 999999999) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    .
    Unsupported: The caller requires major Python version 1 or newer, minor version 999999999 or newer, running ...
    >>> requirePythonVersion((1, 999999999), legend='Legacy widget')
    >>> requirePythonVersion((0, 1), (1999999999, 999999999), legend='Legacy widget') #doctest: +ELLIPSIS
    Traceback (most recent call last):
    .
    Unsupported: Legacy widget requires major Python version 0 or newer (less than 1), minor version 1999999999 or newer (less than 999999999), running ...
    """

    if 'version_info' not in dir(sys):
        python = (1, 0, 0, 'unknown', 0)
    else:
        python = sys.version_info
    if _inBoundaries(python[0], major):
        if minor is None or _inBoundaries(python[1], minor):
            return
    constraints = ''
    if type(major) is tuple:
        constraints += "%d or newer (less than %d)" % major
    else:
        constraints += "%d or newer" % major
    if minor is not None:
        constraints += ", minor version "
        if type(minor) is tuple:
            constraints += "%d or newer (less than %d)" % minor
        else:
            constraints += "%d or newer" % minor
    
    raise Unsupported(
        "%s requires major Python version %s, running Python %s.%s"
        % ((legend, constraints) + python[:2])
    )

class Unsupported(Exception):
    """
    Raised by this module when a version check fails.

    Parameters
    ----------
    message : str
        Detailed error message
    """

    def __init__(self, message):
        super(Unsupported, self).__init__(message)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
