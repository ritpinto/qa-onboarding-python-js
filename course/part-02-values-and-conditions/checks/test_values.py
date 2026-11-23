"""Checks for part 2. Run with: uv run pytest course/part-02-values-and-conditions/checks"""

import pytest


def show(name, args):
    return f"{name}({', '.join(repr(arg) for arg in args)})"


def result_of(module, name, *args):
    """Call a learner function and turn any crash into a short, readable failure."""
    function = getattr(module, name, None)
    if function is None:
        pytest.fail(f"There is no function named {name}. Was it renamed or deleted?", pytrace=False)
    try:
        return function(*args)
    except Exception as error:
        pytest.fail(
            f"{show(name, args)} stopped with {type(error).__name__}: {error}", pytrace=False
        )


def expect(module, name, args, expected):
    actual = result_of(module, name, *args)
    # type() is compared too, so the text "200" does not pass for the number 200
    if actual != expected or type(actual) is not type(expected):
        pytest.fail(
            f"{show(name, args)}\n  expected: {expected!r}\n  your code returned: {actual!r}",
            pytrace=False,
        )


# ---------------------------------------------------------------- ex1


@pytest.mark.parametrize(
    "args, expected",
    [
        (("WEB", 7, "Login fails"), "WEB-7: Login fails"),
        (("MOB", 12, "Profile photo upload fails"), "MOB-12: Profile photo upload fails"),
    ],
)
def test_ex1_ticket_label(load, args, expected):
    expect(load("ex1_ticket_label"), "ticket_label", args, expected)


@pytest.mark.parametrize(
    "username, expected",
    [
        ("  Tester ", "tester"),
        ("ADMIN", "admin"),
        ("maria", "maria"),
        (" Maria Santos ", "maria santos"),
    ],
)
def test_ex1_clean_username(load, username, expected):
    expect(load("ex1_ticket_label"), "clean_username", (username,), expected)


# ---------------------------------------------------------------- ex2


@pytest.mark.parametrize("milliseconds, expected", [(1250, 1.25), (500, 0.5), (3000, 3.0)])
def test_ex2_to_seconds(load, milliseconds, expected):
    expect(load("ex2_response_time"), "to_seconds", (milliseconds,), expected)


@pytest.mark.parametrize(
    "args, expected",
    [((1200, 1000), True), ((1000, 1000), False), ((999, 1000), False), ((301, 300), True)],
)
def test_ex2_is_slow(load, args, expected):
    expect(load("ex2_response_time"), "is_slow", args, expected)


@pytest.mark.parametrize(
    "args, expected", [((18, 20), 90.0), ((2, 3), 66.7), ((0, 5), 0.0), ((7, 7), 100.0)]
)
def test_ex2_pass_rate(load, args, expected):
    expect(load("ex2_response_time"), "pass_rate", args, expected)


# ---------------------------------------------------------------- ex3


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Login fails", True),
        ("abc", True),
        ("x" * 120, True),
        ("  abc  ", True),
        ("ab", False),
        ("", False),
        ("     ", False),
        ("   ab   ", False),
        ("x" * 121, False),
    ],
)
def test_ex3_title_is_valid(load, title, expected):
    expect(load("ex3_title_rules"), "title_is_valid", (title,), expected)


@pytest.mark.parametrize(
    "priority, expected",
    [
        ("low", True),
        ("medium", True),
        ("high", True),
        ("critical", True),
        ("urgent", False),
        ("High", False),
        ("", False),
    ],
)
def test_ex3_priority_is_valid(load, priority, expected):
    expect(load("ex3_title_rules"), "priority_is_valid", (priority,), expected)


# ---------------------------------------------------------------- ex4 (checkpoint)


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (100, "informational"),
        (199, "informational"),
        (200, "success"),
        (201, "success"),
        (299, "success"),
        (300, "redirect"),
        (301, "redirect"),
        (399, "redirect"),
        (400, "client error"),
        (404, "client error"),
        (499, "client error"),
        (500, "server error"),
        (503, "server error"),
        (599, "server error"),
        (600, "unknown"),
        (99, "unknown"),
        (0, "unknown"),
    ],
)
def test_ex4_classify(load, status_code, expected):
    expect(load("ex4_status_codes"), "classify", (status_code,), expected)


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (200, "200: success"),
        (404, "404: client error"),
        (503, "503: server error"),
        (700, "700: unknown"),
    ],
)
def test_ex4_describe(load, status_code, expected):
    expect(load("ex4_status_codes"), "describe", (status_code,), expected)


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (429, True),
        (500, True),
        (503, True),
        (599, True),
        (200, False),
        (404, False),
        (428, False),
        (600, False),
    ],
)
def test_ex4_should_retry(load, status_code, expected):
    expect(load("ex4_status_codes"), "should_retry", (status_code,), expected)
