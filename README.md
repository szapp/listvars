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
╭───────┬──────────┬──────┬──────────────────────────────╮
│ Name  │   Type   │ Size │            Value             │
├───────┼──────────┼──────┼──────────────────────────────┤
│     a │      str │   34 │ 'Long string containing \n…' │
│ array │  float64 │ (6,) │             min: 1, max: 3.5 │
│     b │      int │      │                           42 │
│     c │ NoneType │      │                         None │
│     d │     dict │    2 │     {0: 'Hello', 1: 'World'} │
│  var1 │      str │    5 │                      'hello' │
│  var2 │      str │    5 │                      'world' │
│  var3 │      int │      │                           13 │
│  var4 │     dict │    2 │   {'key0': 'var0', 'key1': … │
╰───────┴──────────┴──────┴──────────────────────────────╯
```


## Fields

Different columns may be shown by specifying them with the optional `fields` parameter.

```python
>>> listvars(fields=['name', 'value'])
╭───────┬──────────────────────────────╮
│ Name  │            Value             │
├───────┼──────────────────────────────┤
│     a │ 'Long string containing \n…' │
│ array │             min: 1, max: 3.5 │
│     b │                           42 │
│     c │                         None │
│     d │     {0: 'Hello', 1: 'World'} │
│  var1 │                      'hello' │
│  var2 │                      'world' │
│  var3 │                           13 │
│  var4 │   {'key0': 'var0', 'key1': … │
╰───────┴──────────────────────────────╯
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
╭──────┬──────┬──────┬──────────────────────────────╮
│ Name │ Type │ Size │            Value             │
├──────┼──────┼──────┼──────────────────────────────┤
│    a │  str │   34 │ 'Long string containing \n…' │
│ var1 │  str │    5 │                      'hello' │
│ var2 │  str │    5 │                      'world' │
│ var3 │  int │      │                           13 │
│ var4 │ dict │    2 │   {'key0': 'var0', 'key1': … │
╰──────┴──────┴──────┴──────────────────────────────╯

>>> # Only show variables that are both strings and whose names start with 'var'
>>> listvars(filters=[[str, '^var.*']])
╭──────┬──────┬──────┬─────────╮
│ Name │ Type │ Size │  Value  │
├──────┼──────┼──────┼─────────┤
│ var1 │  str │    5 │ 'hello' │
│ var2 │  str │    5 │ 'world' │
╰──────┴──────┴──────┴─────────╯

>>> # Same as above but also show dictionaries
>>> listvars(filters=[[str, '^var.*'], dict])
╭──────┬──────┬──────┬────────────────────────────╮
│ Name │ Type │ Size │           Value            │
├──────┼──────┼──────┼────────────────────────────┤
│ var1 │  str │    5 │                    'hello' │
│ var2 │  str │    5 │                    'world' │
│    d │ dict │    2 │   {0: 'Hello', 1: 'World'} │
│ var4 │ dict │    2 │ {'key0': 'var0', 'key1': … │
╰──────┴──────┴──────┴────────────────────────────╯

>>> # Exlude all None types or integers (overwrites the default exclude filter!)
>>> from listvars import excl_default
>>> listvars(excl=excl_default+[type(None), int])
╭──────────────┬─────────┬───────┬──────────────────────────────╮
│     Name     │  Type   │ Size  │            Value             │
├──────────────┼─────────┼───────┼──────────────────────────────┤
│            a │     str │    34 │ 'Long string containing \n…' │
│        array │ float64 │  (6,) │             min: 1, max: 3.5 │
│            d │    dict │     2 │     {0: 'Hello', 1: 'World'} │
│ excl_default │    list │ (14,) │   [<class 'module'>, <class… │
│         var1 │     str │     5 │                      'hello' │
│         var2 │     str │     5 │                      'world' │
│         var4 │    dict │     2 │   {'key0': 'var0', 'key1': … │
╰──────────────┴─────────┴───────┴──────────────────────────────╯
```
