.. Copyright (c) Moshe Zadka
   See LICENSE for details.

Middlefield
===========

.. toctree::
   :maxdepth: 2

Middlefield is a framework for building build tools.
Since every build tool is different,
middlefield is plugin-based.

Every plugin must be registered with :code:`gather`.

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
