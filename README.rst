..
   Copyright © 2016, 2019 Stan Livitski
   
   Licensed under the Apache License, Version 2.0 with modifications,
   (the "License"); you may not use this file except in compliance
   with the License. You may obtain a copy of the License at
   
    https://raw.githubusercontent.com/StanLivitski/EPyColl/master/LICENSE
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

======================
Python runtime helpers 
======================

Helpers that provide Python runtime information to the callers
and allow modules to declare their runtime constraints.

Quick start
-----------

1. Add a copy of this directory to your ``PYTHONPATH`` or copy
   its contents to a package within your project. *If you place
   this code in a package, you'll have to qualify the following*
   ``import`` *statements with its name.*

2. Import the ``version`` module near the top of your code. ::

       import version

3. To declare the lowest supported Python version, add the following
   line next to the above ``import`` statement::

       version.requirePythonVersion(3, 2)

   Replace ``3`` and ``2`` with applicable major and minor Python
   version numbers. The minor version number argument is optional. 

4. To retrieve the major and minor Python version numbers of the
   current runtime environment, read the ``version.Python`` tuple.

5. To use other modules or obtain additional information please
   refer to the modules' PyDoc comments.
