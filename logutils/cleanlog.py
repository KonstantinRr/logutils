#!/usr/bin/env python

""" Log cleaning functions """

__author__ = "Konstantin Rolf"
__copyright__ = "Copyright 2020, ALLTHEWAYAPP LTD"
__credits__ = []

__license__ = """ Copyright (C) ALLTHEWAYAPP, LTD - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential.
Written by Konstantin Rolf <konstantin.rolf@gmail.com>, January 2021 """

__version__ = "0.0.1"
__maintainer__ = "Konstantin Rolf"
__email__ = "konstantin.rolf@gmail.com"
__status__ = "Prototype"

import sys # sys.exit

import argparse
import os

from shutil import rmtree

def cleanLogs(logDir:str='./logs'):
    if os.path.isdir(logDir):
        rmtree(logDir)
    else:
        print('Path does not denote a valid directory...')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log directory')
    parser.add_argument('--logdir', type=str, default='./logs',
        help='Log directory (default: \'./logs\'')
    parser.add_argument('--force', type=bool, default=True,
        help='Whether to delete the directory without asking for permission')

    args = parser.parse_args()

    print('Are you sure you want to delete {}? (Y/N)'.format(args.logdir))
    inp = input()
    if inp.lower() != 'y':
        print('Aborting action')
        sys.exit(-1)
    
    print('Cleaning logs...')
    cleanLogs(logDir=args.logdir)
    print('Cleaned logs successfully.')