# Part 3: Collections and loops

## What you will be able to do

- Keep many values together in a list and get them back out.
- Describe one thing, such as a ticket, with a dict.
- Repeat work over every item with a `for` loop.
- Use the four loop patterns testers need most: filter, total, count and group.
- Read a traceback and find the line that failed.
- Summarise a log file by error type, which is this part's checkpoint.

Type the examples. For each one, predict the output before you run it.

## 1. Lists

A **list** is an ordered collection of values, written in square brackets.

```python
status_codes = [200, 404, 500, 200]

print(status_codes)
print(len(status_codes))
print(status_codes[0])
print(status_codes[1])
print(status_codes[-1])
```

Output:

```text
[200, 404, 500, 200]
4
200
404
200
```

- `len(...)` gives the number of items.
- The number in square brackets is the **index**: the position of an item. Counting starts at 0, so the first item is `[0]` and the last of four items is `[3]`.
- `[-1]` is the last item, whatever the length.

### Changing a list

```python
failures = []
failures.append("test_login")
failures.append("test_checkout")

print(failures)
print("test_login" in failures)
print("test_search" in failures)
```

Output:

```text
['test_login', 'test_checkout']
True
False
```

`[]` is an empty list. `.append(...)` adds an item to the end. `in` asks whether a value is in the list.

## 2. `for` loops

A **loop** repeats lines of code. A `for` loop runs its block once for each item in a list.

```python
status_codes = [200, 404, 500]

for code in status_codes:
    print(f"Got {code}")

print("Done")
```

Output:

```text
Got 200
Got 404
Got 500
Done
```

`code` is a variable. On each pass it holds the next item. You choose the name. The indented lines are the loop's block, the same rule as for `if`. `print("Done")` is not indented, so it runs once, after the loop.

### Pattern 1: filter

Start with an empty list. Add the items you want.

```python
status_codes = [200, 404, 500, 201, 403]
errors = []

for code in status_codes:
    if code >= 400:
        errors.append(code)

print(errors)
```

Output:

```text
[404, 500, 403]
```

The `if` is inside the loop, so it is indented once. The `append` is inside the `if`, so it is indented twice.

### Pattern 2: total

Start at zero. Add to it on each pass.

```python
times_ms = [120, 340, 95]
total = 0

for time in times_ms:
    total = total + time

print(total)
print(total / len(times_ms))
```

Output:

```text
555
185.0
```

`total = total + time` means "the new total is the old total plus this item".

## 3. Dicts

A **dict** (dictionary) stores pairs: a **key** and its **value**. Use one to describe a single thing with named parts. An API returns a ticket in this shape.

```python
ticket = {
    "id": 1,
    "title": "Login fails with valid password",
    "status": "open",
    "assignee_id": None,
}

print(ticket["title"])
print(ticket["status"])

ticket["status"] = "in_progress"
ticket["priority"] = "critical"
print(ticket)
```

Output:

```text
Login fails with valid password
open
{'id': 1, 'title': 'Login fails with valid password', 'status': 'in_progress', 'assignee_id': None, 'priority': 'critical'}
```

- A dict is written in curly braces, with a colon between each key and its value.
- `ticket["title"]` reads the value stored under the key `"title"`.
- `ticket["status"] = ...` changes a value. If the key does not exist yet, as with `"priority"`, it is added.

### When a key might be missing

Reading a key that is not there is an error. Two ways to stay safe:

```python
ticket = {"id": 1, "title": "Login fails"}

print("assignee" in ticket)
print(ticket.get("assignee"))
print(ticket.get("assignee", "Unassigned"))
```

Output:

```text
False
None
Unassigned
```

`in` asks whether the key exists. `.get(key, default)` reads the value, or gives you the default when the key is missing.

### A list of dicts

Most API responses you will test are a list of dicts. A loop walks the list; inside it you read keys.

```python
tickets = [
    {"id": 1, "title": "Login fails", "status": "open"},
    {"id": 2, "title": "Cart total wrong", "status": "in_progress"},
    {"id": 3, "title": "Search is slow", "status": "open"},
]

for ticket in tickets:
    if ticket["status"] == "open":
        print(f"#{ticket['id']} {ticket['title']}")
```

Output:

```text
#1 Login fails
#3 Search is slow
```

Inside an f-string written with double quotes, use single quotes for the key: `ticket['id']`.

To ask whether a value is `None`, write `is None`:

```python
ticket = {"id": 3, "title": "Search is slow", "assignee_id": None}

if ticket["assignee_id"] is None:
    print("Nobody is working on this")
```

Output:

```text
Nobody is working on this
```

### Pattern 3: count

A dict can keep a tally: the thing being counted is the key, the count is the value.

```python
statuses = ["open", "closed", "open", "resolved", "open"]
counts = {}

for status in statuses:
    if status in counts:
        counts[status] = counts[status] + 1
    else:
        counts[status] = 1

print(counts)
```

Output:

```text
{'open': 3, 'closed': 1, 'resolved': 1}
```

The first time a status is seen, it is added with a count of 1. After that, its count goes up by 1. You will use this pattern in the checkpoint.

### Pattern 4: group

The value in a dict can be a list. That lets you sort items into groups: the group is the key, the list of its members is the value.

```python
codes = [200, 404, 201, 500, 403]
groups = {}

for code in codes:
    if code < 400:
        kind = "ok"
    else:
        kind = "failed"
    if kind in groups:
        groups[kind].append(code)
    else:
        groups[kind] = [code]

print(groups)
```

Output:

```text
{'ok': [200, 201], 'failed': [404, 500, 403]}
```

It is the count pattern with one change: the first time a group is seen it gets a list holding one item, and after that the item is appended to that list.

### Looping over a dict

`sorted(...)` gives the keys in alphabetical order, which makes reports stable from run to run.

```python
counts = {"open": 3, "closed": 1, "resolved": 1}

for status in sorted(counts):
    print(f"{status}: {counts[status]}")
```

Output:

```text
closed: 1
open: 3
resolved: 1
```

## 4. Splitting text into parts

Log lines and CSV rows pack several values into one string. `.split(separator)` cuts a string into a list.

```python
line = "2026-01-05 10:00:07 | ERROR | TimeoutError | payment service did not answer"
parts = line.split(" | ")

print(parts)
print(parts[1])
print(parts[2])
```

Output:

```text
['2026-01-05 10:00:07', 'ERROR', 'TimeoutError', 'payment service did not answer']
ERROR
TimeoutError
```

## 5. Reading a traceback

When a script crashes, Python prints a **traceback**: a report of where it was when things went wrong. Beginners see a wall of red and stop reading. A traceback is the most useful message you will get all day.

This script has a mistake.

```py
def first_title(tickets):
    return tickets[0]["titel"]


tickets = [{"id": 1, "title": "Login fails"}]
print(first_title(tickets))
```

```text
Traceback (most recent call last):
  File "example.py", line 6, in <module>
    print(first_title(tickets))
          ~~~~~~~~~~~^^^^^^^^^
  File "example.py", line 2, in first_title
    return tickets[0]["titel"]
           ~~~~~~~~~~^^^^^^^^^
KeyError: 'titel'
```

Read it in this order:

1. **The last line** is what went wrong. `KeyError: 'titel'` means a dict was asked for a key it does not have, and the key was `'titel'`.
2. **The block just above it** is where it happened: file `example.py`, line 2, inside the function `first_title`. The marks under the code point at the exact part.
3. **The blocks further up** show how the script got there: line 6 called `first_title`. Read upwards only if you need to know who called the failing line.

Then look at line 2 with the error in mind. The key is misspelled.

### The errors you will meet in this part

| Last line of the traceback | Meaning | Usual cause |
|---|---|---|
| `IndexError: list index out of range` | The list has no item at that position | Forgot that counting starts at 0, or the list is empty |
| `KeyError: 'name'` | The dict has no such key | Typo in the key, or the key is optional |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | Two types that cannot be combined | A number that is still text; convert with `int(...)` |
| `TypeError: 'NoneType' object is not subscriptable` | You used `[...]` on `None` | A function returned `None` instead of a list or dict |
| `NameError: name 'x' is not defined` | Python does not know that name | Typo, or the variable is created later or inside another block |

## Common mistakes

**Off by one.** A list of 3 items has indexes 0, 1 and 2.

```py
codes = [200, 404, 500]
print(codes[3])
```

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(codes[3])
          ~~~~~^^^
IndexError: list index out of range
```

**Resetting inside the loop.** The total or the empty list must be created before the loop. Created inside, it starts again on every pass, and you keep only the last item. There is no error message; the answer is just wrong.

**Returning inside the loop.** A `return` indented under the `for` ends the function on the first pass. If your function handles only the first item, check the indentation of `return`.

**Adding text to a number.**

```py
total = 0
for duration in ["120", "340"]:
    total = total + duration
```

```text
Traceback (most recent call last):
  File "example.py", line 3, in <module>
    total = total + duration
            ~~~~~~^~~~~~~~~~
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Square brackets or curly braces.** `[...]` makes a list, `{...}` with colons makes a dict. To read from either one you use square brackets: `codes[0]`, `ticket["title"]`.

## Checkpoint

Do the five files in `exercises/`, in order.

- `ex4_fix_the_bugs.py` crashes when you run it. That is the exercise: run it, read the traceback, fix one bug, run it again.
- `ex5_log_summary.py` is the checkpoint. It reads `exercises/data/app.log`. The two lines that read the file are written for you; files are the next part's topic.

Run a file to try it:

```bash
uv run python course/part-03-collections-and-loops/exercises/ex5_log_summary.py
```

Run the checks:

```bash
uv run pytest course/part-03-collections-and-loops/checks
```

Hand in a branch named `part-03-yourname` and a pull request, as described in the [learner guide](../../docs/learner-guide.md). Words you are unsure of are in the [glossary](../../docs/glossary.md).
