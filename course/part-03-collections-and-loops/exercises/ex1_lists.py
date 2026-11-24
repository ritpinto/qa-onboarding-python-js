"""Exercise 1: lists and loops.

failed_codes(status_codes)
    Returns a new list with only the codes that are 400 or more, in the same order.
    failed_codes([200, 404, 500, 201])  ->  [404, 500]
    failed_codes([200, 201])            ->  []

count_failures(status_codes)
    Returns how many codes are 400 or more.
    count_failures([200, 404, 500, 201])  ->  2

average_time(times_ms)
    Returns the average of the response times, rounded to one decimal place.
    The list always has at least one item.
    average_time([120, 340, 95])  ->  185.0
"""


def failed_codes(status_codes):
    # TODO: replace the line below. Start with an empty list and append to it in a loop.
    return None


def count_failures(status_codes):
    # TODO: replace the line below
    return None


def average_time(times_ms):
    # TODO: replace the line below. Add the times up in a loop, then divide.
    return None


# Try your functions.
print(failed_codes([200, 404, 500, 201]))
print(count_failures([200, 404, 500, 201]))
print(average_time([120, 340, 95]))
