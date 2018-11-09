"""
List all global variables with additional filtering options.
"""
import re
import sys
import tableprint as tp
import types

from listvars import resolve


labels = [
    'name',
    'type',
    'shape',
    'minmax',
    'content',
]

contentwidth = 25


def filtervars_sub(vdict, filtr):
    """
    Get dictionary entries that match any filter
    """
    vdict_filtered = dict()
    for varname, var in vdict.items():
        if isinstance(filtr, type):
            if isinstance(var, filtr):
                vdict_filtered[varname] = var
        elif isinstance(filtr, str):
            if re.match(filtr, varname):
                vdict_filtered[varname] = var
        else:
            raise ValueError('Allowed types: str, type, list')
    return vdict_filtered


def filtervars(vdict, filters):
    """
    Reduce dictionary by match-all and match-any filters
    """
    matches = [0] * len(filters)

    for i, filtr in enumerate(filters):
        if isinstance(filtr, list):
            # Match all (inner list)
            matches[i] = vdict.copy()
            for filtrs in filtr:
                matches[i] = filtervars_sub(matches[i], filtrs)
        else:
            # Match any (outer list)
            matches[i] = filtervars_sub(vdict, filtr)

    vdict_filtered = dict()
    for match in matches:
        if (match):
            vdict_filtered.update(match)

    return vdict_filtered


def excludevars(vdict, filters):
    """
    Remove dictionary items by filter
    """
    vdict_remove = dict()
    for filtr in filters:
        a = filtervars_sub(vdict, filtr)
        vdict_remove.update(a)

    vdict_filtered = vdict.copy()
    for key in vdict_remove.keys():
        del vdict_filtered[key]
    return vdict_filtered


def verifyfields(fields):
    """
    Verfiy the field labels
    """
    # Remove invalid fields
    fields = [label.title() for label in fields if label.lower() in labels]

    # Make sure name always exists and is in the first column
    fields = ['Name'] + fields

    # Each field is unique, set() changes order!
    fields_unique = []
    for i in fields:
        if i not in fields_unique:
            fields_unique.append(i)
    fields = fields_unique

    return fields


def resolvefield(field, variable_name, variable):
    """
    Resolve variable to string by field
    """
    # Prevent clash with built-in function
    if field == 'type':
        field = 'dtype'
    return getattr(resolve, field)(variable_name, variable,
                                   maxwidth=contentwidth)


def listvars(filters=[], excl=[types.ModuleType, types.FunctionType, '^__.*'],
             fields=['name', 'type']):
    """
    List filtered global variables and their types

    Parameters
    ----------
    filters : list, optional
        Outer list matches any variable name/type,
        Inner list matches all variable names/types. Default is []

    excl : list, optional
        Exclude filters (name or type). Default is
        [types.ModuleType, types.FunctionType, '^__.*']

    fields : list, optional
        List of columns to display. Default is ['name', 'type']

    Notes
    -----
    String filters/exclude patterns are matched with regular expressions
    against the variable names.

    The filter list may contain strings (filter names), types (filter
    types) and/or another list defining a group in which all filters
    must match. For more details, see the README.md
    """
    # Build dictionary from global variables
    main = sys.modules['__main__']
    vdict = dict()
    for var_name in sorted(dir(main)):
        vdict[var_name] = getattr(main, var_name)

    # Filter dictionary
    if isinstance(filters, list) and filters:
        vdict = filtervars(vdict, filters)

    # Exclude from dictionary
    if isinstance(excl, list) and excl:
        vdict = excludevars(vdict, excl)

    if not vdict:
        print('No variables match the filter')
        return

    # Special field names
    if fields == 'all':
        fields = labels
    elif fields == '':
        fields = []
    elif not isinstance(fields, list):
        raise ValueError('Fields are invalid')

    fields = verifyfields(fields)

    # Build list from variables and fields
    width = list(map(len, fields))
    lines = []
    for var in vdict.items():
        line = [resolvefield(label.lower(), *var) for label in fields]
        lines.append(line)
        for i, w in enumerate(zip(width, list(map(len, line)))):
            width[i] = max(w)

    # Draw chart
    print(tp.header(fields, width=width))
    print(*(tp.row(line, width=width) for line in lines), sep='\n')
    print(tp.bottom(len(fields), width=width))


if __name__ == '__main__':
    listvars()
