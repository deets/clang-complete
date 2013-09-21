from unittest import TestCase
from cStringIO import StringIO

from clangcomplete.libclang import setup
from clangcomplete.api import (
    mainloop,
    AsyncSession,
    )

from .base import source_for_autocomplete

TEST_SOURCE = """
struct Foo {
   int bar;
   int baz;
   };
int main(int argc, const char* argv) {
   // Some comment
   Foo foo;
   foo./*POINT*/
   return 0;
}
"""

class TestAsyncAPI(TestCase):


    def setUp(self):
        setup()


    def test_mainloop(self):
        inf = StringIO("SHUTDOWN\n")
        outf = StringIO()
        mainloop("test.c", inf, outf)



    def test_sourcefile_cmd(self):
        session = AsyncSession("test.c")
        source = TEST_SOURCE
        inf = StringIO("source_length:%i\n%s\n\n" % (len(source), source))
        outf = StringIO()
        session.sourcefile(inf, outf)
        self.assertEqual(
            source,
            session.source,
            )



    def test_completion(self):
        session = AsyncSession("test.c")
        with session:
            point, source = source_for_autocomplete(TEST_SOURCE)
            inf = StringIO("row:%i\ncolumn:%i\nsource_length:%i\n%s\n\n" %
                           (point[0], point[1], len(source), source))
            outf = StringIO()
            session.completion(inf, outf)
            content = outf.getvalue()
            assert content.endswith("$")
            assert "COMPLETION: bar" in content
            assert "COMPLETION: baz" in content
