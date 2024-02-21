"""Run doctest on the entire module."""

import argparse

from .module import Module


def main():
    """Try and test documentation for a whole module."""
    parser = argparse.ArgumentParser()
    parser.add_argument("module")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-r", "--recursive", action="store_true")

    args = parser.parse_args()

    mod = Module(args.module)
    print(mod)
    mod.doctest(verbose=args.verbose, recursive=args.recursive)


if __name__ == "__main__":
    main()
