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
    )


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


