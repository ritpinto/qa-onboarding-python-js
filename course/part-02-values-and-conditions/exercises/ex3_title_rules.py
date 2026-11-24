"""Exercise 3: booleans.

Fill in the functions. Each one must `return` its answer.

Tracklet's rule for a ticket title: after removing spaces from both ends,
it must be 3 to 120 characters long.

title_is_valid(title)
    True when the title follows the rule, otherwise False.
    title_is_valid("Login fails")   ->  True
    title_is_valid("ab")            ->  False   (too short)
    title_is_valid("   ab   ")      ->  False   (still too short once the spaces are removed)
    title_is_valid("x" * 121)       ->  False   (too long; "x" * 121 is 121 x's)

priority_is_valid(priority)
    True when priority is one of: low, medium, high, critical.
    priority_is_valid("high")    ->  True
    priority_is_valid("urgent")  ->  False
    priority_is_valid("High")    ->  False   (the rule is lowercase only)
"""


def title_is_valid(title):
    return 3 <= len(title.strip()) <= 120


def priority_is_valid(priority):
    return (priority == "low" or priority == "medium" or priority == "high" or priority == "critical")


# Try your functions.
print(title_is_valid("Login fails"))
print(title_is_valid("ab"))
print(priority_is_valid("urgent"))
