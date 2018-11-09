"""
Collection of functions returning formatted strings for variables.
"""
import numbers
import numpy as np
import re


def striptype(type):
    """
    Strip <class ''> from type string
    """
    rule = re.compile('<class \'(.*)\'>')
    match = rule.search(type)
    if match:
        return match.group(1)
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
    return striptype(str(type(variable)))


def minmax(variable_name, variable, **kwargs):
    """
    Return minimum and maximum of variable as formatted string
    """
    try:
        minmax = (min(variable), max(variable))
    except Exception:
        return ''
    if all(isinstance(i, numbers.Number) for i in minmax):
        return f'({minmax[0]:.3g}, {minmax[1]:.3g})'
    else:
        return ''


def shape(variable_name, variable, **kwargs):
    """
    Return shape/length of variable as formatted string
    """
    if isinstance(variable, str):
        return f'len({str(len(variable))})'

    try:
        shape = np.array(variable).shape
        if shape is not ():
            return str(shape)
        else:
            return ''
    except Exception:
        return ''


def content(variable_name, variable, maxwidth=25, **kwargs):
    """
    Return content of variable as formatted string
    """
    # Appropriate number formatting
    if isinstance(variable, numbers.Number):
        return f'{variable:.3g}'

    # Object to-string function
    try:
        content = variable.__str__()
    except Exception:
        return ''

    # Remove object contents
    if content.startswith('<') and content.endswith('>'):
        return ''

    # Remove new lines
    if content.find('\n') != -1:
        content = content.replace('\n', '\\n')

    # Cur off long content
    if len(content) > maxwidth:
        content = content[:maxwidth] + '...'

    # Wrap strings in quotes
    if isinstance(variable, str):
        content = f'\'{content}\''

    return content
