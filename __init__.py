"""
listvars
========

List all global variables with additional filtering options.

Recommended import is::

  >>> from listvars import listvars
  >>> listvars()

For more information and filtering options, see the README.md or the
documentation of the listvars method.
"""

from .listvars import (
    listvars,
    content_width,
    filter_default,
    excl_base,
    excl_ipython,
    excl_default,
    fields_default,
)

__all__ = [
    'listvars',
    'content_width',
    'filter_default',
    'excl_base',
    'excl_ipython',
    'excl_default',
    'fields_default',
]
