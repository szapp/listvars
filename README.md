# listvars

Python module to print a formatted list of all global variables with additional filtering options.


## Installation

Clone `listvars` into a directory in your python path.

```bash
git clone https://github.com/szapp/listvars.git
cd listvars
pip install -r requirements.txt
```


## Usage

A formated table of a filtered list of all global variables is drawn.

```python
>>> from listvars import listvars
>>> listvars()
╭──────────┬──────────╮
│   Name   │   Type   │
├──────────┼──────────┤
│        a │      str │
│        b │      int │
│        c │ NoneType │
│        d │     dict │
│ listvars │ function │
│     var1 │      str │
│     var2 │      str │
│     var3 │      int │
│     var4 │     dict │
╰──────────┴──────────╯
```


## Filtering

Additional filtering and excluding options are available as optional parameters.

- `filters` may either be a list of strings and types, a list of lists or a combination of both. The outer list defines 
"or" filters, matching any of the elements, the inner list defines a group of "and" filters, where all elements must
match. Strings are regular expressions that are matched against the variable names, the types match the variable types.
- `excl` is a single list of strings and types (matched in the same way) to exclude.


```python
>>> # Only show string variables and those whose name starts with 'var'
>>> listvars(filters=[str, '^var.*'])
╭──────┬──────╮
│ Name │ Type │
├──────┼──────┤
│    a │  str │
│ var1 │  str │
│ var2 │  str │
│ var3 │  int │
│ var4 │ dict │
╰──────┴──────╯

>>> # Only show variables that are both strings and whose names start with 'var'
>>> listvars(filters=[[str, '^var.*']])
╭──────┬──────╮
│ Name │ Type │
├──────┼──────┤
│ var1 │  str │
│ var2 │  str │
╰──────┴──────╯

>>> # Same as above but also show dictionaries
>>> listvars(filters=[[str, '^var.*'], dict])
╭──────┬──────╮
│ Name │ Type │
├──────┼──────┤
│ var1 │  str │
│ var2 │  str │
│    d │ dict │
│ var4 │ dict │
╰──────┴──────╯

>>> # Exlude all None types or integers (overwrites the default exclude filter!)
>>> listvars(excl=[type(None), int])
╭─────────────────┬──────────╮
│      Name       │   Type   │
├─────────────────┼──────────┤
│ __annotations__ │     dict │
│    __builtins__ │   module │
│      __loader__ │     type │
│        __name__ │      str │
│               a │      str │
│               d │     dict │
│        listvars │ function │
│           types │   module │
│            var1 │      str │
│            var2 │      str │
│            var4 │     dict │
╰─────────────────┴──────────╯
```
