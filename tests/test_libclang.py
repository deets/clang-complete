from ctypes import (
    byref,
    )
import unittest

from clangcomplete.libclang import (
    setup,
    libclang,
    CXUnsavedFile,
    CXCursorVisitor,
    CXChildVisitResult,
    CXCompletionChunkKind,
    )


def source_for_autocomplete(source, marker="/*POINT*/"):
    for row, line in enumerate(source.split("\n"), start=1):
        if marker in line:
            col = line.index(marker) + 1
            return (row, col), source.replace(marker, "")


class TestLibClang(unittest.TestCase):


    def test_setup(self):
        setup()
        idx = libclang.clang_createIndex(0, 0)
        source = """int main(int argc, char** argv) { return 0; }"""
        test_c = CXUnsavedFile(
            "test.c",
            source,
            len(source),
            )
        tu = libclang.clang_parseTranslationUnit(
            idx,
            "test.c",
            None,
            0,
            byref(test_c),
            1,
            0,
            )

        print libclang.clang_reparseTranslationUnit(
            tu,
            1,
            byref(test_c),
            0)

        def visitor(parent, cursor, client_data):
            print "parent", parent, "cursor", cursor
            print "usr", cursor.usr, "spelling", cursor.spelling
            return CXChildVisitResult.CXChildVisit_Recurse

        c_visitor = CXCursorVisitor(visitor)

        libclang.clang_visitChildren(
            libclang.clang_getTranslationUnitCursor(tu),
            c_visitor,
            0,
            )

        self.assertEqual(
            "test.c",
            libclang.clang_getTranslationUnitSpelling(tu),
            )

        libclang.clang_disposeTranslationUnit(tu)
        libclang.clang_disposeIndex(idx)



    def test_auto_completion(self):
        source = """

struct Foo {
  int bar;
  int baz;
  int padamm;
};

int main(int argc, char** argv) {
  Foo foo;
  foo./*POINT*/
}
"""
        point, source = source_for_autocomplete(source)
        self.assertEqual(
            (11, 7),
            point,
            )
        assert "/*POINT*/" not in source
        test_c = CXUnsavedFile(
            "test.c",
            source,
            len(source),
            )
        idx = libclang.clang_createIndex(0, 0)
        tu = libclang.clang_parseTranslationUnit(
            idx,
            "test.c",
            None,
            0,
            byref(test_c),
            1,
            0,
            )

        ac_results = libclang.clang_codeCompleteAt(tu, "test.c", point[0], point[1], byref(test_c), 1, 0)
        self.assertEqual(
            ac_results.contents.NumResults,
            3,
            )
        #libclang.clang_sortCodeCompletionResults(ac_results.contents.Results, ac_results.contents.NumResults)
        for i in xrange(1, 2):#xrange(ac_results.contents.NumResults):
            import pdb; pdb.set_trace()
            cstring = ac_results.contents.Results[i].CompletionString
            for chunk_num in xrange(libclang.clang_getNumCompletionChunks(cstring)):
                kind = libclang.clang_getCompletionChunkKind(cstring, chunk_num)
                if kind == CXCompletionChunkKind.CXCompletionChunk_TypedText:
                    print libclang.clang_getCompletionChunkText(cstring, chunk_num)

        libclang.clang_disposeCodeCompleteResults(ac_results)

