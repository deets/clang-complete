import sys
import logging
from .api import mainloop


def main():
    logging.basicConfig(
        filename="/tmp/clangcomplete.log",
        level=logging.DEBUG,
        )
    filename = sys.argv[-1]
    mainloop(filename, sys.stdin, sys.stdout)

