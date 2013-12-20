#!/usr/bin/env python2.7
import os
import sys
import subprocess
import logging
from cStringIO import StringIO

from ctypes import (
    byref,
    c_char_p,
    )

from abl.util import Bunch

from .libclang import (
    libclang,
    CXUnsavedFile,
    CXCompletionChunkKind,
    setup,
    )

from .util import source_for_autocomplete

logger = logging.getLogger(__name__)


class TranslationUnit(object):

    def __init__(self, idx, point, unsaved_file, args):
        self.idx = idx
        self.point = point
        self.unsaved_file = unsaved_file
        self.filename = unsaved_file.Filename
        self.args = args


    def __enter__(self):
        args = (c_char_p * len(self.args))(*self.args)
        self.tu = libclang.clang_parseTranslationUnit(
            self.idx,
            self.filename,
            args,
            len(args),
            byref(self.unsaved_file),
            1,
            0,
            )
        # TODO-deets: here maybe a reparse call,
        # as in emacs-clang-complete?

        self.ac_results = libclang.clang_codeCompleteAt(
            self.tu,
            self.filename,
            self.point[0], self.point[1],
            byref(self.unsaved_file), 1, 0)

        libclang.clang_sortCodeCompletionResults(self.ac_results.contents.Results, self.ac_results.contents.NumResults)
        return self


    def __iter__(self):
        ac_results = self.ac_results
        for i in xrange(ac_results.contents.NumResults):
            cstring = ac_results.contents.Results[i].CompletionString
            for chunk_num in xrange(libclang.clang_getNumCompletionChunks(cstring)):
                kind = libclang.clang_getCompletionChunkKind(cstring, chunk_num)
                if kind == CXCompletionChunkKind.CXCompletionChunk_TypedText:
                    head = libclang.clang_getCompletionChunkText(cstring, chunk_num)
                    yield Bunch(head=head)


    def __exit__(self, etype, evalue, tb):
        libclang.clang_disposeCodeCompleteResults(self.ac_results)
        libclang.clang_disposeTranslationUnit(self.tu)



class AsyncSession(object):

    def __init__(self, filename, args):
        self.running = True
        self.filename = filename
        self.source = None
        self.args = args


    def __enter__(self):
        self.idx = libclang.clang_createIndex(0, 0)
        return self


    def __exit__(self, etype, evalue, tb):
        libclang.clang_disposeIndex(self.idx)


    def unsaved_file(self):
        assert self.source is not None
        return CXUnsavedFile(
            self.filename,
            self.source,
            len(self.source),
            )


    def sourcefile(self, inf, outf):
        length_line = inf.readline()
        assert length_line.startswith("source_length:")
        length = int(length_line.split(":")[1])
        self.source = inf.read(length)
        # there are two newlines following. For whatever reason
        inf.readline()
        inf.readline()
        logger.debug("updated source with length %i" % length)


    def completion(self, inf, outf):
        row_line = inf.readline()
        assert "row:" in row_line
        column_line = inf.readline()
        assert "column:" in column_line
        # fresh copy of source
        self.sourcefile(inf, outf)
        row = int(row_line.split(":")[1])
        col = int(column_line.split(":")[1])
        logger.debug("completion at (%i:%i)" % (row, col))

        self.run_completion(row, col, outf)
        # *no* newline after this!
        logger.debug("completion finished")
        outf.write("$")
        outf.flush()


    def immediate(self, filename, outf):
        with open(filename) as inf:
            content = inf.read()
        point, source = source_for_autocomplete(content)
        inf = StringIO("row:%i\ncolumn:%i\nsource_length:%i\n%s\n\n" %
                (point[0], point[1], len(source), source))
        self.completion(inf, outf)


    def run_completion(self, row, col, outf):
        with TranslationUnit(self.idx, (row, col), self.unsaved_file(), self.args) as tu:
            for completion in tu:
                completion_line = "COMPLETION: %s\n" % completion.head
                logger.debug(completion_line)
                outf.write(completion_line)


    def reparse(self, inf, outf):
        pass


    def cmdlineargs(self, inf, outf):
        num_args_line = inf.readline()
        assert "num_args:" in num_args_line
        num_args = int(num_args_line.split(":")[1])
        argline = inf.readline().strip()
        logger.debug("argline: %r", argline)
        self.args = argline.split(" ")
        logger.debug("updated cmdline args: %r" % self.args)


    def syntaxcheck(self, inf, outf):
        pass


    def shutdown(self, inf, outf):
        logger.debug("SHUTDOWN")
        self.running = False


def mainloop(filename, args, inf=sys.stdin, outf=sys.stdout, immediate=False):
    logger.debug("args: %r", args)
    setup()
    session = AsyncSession(filename, args)
    with session:
        if immediate:
            session.immediate(filename, outf)
        else:
            while session.running:
                command = inf.readline().strip()
                logger.debug("command: " + command)
                command_callback = {
                    "COMPLETION" : session.completion,
                    "SOURCEFILE" : session.sourcefile,
                    "CMDLINEARGS" : session.cmdlineargs,
                    "SYNTAXCHECK" : session.syntaxcheck,
                    "REPARSE" : session.reparse,
                    "SHUTDOWN" : session.shutdown,
                    }.get(command)
                if command_callback is None:
                    if command:
                        logger.debug("unknown command: %s" % command)
                else:
                    command_callback(inf, outf)

