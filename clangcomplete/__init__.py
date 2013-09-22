import sys
import logging
from .api import mainloop


def main():
    logging.basicConfig(
        filename="/tmp/clangcomplete.log",
        level=logging.DEBUG,
        )
    immediate = False

    if "--immediate" in sys.argv:
        immediate = True
        sys.argv.remove("--immediate")

    filename = sys.argv[-1]
    args = sys.argv[1:-1]
    mainloop(filename, args, sys.stdin, sys.stdout, immediate=immediate)

