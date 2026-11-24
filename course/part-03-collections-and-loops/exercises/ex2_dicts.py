"""Exercise 2: dicts.

A ticket is a dict like this:

    {"id": 1, "title": "Login fails", "status": "open", "priority": "critical", "assignee_id": None}

ticket_summary(ticket)
    Returns one line describing the ticket.
    ticket_summary(the ticket above)  ->  "#1 [open] Login fails (critical)"

assign(ticket, user_id)
    Puts user_id into the ticket's "assignee_id". If the ticket's status is "open",
    also changes it to "in_progress". Any other status stays as it is.
    Returns the ticket.
    assign(the ticket above, 3)
    ->  the same ticket, now with "status": "in_progress" and "assignee_id": 3

unassigned_titles(tickets)
    Takes a list of tickets. Returns a list with the titles of the tickets
    whose "assignee_id" is None, in the same order.
    unassigned_titles([
        {"id": 1, "title": "Login fails", "assignee_id": None},
        {"id": 2, "title": "Typo on the home page", "assignee_id": 3},
    ])
    ->  ["Login fails"]
"""


def ticket_summary(ticket):
    # TODO: replace the line below
    return None


def assign(ticket, user_id):
    # TODO: change the ticket, then return it
    return None


def unassigned_titles(tickets):
    # TODO: replace the line below
    return None


# Try your functions.
example = {
    "id": 1,
    "title": "Login fails",
    "status": "open",
    "priority": "critical",
    "assignee_id": None,
}
print(ticket_summary(example))
print(unassigned_titles([example]))
print(assign(example, 2))
