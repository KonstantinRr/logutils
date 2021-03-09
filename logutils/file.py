#!/usr/bin/env python

""" File utility functions """

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

import os
import shutil

def clearDirectory(folderPath:str, mayThrow:bool=True, mayPrint:bool=False):
    """ Clears all files in the directory that is denoted by folderPath
    This function throws only exceptions if mayThrow is True (default).
    
    Parameters
    ----------
    folderPath : str
        The path of the folder that should be cleared.
    mayThrow : bool (default: True)
        If the function may throw any exceptions.
    """
    try:
        exceptions = []
        for filename in os.listdir(folderPath):
            filePath = os.path.join(folderPath, filename)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as e:
                if mayPrint:
                    print('Failed to delete {}, Reason: {}'.format(filePath, e))
                exceptions.append(e) # Stores the exception

        if len(exceptions) > 0: # raises all exceptions together
            raise MultiException(exceptions)
    except Exception as e:
        if mayPrint:
            print('Unknown error during clearDirectory: {}'.format(e))
        if mayThrow: raise

def clearFile(filePath:str, mayThrow:bool=True, mayPrint:bool=False):
    """ Clears the file denoted by filePath
    
    Parameters
    ----------
    filePath : str
        The path of the file that should be deleted.
    mayThrow : bool (default: True)
        If the function may throw any exceptions.
    """
    try:
        os.remove(filePath)
    except Exception as e:
        if mayPrint:
            print('Unknown error during clearFile: {}'.format(e))
        if mayThrow: raise