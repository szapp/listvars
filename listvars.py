"""
List all global variables with additional filtering options.
"""
import re
import sys
import tableprint as tp
import types


__all__ = ['listvars']


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


def listvars(filters=[], excl=[types.ModuleType, '^__.*']):
    """
    List filtered global variables and their types

    Parameters
    ----------
    filters : list
        Outer list matches any variable name/type
        Inner list matches all variable names/types

    excl : list
        Exclude filters (name or type)

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
    for name in sorted(dir(main)):
        vdict[name] = getattr(main, name)

    # Filter dictionary
    if isinstance(filters, list) and filters:
        vdict = filtervars(vdict, filters)

    # Exclude from dictionary
    if isinstance(excl, list) and excl:
        vdict = excludevars(vdict, excl)

    if not vdict:
        print('No variables match the filter')
        return

    # Find cell widths
    maxlen1 = len('Name')
    maxlen2 = len('Type')
    for varname, var in vdict.items():
        if len(varname) > maxlen1:
            maxlen1 = len(varname)
        ty = striptype(str(type(var)))
        if len(ty) > maxlen2:
            maxlen2 = len(ty)
    width = [maxlen1, maxlen2]

    # Draw chart
    print(tp.header(['Name', 'Type'], width=width))
    for varname, var in vdict.items():
        print(tp.row([varname, striptype(str(type(var)))], width=width))
    print(tp.bottom(2, width=width))


if __name__ == '__main__':
    listvars()
