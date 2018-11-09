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
╭───────┬───────────────╮
│ Name  │     Type      │
├───────┼───────────────┤
│     a │           str │
│ array │ numpy.ndarray │
│     b │           int │
│     c │      NoneType │
│     d │          dict │
│  var1 │           str │
│  var2 │           str │
│  var3 │           int │
│  var4 │          dict │
╰───────┴───────────────╯
```


## Fields

Different columns may be shown by specifying them with the optional `fields` parameter.

```python
>>> listvars(fields=['name', 'content'])
╭───────┬────────────────────────────────╮
│ Name  │             Content            │
├───────┼────────────────────────────────┤
│     a │ 'Long string containing \n...' │
│ array │      [1.  1.5 2.  2.5 3.  3.5] │
│     b │                             42 │
│     c │                           None │
│     d │       {0: 'Hello', 1: 'World'} │
│  var1 │                        'hello' │
│  var2 │                        'world' │
│  var3 │                             13 │
│  var4 │   {'key0': 'var0', 'key1': ... │
╰───────┴────────────────────────────────╯

>>> listvars(fields='all')
╭───────┬───────────────┬────────┬──────────┬────────────────────────────────╮
│ Name  │     Type      │ Shape  │  Minmax  │             Content            │
├───────┼───────────────┼────────┼──────────┼────────────────────────────────┤
│     a │           str │ len(4) │          │ 'Long string containing \n...' │
│ array │ numpy.ndarray │   (6,) │ (1, 3.5) │      [1.  1.5 2.  2.5 3.  3.5] │
│     b │           int │        │          │                             42 │
│     c │      NoneType │        │          │                           None │
│     d │          dict │        │   (0, 1) │       {0: 'Hello', 1: 'World'} │
│  var1 │           str │ len(5) │          │                        'hello' │
│  var2 │           str │ len(5) │          │                        'world' │
│  var3 │           int │        │          │                             13 │
│  var4 │          dict │        │          │   {'key0': 'var0', 'key1': ... │
╰───────┴───────────────┴────────┴──────────┴────────────────────────────────╯
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
╭─────────────────┬───────────────╮
│      Name       │     Type      │
├─────────────────┼───────────────┤
│ __annotations__ │          dict │
│    __builtins__ │        module │
│      __loader__ │          type │
│        __name__ │           str │
│               a │           str │
│           array │ numpy.ndarray │
│               d │          dict │
│        listvars │      function │
│           types │        module │
│            var1 │           str │
│            var2 │           str │
│            var4 │          dict │
╰─────────────────┴───────────────╯
```
