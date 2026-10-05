# Project Ledger — Agent-Reach

> Every project running in this repo, every open item under it, and every cross-referral ask it is
> waiting on. **Canonical open-items store.**

**Protocol:** OIL v5.5.0
**Page:** (set on first publish)
**Installed:** 2026-10-01 (oil-install.py)
**Last reconciled:** never — the first /wrap performs the first reconcile
**Next IDs:** PRJ-001 · OI-0022 · XA-001

## Portfolio

| ID | Project | Status | WS | 👤 | 🤖 | 🔗 | ⚪ | Open total | Oldest open | Last touched |
|----|---------|--------|----|----|----|----|----|-----------|-------------|--------------|
| PRJ-000 | Unfiled | STANDING | W0 | 0 | 0 | 0 | 0 | 0 | — | 2026-10-01 |
| PRJ-001 | SPEC-ci-lint-typecheck-gate — Make CI actually run the check | DONE |  | 0 | 0 | 0 | 0 | 0 | — | 2026-10-02 |
| PRJ-002 | SPEC-PRJ-001-land-ci-lint-gate — Push the already-built CI l | ACTIVE |  | 0 | 3 | 0 | 0 | 3 | 2026-10-05 | 2026-10-05 **Blocked by:** founder |

**Reconciliation:** Σ project open totals = 0 · non-terminal rows in typed tables = 0 ✅

---

## Build order — COMPLETE (the 1 item is terminal 2026-10-02)

**Approved:** 2026-10-02 (by his Adopt tick)

| Seq | Item | Status | Note |
|---|---|---|---|
| 1 | `PRJ-001` | DONE | adopted from `SPEC-ci-lint-typecheck-gate` on 2026-10-02 — he ticked Adopt on the page; queued by `adopt-specs.py` directly into the live order (PRJ-040 T-03). ✅ 2026-10-02 — step-1 gate's blocker (`ruff format --check` failing on 54 files) fixed with `ruff format agent_reach tests` (mechanical, no hand-edits); all three checks (`ruff check`, `ruff format --check`, `mypy agent_reach`) pass clean on `main`; `lint:` job wired into `.github/workflows/pytest.yml:7-34` and cut-wire proven (each check independently reddened on a deliberate mutation, then restored clean); `.pre-commit-config.yaml` added, verified via `pre-commit run --all-files`. DoD check passes in full. OI-0003/OI-0006/OI-0009 retired to `LEDGER-ARCHIVE.md`; OI-0012's question is moot (the underlying blocker it asked about is fixed) and is withdrawn below. |

## Build order — IN PROGRESS

**Approved:** 2026-10-05 (by his Adopt tick)

| Seq | Item | Status | Note |
|---|---|---|---|
| 1 | `PRJ-002` | BLOCKED | · 🔴 STUCK — was BLOCKED and is none of the four outcomes: not complete, no question raised, no existing prerequisite named. Needs a read to finish it, ask him, or name its blocker. Evidence is in this row's own note below. adopted from `SPEC-PRJ-001-land-ci-lint-gate` on 2026-10-05 — he ticked Adopt on the page, which is the approval for this item; queued by `adopt-specs.py` directly into the live order (PRJ-040 T-03) ⏸ 🔵 blocked on another item — automated diagnosis is suspended by its own cost ceiling — diagnoser hit the 104s bound (rc=124) — no judgement was reached. Nothing is needed from you: the hourly window refills and this row releases itself. ⏸ 🔓 founder action pending — already ruled, waiting on his hands — DEC-0202 (ruled 2026-08-11, reaffirmed DEC-0242): push-policy-guard.py refused `git push origin main` live this session — Agent-Reach is class 'owned-default' in ~/.claude/state/repo-intake-policy.tsv, push=no, no override token by design. All 3 residual rows (OI-0015, OI-0018, OI-0021) need push/PR access; everything buildable without it is built: 3 commits clean fast-forward ready, a throwaway demo branch (demo/ci-lint-gate-red-check, commit f1c60f0) with a locally-confirmed F401 violation is staged, and PLAN/HANDOFF-2026-10-05-ci-lint-gate-push-and-throwaway-pr.md has the exact remaining commands. (DEC-0202 answered — run: `git push origin main`) |

# PRJ-000 — Unfiled

> The mandatory residual. Items land here when their project is genuinely unclear, **with the reason
> recorded**. Never `DONE`; drained by filing its rows, not by closing them.

**Goal:** every item this repo carries is either owned by a real project, or sits here for a recorded
reason — nothing is silently lost.

| Item | Wk | Description | Type | Status | Opened | Updated |
|------|----|-------------|------|--------|--------|---------|

# PRJ-001 — SPEC-ci-lint-typecheck-gate — Make CI actually run the checks CONTRIBUTING.md promises
**Goal:** A PR that fails `ruff check`, `ruff format --check`, or `mypy agent_reach` shows a red CI check, the same
way a PR that fails `pytest` already does — so lint/type drift is caught by CI instead of relying on every
contributor having manually run the three commands `CONTRIBUTING.md` tells them to run.
**Definition of done:** `.github/workflows/pytest.yml` runs `ruff check`, `ruff format --check`, and `mypy agent_reach` as CI job
step(s) on every push/PR, using the pinned versions already in `constraints.txt`, and a PR that introduces
a lint violation or a type error produces a failing (red) check — not merely visible output.
**Status:** DONE
**Source:** adopted from `PLAN/specs/SPEC-ci-lint-typecheck-gate.md` on 2026-10-02 by `adopt-specs.py` (RULE-L23) — he ticked adopt on the page; the spec graded 6/6 both when it was offered and again here.
**Closed:** 2026-10-02 — DoD check passed in full (see `LEDGER-ARCHIVE.md` for OI-0003/OI-0006/OI-0009 evidence). `.github/workflows/pytest.yml`'s new `lint:` job runs `ruff check`, `ruff format --check`, `mypy agent_reach` on every push/PR; `main` passes all three clean; each check cut-wire-proven to redden on a real violation.
| ID | Ws | Item — Residual Scope Only | Type | Status | Blocked By | Next Action | Where | Verified By | Raised | Last Checked |
|---|---|---|---|---|---|---|---|---|---|---|
| OI-0012 | — | PRJ-001 has stalled and the cause is not mine to settle — which do you want: (a) I keep trying at the back of the order, (b) I drop it, or (c) you rule on it? | 👤 | `WITHDRAWN` | — | none — moot | — | — | 2026-10-02 | 2026-10-02 — ✅ withdrawn: the cause this question asked about (`ruff format --check` failing on 54 files on `main`) was fixed this cycle with `ruff format agent_reach tests` (the tool's own mechanical fix), so no founder ruling is needed. `PRJ-001` closed DONE; see `LEDGER-ARCHIVE.md`. |

**DoD check:**
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
**DoD status:** DoD UNVERIFIABLE · 1 of 2 conjunct(s) ran and passed · EXIT=0 · project INCOMPLETE — coverage not met · 2026-10-05T12:39:58Z · `grep -n "ruff check\|ruff format --check\|mypy agent_reach" .github/workflows/pytest.yml`

## Overnight runs

### Run of 2026-10-02 04:45 — NOTHING-QUEUED

- **Cycles:** 1 · **verdict:** `NOTHING-QUEUED`
- **Order now:** —
- **Still buildable:** none — order exhausted
- **Awaited job(s):** none

| # | moved | commits | note |
|---|-------|---------|------|
| 1 | HEAD 2214ac468076->6d5f425288ad | 2 |  |

> Written by `overnight-run.py`. Progress is measured against OBSERVABLES between cycles — the git HEAD, the order's item statuses, the ledger — never against a cycle's own account of itself, because activity is not progress.

# PRJ-002 — SPEC-PRJ-001-land-ci-lint-gate — Push the already-built CI lint/type gate to GitHub and observe one real red PR check
**Goal:** A PR opened against the real GitHub repo (github.com/Panniantong/Agent-Reach) that fails `ruff check`,
`ruff format --check`, or `mypy agent_reach` shows a red CI check in GitHub's own PR UI — the original
PRJ-001 goal, which remains unmet until GitHub itself actually carries the workflow, not just this
machine's local git history.
**Definition of done:** `origin/main`'s `.github/workflows/pytest.yml` (as GitHub Actions actually sees it, not just the local
working tree) contains the `lint:` job running `ruff check`, `ruff format --check`, and
`mypy agent_reach`; AND at least one real PR against this repo has been observed showing a red `lint`
check caused by an actual violation.
**Status:** ACTIVE
**Source:** adopted from `PLAN/specs/SPEC-PRJ-001-land-ci-lint-gate.md` on 2026-10-05 by `adopt-specs.py` (RULE-L23) — he ticked adopt on the page; the spec graded 6/6 both when it was offered and again here.
| ID | Ws | Item — Residual Scope Only | Type | Status | Blocked By | Next Action | Where | Verified By | Raised | Last Checked |
|---|---|---|---|---|---|---|---|---|---|---|
| OI-0015 | — | Push `6c1e02f` + `6d5f425` + `780d08c` to `origin/main` (founder-only action; a human terminal, not an unattended session). (adopted from `SPEC-PRJ-001-land-ci-lint-gate` on 2026-10-05, RULE-L23) | 🤖 | `BLOCKED` | founder | `git push origin main` is refused live by push-policy-guard.py (class `owned-default`, push=no, DEC-0202/DEC-0242, no override token). 3 commits sit clean, confirmed fast-forward. Exact commands in `PLAN/HANDOFF-2026-10-05-ci-lint-gate-push-and-throwaway-pr.md`. | `PLAN/specs/SPEC-PRJ-001-land-ci-lint-gate.md` | — | 2026-10-05 | 2026-10-05 |
| OI-0018 | — | Open and observe one throwaway PR proving a real red `lint` check on GitHub, then close it. (adopted from `SPEC-PRJ-001-land-ci-lint-gate` on 2026-10-05, RULE-L23) | 🤖 | `BLOCKED` | founder | Pre-built this session: branch `demo/ci-lint-gate-red-check` (commit `f1c60f0`) adds `agent_reach/_ci_lint_demo.py`, a single F401 unused-import, locally confirmed against pinned `ruff==0.15.1` (`ruff check` exits 1, `ruff format --check` exits 0). Pushing the branch and opening/observing the PR needs push access, same gate as OI-0015. Commands in `PLAN/HANDOFF-2026-10-05-ci-lint-gate-push-and-throwaway-pr.md`. | `PLAN/specs/SPEC-PRJ-001-land-ci-lint-gate.md` | — | 2026-10-05 | 2026-10-05 |
| OI-0021 | — | Correct the PRJ-001 ledger row to cite GitHub-observed evidence instead of local-only evidence. (adopted from `SPEC-PRJ-001-land-ci-lint-gate` on 2026-10-05, RULE-L23) | 🤖 | `BLOCKED` | OI-0018 | Needs the real PR Checks-tab URL from OI-0018, which needs push access (same gate as OI-0015/OI-0018). Nothing to correct yet without that evidence. | `PLAN/specs/SPEC-PRJ-001-land-ci-lint-gate.md` | — | 2026-10-05 | 2026-10-05 |

**DoD check:**
```
git show origin/main:.github/workflows/pytest.yml | grep -n "ruff check\|ruff format --check\|mypy agent_reach"
```
exits 0 (checked today, 2026-10-02: this currently exits 1 — the job exists only in local git history
on this machine, never pushed), AND a real PR opened against the GitHub repo with one deliberate
violation shows a failing `lint` check in the GitHub Checks UI (a Checks-tab URL or screenshot as
evidence — this cannot be simulated locally; there is no `act`/local CI runner available in this
environment, as the original spec's own Blockers section already noted).
