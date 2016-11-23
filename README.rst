======================
Python runtime helpers 
======================

Helpers that provide Python runtime information to the callers
and allow modules to declare their runtime constraints.

Quick start
-----------

1. Add a copy of this directory to your ``PYTHONPATH`` or copy
   its contents to a package within your project. *If you place
   this code in a package, you'll have to qualify the following
   ``import`` statements with its name.*

2. Import the ``version`` module near the top of your code.

	import version

3. To declare the lowest supported Python version, add the following
   line next to the above ``import`` statement: 

	version.requirePythonVersion(3, 2)

   Replace ``3`` and ``2`` with applicable major and minor Python
   version numbers. The minor version number argument is optional. 

4. To retrieve the major and minor Python version numbers of the
   current runtime environment, read the ``version.Python`` tuple.

Please refer to the module's PyDoc comments for additional information.
