"""Exercise 5 (checkpoint): summarise a log file.

Each line of data/app.log has four parts separated by " | ":

    2026-01-05 10:00:07 | ERROR | TimeoutError | payment service did not answer
    (time)              | (level) | (name)     | (message)

The level is INFO, WARNING or ERROR. The file also contains empty lines; skip them.

The examples below use this list of three lines:

    [
        "2026-01-05 10:00:01 | INFO | Startup | started",
        "2026-01-05 10:00:07 | ERROR | TimeoutError | payment service did not answer",
        "2026-01-05 10:00:09 | INFO | Report | no ERROR lines in the last minute",
    ]

count_levels(lines)
    Takes a list of log lines. Returns a dict with how many lines have each level.
    Levels that do not appear are left out.
    count_levels(the list above)  ->  {"INFO": 2, "ERROR": 1}

count_error_types(lines)
    Returns a dict counting the name (third part) of the lines whose level
    (second part) is ERROR. The word ERROR somewhere else in a line, as in the
    third line above, does not make it an ERROR line.
    count_error_types(the list above)  ->  {"TimeoutError": 1}

Write and check the two functions first. Then finish the script at the bottom
so that running this file prints every error type in data/app.log with its
count, in alphabetical order, one per line, in this form (these names and
numbers are made up):

    DiskError: 3
    LoginError: 1
"""

from pathlib import Path


def count_levels(lines):
    # TODO: replace the line below
    return None


def count_error_types(lines):
    # TODO: replace the line below
    return None


# These two lines read the log file into a list of lines. They are written for you;
# reading files is the next part's topic.
log_path = Path(__file__).parent / "data" / "app.log"
lines = log_path.read_text().splitlines()

print(f"Read {len(lines)} lines")
print(count_levels(lines))

# TODO: call count_error_types(lines) and print each error type with its count,
# in alphabetical order, in the form  DiskError: 3
