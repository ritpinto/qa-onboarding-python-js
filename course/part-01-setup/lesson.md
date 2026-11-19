# Part 1: Setup and your first script

## What you will be able to do

- Create your own repository on GitHub and give your mentors access to it.
- Open a terminal and move around folders with four commands.
- Install the three tools the course uses: git, uv and VS Code.
- Write a `pyproject.toml` and let uv install Python and packages from it.
- Create an SSH key and use it to clone your repository.
- Run a Python script and read what it prints.
- Save your work with git and open a pull request for review.

Nothing here needs prior knowledge. Type every command and every example yourself. Typing is slower than pasting, and that is the point: your fingers learn the shapes.

New words are explained as they come up. There is also a [glossary](../../docs/glossary.md).

## 1. Your repository on GitHub

A **repository** (repo) is a project folder whose history is tracked by a tool called git. **GitHub** is a website that stores repositories, so that several people can work on the same one. You do the whole course in a repository of your own. Your mentors put each part of the course into it, and you hand your work in there.

This section needs only a browser. If you have no GitHub account, create one at <https://github.com/signup> first.

### Create the repository

1. Sign in to GitHub. Click **+** in the top right corner, then **New repository**.
2. **Repository name:** type `qa-onboarding-python-js`, exactly like that.
3. **Visibility:** choose **Public**.
4. Leave everything else as it is. Do not add a README, a `.gitignore` or a license: the repository must start empty, or your mentors cannot put the course into it.
5. Press **Create repository**.

### Give your mentors access

Anyone can read a public repository, but only people you invite can change it. Your mentors need to change it, to add the course parts.

1. In the repository, open **Settings**, then **Collaborators** in the left bar.
2. Press **Add people** and type the GitHub username of a mentor. Your mentors will tell you their usernames.
3. Press **Add to this repository**. Repeat for each mentor.

### Send the link

Copy the address of the repository from the browser's address bar. It looks like this:

```text
https://github.com/your-username/qa-onboarding-python-js
```

Send it to your mentors. They will put the first part of the course into the repository and tell you when it is there. Carry on with sections 2 to 4 while you wait; you need the course itself only from section 5.

## 2. The terminal

A **terminal** is a window where you type commands instead of clicking. Testers who automate spend a lot of time in one, because that is where tests are run.

- **macOS:** open the app called Terminal (press Cmd+Space, type `Terminal`).
- **Windows:** open PowerShell (press the Windows key, type `PowerShell`).

A **command** is one line you type, followed by Enter. Try these four.

| Command | What it does |
|---|---|
| `pwd` | Prints the folder you are in ("print working directory") |
| `ls` | Lists what is in that folder |
| `cd Documents` | Moves into the folder named `Documents` |
| `cd ..` | Moves up one folder |

Two habits that save time:

- Press Tab while typing a folder or file name and the terminal completes it.
- Press the up arrow to bring back the previous command.

A **path** is the address of a file or folder, such as `course/part-01-setup/lesson.md`. The slashes separate folders. Windows also shows paths with backslashes (`course\part-01-setup`); both work in PowerShell.

## 3. Install git

**git** records the history of a project and lets several people work on it. Every test framework you will meet lives in git.

macOS:

```bash
xcode-select --install
```

Windows:

```powershell
winget install --id Git.Git -e
```

Close the terminal, open it again, then check:

```bash
git --version
```

You should see a line such as `git version 2.47.0`. The exact number does not matter.

Tell git who you are. It writes this on every change you save. Use the email address of your GitHub account, so that GitHub shows your changes under your name.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 4. An SSH key

GitHub has to know that a change sent from your machine comes from you. Typing a password every time would be slow, so you use an **SSH key** instead. A key is a pair of files:

- The **private key** stays on your machine. Never send it to anyone and never paste it anywhere.
- The **public key**, the file ending in `.pub`, is the half you give to GitHub. It is safe to share.

GitHub accepts a connection only from a machine that holds the private key matching a public key in your account.

### Step 1: create the key

The command is the same on macOS and Windows. Use your own email address; it is only a label on the key.

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

It asks three questions. Press Enter for each one:

```text
Enter file in which to save the key (/Users/you/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

The first Enter accepts the suggested file. The other two leave the key without a **passphrase**, a password for the key itself. You may type one if you prefer: the key is then useless to anyone who copies it, and you are asked for the passphrase when you send or fetch changes. Nothing appears on the screen while you type it.

If the first question says the file `already exists`, you made a key before. Answer `n` and use the key you have.

### Step 2: copy the public key

Print it:

```bash
cat ~/.ssh/id_ed25519.pub
```

Output, one long line:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFh3k0pQ...dZ you@example.com
```

Select the whole line, from `ssh-ed25519` to the end of the email address, and copy it. Check the file name ends in `.pub`: `id_ed25519` without it is the private key.

### Step 3: add it to GitHub

1. On GitHub, click your picture in the top right corner, then **Settings**.
2. In the left bar, open **SSH and GPG keys** and press **New SSH key**.
3. **Title:** a name for this machine, such as `Work laptop`.
4. **Key type:** leave it on `Authentication Key`.
5. **Key:** paste the line you copied.
6. Press **Add SSH key**.

### Step 4: test it

```bash
ssh -T git@github.com
```

The first time, your machine does not know GitHub yet and asks:

```text
The authenticity of host 'github.com (140.82.121.4)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type `yes` and press Enter. Then you should see:

```text
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

That message means it works. The second half is normal: this connection is only for git.

## 5. Clone your repository

Copying a repository from GitHub to your machine is called **cloning**. Wait until your mentors say the first part is in your repository; before that there is nothing to copy.

On the repository's page on GitHub, press the green **Code** button, choose the **SSH** tab and copy the address. It starts with `git@github.com:`. Then:

```bash
cd Documents
git clone git@github.com:your-username/qa-onboarding-python-js.git
cd qa-onboarding-python-js
```

Use your own username in the address. git creates a folder named `qa-onboarding-python-js` with the course inside. Every command in the course is run from that folder.

When your mentors add a later part, you fetch it with `git pull`. The [learner guide](../../docs/learner-guide.md) shows when.

## 6. Install uv and VS Code

### uv

**uv** installs Python and the extra code this course uses, and runs your scripts with them. You do not need to install Python separately.

macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:

```powershell
winget install --id astral-sh.uv -e
```

Close and reopen the terminal, then check:

```bash
uv --version
```

### VS Code

**VS Code** is the editor you will write code in. Download it from <https://code.visualstudio.com> and install it. Then open it, click the Extensions icon in the left bar, search for `Python` (published by Microsoft) and install it.

Open the course folder: **File > Open Folder**, then choose `qa-onboarding-python-js`.

VS Code has a terminal built in: menu **Terminal > New Terminal**. It opens in the course folder. From now on you can use that one.

## 7. Set up the Python project

Before uv can install anything, it needs to know which Python the project uses and which packages. It reads both from a file named `pyproject.toml` at the top of the project. Your repository does not have one yet, so you write it.

### Write `pyproject.toml`

In VS Code, right-click the empty space below the file list and choose **New File**. Name it `pyproject.toml`. It must sit at the top of `qa-onboarding-python-js`, next to the `course` folder, not inside it.

Type this into it and save:

```toml
[project]
name = "qa-onboarding-python-js"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
```

The file is written in **TOML**, a format for settings. A name in square brackets starts a section, and each line under it is `name = value`. Text goes in quotes, as in Python.

| Line | What it says |
|---|---|
| `[project]` | The lines below describe the project |
| `name = "qa-onboarding-python-js"` | The project's name, the same as the repository's |
| `version = "0.1.0"` | Its version. uv needs one; it stays `0.1.0` for the whole course |
| `requires-python = ">=3.12"` | The project needs Python 3.12 or newer |
| `dependencies = []` | The packages the project needs. `[]` is an empty list: none yet |

### Install Python

In the course folder, run:

```bash
uv sync
```

uv reads `pyproject.toml` and looks for Python 3.12 or newer on your machine. If there is none, it downloads one. Then it creates a folder named `.venv` and a file named `uv.lock`. The output looks like this:

```text
Downloading cpython-3.14.7-macos-aarch64-none (download) (25.3MiB)
 Downloaded cpython-3.14.7-macos-aarch64-none (download)
Using CPython 3.14.7
Creating virtual environment at: .venv
Resolved 1 package in 1ms
```

Your version number may be different. If your machine already has a recent Python, there are no `Download` lines.

### What `.venv` is

Python projects use **packages**: code written by other people that you install and reuse. Different projects need different packages, in different versions. A **virtual environment** is a private folder holding the packages for one project, so projects do not disturb each other. `.venv` is that folder for this course.

You never edit `.venv` or open it. You only need to know two things:

- `uv sync` creates it or brings it up to date.
- Starting a command with `uv run` makes the command use it.

### Add your first package

The checks at the end of every part are run by **pytest**, a package for testing. Add it to the project:

```bash
uv add pytest
```

```text
Resolved 7 packages in 121ms
Installed 5 packages in 15ms
 + iniconfig==2.3.1
 + packaging==26.3
 + pluggy==1.7.0
 + pygments==2.21.0
 + pytest==9.2.0
```

`uv add` installs the package into `.venv` and writes it into `pyproject.toml`. The other four are packages pytest itself needs. Open `pyproject.toml` again. The `dependencies` line has changed:

```toml
dependencies = [
    "pytest>=9.2.0",
]
```

`>=9.2.0` means "this version or newer". Your number may be higher.

`uv.lock` records the exact version of every package installed, including the four that came with pytest. uv writes it and you never edit it. It goes into git with `pyproject.toml`, so your mentors get the same versions as you.

Later parts add packages the same way. When a part needs one, its lesson tells you which, and you run `uv add`. By the end of the course `pyproject.toml` lists everything your tests use.

## 8. Run Python

Create a file. In VS Code, right-click `course/part-01-setup/exercises` in the file list, choose **New File**, and name it `scratch.py`. A file ending in `.py` is a Python **script**: a list of instructions Python carries out from top to bottom.

Type this into it and save (Cmd+S or Ctrl+S):

```python
print("Tracklet is up")
```

Run it from the terminal:

```bash
uv run python course/part-01-setup/exercises/scratch.py
```

Output:

```text
Tracklet is up
```

`print` shows something on the screen. The text between the quotes is shown exactly as typed.

### More than one line

Python runs the lines in order.

```python
print("Starting smoke test")
print("Login page: OK")
print("Ticket list: OK")
print("Finished")
```

Output:

```text
Starting smoke test
Login page: OK
Ticket list: OK
Finished
```

### Comments

A line that starts with `#` is a **comment**. Python ignores it. Comments are notes for people.

```python
# This script reports one check
print("Health check: OK")  # a comment can also follow code
```

Output:

```text
Health check: OK
```

In the exercises you will see comments that start with `TODO`. They mark the places where you write code.

### Names for values

You can give a value a name and use the name later. The name is called a **variable**. Part 2 covers this properly; here is just enough for this part.

```python
tester = "Maria"
passed = 18
failed = 2
print("Tester:", tester)
print("Passed:", passed)
print("Total:", passed + failed)
```

Output:

```text
Tester: Maria
Passed: 18
Total: 20
```

Text goes in quotes. Numbers do not. `print` accepts several things separated by commas and puts a space between them.

## 9. Save and share your work with git

The cycle below is the same in every part. The [learner guide](../../docs/learner-guide.md) repeats it.

### Step 1: make a branch

A **branch** is your own line of work. Changes on it do not touch the main line, called `main`, until they are reviewed.

```bash
git switch -c part-01-yourname
```

Use your own name. `switch -c` means "create this branch and move onto it".

### Step 2: do the work, then look at what changed

```bash
git status
```

git lists the files you changed in red. Run `git status` whenever you are unsure what state things are in. It never changes anything.

### Step 3: commit

A **commit** is a saved snapshot with a message. First choose what goes into it, then save it.

```bash
git add course/part-01-setup pyproject.toml uv.lock
git commit -m "Part 1: project file and setup exercises"
```

`pyproject.toml` and `uv.lock` are part of this part's work, so they go in too. `.venv` stays out: uv tells git to ignore it.

### Step 4: push

Your commit exists only on your machine. **Pushing** sends it to the shared repository.

```bash
git push -u origin part-01-yourname
```

### Step 5: open a pull request

A **pull request** (PR) asks for your branch to be merged into `main`, and is where your mentors review it. After the push, git prints a web address. Open it, fill in the description, and press **Create pull request**. Your mentors see it because you added them to the repository in section 1.

## Common mistakes

**`command not found: uv`** (macOS) or **`uv : The term 'uv' is not recognized`** (Windows). The terminal was open while you installed uv. Close it and open a new one.

**``error: No `pyproject.toml` found in current directory or any parent directory``**. uv cannot find the project file. Run `pwd`: you should be in `qa-onboarding-python-js`. If you are, the file is in the wrong place or has the wrong name. It must be called exactly `pyproject.toml` and sit next to the `course` folder. A white dot on its tab means it is not saved yet.

**`TOML parse error`**. A typo in `pyproject.toml`. uv shows the line and puts `^` under the spot:

```text
error: Failed to parse: `pyproject.toml`
  cause: TOML parse error at line 2, column 32
           |
         2 | name = "qa-onboarding-python-js
           |                                ^
         invalid basic string, expected `"`
```

Here the closing quote is missing. Compare the file with section 7, character by character.

**`` error: Failed to spawn: `pytest` ``**. pytest is not in the project yet. Run `uv add pytest` (section 7).

**`can't open file ... [Errno 2] No such file or directory`**. Python cannot find the script. Either the path has a typo or you are in the wrong folder. Run `pwd` to see where you are; you should be in `qa-onboarding-python-js`. Use Tab to complete the path instead of typing all of it.

**A missing quote.**

```py
print("Health check: OK)
```

```text
  File "scratch.py", line 1
    print("Health check: OK)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

Read an error from the bottom. The last line names the problem: a **string** (text in quotes) was opened and never closed. The lines above show where: line 1, with `^` pointing at the spot. A `SyntaxError` means Python could not read the file at all, so nothing ran.

**A misspelled name.**

```py
passed = 18
print(pased)
```

```text
Traceback (most recent call last):
  File "scratch.py", line 2, in <module>
    print(pased)
          ^^^^^
NameError: name 'pased' is not defined. Did you mean: 'passed'?
```

Python does not know the name `pased`. It often suggests the name you meant.

**`fatal: not a git repository`**. You ran a git command outside the course folder. `cd` into `qa-onboarding-python-js`.

**`git@github.com: Permission denied (publickey)`**. GitHub does not know your key. Print the public key again (section 4, step 2) and compare it with the one under **SSH and GPG keys** in your GitHub settings. If they differ, add the one from your machine.

**`ERROR: Repository not found`** when cloning. The address has a typo, usually in the username or the repository name. Copy it again from the green **Code** button.

**`warning: You appear to have cloned an empty repository`**. The course is not in your repository yet. Delete the empty folder, wait for your mentors, and clone again.

**Nothing printed.** The file was not saved. A white dot on the file's tab in VS Code means unsaved changes.

## Checkpoint

Do the three files in `exercises/`, in order. Each one explains its task at the top.

Run the checks:

```bash
uv run pytest course/part-01-setup/checks
```

The last line says how many passed and failed, for example `7 passed`. For a failed check, read the lines marked `E` or the short summary at the bottom: they say what was expected and what your script printed.

Hand in:

1. A branch named `part-01-yourname` with your three finished exercise files, `pyproject.toml` and `uv.lock`. Git ignores `scratch.py`, so it stays out of the branch.
2. A pull request against `main`, with the three questions from the [learner guide](../../docs/learner-guide.md#handing-in) answered.

You are done when all checks pass and your mentor approves the PR.
