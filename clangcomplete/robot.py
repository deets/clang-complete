import logging

from abl.util import Bunch
from abl.robot import Robot

from .api import mainloop

logger = logging.getLogger(__name__)

class ClangCompleteRobot(Robot):

    CONFIG_NAME = ".clang-completerc"

    SEARCH_PATHS = "~"


    EXCEPTION_MAILING = "diez.roggisch@ableton.com"
    AUTHOR = "diez.roggisch@ableton.com"

    def __init__(self):
        super(ClangCompleteRobot, self).__init__()
        # replace the commandline parser
        # because we don't accept any
        self.parser = Bunch(parse_args=lambda argv: (
                Bunch(
                    raise_exceptions=None,
                    config=None,
                    logfile=None,
                    loglevel=None,
                    logformat=None,
                    config_spec=False,
                    default_config=None,
                    ), []))


    def work(self):
        logger.info("Starting clang-complete")
        mainloop()


