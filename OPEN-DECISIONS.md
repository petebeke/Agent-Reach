# Open decisions

One block per 👤 row. Five fields, every one required — a decision brief with a missing field renders as `MISSING` on his page.

None open. `DEC-0012` (the only one filed) was withdrawn 2026-10-02 — its underlying cause (`ruff format --check` failing on 54 files on `main`) was fixed in the same build cycle with `ruff format agent_reach tests`, so no ruling was needed. See `PROJECT-LEDGER.md` (`OI-0012`, `WITHDRAWN`) and `LEDGER-ARCHIVE.md` for evidence.

## DEC-0024 — Will you open https://github.com/petebeke/Agent-Reach/actions and click the one-time 'I understand my workflows, go ahead and…?

<!-- park-key: gh-actions-fork-enable-agent-reach -->
**Row:** OI-0024 (PRJ-002)
**Clock:** not urgent, but it blocks the row above until answered
**What is true right now:** OBSERVED 2026-10-05: pushed 6c1e02f/6d5f425/780d08c/89e0e5a to origin/main (OI-0015 DONE); pushed demo/ci-lint-gate-red-check and opened https://github.com/petebeke/Agent-Reach/pull/1 (OI-0018). gh api repos/petebeke/Agent-Reach/actions/runs -> total_count=0 across all history incl. 2 pushes to main + 2 to the demo branch today; gh run list on the PR's branch -> 'no checks reported'; a fresh nudge commit pushed to rule out propagation delay produced no run after 20s. RE-CONFIRMED 2026-10-10: pushed a second nudge commit (`5b7cf46`), waited 25s, still total_count=0; `actions/workflows` shows the `ci` workflow `state: "active"` and `actions/permissions` shows `enabled: true` — rules out a disabled workflow, leaves only the fork first-run consent banner.
**Your options:** A) Click the banner at https://github.com/petebeke/Agent-Reach/actions (~1 click, 10s) -> OI-0018/OI-0021 finish inside PR #1 with no further action from you. B) Leave Actions disabled -> PRJ-002's own DoD second clause ('a Checks-tab URL or screenshot ... cannot be simulated locally') goes unmet and the project closes PARTIAL, not DONE.
**The moment you answer:** I open PR #1's Checks tab, confirm the lint job is red, copy its URL, revert agent_reach/_ci_lint_demo.py, push, confirm the same check goes green, close PR #1 with --delete-branch, and mark OI-0018/OI-0021/PRJ-002 DONE with the Checks URL as evidence.
