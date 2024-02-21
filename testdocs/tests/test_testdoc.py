# from ..import module
from ..module import Module

def test_modules():
    # print(__name__)
    mod = Module(__name__)
    parent = mod.parent()
    grand_parent = parent.parent()
    print(mod)
    print(parent)
    print(grand_parent)
    print(grand_parent.parent())

    ps = parent.submodules()
    ps_names = [p.name() for p in ps]
    print(ps_names)
    # Assert the number of submodules

    gp_sn = grand_parent.submodule_names()
    assert "testdocs.module" in gp_sn
    assert "testdocs.tests" in gp_sn

    assert grand_parent.name() == "testdocs"


def test_documentation():
    """Meta!"""
    test_mod = Module(__name__)
    testdoc = test_mod.grand_parent()
    root = test_mod.root()

    assert testdoc.name() == root.name()

    root.doctest(recursive=True, verbose=True)

def test_info():
    """Get some information about the output."""
    sys = Module("sys")
    print(sys)
    print(sys.submodule_names())
    col = Module("collections")
    print(col.submodule_names())

def test_xml():
    """Traverse the XML module tree."""

    xml = Module('xml')
    print(xml)
    print(xml.submodule_names())
    etree = xml.submodules()[0]
    print(etree.submodule_names())