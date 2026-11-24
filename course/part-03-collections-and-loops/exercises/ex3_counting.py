"""Exercise 3: counting and grouping with a dict.

Each function takes a list of tickets. A ticket is a dict with at least
"title", "status" and "priority".

count_by_status(tickets)
    Returns a dict: each status that appears, and how many tickets have it.
    Statuses that do not appear are left out.

    count_by_status([
        {"title": "A", "status": "open", "priority": "low"},
        {"title": "B", "status": "closed", "priority": "high"},
        {"title": "C", "status": "open", "priority": "high"},
    ])
    ->  {"open": 2, "closed": 1}

titles_by_priority(tickets)
    Returns a dict: each priority that appears, and the list of titles with it,
    in the order they came.

    titles_by_priority(the same list)
    ->  {"low": ["A"], "high": ["B", "C"]}
"""


def count_by_status(tickets):
    # TODO: replace the line below. Start with an empty dict.
    return None


def titles_by_priority(tickets):
    # TODO: replace the line below. The value for each key is a list you append to
    # (pattern 4 in the lesson).
    return None


# Try your functions.
examples = [
    {"title": "A", "status": "open", "priority": "low"},
    {"title": "B", "status": "closed", "priority": "high"},
    {"title": "C", "status": "open", "priority": "high"},
]
print(count_by_status(examples))
print(titles_by_priority(examples))
