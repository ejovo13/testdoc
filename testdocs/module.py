"""Utilities for navigating the hierarchy of modules."""

from __future__ import annotations

import doctest
import sys
from typing import Any, Optional

from .exceptions import DocumentationError


class Module:
    """Wrapper around the built in ModuleType.

    Examples
    --------
    ```python
    >>> mod = Module('collections')
    >>> mod.name()
    'collections'

    >>> mod.submodule_names()
    ['collections.abc']

    ```

    """

    def __init__(self, module: str):
        """Look inside the sys.modules dictionary to get a handle to our module.

        Examples
        --------
        ```py
        >>> mod = Module('typing')
        >>> mod.name()
        'typing'

        ```

        """
        self.mod = sys.modules[module]

    def __str__(self) -> str:
        return str(self.mod)

    def __repr__(self) -> str:
        return repr(self.mod)

    def name(self) -> str:
        """Return the full name of our module."""
        return self.mod.__name__

    def root(self) -> Module:
        """Return the root module."""
        return Module(self.name().split(".")[0])

    def parent(self) -> Optional[Module]:
        """Return the parent module of `self` if it exists."""
        # Let's count the number of dots.
        n_dots = self.mod.__name__.count(".")

        return (
            None
            if n_dots == 0
            else (Module(".".join(self.mod.__name__.split(".")[:n_dots])))
        )

    def grand_parent(self) -> Optional[Module]:
        """Return self.parent().parent(), if it exists."""
        parent = self.parent()
        return None if parent is None else (parent.parent())

    def _mod_type(self) -> type:
        """Return the type `ModuleType`. For some reason we can't access this named tuple so we retrieve it dynamically."""
        return type(self.mod)

    def _new_child(self, mod_name: str) -> Optional[Module]:
        """Create a new Module that is a submodule of `self`."""
        child_name = f"{self.mod.__name__}.{mod_name}"
        try:
            return Module(child_name)
        except Exception:
            return None

    def submodules(self) -> list[Module]:
        """Return a list of modules belonging to `self`."""
        modules = [
            self._new_child(att) for att in dir(self.mod) if self._attr_is_module(att)
        ]
        return [m for m in modules if m is not None]

    def submodule_names(self) -> list[str]:
        """Return a list of submodule names that are children of `self`.

        Examples
        --------
        ```python
        >>> mod = Module('xml.etree')
        >>> mod.submodule_names()
        ['xml.etree.ElementPath', 'xml.etree.ElementTree']

        ```

        """
        return [child.name() for child in self.submodules()]

    def _attr_type(self, attribute_name: str) -> type:
        """Return the type of `attribute_name`."""
        return type(self._attr(attribute_name))

    def _attr(self, attribute_name: str) -> Any:
        """Retrieve an attribute from the underlying module."""
        return getattr(self.mod, attribute_name, None)

    def _attr_is_module(self, attribute_name: str) -> bool:
        """Check if the attribute in `dir(self)` is a submodule."""
        return isinstance(self._attr(attribute_name), self._mod_type())

    def doctest(self, verbose: bool = True, recursive: bool = False):
        """Call `doctest.testmod` on this module."""
        res = doctest.testmod(self.mod, verbose=verbose)
        if res.failed > 0:
            raise DocumentationError("Documentation error!")
        if recursive:
            for s in self.submodules():
                s.doctest(verbose=verbose, recursive=recursive)


def testmod(module: str, recursive=True, verbose: bool = False):
    """Call doctest on this module and if `submodules`, on all of it's submodules as well."""
    mod = Module(module)
    mod.doctest(verbose=verbose, recursive=recursive)
