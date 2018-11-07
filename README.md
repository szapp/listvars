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
from listvars import listvars

listvars()
```


## Filtering

Additional filtering and excluding options are available as optional parameters.

- `filters` may either be a list of strings and types, a list of lists or a combination of both. The outer list defines 
"or" filters, matching any of the elements, the inner list defines a group of "and" filters, where all elements must
match. Strings are regular expressions that are matched against the variable names, the types match the variable types.
- `excl` is a single list of strings and types (matched in the same way) to exclude.


```python
# Only show string variables and those whose name starts with 'var'
listvars(filters=[str, '^var.*'])

# Only show variables that are both strings and whose names start with 'var'
listvars(filters=[[str, '^var.*']])

# Same as above but also show dictionaries
listvars(filters=[[str, '^var.*'], dict])

# Exlude all None types or integers
listvars(excl=[type(None)])
```
