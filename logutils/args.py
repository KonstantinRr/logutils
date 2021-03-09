#!/usr/bin/env python

""" Argument Utility functions

This file combines some utility functions to check arguments.
"""

__author__ = "Konstantin Rolf"
__copyright__ = "Copyright 2020, ALLTHEWAYAPP LTD"
__credits__ = []

__license__ = """ MIT """

__version__ = "0.0.1"
__maintainer__ = "Konstantin Rolf"
__email__ = "konstantin.rolf@gmail.com"
__status__ = "Prototype"

from abc import ABC, abstractmethod
from collections.abc import Sequence, Iterable

class AbstractValidator(ABC): 
    """ The general interface of any validator. Each subclass must
    implement the call method with a single parameter. It should
    return the validated block iff the validator test passed, None otherwise. """

    @abstractmethod
    def __call__(self, value):
        pass

class ReplaceValidator(AbstractValidator):
    """ Validates the given input and replaces the input with a replacement
    value if the validator does not parse the value successful. """

    def __init__(self, validator:AbstractValidator, replacement):
        """ Creates a new ReplaceValidator.
        
        Parameters
        ----------
        validator : AbstractValidator
            The validator used to validate any input.
        replacement :
            The value that is returned if the validation fails.
        """
        self.validator = validator
        self.replacement = replacement

    def __call__(self, value):
        return value if self.validator(value) else self.replacement

    def __str__(self):
        return 'Replacement[validator={} replacement={}]'.format(
            self.validator, self.replacement)

    def __repr__(self):
        return self.__str__()
            
# logical validator operators #

class AllValidator(AbstractValidator):
    """ Combines multiple validators in one class and returns the
    validated block iff all validators are successful, None otherwise. """

    def __init__(self, validators=[], shortCircuit:bool=False, allowEmpty:bool=False):
        """ Creates a new all validator with a list of subchecks
        
        Parameters
        ----------
        validators :
            The list of subvalidators that need to be validated
        shortCircuit : bool
            Whether the list of validators can be short-evaluated. All validators are
            skipped if a previous validator returned True (default is False).
        allowEmpty : bool
            Whether a value should be accepeted iff there is no validator specified.
            (default is False) 
        """
        self.validators = validators
        self.shortCircuit = shortCircuit
        self.allowEmpty = allowEmpty

    def __call__(self, value):
        if not self.validators:
            return value if self.allowEmpty else None

        checkResult = True
        for validator in self.validators:
            checkResult = checkResult and validator(value)
            if self.shortCircuit and not checkResult:
                break
        return value if checkResult else None

    def __str__(self):
        return 'All[validators={}, circuit={}, allowEmpty={}]'.format(
            self.validators, self.shortCircuit, self.allowEmpty)

    def __repr__(self):
        return self.__str__()

class AnyValidator(AbstractValidator):
    """ Combines multiple validators in one class and returns the
    validated block iff any validator was successful, None otherwise. """

    def __init__(self, validators=[], shortCircuit:bool=False, allowEmtpy:bool=False):
        """ Creates a new all validator with a list of subchecks
        
        Parameters
        ----------
        validators : Sequence[AbstractValidator]
            The list of subvalidators that need to be validated
        shortCircuit : bool
            Whether the list of validators can be short-evaluated.
            All validators are skipped iff a previous validator returned True.
        allowEmpty : bool
            Whether a value should be accepeted iff there is no validator specified.
            (default is False) 
        """
        self.validators = validators
        self.shortCircuit = shortCircuit
        self.allowEmpty = allowEmtpy

    def __call__(self, value):
        if not self.validators:
            return value if self.allowEmpty else None

        checkResult = False
        for validator in self.validators:
            checkResult = checkResult or validator(value)
            if self.shortCircuit and not checkResult:
                break
        return value if checkResult else None

    def __str__(self):
        return 'Any[validators={}, circuit={}, allowEmpty={}]'.format(
            self.validators, self.shortCircuit, self.allowEmpty)

    def __repr__(self):
        return self.__str__()


class TypeValidator(AbstractValidator):
    """ Validator that checks if a variable is of given type """

    def __init__(self, tp):
        """ Creates a new type validator from a given type
        
        Parameters
        ----------
        tp :
            The type which the value is validated against
        """
        self.tp = tp

    def __call__(self, value):
        """ Returns True iff value is of a given type, False otherwise """ 
        return value if isinstance(value, self.tp) else None

    def __str__(self):
        return 'Type[type={}]'.format(self.tp)

    def __repr__(self):
        return self.__str__()


class ListValidator(AbstractValidator):
    """ Creates a checker that checks if a variable is a of a given type
    and if all children (when iterated) satisfy a a another checker. """

    def __init__(self, validator, removeIfNone:bool=True):
        """ Creates a new list validator

        Parameters
        ----------
        validator : AbstractValidator
            The validator used to validate all objects in the list
        removeIfNone : bool
            Whether to remove all values that are None from the list.
            The default value is True.
        """
        self.validator = validator
        self.removeIfNone = removeIfNone

    def __call__(self, value):
        if not isinstance(value, Iterable):
            return None
        newValues = (self.validator(val) for val in value)
        return ([val for val in newValues if val is not None]
            if self.removeIfNone else [newValues])

    def __str__(self):
        return 'List[validator={}, removeIfNone={}]'.format(
            self.validator, self.removeIfNone)

    def __repr__(self):
        return self.__str__()

class DictValidator(AbstractValidator):
    def __init__(self, keyValidator, valueValidator):
        self.keyValidator = keyValidator
        self.valueValidator = valueValidator

    def __call__(self, value):
        if not isinstance(value, dict):
            return None
        return {self.keyValidator(k): self.valueValidator(v)
            for k, v in value.items()}

    def __str__(self):
        return 'Dict[keyValidator={}, valueValidator{}]'.format(
            self.keyValidator, self.valueValidator)

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    print('FILE: args.py')
    print('This file does not have any functionality on its own.')

    def unitTest(inp, validator):
        print('Input:', inp)
        print('Validator:', validator)
        result = validator(inp)
        print('Result:', result)

    unitTest(
        [1, 'str', 3],
        ListValidator(ReplaceValidator(TypeValidator(int), 3))
    )
