# SPEC-PRJ-001-land-ci-lint-gate — Get the founder to click GitHub's one-time Actions-consent banner so the already-live lint gate can actually run on a PR

**Source:** PROJECT-LEDGER.md rows OI-0015 (DONE), OI-0018 (BLOCKED), OI-0021 (BLOCKED), OI-0024 (OPEN, founder decision) under PRJ-002 (the adopted successor to PRJ-001, adopted 2026-10-05) + live re-verification on 2026-10-16
**Status:** DRAFT — NOT YET REVIEWED BY FOUNDER

## Goal
A PR opened against `origin/main` (github.com/petebeke/Agent-Reach, the repo this spec's own adopted
DoD scopes to) that fails `ruff check`, `ruff format --check`, or `mypy agent_reach` shows a red CI
check in GitHub's own PR UI — the original PRJ-001 goal. The workflow file has carried this job on
`origin/main` since 2026-10-05 (OI-0015, DONE); what remains unmet, re-confirmed live today
(2026-10-16), is that GitHub Actions has never once executed on this fork, so nobody has actually
seen the check fire, red or green.

## Done when
`origin/main`'s `.github/workflows/pytest.yml` (as GitHub Actions actually sees it) contains the
`lint:` job running all three checks — already true, re-verified today — AND at least one real GitHub
Actions run has actually executed against a PR on this repo and shown a red `lint` check caused by a
real violation, then green after it's fixed.

## DoD check
```
git show origin/main:.github/workflows/pytest.yml | grep -n "ruff check\|ruff format --check\|mypy agent_reach"
```
Re-ran live today (2026-10-16): exits 0, 5 matches (lines 24, 26, 28, 30, 34) — confirmed two ways:
`git fetch origin main` shows local `main` and `origin/main` at the identical SHA `b1ed54f`, and
GitHub's own Contents API for `petebeke/Agent-Reach` (not just this local clone) returns the same
file with sha `e7fdd95c...` containing the job. Conjunct 1 is MET.

Conjunct 2 (a real PR observed showing red, caused by Actions actually running) is NOT met:
`gh api repos/petebeke/Agent-Reach/actions/runs --jq '.total_count'` returns `0` — re-run live today,
unchanged from the `0` recorded on 2026-10-05 and 2026-10-10. Zero Actions runs have ever fired on
this fork, for any push or PR, ever — not a transient gap.

## Fits
- `.github/workflows/pytest.yml:8` (confirmed on `origin/main`, not just the local working tree) —
  the `lint:` job starts here, and is complete: `ruff check agent_reach tests` runs at
  `.github/workflows/pytest.yml:26`, `ruff format --check agent_reach tests` at
  `.github/workflows/pytest.yml:30`, `mypy agent_reach` at `.github/workflows/pytest.yml:34`.
- Re-ran all three locally today against the pinned versions in `constraints.txt:15`
  (`ruff==0.15.1`, `mypy==1.19.1`, plus `types-requests==2.32.4.20260107` and
  `types-PyYAML==6.0.12.20250915`): `ruff check` → "All checks passed!", `ruff format --check` → "71
  files already formatted", `mypy agent_reach` → "Success: no issues found in 36 source files". All
  exit 0. The code side of this project has been correct since 2026-10-02 and still is.
- A throwaway PR already exists and is still open, unmodified, exactly as a prior pass left it:
  `https://github.com/petebeke/Agent-Reach/pull/1` ("demo: throwaway lint violation (do not merge)",
  branch `demo/ci-lint-gate-red-check`, head commit adds a new demo-only source file (exists only on
  that remote branch, not in this local checkout) containing one deliberate unused import.
  `gh pr view 1 -R petebeke/Agent-Reach` shows `statusCheckRollup: []` — no check has ever attached
  to it, confirming Actions never ran even on this specific PR.

## Wiring
producer: the `lint:` job declared in `.github/workflows/pytest.yml` (same file and mechanism as the
already-working `test:` job documented in `PROJECT-LEDGER.md`), live on `origin/main` since
2026-10-05 -> consumer: GitHub Actions, which would render it as a PR check in the Checks UI. This
link is wired
and present on GitHub's side (confirmed via the Contents API against the real remote, not the local
clone) but has never fired: `gh api repos/petebeke/Agent-Reach/actions/workflows` shows the `ci`
workflow's own `state: "active"` (GitHub does not report it disabled), and
`repos/petebeke/Agent-Reach/actions/permissions` reports `enabled: true, allowed_actions: "all"` —
ruling out an org-level block or a disabled workflow. The one thing neither the REST API nor the `gh`
CLI exposes a way to click is GitHub's one-time "I understand my workflows, go ahead and enable them"
consent banner that appears on every freshly-forked repo's Actions tab. That banner, not a policy or
a code gap, is the entire remaining link in this chain.

## Conflicts
- The note this grounding pass was originally handed claimed push access is what's blocking this
  project ("BLOCKED ON YOU: only you... can send the already-built fix to GitHub"). That claim is
  stale and wrong: `PROJECT-LEDGER.md` row OI-0015 recorded on 2026-10-05 that the repo's own push
  policy guard returns `BLOCKED=False` for this repo, and `git push origin main` already ran and
  succeeded that day (`2214ac4..89e0e5a`). Re-confirmed live today: local `main` and `origin/main`
  are at the same SHA, with no divergence. The push is not, and has not been for 11 days, the open
  item.
- `PROJECT-LEDGER.md` tracks this work under `PRJ-002` (adopted 2026-10-05 from this same spec slug),
  not `PRJ-001` — `PRJ-001` itself still reads `DONE`, closed 2026-10-02, which is also stale (closed
  before the push, let alone the Actions-run step, had happened). Whoever reviews this should treat
  `PRJ-002` as the live row and `PRJ-001` as a closed duplicate that was never reopened.
- rules: no repo-specific push or Actions policy found in `~/.claude/commands/CLAUDE.md` beyond the
  general git-mutation restriction already governing this grounding run itself.

## Blast radius
Nothing further needs to be built or pushed — zero new code changes. The only action is a UI click
on GitHub (not a git operation, not reachable via `gh` or the REST API) plus, afterward, reverting
the demo PR's one deliberate violation and closing it. Once Actions can run, every future PR against
this fork gets a real `lint` check in its Checks list — this is the intended behavior, not a new risk.
There is no blast radius on the canonical upstream project (`Panniantong/Agent-Reach`): this fork's
CI config has no effect there, and the adopted spec's own DoD was already scoped to `origin/main`
(the fork), not upstream, so that boundary is a decided fact, not an open question this draft reopens.

## Blockers
- **BLOCKER — founder-only, not executable by any unattended or CLI-driven session:** GitHub disables
  Actions on every newly-forked repo until the owning account visits the Actions tab and clicks the
  one-time "I understand my workflows, go ahead and enable them" banner. There is no REST or `gh` CLI
  endpoint for this consent — confirmed again today the same way prior passes confirmed it on
  2026-10-05 and 2026-10-10: the workflow's own `state` is `"active"`, account-level Actions
  permissions report `enabled: true`, and `gh api repos/petebeke/Agent-Reach/actions/runs` still
  returns `total_count: 0` after 11 days and multiple pushes, including dedicated "nudge" commits
  pushed specifically to rule out propagation delay. Nothing short of that one click moves this.
- No other blocker exists. The code is correct, the file is on GitHub, the demo PR is already open
  and waiting — this is a single, already-isolated, already-explained founder action.

## Questions
None. This is not an ambiguity for the founder to resolve — it's a specific, already-identified action
only the founder's GitHub account can take (a one-time consent click), with no decision content beyond
"yes, enable Actions on this fork."

## Build order
1. Founder clicks the one-time Actions-consent banner at `https://github.com/petebeke/Agent-Reach/actions`. — gate: `gh api repos/petebeke/Agent-Reach/actions/runs --jq '.total_count'` returns > 0.
2. Open PR #1's Checks tab (`https://github.com/petebeke/Agent-Reach/pull/1`) and confirm the `lint` job is red. — gate: `gh pr checks 1 -R petebeke/Agent-Reach` lists a failing `lint` check.
3. Revert `agent_reach/_ci_lint_demo.py`, push the same branch, confirm the same check goes green. — gate: `gh pr checks 1 -R petebeke/Agent-Reach` lists a passing `lint` check.
4. Close PR #1 with `--delete-branch` and correct the `PRJ-002`/`PRJ-001` ledger rows with the real Checks URLs from steps 2-3. — gate: the ledger row cites a real GitHub Checks observation, not a local exit code.

## Deploy target
N/A — this is a CI/repo-hygiene change to GitHub's own check pipeline, not an application with a
live deploy. `origin/main` on `petebeke/Agent-Reach` is the only "live" surface, and it is already
confirmed current (see DoD check above).

## Items
- Get the founder's one-time click on the GitHub Actions fork-consent banner (the only action left
  that nothing else can substitute for).
- Observe and record the real red-then-green `lint` check on the already-open demo PR #1.
- Close PR #1 and correct both the `PRJ-001` and `PRJ-002` ledger rows to cite that real observation.
