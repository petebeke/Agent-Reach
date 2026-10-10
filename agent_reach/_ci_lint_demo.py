"""THROWAWAY file for OI-0018 (SPEC-PRJ-001-land-ci-lint-gate).

Purpose: a single deliberate `ruff check` violation (unused import) to prove the
`lint` job on `origin/main` renders a real red check in GitHub's PR Checks UI.

Delete this file (and close/delete this branch and its PR) once the red check has
been observed — do not merge it.
"""

import os  # this unused import is the deliberate violation (do not suppress it).
# nudge 1791211155
