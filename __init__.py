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

from .listvars import listvars, contentwidth

__all__ = ['listvars', 'contentwidth']


# Remove private objects
resolve = None
del resolve
