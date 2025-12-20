  # ScORCH — Copilot / AI Agent Instructions (repo-specific)
  This file augments the generic agent rules above with concise, actionable guidance to work productively in this repository.
  - Purpose: automate small edits, add/modify shell `functions/` scripts, update `plugins/`, and implement light Python helpers in `python/`.

  What to run first
  - `bash -n scorch` - syntax-check core entrypoint
  - `pytest -q` - run lightweight smoke tests (`tests/test_smoke.py`)
  - `./scorch -v` - quick smoke run that prints version
  - `echo CANCEL | scorch -new` -- dry-run new job submission (loads plugins, creates no jobs, tests job creation path)

  Quick checks and developer commands
  - **Install / run:** follow [README.md](../README.md) — the installer is `./install` (see README example).
  - **Sanity checks:** run `bash -n` on shell entrypoints (tests use this). Example test command: `pytest -q` (see `tests/test_smoke.py`).
  - **Smoke run:** `./scorch -v` should exit 0 and print version (tested by `tests/test_smoke.py`).

  Project layout & important files
  - **Core scripts:** repository root contains the main shell entrypoints (`scorch`, `obrar`) — treat these as thin orchestrators.
  - **Shell library:** [functions/](../functions/) contains reusable `fn_` functions sourced by scripts. Example: [functions/Scorch_Dispatcher](../functions/Scorch_Dispatcher) (dispatcher loop, job lifecycle).
  - **Helpers/CLI:** [bin/](../bin/) holds utility scripts invoked interactively (e.g., `install`, `scorchdb`).
  - **Python utilities:** [python/showJobs.py](../python/showJobs.py) is a reference for job-listing logic and CLI parsing.
  - **Jobs:** [jobs/](../jobs/) contains sub directories representing states (`active`, `pending`, `queued`, `running`, `completed`, `failed`, etc.). Job filenames follow a convention parsed by code (see examples in `jobs/active`).
  - **Plugins:** [plugins/README.md](../plugins/README.md) must exist (tests assert this). Plugins are organized under `plugins/<TYPE>/`.

  Naming, coding and runtime conventions (specific)
  - **Hungarian-style prefixes:** variables and functions commonly use prefixes: `int_`, `str_`, `arr_`, `file_`, `fn_`, `b_` (boolean). Follow this naming in new shell and Python code to match style.
  - **Function names:** shell functions use `fn_` prefix and are often followed by `readonly -f fn_Name`.
  - **Job filename format:** job files are split on `_` — tools expect at least 6 parts; `showJobs.py` extracts JobID, Action, Env, Release from indexes 1,3,4,5. Use existing job examples in `jobs/active` when constructing tests.
  - **Locking & dispatch:** dispatcher uses lock files / symlink locks (see `file_DispatchLock` and job lock patterns in [functions/Scorch_Dispatcher](../functions/Scorch_Dispatcher)). Prefer symlink-based locks when interacting with job lifecycle.
  - **Logs & audit:** logs are stored under `var/log`; auditors write `AUDIT:START:<timestamp>` lines — `showJobs.py` reads these to compute running time.

  Testing & linting
  - **Bash syntax:** use `bash -n <file>` (tests call this for `scorch` and `obrar`).
  - **Python:** run `python3 -m pytest -q` or `pytest -q` from repo root.

  When editing
  - Keep changes minimal and test locally: run `bash -n` on changed shell files and `pytest` for quick checks.
  - Match existing idioms: variable prefixes, `fn_` naming, use `lst_` for lists and use `arr_` for arrays.

  Examples to reference while editing
  - Job parsing and column logic: [python/showJobs.py](../python/showJobs.py)
  - Dispatcher and job state transitions: [functions/Scorch_Dispatcher](../functions/Scorch_Dispatcher)
  - Repo overview / installer: [README.md](../README.md)

  If anything above is unclear or you'd like different emphasis (more Python, tests, or plugin authoring examples), tell me which area to expand.

Confirm