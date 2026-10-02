# Project Ledger — Agent-Reach

> Every project running in this repo, every open item under it, and every cross-referral ask it is
> waiting on. **Canonical open-items store.**

**Protocol:** OIL v5.5.0
**Page:** (set on first publish)
**Installed:** 2026-10-01 (oil-install.py)
**Last reconciled:** never — the first /wrap performs the first reconcile
**Next IDs:** PRJ-001 · OI-0013 · XA-001

## Portfolio

| ID | Project | Status | WS | 👤 | 🤖 | 🔗 | ⚪ | Open total | Oldest open | Last touched |
|----|---------|--------|----|----|----|----|----|-----------|-------------|--------------|
| PRJ-000 | Unfiled | STANDING | W0 | 0 | 0 | 0 | 0 | 0 | — | 2026-10-01 |
| PRJ-001 | SPEC-ci-lint-typecheck-gate — Make CI actually run the check | DONE |  | 0 | 0 | 0 | 0 | 0 | — | 2026-10-02 |

**Reconciliation:** Σ project open totals = 0 · non-terminal rows in typed tables = 0 ✅

---

## Build order — COMPLETE (the 1 item is terminal 2026-10-02)

**Approved:** 2026-10-02 (by his Adopt tick)

| Seq | Item | Status | Note |
|---|---|---|---|
| 1 | `PRJ-001` | DONE | adopted from `SPEC-ci-lint-typecheck-gate` on 2026-10-02 — he ticked Adopt on the page; queued by `adopt-specs.py` directly into the live order (PRJ-040 T-03). ✅ 2026-10-02 — step-1 gate's blocker (`ruff format --check` failing on 54 files) fixed with `ruff format agent_reach tests` (mechanical, no hand-edits); all three checks (`ruff check`, `ruff format --check`, `mypy agent_reach`) pass clean on `main`; `lint:` job wired into `.github/workflows/pytest.yml:7-34` and cut-wire proven (each check independently reddened on a deliberate mutation, then restored clean); `.pre-commit-config.yaml` added, verified via `pre-commit run --all-files`. DoD check passes in full. OI-0003/OI-0006/OI-0009 retired to `LEDGER-ARCHIVE.md`; OI-0012's question is moot (the underlying blocker it asked about is fixed) and is withdrawn below. |

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
