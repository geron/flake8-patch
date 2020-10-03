from flake8_plugin_utils import assert_error, assert_not_error

from flake8_patch.errors import AssignmentError
from flake8_patch.visitors.assignment import AssignmentVisitor


def test_ignores_single_target():
    code = """
        import a
        a = 42
    """
    assert_not_error(AssignmentVisitor, code)


def test_ignores_non_imported_target():
    code = """
        a.b = 42
    """
    assert_not_error(AssignmentVisitor, code)


def test_returns_error_for_attribute_ref():
    code = """
        import a
        a.b = 42
    """
    assert_error(AssignmentVisitor, code, AssignmentError, name="a")


def test_handles_iterable_target():
    code = """
        import b
        (a, (b.c, c), d) = 42, (43, 44), 45
    """
    assert_error(AssignmentVisitor, code, AssignmentError, name="b")


def test_handles_subscription():
    code = """
        import a
        a["k"] = 42
    """
    assert_error(AssignmentVisitor, code, AssignmentError, name="a")


def test_handles_attribute_subscription():
    code = """
        import a
        a.b["k"] = 42
    """
    assert_error(AssignmentVisitor, code, AssignmentError, name="a")


def test_ignores_usage_in_subscription():
    code = """
        import b
        a[b.c] = 42
    """
    assert_not_error(AssignmentVisitor, code)


def test_handles_slice():
    code = """
        import a
        a[:4] = [42, 43]
    """
    assert_error(AssignmentVisitor, code, AssignmentError, name="a")


def test_ignores_usage_in_slice():
    code = """
        import b
        a[:b.c] = [42, 43]
    """
    assert_not_error(AssignmentVisitor, code)


def test_ignores_single_star():
    code = """
        import b
        a, *b = 42, 43, 44
    """
    assert_not_error(AssignmentVisitor, code)


def test_returns_error_for_star_with_attribute():
    code = """
        import b
        a, *b.c = 42, 43, 44
    """
    assert_error(AssignmentVisitor, code, AssignmentError, name="b")


def test_ignores_usage_in_argument():
    code = """
        import e, f
        f(e.d, "c").b.a = 42
    """
    assert_not_error(AssignmentVisitor, code)


def test_ignores_usage_in_value_expression():
    code = """
        import b
        a = b.c
    """
    assert_not_error(AssignmentVisitor, code)


def test_handles_aug_assign():
    code = """
        import a
        a.b += 42
    """
    assert_error(AssignmentVisitor, code, AssignmentError, name="a")
