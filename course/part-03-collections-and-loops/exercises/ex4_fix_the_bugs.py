"""Exercise 4: read the traceback, fix the bug.

This file crashes. There are three bugs, one in each function.

How to work:
  1. Run the file:
         uv run python course/part-03-collections-and-loops/exercises/ex4_fix_the_bugs.py
  2. Read the traceback from the bottom: what went wrong, then on which line.
  3. Fix that one bug. Run again. The next bug will show itself.

Change as little as you can. The text under each `def` line says what the
function should do; that text is right and the code is wrong.
"""


def last_status(status_codes):
    """Returns the last status code in the list.

    last_status([200, 404, 500])  ->  500
    """
    return status_codes[len(status_codes)]


def assignee_of(ticket):
    """Returns the ticket's "assignee", or "Unassigned" when the ticket has no such key.

    assignee_of({"id": 1, "assignee": "Maria"})  ->  "Maria"
    assignee_of({"id": 2})                       ->  "Unassigned"
    """
    return ticket["assignee"]


def total_duration(durations):
    """Returns the total of the durations as a whole number.

    The durations were read from a log file, so each one is text.
    total_duration(["120", "340", "95"])  ->  555
    """
    total = 0
    for duration in durations:
        total = total + duration
    return total


# The lines below run when you run this file, but not when the checks load it, so each
# function is checked on its own. Part 4 explains the `if` line; leave it as it is.
if __name__ == "__main__":
    print(last_status([200, 404, 500]))
    print(assignee_of({"id": 1, "assignee": "Maria"}))
    print(assignee_of({"id": 2}))
    print(total_duration(["120", "340", "95"]))
