"""Exercise 2: numbers and comparisons.

Fill in the functions. Each one must `return` its answer.

to_seconds(milliseconds)
    Converts a response time from milliseconds to seconds.
    to_seconds(1250)  ->  1.25

is_slow(milliseconds, limit_ms)
    True when the response took longer than the limit, otherwise False.
    Exactly on the limit is not slow.
    is_slow(1200, 1000)  ->  True
    is_slow(1000, 1000)  ->  False

pass_rate(passed, total)
    The percentage of tests that passed, rounded to one decimal place.
    pass_rate(18, 20)  ->  90.0
    pass_rate(2, 3)    ->  66.7
"""


def to_seconds(milliseconds):
    # TODO: replace the line below
    return None


def is_slow(milliseconds, limit_ms):
    # TODO: replace the line below. A comparison already gives True or False.
    return None


def pass_rate(passed, total):
    # TODO: replace the line below
    return None


# Try your functions.
print(to_seconds(1250))
print(is_slow(1200, 1000))
print(pass_rate(18, 20))
