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
    assert "testdoc.module" in gp_sn
    assert "testdoc.tests" in gp_sn

    assert grand_parent.name() == "testdoc"


def test_documentation():
    """Meta!"""
    test_mod = Module(__name__)
    testdoc = test_mod.grand_parent()
    root = test_mod.root()

    assert testdoc.name() == root.name()

    root.test(verbose=True)
    for s in root.submodules():
        s.test(verbose=True)

