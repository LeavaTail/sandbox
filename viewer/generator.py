"""generate the instance for some class

This modules define the method to create the some instances
"""

import re
from logging import getLogger, CRITICAL
from .testcase import PassedClass, SkippedClass, FailedClass

logger = getLogger("__main__").getChild("generator")

def read_results(directory):
    """Create the list of TestClass instance.

    This method uses "check.log" that is the xfstests result file, and
    categorize as "Passed", "Skipped" and "Failed" testcase. However,
    the instance doesn't include the details xfstests logs.
    (e.g. Cause of skip, timestamp)

    Note:
        Only obtain the log in last result 
    """
    testlist = []
    formattedlist = {}
    passedlist = []
    skippedlist = []
    failedlist = []

    try:
        with open(directory + '/check.log', 'r') as f:
            logs = f.read()
        with open(directory + '/check.time', 'r') as f:
            time = f.read()
    except OSError:
        logger.error("Could not open file under " + directory)
        sys.exit()

    # Obtain from last log
    testlog = logs.split('\n\n')[-1]

    if testlog:
        # test logs are divided into 3 sections
        # 1. Ran (All testcases)
        # 2. Not run (Skipped testcases)
        # 3. Failures: (Failed testcases)
        alltest = testlog.split('\n')[1]
        skippedtest = testlog.split('\n')[2]
        failedtest = testlog.split('\n')[3]

        # test is separated by a space
        testlist = alltest.split(' ')

    # First argument is index 'Ran:' should be skipped
    for test in testlist[1:-1]:
        if test in skippedtest:
            s = SkippedClass(test)
            update_details(s, time, directory)
            skippedlist.append(s)
            logger.debug(test + ' :Skipped')
        elif test in failedtest:
            f = FailedClass(test)
            update_details(f, time, directory)
            failedlist.append(f)
            logger.debug(test + ' :Failed')
        else:
            p = PassedClass(test)
            update_details(p, time, directory)
            passedlist.append(p)
            logger.debug(test + ' :Passed')

    formattedlist["passed"] = passedlist
    formattedlist["failed"] = failedlist
    formattedlist["skipped"] = skippedlist

    return formattedlist

def update_details(testcase, time, directory):
    testcase.update_summary(directory + '/')
    testcase.update_path(directory)

    # timestamp is separated by a space
    line = re.findall(testcase.name + ' ' + '\d+', time)
    # passed testcase
    if line:
        testcase.update_time(line[0].split(' ')[1])
    # skipped or failed testcase
    else:
        pass
