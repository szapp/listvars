"""
List all global variables with additional filtering options.
"""
import os
import re
import sys
import tableprint as tp
import types

from listvars import resolve

try:
    from IPython.core.autocall import ZMQExitAutocall
    ipython_types = [ZMQExitAutocall]
except ImportError:
    ipython_types = []


# Available columns
labels = [
    'name',
    'type',
    'size',
    'value',
]

# Default filter
filter_default = []

# Exclude patterns
excl_base = [
    types.ModuleType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodType,
    '^__.*',
]

excl_ipython = [
    'In',
    'Out',
    '_',
    '_dh',
    '_i(\\d*|ii)',
    '_oh',
    'get_ipython',
] + ipython_types

excl_default = excl_base + excl_ipython

# Default fields
fields_default = 'all'


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
    return getattr(resolve, field)(variable_name, variable)


def listvars(filters=filter_default, excl=excl_default,  # noqa: C901
             fields=fields_default, vars=None):
    """
    List filtered global variables and their types

    Parameters
    ----------
    filters : list, optional
        Outer list matches any variable name/type,
        Inner list matches all variable names/types. Default is
        filter_default

    excl : list, optional
        Exclude filters (name or type). Default is excl_default

    fields : list, optional
        List of columns to display. Default is fields_default

    vars : dict, optional
        Provide a dict of variables instead of inferring the locals.
        Default is None.

    Notes
    -----
    String filters/exclude patterns are matched with regular expressions
    against the variable names.

    The filter list may contain strings (filter names), types (filter
    types) and/or another list defining a group in which all filters
    must match. For more details, see the README.md
    """
    # Build dictionary from global or supplied dict of variables
    vdict = dict()
    if vars is None:
        main = sys.modules['__main__']
        for var_name in sorted(dir(main)):
            vdict[var_name] = getattr(main, var_name)
    elif isinstance(vars, type(dict())):
        for var_name in sorted(vars.keys()):
            vdict[var_name] = vars.get(var_name, None)
    else:
        raise ValueError('The provided vars is not a dictionary')

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

    # Reduce to maximum width
    max_width = int(os.environ.get('COLUMNS', '999'))
    space = max_width - (sum(width) + len(width) * 3 + 1)
    if space < 0:
        opt = int((max_width - (len(width) * 3 + 1)) / len(width))
        pool = 0
        large = []
        for i, w in enumerate(width):
            if w <= opt:
                pool += opt - w
            else:
                large.append(i)
        donate = int(pool / len(large))
        for i in large:
            width[i] = opt + donate

        for ll in lines:
            for i in large:
                if len(ll[i]) > opt + donate - 2:
                    ll[i] = ll[i][:opt + donate - 2] + '…'
                if ll[i].count('\'') % 2 == 1:
                    ll[i] += '\''

    # Draw chart
    tp.table(lines, fields, width=width)


if __name__ == '__main__':
    listvars()
