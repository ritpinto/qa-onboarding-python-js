# Part 2: Values and conditions

## What you will be able to do

- Store values in variables and say what type each one is.
- Build and clean up text: ticket labels, usernames, messages.
- Do arithmetic on test results and response times.
- Compare values and make the script choose what to do with `if`.
- Classify an HTTP status code, which is this part's checkpoint.

Type the examples into `scratch.py` in this part's `exercises` folder, as in part 1, and run them with `uv run python course/part-02-values-and-conditions/exercises/scratch.py`. Git ignores that file, so it is not handed in. Change one thing in each and predict the output before you run it.

## 1. Values and types

Everything a script works with is a **value**. Every value has a **type**, which is the kind of thing it is.

| Type | Python name | Examples | Used for |
|---|---|---|---|
| Whole number | `int` | `200`, `0`, `-1` | Status codes, counts, ids |
| Decimal number | `float` | `0.35`, `99.5` | Durations, percentages |
| Text | `str` (string) | `"open"`, `"Login fails"` | Titles, statuses, messages |
| Yes or no | `bool` (boolean) | `True`, `False` | Results of checks |
| Nothing | `NoneType` | `None` | "No value", such as a ticket with no assignee |

`type()` tells you the type of a value.

```python
print(type(200))
print(type(0.35))
print(type("open"))
print(type(True))
print(type(None))
```

Output:

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

The type matters because it decides what you can do with the value. `200` and `"200"` look alike to a person. To Python the first is a number and the second is text, and they are not equal.

## 2. Variables

A **variable** is a name that refers to a value. `=` gives the name its value. Read it as "becomes", not "equals".

```python
status_code = 200
title = "Login fails with valid password"
assignee = None

print(status_code)
print(title)
print(assignee)
```

Output:

```text
200
Login fails with valid password
None
```

A variable can be given a new value later. The old one is forgotten.

```python
status = "open"
print(status)
status = "in_progress"
print(status)
```

Output:

```text
open
in_progress
```

Names can use letters, digits and underscores, and cannot start with a digit. By convention, variables use lowercase with underscores between words. Pick names that say what the value is. `response_time_ms` tells the reader more than `t`.

## 3. Strings

A **string** is text in quotes. Single or double quotes both work; this course uses double.

### Putting values into text

An **f-string** is a string with an `f` before the opening quote. Inside it, anything in curly braces is replaced by its value.

```python
project_key = "WEB"
ticket_id = 7
title = "Login fails"

print(f"{project_key}-{ticket_id}: {title}")
```

Output:

```text
WEB-7: Login fails
```

You will use f-strings constantly: for messages, URLs and test names.

### Useful things strings can do

A **method** is an action that belongs to a value. You call it with a dot after the value.

```python
username = "  Tester  "

print(len(username))
print(username.strip())
print(username.strip().lower())
print(username.upper())
print("fail" in "Login fails")
print("Login fails".startswith("Login"))
```

Output:

```text
10
Tester
tester
  TESTER  
True
True
```

- `len(...)` counts characters, spaces included.
- `.strip()` removes spaces from both ends. Users type them by accident, and tests must cope.
- `.lower()` and `.upper()` change the case.
- `in` asks whether one string appears inside another.
- `.startswith(...)` asks whether the string begins with some text.

None of these change the original. They produce a new string. To keep the result, give it a name: `clean = username.strip()`.

## 4. Numbers

```python
passed = 18
failed = 2
total = passed + failed

print(total)
print(passed / total)
print(passed / total * 100)
print(1250 / 1000)
print(round(2.34567, 1))
```

Output:

```text
20
0.9
90.0
1.25
2.3
```

`+`, `-`, `*` and `/` work as you expect. `/` always gives a `float`, even when the answer is whole. `round(value, 1)` keeps one decimal place.

### Converting between types

Values read from files, web pages and API responses often arrive as text. Convert them before doing arithmetic.

```python
text = "200"
number = int(text)

print(number + 1)
print(str(number) + " OK")
print(float("0.35") * 2)
```

Output:

```text
201
200 OK
0.7
```

`int(...)` makes a whole number, `float(...)` a decimal, `str(...)` a string.

## 5. Comparisons and booleans

A **comparison** asks a question and gives back `True` or `False`.

| Operator | Meaning |
|---|---|
| `==` | equal to |
| `!=` | not equal to |
| `<` `>` | less than, greater than |
| `<=` `>=` | less than or equal, greater than or equal |

```python
status_code = 404

print(status_code == 200)
print(status_code != 200)
print(status_code >= 400)
print(400 <= status_code <= 499)
print("200" == 200)
```

Output:

```text
False
True
True
True
False
```

One `=` gives a name a value. Two `==` compare. Mixing them up is the most common slip of this part. The last line shows the type trap again: text is never equal to a number.

### Combining questions

`and`, `or` and `not` join comparisons.

```python
status_code = 503
response_time_ms = 1800

print(status_code == 200 and response_time_ms < 1000)
print(status_code == 429 or status_code >= 500)
print(not status_code == 200)
```

Output:

```text
False
True
True
```

- `and` is `True` only when both sides are.
- `or` is `True` when at least one side is.
- `not` flips `True` and `False`.

## 6. Choosing with `if`

`if` runs some lines only when a condition is `True`.

```python
status_code = 404

if status_code == 200:
    print("OK")
elif status_code == 404:
    print("Not found")
else:
    print("Something else")
```

Output:

```text
Not found
```

How to read it:

- Python checks the conditions from the top and runs the first block whose condition is `True`. The rest are skipped.
- `elif` means "otherwise, if". You can have as many as you need.
- `else` catches everything left over. It is optional.
- Each condition line ends with a colon.
- The lines that belong to a condition are **indented**: they start with four spaces. The indentation is how Python knows which lines belong to which condition. VS Code adds it when you press Enter after a colon.

Order matters when conditions overlap. Put the most specific first.

```python
response_time_ms = 2500

if response_time_ms > 2000:
    print("very slow")
elif response_time_ms > 1000:
    print("slow")
else:
    print("fine")
```

Output:

```text
very slow
```

If the two tests were swapped, 2500 would be reported as only "slow", because it is also greater than 1000 and that test would come first.

## 7. Filling in a function

This part's exercises ask you to fill in **functions**. A function is a named block of code that takes values in and hands one value back with `return`. Part 4 teaches them properly. For now, you only write the lines inside.

```python
def is_error(status_code):
    if status_code >= 400:
        return True
    return False


print(is_error(200))
print(is_error(500))
```

Output:

```text
False
True
```

- `def is_error(status_code):` starts the function. `status_code` is the value it receives.
- Everything indented under it is the function's code.
- `return` ends the function and hands back a value. Nothing after a `return` that ran is carried out.
- `is_error(500)` **calls** the function with the value 500.

The checks call your functions with different values and compare what comes back. So a function must `return` its answer. Printing it is not enough.

## Common mistakes

Read errors from the bottom: the last line names the problem, the lines above say where.

**One `=` where two are needed.**

```py
if status_code = 200:
    print("OK")
```

```text
  File "example.py", line 1
    if status_code = 200:
       ^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

**A missing colon.**

```py
if status_code == 200
    print("OK")
```

```text
  File "example.py", line 1
    if status_code == 200
                         ^
SyntaxError: expected ':'
```

**Wrong indentation.**

```py
if status_code == 200:
print("OK")
```

```text
  File "example.py", line 2
    print("OK")
    ^^^^^
IndentationError: expected an indented block after 'if' statement on line 1
```

**Mixing text and numbers.**

```py
status_code = 200
print("Status: " + status_code)
```

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print("Status: " + status_code)
          ~~~~~~~~~~~^~~~~~~~~~~~~
TypeError: can only concatenate str (not "int") to str
```

`+` cannot join text to a number. Use an f-string instead: `print(f"Status: {status_code}")`.

**Text that is not a number.**

```py
int("two hundred")
```

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    int("two hundred")
    ~~~^^^^^^^^^^^^^^^
ValueError: invalid literal for int() with base 10: 'two hundred'
```

**`or` between values instead of between comparisons.**

```py
priority = "urgent"
print(priority == "low" or "medium")
```

```text
medium
```

Python reads this as `(priority == "low") or "medium"`. The first half is `False`, so the answer is the text `"medium"`, which is neither `True` nor `False`. Write a whole comparison on each side: `priority == "low" or priority == "medium"`.

**Printing instead of returning.** The check says `your code returned: None`. Your function printed the answer, or never reached a `return`. A function with no `return` hands back `None`.

**Comparing text with a number.** `"200" == 200` is `False` and raises no error, so the script quietly takes the wrong branch. If an `if` never seems to match, print `type(...)` of the value.

## Checkpoint

Do the four files in `exercises/`, in order. The last one, `ex4_status_codes.py`, is the checkpoint.

Each file ends with a few `print` lines that call your functions. Run the file to try your code:

```bash
uv run python course/part-02-values-and-conditions/exercises/ex4_status_codes.py
```

Run the checks:

```bash
uv run pytest course/part-02-values-and-conditions/checks
```

A failed check shows the call it made, what it expected and what your code returned.

Hand in a branch named `part-02-yourname` and a pull request, as described in the [learner guide](../../docs/learner-guide.md). Words you are unsure of are in the [glossary](../../docs/glossary.md).
