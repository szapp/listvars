"""
Collection of functions returning formatted strings for variables.
"""
import collections
import numbers
import numpy as np
import re


# Maximum width for value column
value_width = 25

# Pre-compile regular expression for performance
rule = re.compile('<class \'(.*\\.)*([^\\.]*)\'>')


def striptype(type):
    """
    Strip <class ''> from type string and remove module prefixes
    """
    match = rule.search(type)
    if match:
        return match.group(2)
    else:
        return type


def name(variable_name, variable, **kwargs):
    """
    Return name of variable
    """
    return variable_name


def dtype(variable_name, variable, **kwargs):
    """
    Return type of variable as formatted string
    """
    if isinstance(variable, np.ndarray):
        if variable.dtype.names:
            tp = str(variable.dtype.names)
        else:
            tp = str(variable.dtype)
    else:
        tp = striptype(str(type(variable)))

    # Trim long type names
    if len(tp) > value_width:
        tp = tp[:value_width] + '…'
        if tp.count('\'') % 2 == 1:
            tp += '\''

    return tp


def minmax(variable_name, variable, **kwargs):
    """
    Return minimum and maximum of variable as formatted string
    """
    try:
        varr = np.asarray(variable, 'O')
        mm = (np.min(varr), np.max(varr))
    except Exception:
        return ''

    if varr.size > 1 and all(isinstance(i, numbers.Number) for i in mm):
        return f'min: {mm[0]:.3g}, max: {mm[1]:.3g}'
    else:
        return ''


def size(variable_name, variable, **kwargs):
    """
    Return size/shape of variable as formatted string
    """
    if isinstance(variable, str) or isinstance(variable, collections.Mapping):
        try:
            return str(len(variable))
        except ValueError:
            # Closed h5py handle
            return ''
        except TypeError:
            # Closed h5py handle
            return ''

    try:
        sze = np.asarray(variable, 'O').shape
        if sze != ():
            return str(sze)
        else:
            return ''
    except Exception:
        return ''


def setvaluewidth(val):
    """
    Set the maximum width of the value column
    """
    global value_width
    if isinstance(val, numbers.Number):
        value_width = val


def value(variable_name, variable, **kwargs):  # noqa: C901
    """
    Return value of variable as formatted string
    """
    # Show min-max for list types
    mm = minmax(variable_name, variable, **kwargs)
    if mm:
        return mm

    # Appropriate number formatting
    if isinstance(variable, numbers.Number):
        return f'{variable:.3g}'

    # To-string method
    try:
        value = variable.__str__()
    except Exception:
        return ''

    # Remove object identifier
    if value.startswith('<') and value.endswith('>'):
        return ''

    # Remove new lines
    if value.find('\n') != -1:
        if isinstance(variable, str):
            value = value.replace('\n', '\\n')
        else:
            value = value.replace('\n', ' ')

    # Trim long values
    if len(value) > value_width:
        value = value[:value_width] + '…'
        if value.count('\'') % 2 == 1:
            value += '\''

    # Wrap strings in quotes
    if isinstance(variable, str):
        value = f'\'{value}\''

    return value
