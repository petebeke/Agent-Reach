# Open decisions

One block per 👤 row. Five fields, every one required — a decision brief with a missing field renders as `MISSING` on his page.

None open. `DEC-0012` (the only one filed) was withdrawn 2026-10-02 — its underlying cause (`ruff format --check` failing on 54 files on `main`) was fixed in the same build cycle with `ruff format agent_reach tests`, so no ruling was needed. See `PROJECT-LEDGER.md` (`OI-0012`, `WITHDRAWN`) and `LEDGER-ARCHIVE.md` for evidence.
## DEC-0024 — Will you open https://github.com/petebeke/Agent-Reach/actions and click the one-time 'I understand my workflows, go ahead and…?

<!-- park-key: gh-actions-fork-enable-agent-reach -->
**Row:** OI-0024 (PRJ-002)
**Clock:** not urgent, but it blocks the row above until answered
**What is true right now:** OBSERVED 2026-10-05: pushed 6c1e02f/6d5f425/780d08c/89e0e5a to origin/main (OI-0015 DONE); pushed demo/ci-lint-gate-red-check and opened https://github.com/petebeke/Agent-Reach/pull/1 (OI-0018). gh api repos/petebeke/Agent-Reach/actions/runs -> total_count=0 across all history incl. 2 pushes to main + 2 to the demo branch today; gh run list on the PR's branch -> 'no checks reported'; a fresh nudge commit pushed to rule out propagation delay produced no run after 20s. RE-CONFIRMED 2026-10-10: pushed a second nudge commit (`5b7cf46`), waited 25s, still total_count=0; `actions/workflows` shows the `ci` workflow `state: "active"` and `actions/permissions` shows `enabled: true` — rules out a disabled workflow, leaves only the fork first-run consent banner. RE-CONFIRMED 2026-10-17: `repos/petebeke/Agent-Reach` confirmed `fork: true`, `parent: Panniantong/Agent-Reach`; `actions/runs` (unfiltered and `?branch=demo/ci-lint-gate-red-check`) both still `total_count: 0`; `gh pr checks 1` -> "no checks reported"; `actions/permissions` still `enabled: true`. Separately, the CI workflow itself (`origin/main:.github/workflows/pytest.yml`) now DOES contain the ruff/mypy steps (`git show` + grep exits 0) — PRJ-002's DoD first clause passes; only the second clause (a live Checks-tab URL) remains blocked on this banner. Unchanged otherwise; not re-asking. ⚠️ CORRECTION, re-probed live 2026-10-17 (later this cycle): the push-access side of this row's history ("push=yes per DEC-0242") no longer holds — a live `git push origin main` was refused this cycle by the pre-bash guard (`class: owned-default`, push=no, DEC-0202), confirmed by reading `~/.claude/state/repo-intake-policy.tsv` directly (row 177: `owned-default\tyes\tno\tno\t*`). The banner is still the only thing blocking this decision; this just means the eventual revert/push/confirm-green step may need one more click (`attended-push-grant.py`) or will queue — not a new ask.
**Your options:** A) Click the banner at https://github.com/petebeke/Agent-Reach/actions (~1 click, 10s) -> OI-0018/OI-0021 finish inside PR #1 with no further action from you. B) Leave Actions disabled -> PRJ-002's own DoD second clause ('a Checks-tab URL or screenshot ... cannot be simulated locally') goes unmet and the project closes PARTIAL, not DONE.
**The moment you answer:** I open PR #1's Checks tab, confirm the lint job is red, copy its URL, revert agent_reach/_ci_lint_demo.py, push, confirm the same check goes green, close PR #1 with --delete-branch, and mark OI-0018/OI-0021/PRJ-002 DONE with the Checks URL as evidence.


## Settled decisions (history)

> Decisions whose work is complete. Kept for the record; nothing here is waiting on you.

## DEC-0027 — Which of them should go into the build order?

<!-- park-key: overnight-run:Agent-Reach:ORDER-EXHAUSTED-WORK-REMAINS -->
**Row:** OI-0027 (PRJ-002)
**Clock:** not urgent, but it blocks the row above until answered
**What is true right now:** The repo is NOT building. Its supervisor stands down immediately with verdict ORDER-EXHAUSTED-WORK-REMAINS, 0 cycles.
**Your options:** No discrete options — your call in your own words.
**The moment you answer:** The moment any of those rows is in the approved order, the repo builds it on the next tick and this question withdraws itself.

**Withdrawn:** the condition this question was raised about no longer holds, so there is nothing left for you to decide.

**The probe that established that:** probed: the repo has a live item its order can reach, and is building

Withdrawn automatically by the loop that raised it (`park-question.py --withdraw`, key `overnight-run:Agent-Reach:ORDER-EXHAUSTED-WORK-REMAINS`). Row(s) restamped `WITHDRAWN`: `OI-0027`. The question and its five fields are kept above, unchanged, as the record.

## DEC-0030 — Which of them should go into the build order?

<!-- park-key: overnight-run:Agent-Reach:ORDER-EXHAUSTED-WORK-REMAINS -->
**Row:** OI-0030 (PRJ-002)
**Clock:** not urgent, but it blocks the row above until answered
**What is true right now:** The repo is NOT building. Its supervisor stands down immediately with verdict ORDER-EXHAUSTED-WORK-REMAINS, 0 cycles.
**Your options:** No discrete options — your call in your own words.
**The moment you answer:** The moment any of those rows is in the approved order, the repo builds it on the next tick and this question withdraws itself.

**Withdrawn:** the condition this question was raised about no longer holds, so there is nothing left for you to decide.

**The probe that established that:** probed: the repo has a live item its order can reach, and is building

Withdrawn automatically by the loop that raised it (`park-question.py --withdraw`, key `overnight-run:Agent-Reach:ORDER-EXHAUSTED-WORK-REMAINS`). Row(s) restamped `WITHDRAWN`: `OI-0030`. The question and its five fields are kept above, unchanged, as the record.

## DEC-0033 — Which of them should go into the build order?

<!-- park-key: overnight-run:Agent-Reach:ORDER-EXHAUSTED-WORK-REMAINS -->
**Row:** OI-0033 (PRJ-002)
**Clock:** not urgent, but it blocks the row above until answered
**What is true right now:** The repo is NOT building. Its supervisor stands down immediately with verdict ORDER-EXHAUSTED-WORK-REMAINS, 0 cycles.
**Your options:** No discrete options — your call in your own words.
**The moment you answer:** The moment any of those rows is in the approved order, the repo builds it on the next tick and this question withdraws itself.

**Withdrawn:** the condition this question was raised about no longer holds, so there is nothing left for you to decide.

**The probe that established that:** probed: the repo has a live item its order can reach, and is building

Withdrawn automatically by the loop that raised it (`park-question.py --withdraw`, key `overnight-run:Agent-Reach:ORDER-EXHAUSTED-WORK-REMAINS`). Row(s) restamped `WITHDRAWN`: `OI-0033`. The question and its five fields are kept above, unchanged, as the record.

