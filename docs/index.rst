.. Copyright (c) Moshe Zadka
   See LICENSE for details.

Middlefield
===========

.. toctree::
   :maxdepth: 2

Middlefield is a framework for building build tools.
Since every build tool is different,
middlefield is plugin-based.

Every plugin must be registered with :code:`gather`
in its :code:`setup.py`.

Registering
-----------

The :code:`middlefield.COMMAND` object collects dependencies and commands.
It is an :code:`elcaminoreal.Commands`.

Built-in functionality
----------------------

Middlefield itself registers two important things:

* :code:`executor` is a dependency that maps to a :code:`seashore.Executor`. 
* :code:`self-build` is a command that will rebuild a middlefield pex --
  with the requested packages added (for plugins)

Self Build
----------

The :code:`self-build` commands builds a :code:`middlefield`-based
PEX with the requested plugins.
This allows distributing a single file which knows which middlefield
plugins to use

Options:

* :code:`--requirements` takes a :code:`requirements.txt` file.
  This option can be given several times (or none)
* :code:`--package` specifies a PyPI package name.
  This option can be given several times (or none)
* :code:`--output` specifies the output file.
  The file will be executable.
  It is suggested that the name will be something similar to :code:`mf`
  or :code:`mf.pex`,
  for consistency.
* :code:`--shebang` specifies the shebang line the interpreter will use.
  Often, :code:`/usr/bin/env python3` is a good choice --
  but that depends on the way the Python interpreter is installed.
