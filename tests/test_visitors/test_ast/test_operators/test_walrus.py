import pytest

from wemake_python_styleguide.violations.consistency import WalrusViolation
from wemake_python_styleguide.visitors.ast.operators import WalrusVisitor

# Correct:
correct_assignment = 'x = 1'
correct_if_condition = """
some = call()
if some:
    ...
"""

correct_comprehension = """
some = [
    x * 2
    for y in [1, 2, 3]
    if y > 2
]
"""
correct_walrus_comprehension = """
some = [
    x + y
    for y in [1, 2, 3]
    if (x := y) > 2
]
"""

correct_dict_comprehension = """
some = {
    (key := compute_key(i)): values[key]
    for i in range(10)
}
"""

# Wrong:
wrong_assignment = 'print(x := 1)'
wrong_if_condition = """
if some := call():
    ...
"""


@pytest.mark.parametrize(
    'code',
    [
        correct_assignment,
        correct_if_condition,
        correct_comprehension,
        correct_walrus_comprehension,
        correct_dict_comprehension,
    ],
)
def test_not_walrus(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that regular code is allowed."""
    tree = parse_ast_tree(code)

    visitor = WalrusVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        wrong_assignment,
        wrong_if_condition,
    ],
)
def test_walrus(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that ``:=`` is not allowed."""
    tree = parse_ast_tree(code)

    visitor = WalrusVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WalrusViolation])
