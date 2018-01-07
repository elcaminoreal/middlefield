"""
Test middlefield
"""

import functools
import json
import os
import tempfile
import unittest

import attr
import seashore

import middlefield


@attr.s(frozen=True)
class Files(object):

    """
    File-system interface that forbids interaction outside tempdir
    """

    def put_file(self, fname, content):
        """
        Create file with given content, if the file is temporary
        """
        if not fname.startswith(tempfile.gettempdir()):
            raise ValueError("tried to create a file outside sandbox",
                             tempfile.gettempdir(),
                             fname)
        with open(fname, 'wb') as filep:
            filep.write(content)


@attr.s(frozen=True)
class FakeShell(object):

    """
    Fake for seashore.Shell
    """

    _fs = attr.ib()

    def clone(self):
        """
        Create a duplicate
        """
        return attr.evolve(self)

    def batch(self, _cmd, *args, **kwargs):
        """
        Run commands, wait until they finish, return stdout/stderr
        """
        if _cmd[:2] == ['pip', 'wheel']:
            del _cmd[:2]
            idx = _cmd.index('--wheel-dir')
            wheel_dir = _cmd[idx+1]
            del _cmd[idx:idx+2]
            packages = [pkg.replace('==', '-') + '.whl'
                        for pkg in _cmd]
            for pkg in packages:
                self._fs.put_file(os.path.join(wheel_dir, pkg), b'')
            return
        raise NotImplementedError(_cmd, args, kwargs)


@attr.s
class FakeBuilder(object):

    """
    Fake for pex.pex_builder.PEXBuilder
    """

    _fs = attr.ib()
    _dists = attr.ib(init=False, default=attr.Factory(list))
    _shebang = '/usr/bin/env python'

    def set_entry_point(self, _entry_point):
        """
        Set the entry point
        """

    def set_shebang(self, shebang):
        """
        Set the shebang
        """
        self._shebang = shebang

    def add_dist_location(self, dist):
        """
        Add a wheel to the Pex file
        """
        self._dists.append(dist)

    def build(self, output):
        """
        Pretend to create a Pex file
        """
        summary = dict(shebang=self._shebang, dists=self._dists)
        self._fs.put_file(output, json.dumps(summary).encode('ascii'))


class InternalTest(unittest.TestCase):

    """
    Tests for the fakes
    """

    def test_invalid_file(self):
        """
        Creating files outside the tempdir errors out
        """
        my_files = Files()
        with self.assertRaises(ValueError):
            my_files.put_file('/', b'hello')

    def test_invalid_command(self):
        """
        Running unknown commands errors out
        """
        shell = FakeShell(Files())
        xctor = seashore.Executor(shell)
        with self.assertRaises(NotImplementedError):
            xctor.command(['do-stuff']).batch()


class APITest(unittest.TestCase):

    """
    Test the public API of middlefield
    """

    def test_graph(self):
        """
        The dependency graph has a pex builder and a seashore executor
        """
        graph = middlefield.COMMANDS.mkgraph(['pex_builder', 'executor'])
        builder = graph.pop('pex_builder')
        self.assertTrue(callable(builder.build))
        executor = graph.pop('executor')
        out, dummy_err = executor.command(['echo', 'hello']).batch()
        self.assertEquals(out.decode('ascii').strip(), 'hello')
        self.assertEquals(graph, {})

    def test_self_build(self):
        """
        Running "mf self-build" creates a wheel and builds it into a pex
        """
        my_files = Files()
        shell = FakeShell(my_files)
        executor = seashore.Executor(shell)
        builder = functools.partial(FakeBuilder, my_files)
        override = dict(executor=executor, pex_builder=builder)
        with tempfile.NamedTemporaryFile() as filep:
            middlefield.COMMANDS.run(['self-build',
                                      '--output', filep.name],
                                     override_dependencies=override)
            content = filep.read()
        res = json.loads(content.decode('ascii'))['dists']
        name = os.path.basename(res.pop(0))
        self.assertEquals(res, [])
        base, ext = os.path.splitext(name)
        self.assertEquals(ext, '.whl')
        dist_name, dummy_version = base.split('-')
        self.assertEquals(dist_name, 'middlefield')

    def test_self_build_shebang(self):
        """
        Running "mf self-build --shebang" sets the shebang line
        """
        my_files = Files()
        shell = FakeShell(my_files)
        executor = seashore.Executor(shell)
        builder = functools.partial(FakeBuilder, my_files)
        override = dict(executor=executor, pex_builder=builder)
        with tempfile.NamedTemporaryFile() as filep:
            middlefield.COMMANDS.run(['self-build',
                                      '--shebang', '/usr/bin/python',
                                      '--output', filep.name],
                                     override_dependencies=override)
            content = filep.read()
        res = json.loads(content.decode('ascii'))['shebang']
        self.assertEquals(res, '/usr/bin/python')
