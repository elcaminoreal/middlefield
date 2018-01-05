import functools
import json
import os
import tempfile
import unittest

import attr
import middlefield
import seashore

@attr.s(frozen=True)
class Files(object):

    def putFile(self, fname, content):
        if not fname.startswith(tempfile.gettempdir()):
            raise ValueError("tried to create a file outside sandbox",
                             tempfile.gettempdir(),
                             fname)
        with open(fname, 'wb') as fp:
            fp.write(content)

@attr.s(frozen=True)
class FakeShell(object):
    _fs = attr.ib()

    def clone(self):
        return attr.evolve(self)

    def batch(self, _cmd, *args, **kwargs):
        if _cmd[:2] == ['pip', 'wheel']:
            del _cmd[:2]
            idx = _cmd.index('--wheel-dir')
            wheel_dir = _cmd[idx+1]
            del _cmd[idx:idx+2]
            packages = [pkg.replace('==', '-') + '.whl'
                        for pkg in _cmd]
            for pkg in packages:
                self._fs.putFile(os.path.join(wheel_dir, pkg), b'')
            return
        raise NotImplementedError(_cmd, args, kwargs)

@attr.s
class FakeBuilder(object):

    _fs = attr.ib()
    _dists = attr.ib(init=False, default=attr.Factory(list))

    def set_entry_point(self, ep):
        self.ep = ep

    def add_dist_location(self, dist):
        self._dists.append(dist)

    def build(self, output):
        self._fs.putFile(output, json.dumps(self._dists).encode('ascii'))

class InternalTest(unittest.TestCase):

    def test_invalid_file(self):
        fs = Files()
        with self.assertRaises(ValueError):
            fs.putFile('/', b'hello')

    def test_invalid_command(self):
        shell = FakeShell(Files())
        xctor = seashore.Executor(shell)
        with self.assertRaises(NotImplementedError):
            xctor.command(['do-stuff']).batch()

class APITest(unittest.TestCase):

    def test_graph(self):
        graph = middlefield.COMMANDS.mkgraph(['pex_builder', 'executor'])
        builder = graph.pop('pex_builder')
        self.assertTrue(callable(builder.build))
        executor = graph.pop('executor')
        out, err = executor.command(['echo', 'hello']).batch()
        self.assertEquals(out.decode('ascii').strip(), 'hello')
        self.assertEquals(graph, {})

    def test_self_build(self):
        fs = Files()
        shell = FakeShell(fs)
        executor = seashore.Executor(shell)
        builder = functools.partial(FakeBuilder, fs)
        override = dict(executor=executor, pex_builder=builder)
        with tempfile.NamedTemporaryFile() as filep:
            middlefield.COMMANDS.run(['self-build',
                                      '--output', filep.name],
                                     override_dependencies=override)
            content = filep.read()
        res = json.loads(content.decode('ascii'))
        name = os.path.basename(res.pop(0))
        self.assertEquals(res, [])
        base, ext = os.path.splitext(name)
        self.assertEquals(ext, '.whl')
        dist_name, version = base.split('-')
        self.assertEquals(dist_name, 'middlefield')
