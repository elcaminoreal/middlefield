import functools
import unittest

import attr
import middlefield
import seashore

class MemoryFS(object):
    pass

@attr.s(frozen=True)
class FakeShell(object):
    _fs = attr.ib()

    def clone(self):
        return attr.evolve(self)

    def batch(self, _cmd, *args, **kwargs):
        raise NotImplementedError(_cmd, args, kwargs)

@attr.s
class FakeBuilder(object):

    _fs = attr.ib()

    def set_entry_point(self, ep):
        self.ep = ep

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
        fs = MemoryFS()
        shell = FakeShell(fs)
        executor = seashore.Executor(shell)
        builder = functools.partial(FakeBuilder, fs)
        override = dict(executor=executor, pex_builder=builder)
        middlefield.COMMANDS.run(['self-build', '--output', '/foo'],
                                 override_dependencies=override)
