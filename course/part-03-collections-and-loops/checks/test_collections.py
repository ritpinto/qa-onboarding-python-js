"""Checks for part 3. Run with: uv run pytest course/part-03-collections-and-loops/checks"""

import copy

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
    shown = show(name, copy.deepcopy(args))  # remember the input before the function changes it
    actual = result_of(module, name, *args)
    if actual != expected or type(actual) is not type(expected):
        pytest.fail(
            f"{shown}\n  expected: {expected!r}\n  your code returned: {actual!r}", pytrace=False
        )


def ticket(**changes):
    base = {
        "id": 1,
        "title": "Login fails",
        "status": "open",
        "priority": "critical",
        "assignee_id": None,
    }
    return {**base, **changes}


# ---------------------------------------------------------------- ex1


@pytest.mark.parametrize(
    "codes, expected",
    [
        ([200, 404, 500, 201], [404, 500]),
        ([200, 201], []),
        ([], []),
        ([400, 399], [400]),
        ([503, 200, 503], [503, 503]),
    ],
)
def test_ex1_failed_codes(load, codes, expected):
    expect(load("ex1_lists"), "failed_codes", (codes,), expected)


@pytest.mark.parametrize(
    "codes, expected", [([200, 404, 500, 201], 2), ([200, 201], 0), ([], 0), ([400], 1)]
)
def test_ex1_count_failures(load, codes, expected):
    expect(load("ex1_lists"), "count_failures", (codes,), expected)


@pytest.mark.parametrize(
    "times, expected", [([120, 340, 95], 185.0), ([100], 100.0), ([100, 101, 101], 100.7)]
)
def test_ex1_average_time(load, times, expected):
    expect(load("ex1_lists"), "average_time", (times,), expected)


# ---------------------------------------------------------------- ex2


@pytest.mark.parametrize(
    "a_ticket, expected",
    [
        (ticket(), "#1 [open] Login fails (critical)"),
        (
            ticket(id=12, title="Upload fails", status="closed", priority="high"),
            "#12 [closed] Upload fails (high)",
        ),
    ],
)
def test_ex2_ticket_summary(load, a_ticket, expected):
    expect(load("ex2_dicts"), "ticket_summary", (a_ticket,), expected)


@pytest.mark.parametrize(
    "status, expected_status",
    [("open", "in_progress"), ("in_progress", "in_progress"), ("resolved", "resolved")],
)
def test_ex2_assign(load, status, expected_status):
    expected = ticket(status=expected_status, assignee_id=3)
    expect(load("ex2_dicts"), "assign", (ticket(status=status), 3), expected)


def test_ex2_unassigned_titles(load):
    tickets = [
        ticket(id=1, title="First"),
        ticket(id=2, title="Second", assignee_id=2),
        ticket(id=3, title="Third"),
    ]
    module = load("ex2_dicts")
    expect(module, "unassigned_titles", (tickets,), ["First", "Third"])
    expect(module, "unassigned_titles", ([ticket(assignee_id=1)],), [])
    expect(module, "unassigned_titles", ([],), [])


# ---------------------------------------------------------------- ex3

TICKETS = [
    {"title": "A", "status": "open", "priority": "low"},
    {"title": "B", "status": "closed", "priority": "high"},
    {"title": "C", "status": "open", "priority": "high"},
    {"title": "D", "status": "open", "priority": "critical"},
]


def test_ex3_count_by_status(load):
    module = load("ex3_counting")
    expect(module, "count_by_status", (TICKETS,), {"open": 3, "closed": 1})
    expect(module, "count_by_status", ([],), {})


def test_ex3_titles_by_priority(load):
    module = load("ex3_counting")
    expected = {"low": ["A"], "high": ["B", "C"], "critical": ["D"]}
    expect(module, "titles_by_priority", (TICKETS,), expected)
    expect(module, "titles_by_priority", ([],), {})


# ---------------------------------------------------------------- ex4


@pytest.mark.parametrize(
    "codes, expected", [([200, 404, 500], 500), ([201], 201), ([200, 200, 404], 404)]
)
def test_ex4_last_status(load, codes, expected):
    expect(load("ex4_fix_the_bugs"), "last_status", (codes,), expected)


@pytest.mark.parametrize(
    "a_ticket, expected",
    [({"id": 1, "assignee": "Maria"}, "Maria"), ({"id": 2}, "Unassigned")],
)
def test_ex4_assignee_of(load, a_ticket, expected):
    expect(load("ex4_fix_the_bugs"), "assignee_of", (a_ticket,), expected)


@pytest.mark.parametrize("durations, expected", [(["120", "340", "95"], 555), (["7"], 7), ([], 0)])
def test_ex4_total_duration(load, durations, expected):
    expect(load("ex4_fix_the_bugs"), "total_duration", (durations,), expected)


# ---------------------------------------------------------------- ex5 (checkpoint)

LINES = [
    "2026-02-01 08:00:00 | INFO | Startup | started",
    "2026-02-01 08:00:01 | ERROR | TimeoutError | no answer",
    "",
    "2026-02-01 08:00:02 | WARNING | SlowQuery | search took 2 s",
    "2026-02-01 08:00:03 | ERROR | KeyError | missing field",
    "2026-02-01 08:00:04 | ERROR | TimeoutError | no answer",
    "2026-02-01 08:00:05 | INFO | Report | no ERROR lines in the last hour",
]


def test_ex5_count_levels(load):
    module = load("ex5_log_summary")
    expect(module, "count_levels", (LINES,), {"INFO": 2, "ERROR": 3, "WARNING": 1})
    expect(module, "count_levels", ([],), {})


def test_ex5_count_error_types(load):
    module = load("ex5_log_summary")
    expect(module, "count_error_types", (LINES,), {"TimeoutError": 2, "KeyError": 1})
    expect(module, "count_error_types", (LINES[:1],), {})


def test_ex5_script_prints_the_summary(run_script):
    printed = [line.strip() for line in run_script("ex5_log_summary").splitlines()]
    expected = ["ConnectionError: 2", "PermissionError: 1", "TimeoutError: 4", "ValidationError: 1"]
    found = [line for line in printed if line in expected]
    if found != expected:
        wanted = "\n".join(f"    {line}" for line in expected)
        shown = "\n".join(f"    {line}" for line in printed) or "    (nothing)"
        pytest.fail(
            "Running ex5_log_summary.py should print these lines, in this order:\n"
            f"{wanted}\n  your script printed:\n{shown}",
            pytrace=False,
        )
