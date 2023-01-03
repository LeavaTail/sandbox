#!/usr/bin/env python3
# coding: utf-8
"""organize the xfstests result

This modules organize and format the xfstests results. This use timestamp and
logfile as well as result directory. As a result, return the lists that is
formatted by JSON.

Example:

    $ python3 __main__.py /xfstests/results
"""

import os
import sys
import argparse
from logging import getLogger, StreamHandler, DEBUG, CRITICAL, WARNING

from generator import read_results
from conv_json import ConvJsonClass
from conv_excel import ConvExcelClass

logger = getLogger(__name__)

def set_logger(opts):
    """Set the parameter in logger.

    This module set the logger based on the mode that is "Default",
    "Verbose mode" and "Quite mode".
    """
    global logger

    # Set the log level
    if (opts.verbose):
        level = DEBUG
    elif (opts.quite):
        level = CRITICAL
    else:
        level = WARNING

    handler = StreamHandler()
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    return level

def get_opts():
    """Analyze the command line argument.

    This module can set the parameter by command line argument.
      -o, --output: The strategy in output
      -q, --quite: Restrict the message
      -v, --verbose: Output debug message
    """

    parser = argparse.ArgumentParser(
        prog='xfstests-test-viewer',
        description='Output json file from xfstests result')

    parser.add_argument('results', help='xfstests results directory path')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--format', help='Output format type')
    parser.add_argument('-q', '--quite', help='Quite mode', action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
    opts = parser.parse_args()

    return opts

def main():
    opts = get_opts()
    if opts.format == 'excel':
        conv = ConvExcelClass()
    else:
        conv = ConvJsonClass()

    level = set_logger(opts)
    formattedlist = read_results(opts.results)

    conv.dump_results(formattedlist, opts.output)

if __name__ == "__main__":
    main()
