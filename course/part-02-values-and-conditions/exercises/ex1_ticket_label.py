"""Exercise 1: strings.

Fill in the two functions. Each one must `return` its answer.

ticket_label(project_key, ticket_id, title)
    Builds the label shown at the top of a ticket.
    ticket_label("WEB", 7, "Login fails")  ->  "WEB-7: Login fails"

clean_username(username)
    Removes spaces from both ends and makes the text lowercase.
    clean_username("  Tester ")  ->  "tester"
"""


def ticket_label(project_key, ticket_id, title):
    return f"{project_key}-{ticket_id}: {title}"


def clean_username(username):
    return username.strip().lower()


# Try your functions: run this file and compare with the examples above.
print(ticket_label("WEB", 7, "Login fails"))
print(clean_username("  Tester "))
