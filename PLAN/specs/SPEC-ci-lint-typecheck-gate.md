# SPEC-ci-lint-typecheck-gate — Make CI actually run the checks CONTRIBUTING.md promises

**Source:** PLAN/dumps/202610011705-estate-intake-onboarding.md
**Status:** ADOPTED — became PRJ-001 on 2026-10-02

## Goal
A PR that fails `ruff check`, `ruff format --check`, or `mypy agent_reach` shows a red CI check, the same
way a PR that fails `pytest` already does — so lint/type drift is caught by CI instead of relying on every
contributor having manually run the three commands `CONTRIBUTING.md` tells them to run.

## Done when
`.github/workflows/pytest.yml` runs `ruff check`, `ruff format --check`, and `mypy agent_reach` as CI job
step(s) on every push/PR, using the pinned versions already in `constraints.txt`, and a PR that introduces
a lint violation or a type error produces a failing (red) check — not merely visible output.

## DoD check
```
grep -n "ruff check\|ruff format --check\|mypy agent_reach" .github/workflows/pytest.yml
```
exits 0 (all three present), AND a one-off local proof that the commands actually fail on a violation
(since there is no `act`/local-CI runner available in this environment):
```
pip install -c constraints.txt ruff==0.15.1 mypy==1.19.1 types-requests==2.32.4.20260107 \
  types-PyYAML==6.0.12.20260107 -q
ruff check agent_reach tests
ruff format --check agent_reach tests
mypy agent_reach
```
Run this on current `main` BEFORE wiring it into CI — if any of the three already fails on `main` as-is,
that failure must be fixed (or the specific rule intentionally suppressed in `pyproject.toml`) first, or
the new CI job goes red on its very first run with no PR having caused it.

## Fits
- `.github/workflows/pytest.yml:7-30` — the `test:` job. Add lint/type steps either here (after "Install
  package and test deps", before "Run tests") or as a new sibling job `lint:` alongside `test:`,
  `windows-test:` (`:32`), `wheel-gate:` (`:57`). A sibling job is preferred: it runs in parallel with
  `test:` and its failure reads as "lint failed", not "tests failed", in the PR checks list.
- `CONTRIBUTING.md:32-44` — already documents the exact three commands (`ruff check agent_reach tests`,
  `ruff format agent_reach tests`, `mypy agent_reach`) as the required pre-PR check. This spec wires CI to
  enforce what is already written down, not invent a new policy.
- `constraints.txt:13-15` — already pins `ruff==0.15.1`, `mypy==1.19.1`,
  `types-requests==2.32.4.20260107`, `types-PyYAML==6.0.12.20250915`. The new CI step installs from this
  file (`pip install -c constraints.txt .[dev]`, matching what `test:` already does at
  `.github/workflows/pytest.yml:24`), so no new version decision is needed.
- `pyproject.toml:46-59` — `[tool.ruff]` and `[tool.mypy]` sections already configured (`line-length = 100`,
  `select = ["E", "F", "I"]`, `ignore = ["E501"]`; mypy `warn_unused_configs`, `check_untyped_defs`, etc.,
  `exclude = ["^tests/"]`). The new job runs against this existing config unchanged.
- `CONTRIBUTING.md:24-25` — "Install pre-commit hooks (optional but recommended): `pre-commit install`" —
  checked, there is no pre-commit config file anywhere in the repo
  (`find . -iname "*.pre-commit*" -not -path "./.git/*"` → no output, so no file named .pre-commit-config.yaml
  or similar exists). The instruction currently points at a file that does not exist. Folded into this
  spec since it is the same "docs promise a check that doesn't run" defect — fix by either adding a
  minimal pre-commit config that runs the same three commands, or removing the dangling instruction from
  `CONTRIBUTING.md`.

## Wiring
producer: `.github/workflows/pytest.yml` (new `lint:` job, triggered by GitHub Actions on every
`push`/`pull_request` — same `on:` block already at `.github/workflows/pytest.yml:3-5`) → consumer: GitHub's
PR checks UI, which is what contributors and `petebeke` actually look at before merging, enforcing the same
contract already written in prose at `CONTRIBUTING.md:32-44`. No application code reads this; it is
CI-infrastructure, self-contained within the workflow file. Enumerated for other consumers of this workflow
file: `grep -rln "pytest.yml" . --include="*.md" --include="*.py"` → no hits, nothing else references it
by path.

## Conflicts
- rules: `grep -n "ruff\|mypy\|lint" ~/.claude/commands/CLAUDE.md` → no hits; no standing rule mandates or
  forbids a specific CI shape.
- live rows: ledger is empty (PRJ-000 only) — nothing to conflict with.
- decisions: `grep -n "agent.reach\|lint\|ruff\|mypy" ~/.claude/DECISIONS.md` → no hits.
- in-repo: does not conflict with `SPEC-cut-pending-release.md` — that spec only touches version/CHANGELOG
  files and never edits `.github/workflows/pytest.yml`; both specs can build in either order or in parallel.

## Blast radius
Adding a job to a GitHub Actions workflow cannot affect runtime behavior or any existing test; it can only
add a new, independent CI check. The one real risk is the DoD check's own warning: if `ruff`/`mypy` already
fail against current `main`'s source (not just test files, since `mypy` excludes `tests/`), turning this on
makes every PR red starting now, including unrelated ones. That must be checked BEFORE merging the workflow
change (see DoD check's ordering) — not assumed clean. No other file or consumer reads `.github/workflows/`
contents besides GitHub Actions itself (checked above in Wiring).

## Blockers
- **BLOCKER:** the pre-wiring clean-run proof (DoD check's second command block) could not be executed
  during this planning pass — `which ruff mypy` → "ruff not found", "mypy not found" (checked this
  session); control: `which python3` → present, so this sandbox can run Python, it just lacks the two
  pinned tools. **Resolved:** no founder ruling needed — installing `ruff==0.15.1`/`mypy==1.19.1` from
  `constraints.txt` needs only `pip` network access, which the execution session already has (the same
  access `test:` uses at `.github/workflows/pytest.yml:24`); this is Build order step 1, not a block on
  adoption.
- **BLOCKER:** whether current `main` already passes `ruff check`/`ruff format --check`/`mypy agent_reach`
  is unverified — the three commands were never run this session (tool absence above), so "CI would go
  green on day one" is unconfirmed; control: `pytest tests/ -q` was separately attempted this session and
  queued on a local suite-admission limiter rather than completing, so even the unrelated test suite could
  not be used as a proxy signal. **Resolved:** no founder ruling needed — Build order step 1 both answers
  this and fixes it before step 2 ever touches the workflow file, so the spec cannot land in a state where
  CI starts red through nobody's fault.

## Questions
None. `CONTRIBUTING.md` already specifies the exact commands and tool versions; wiring CI to run them is a
mechanical closure of a documented-but-unenforced policy, not a product or scope decision.

## Build order
1. Install pinned `ruff`/`mypy` from `constraints.txt` and run the three commands against current `main` — gate: all three exit 0, or any failure is triaged (fixed or the specific rule explicitly suppressed in `pyproject.toml` with a one-line reason) before step 2
2. Add a `lint:` job to `.github/workflows/pytest.yml` running `ruff check agent_reach tests`, `ruff format --check agent_reach tests`, `mypy agent_reach`, installed via `pip install -c constraints.txt -e .[dev]` — gate: a throwaway branch with one deliberate lint violation pushed to GitHub shows the new check red, then the violation is reverted
3. Resolve the dangling `pre-commit install` instruction in `CONTRIBUTING.md:25` — either add a matching pre-commit config or remove the instruction — gate: `grep -q "pre-commit install" CONTRIBUTING.md && test -f .pre-commit-config.yaml` passes, or neither the file reference nor the instruction exists

## Items
- Confirm `ruff check`, `ruff format --check`, `mypy agent_reach` all pass clean on current `main` (fix or
  explicitly suppress anything that doesn't)
- Add a `lint:` job to `.github/workflows/pytest.yml` running those three commands on every push/PR
- Resolve `CONTRIBUTING.md`'s dangling reference to a non-existent `.pre-commit-config.yaml`
