#!/usr/bin/env python2.7
import os
import sys
import subprocess
import logging

logger = logging.getLogger()

readline = sys.stdin.readline

def sourcefile():
    length_line = readline()
    assert length_line.startswith("source_length:")
    length = int(length_line.split(":")[1])
    source = sys.stdin.read(length)
    # there are two newlinse following. For whatever reason
    readline()
    readline()
    logger.debug("updated source with length %i" % length)


def completion():
    row_line = readline()
    assert "row:" in row_line
    column_line = readline()
    assert "column:" in column_line
    # fresh copy of source
    sourcefile()
    row = int(row_line.split(":")[1])
    col = int(column_line.split(":")[1])
    logger.debug("completion at (%i:%i)" % (row, col))
    sys.stdout.write("""COMPLETION: assign : [#void#]assign(<#_InputIterator __first#>, <#_InputIterator __last#>)
COMPLETION: at : [#const_reference#]at(<#size_type __n#>) const
COMPLETION: back : [#const_reference#]back() const
COMPLETION: begin : [#const_iterator#]begin() const
COMPLETION: capacity : [#size_type#]capacity() const
COMPLETION: data : [#const_pointer#]data() const
COMPLETION: empty : [#bool#]empty() const
COMPLETION: end : [#const_iterator#]end() const
COMPLETION: front : [#const_reference#]front() const
COMPLETION: get_allocator : [#allocator_type#]get_allocator() const
COMPLETION: insert : [#void#]insert(<#iterator __position#>, <#_InputIterator __first#>, <#_InputIterator __last#>)
COMPLETION: max_size : [#size_type#]max_size() const
COMPLETION: operator[] : [#const_reference#]operator[](<#size_type __n#>) const
COMPLETION: rbegin : [#const_reverse_iterator#]rbegin() const
COMPLETION: rend : [#const_reverse_iterator#]rend() const
COMPLETION: size : [#size_type#]size() const
COMPLETION: vector : vector::
COMPLETION: vector : [#void#]vector(<#_InputIterator __first#>, <#_InputIterator __last#>{#, <#const allocator_type &__a#>#})
""")
    # *no* newline after this!
    sys.stdout.write("$")
    sys.stdout.flush()


def reparse():
    pass


def cmdlineargs():
    num_args_line = readline()
    assert "num_args:" in num_args_line
    num_args = int(num_args_line.split(":")[1])
    args = [readline.strip() for _ in xrange(num_args)]
    logger.debug("updated cmdline args: %r" % args)


def syntaxcheck():
    pass


def shutdown():
    global RUNNING
    RUNNING = False


def mainloop():
    global RUNNING
    RUNNING = True
    while RUNNING:
        command = sys.stdin.readline().strip()
        logger.debug("command: " + command)
        command_callback = {
            "COMPLETION" : completion,
            "SOURCEFILE" : sourcefile,
            "CMDLINEARGS" : cmdlineargs,
            "SYNTAXCHECK" : syntaxcheck,
            "REPARSE" : reparse,
            "SHUTDOWN" : shutdown,
            }.get(command)
        if command_callback is None:
            if command:
                logger.debug("unknown command: %s" % command)
        else:
            command_callback()

