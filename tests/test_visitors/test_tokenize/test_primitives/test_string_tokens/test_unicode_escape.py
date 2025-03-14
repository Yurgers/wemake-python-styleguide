import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongUnicodeEscapeViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongStringTokenVisitor,
)


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize(
    'code',
    [
        r"b'\ua'",
        r"b'\u1'",
        r"b'\Ua'",
        r"b'\N{GREEK SMALL LETTER ALPHA}'",
    ],
)
def test_wrong_unicode_escape(  # pragma: >=3.12 cover
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that wrong unicode escape raises a warning."""
    try:
        file_tokens = parse_tokens(code)
    except SyntaxError:  # pragma: no cover
        pytest.skip(f'SyntaxError on unicode escapes: {code}')

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongUnicodeEscapeViolation])


@pytest.mark.parametrize(
    'code',
    [
        r"'\ua'",
        r"'\u1'",
        r"'\Ua'",
        r"'\N{GREEK SMALL LETTER ALPHA}'",
    ],
)
def test_correct_unicode_escape(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct unicode escape does not raise a warning."""
    file_tokens = parse_tokens(code, do_compile=False)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
