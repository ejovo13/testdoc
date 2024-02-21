"""Utilities for navigating the hierarchy of modules."""

from __future__ import annotations

import doctest
import sys
from typing import Any, Optional


class Module:
    """Wrapper around the built in ModuleType.

    Examples
    --------
    >>> mod = Module('sys')
    >>> mod.name()
    'sys'

    """

    def __init__(self, module: str):
        """Look inside the sys.modules dictionary to get a handle to our module."""
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

    def mod_type(self) -> type:
        """Return the type `ModuleType`. For some reason we can't access this named tuple so we retrieve it dynamically."""
        return type(self.mod)

    def new_child(self, mod_name: str) -> Module:
        """Create a new Module that is a submodule of `self`."""
        child_name = f"{self.mod.__name__}.{mod_name}"
        return Module(child_name)

    def submodules(self) -> list[Module]:
        """Return a list of modules belonging to `self`."""
        return [
            self.new_child(att) for att in dir(self.mod) if self.attr_is_module(att)
        ]

    def submodule_names(self) -> list[str]:
        """Return a list of submodule names that are children of `self`."""
        return [child.name() for child in self.submodules()]

    def attr_type(self, attribute_name: str) -> type:
        """Return the type of `attribute_name`."""
        return type(self.attr(attribute_name))

    def attr(self, attribute_name: str) -> Any:
        """Retrieve an attribute from the underlying module."""
        return getattr(self.mod, attribute_name, None)

    def attr_is_module(self, attribute_name: str) -> bool:
        """Check if the attribute in `dir(self)` is a submodule."""
        return isinstance(self.attr(attribute_name), self.mod_type())

    def test(self, **kwargs):
        """Call `doctest.testmod` on this module."""
        res = doctest.testmod(self.mod, **kwargs)
        if res.failed > 0:
            raise Exception("Documentation error!")


def testmod(module: str, submodules: bool = False, verbose: bool = False):
    """Call doctest on this module and if `submodules`, on all of it's submodules as well."""
    mod = Module(module)
    mod.test(verbose=verbose)
    if submodules:
        for s in mod.submodules():
            res = s.test(verbose=verbose)
            assert res
