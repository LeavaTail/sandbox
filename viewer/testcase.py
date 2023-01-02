"""xfstests result information

This modules stored the xfstests results information. This information use
timestamp and logfile as well as result directory.
"""

import sys
from logging import getLogger
import dataclasses

logger = getLogger("__main__").getChild("testcase")

@dataclasses.dataclass
class TestClass():
    name: str
    sec: int
    path: str
    remarks: str
    """Test result generic class

    The generic class to store xfstests result

    Args:
        name (str): Testcase name

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """

    def __init__(self, name=''):
        self.name = name
        self.sec = 0
        self.remarks = ''
        self.path = ''

    def update_time(self, sec):
        self.sec = sec

    def update_summary(self, pathname):
        pass

    def update_path(self, base):
        self.path = base + '/' + self.name


class PassedClass(TestClass):
    """Passed result class

    The class to store passed xfstests result

    Args:
        name (str): Testcase name

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """


    def __init__(self, name=''):
        super().__init__(name)


class SkippedClass(TestClass):
    """Skipped result class

    The class to store skipped xfstests result

    Args:
        name (str): Testcase name

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """

    def __init__(self, name=''):
        super().__init__(name)

    def update_summary(self, pathname):
        try:
            with open(pathname + self.name + '.' + 'notrun', 'r') as f:
                contents = f.read()
        except OSError:
            logger.error("Could not open file:" + pathname + self.name + '.' + 'notrun')
            sys.exit()
        self.remarks = contents


class FailedClass(TestClass):
    """Failed result class

    The class to store failed xfstests result

    Args:
        name (str): Testcase name

    Attributes:
        name (str): Testcase name
        sec (int): The elapsed time (second)
        remarks (str): Additional information (e.g. Skipped cause)
        path (str): The pathname for xfstests result
    """

    def __init__(self, name=''):
        super().__init__(name)
