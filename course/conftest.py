"""Shared helpers for every part's checks.

By default the checks grade the files in `exercises/`. Mentors and CI set
COURSE_TARGET=solutions to grade the reference solutions with the same checks.
"""

import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
import uuid
from pathlib import Path

import pytest

TARGET = os.environ.get("COURSE_TARGET", "exercises")


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """A check that fails with pytrace=False shows its message and nothing else.

    Without this, a check that fails while it is handling the learner's error also prints
    that error under "During handling of the above exception", which buries the message.
    """
    error = call.excinfo.value if call.excinfo else None
    if isinstance(error, pytest.fail.Exception) and not error.pytrace:
        error.__suppress_context__ = True
    return (yield)


@pytest.fixture
def target_dir(request) -> Path:
    """The folder being graded: this part's exercises/ or solutions/."""
    return Path(request.path).parent.parent / TARGET


@pytest.fixture
def load(target_dir, monkeypatch):
    """Import a learner file by name, for example `load("status_codes")`."""
    monkeypatch.syspath_prepend(str(target_dir))

    def _load(name: str):
        path = target_dir / f"{name}.py"
        if not path.exists():
            pytest.fail(f"Expected to find {path}", pytrace=False)
        unique = f"{target_dir.parent.name}_{TARGET}_{name}".replace("-", "_")
        spec = importlib.util.spec_from_file_location(unique, path)
        module = importlib.util.module_from_spec(spec)
        problem = None
        try:
            spec.loader.exec_module(module)
        except Exception as error:
            problem = f"{type(error).__name__}: {error}"
        if problem:  # outside the except block, so only the learner's own error is shown
            pytest.fail(f"{path.name} could not be run: {problem}", pytrace=False)
        return module

    return _load


@pytest.fixture
def run_script(target_dir):
    """Run a learner script the way they would in the terminal; return what it printed."""

    def _run(name: str, *args: str, stdin: str = "") -> str:
        path = target_dir / f"{name}.py"
        if not path.exists():
            pytest.fail(f"Expected to find {path}", pytrace=False)
        result = subprocess.run(
            [sys.executable, str(path), *args],
            input=stdin,
            capture_output=True,
            text=True,
            cwd=target_dir,
            timeout=30,
        )
        if result.returncode != 0:
            last_line = (
                result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "no error text"
            )
            pytest.fail(f"{path.name} stopped with an error: {last_line}", pytrace=False)
        return result.stdout

    return _run


# ---------------------------------------------------------------- parts 8-12: grading test suites

ROOT = Path(__file__).parent.parent


class Outcome:
    """What happened when a learner's tests were run."""

    def __init__(self, output: str, inspection=None):
        self.output = output
        self.inspection = inspection  # whatever the `inspect` callback returned
        summary = self._summary_line(output)
        self.passed = self._count(summary, "passed")
        self.failed = self._count(summary, "failed")
        self.errors = self._count(summary, "error")
        self.skipped = self._count(summary, "skipped")

    @staticmethod
    def _summary_line(output: str) -> str:
        """pytest's last line, "3 passed, 1 failed in 2.01s", even if stderr follows it."""
        lines = output.strip().splitlines()
        for line in reversed(lines):
            if re.search(r"\b(passed|failed|errors?|skipped|no tests ran)\b.* in [\d.]+s\b", line):
                return line
        return lines[-1] if lines else ""

    @staticmethod
    def _count(summary: str, word: str) -> int:
        match = re.search(rf"(\d+) {word}", summary)
        return int(match.group(1)) if match else 0

    @property
    def green(self) -> bool:
        return self.passed > 0 and self.failed == 0 and self.errors == 0

    def tail(self, lines: int = 25) -> str:
        return "\n".join(self.output.strip().splitlines()[-lines:])


@pytest.fixture
def run_learner_tests(target_dir):
    """Run test files from the graded folder against a private copy of Tracklet.

    `bugs` is False for a healthy app, True for every seeded bug, or one bug's name.
    `extra_tickets` gives the app more than the 12 starting tickets, even after a reset.
    Paths are relative to the graded folder unless they are absolute.
    `inspect`, if given, is called with the app address after the tests have run.
    """
    from practice_app.server import running_app

    def _run(
        *paths: str,
        bugs: bool | str = False,
        args: tuple[str, ...] = (),
        inspect=None,
        extra_tickets: int = 0,
    ) -> Outcome:
        targets = [str(path if Path(path).is_absolute() else target_dir / path) for path in paths]
        missing = [target for target in targets if not Path(target.split("::")[0]).exists()]
        if missing:
            pytest.fail(f"Expected to find {missing[0]}", pytrace=False)
        with running_app(bugs=bugs, extra_tickets=extra_tickets) as url:
            env = {**os.environ, "TRACKLET_URL": url}
            env.pop("BUGS", None)
            env.pop("TRACKLET_EXTRA_TICKETS", None)
            result = subprocess.run(
                [sys.executable, "-m", "pytest", *targets, "-q", "-p", "no:cacheprovider", *args],
                capture_output=True,
                text=True,
                cwd=ROOT,
                env=env,
                timeout=300,
            )
            # look at the app after the run, before it is shut down
            inspection = inspect(url) if inspect else None
        return Outcome(result.stdout + result.stderr, inspection)

    return _run


def _code_only(source: str) -> str:
    """The source with comments and docstrings blanked out, so instructions are not graded."""
    lines = source.splitlines(keepends=True)
    previous = tokenize.INDENT
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        is_docstring = token.type == tokenize.STRING and previous in (
            tokenize.INDENT,
            tokenize.NEWLINE,
            tokenize.DEDENT,
        )
        if token.type == tokenize.COMMENT or is_docstring:
            (first_row, first_col), (last_row, last_col) = token.start, token.end
            for row in range(first_row, last_row + 1):
                line = lines[row - 1]
                begin = first_col if row == first_row else 0
                finish = last_col if row == last_row else len(line.rstrip("\n"))
                lines[row - 1] = line[:begin] + " " * (finish - begin) + line[finish:]
        if token.type not in (tokenize.NL, tokenize.COMMENT):
            previous = token.type
    return "".join(lines)


@pytest.fixture
def source_of(target_dir):
    """The code of a file in the graded folder, for checks about how something was written.

    Comments and docstrings are blanked out; everything else is unchanged.
    """

    def _read(name: str) -> str:
        path = target_dir / name
        if not path.exists():
            pytest.fail(f"Expected to find {path}", pytrace=False)
        try:
            return _code_only(path.read_text())
        except (tokenize.TokenError, IndentationError) as error:
            pytest.fail(f"{path.name} is not valid Python: {error}", pytrace=False)

    return _read


# ---------------------------------------------------------------- parts 13-16: JavaScript

JEST = ROOT / "node_modules" / ".bin" / "jest"
GRADING = ROOT / ".grading"  # scratch space inside the project, so Jest finds its configuration

# A JavaScript mutant is one planted bug: in `file`, replace `old` with `new`.
# `hint` tells the learner what their tests missed.
JsMutant = tuple[str, str, str, str]  # (file, old, new, hint)


def _require_node() -> str:
    node = shutil.which("node")
    if node is None:
        pytest.fail(
            "Node.js is not installed. Part 13's lesson shows how to install it.", pytrace=False
        )
    return node


class JestOutcome:
    """What happened when Jest ran a learner's test files."""

    def __init__(self, output: str, report: dict | None):
        self.output = re.sub(r"\x1b\[[0-9;]*m", "", output)  # Jest colours its code frames
        self.passed: list[str] = []
        self.failed: list[str] = []
        self.skipped: list[str] = []
        self.broken_files: list[str] = []  # test files Jest could not run at all
        for suite in (report or {}).get("testResults", []):
            if suite.get("status") == "failed" and not suite.get("assertionResults"):
                self.broken_files.append(Path(suite.get("name", "?")).name)
            for case in suite.get("assertionResults", []):
                bucket = {"passed": self.passed, "failed": self.failed}.get(
                    case.get("status"), self.skipped
                )
                bucket.append(case.get("fullName", "?"))
        self.ran = report is not None

    @property
    def total(self) -> int:
        return len(self.passed) + len(self.failed) + len(self.skipped)

    @property
    def green(self) -> bool:
        return self.ran and bool(self.passed) and not self.failed and not self.broken_files

    def tail(self, lines: int = 30) -> str:
        return "\n".join(self.output.strip().splitlines()[-lines:])


@pytest.fixture
def run_node(target_dir):
    """Run a learner's JavaScript file with Node; return what it printed."""

    def _run(name: str, *args: str, stdin: str = "") -> str:
        node = _require_node()
        path = target_dir / name
        if not path.exists():
            pytest.fail(f"Expected to find {path}", pytrace=False)
        result = subprocess.run(
            [node, str(path), *args],
            input=stdin,
            capture_output=True,
            text=True,
            cwd=target_dir,
            timeout=30,
        )
        if result.returncode != 0:
            lines = [line for line in result.stderr.strip().splitlines() if line.strip()]
            errors = [line for line in lines if re.match(r"^\w*Error\b", line)]
            reason = errors[0] if errors else (lines[-1] if lines else "no error text")
            pytest.fail(f"{path.name} stopped with an error: {reason}", pytrace=False)
        return result.stdout

    return _run


@pytest.fixture
def run_jest(target_dir):
    """Run Jest test files from the graded folder; return a JestOutcome.

    Paths are relative to the graded folder. With no paths, every test file in it runs.
    `env` adds environment variables, for example {"BUGS": "on"} for the widgets in frontend/.
    `mutant` and `extra_files` make Jest run in a temporary copy of the graded folder:
    the mutant plants one bug in one file, and extra_files (name -> content) are added to it.
    The graded folder itself is never changed.
    """
    copies: list[Path] = []

    def _run(
        *paths: str,
        env: dict[str, str] | None = None,
        mutant: JsMutant | None = None,
        extra_files: dict[str, str] | None = None,
    ) -> JestOutcome:
        _require_node()
        if not JEST.exists():
            pytest.fail(
                "Jest is not installed. Run `npm install` in the project folder.", pytrace=False
            )
        folder = target_dir
        missing = [
            path
            for path in paths
            if not (folder / path).exists() and path not in (extra_files or {})
        ]
        if missing:
            pytest.fail(f"Expected to find {folder / missing[0]}", pytrace=False)

        if mutant is not None or extra_files:
            folder = GRADING / uuid.uuid4().hex[:12]
            copies.append(folder)
            shutil.copytree(target_dir, folder, ignore=shutil.ignore_patterns("node_modules"))
            if mutant is not None:
                file, old, new, _hint = mutant
                code = (folder / file).read_text()
                if code.count(old) != 1:
                    pytest.fail(
                        f"{file} is not the file the course shipped, so it cannot be checked. "
                        "Restore it with: git checkout main -- "
                        f"{(target_dir / file).relative_to(ROOT).as_posix()}",
                        pytrace=False,
                    )
                (folder / file).write_text(code.replace(old, new))
            for name, content in (extra_files or {}).items():
                (folder / name).parent.mkdir(parents=True, exist_ok=True)
                (folder / name).write_text(content)

        # The report goes outside the project, so no other run can remove its folder.
        report_dir = Path(tempfile.mkdtemp(prefix="jest-report-"))
        report_path = report_dir / "report.json"
        targets = [str(folder / path) for path in paths] or [str(folder) + os.sep]
        run_env = {**os.environ, "CI": "true", **(env or {})}
        if "BUGS" not in (env or {}):
            run_env.pop("BUGS", None)
        try:
            result = subprocess.run(
                [
                    str(JEST),
                    *(
                        ["--runTestsByPath", *targets]
                        if paths
                        else ["--testPathPatterns", re.escape(targets[0])]
                    ),
                    "--json",
                    f"--outputFile={report_path}",
                    "--colors=false",
                    "--passWithNoTests",
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
                env=run_env,
                timeout=300,
            )
            report = json.loads(report_path.read_text()) if report_path.exists() else None
        finally:
            shutil.rmtree(report_dir, ignore_errors=True)
        return JestOutcome(result.stderr + result.stdout, report)

    yield _run

    for folder in copies:
        shutil.rmtree(folder, ignore_errors=True)
    try:
        GRADING.rmdir()  # only succeeds when empty; another run may still be using it
    except OSError:
        pass
