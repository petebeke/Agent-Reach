# HANDOFF — ci-lint-gate-push-and-throwaway-pr

**Date:** 2026-10-05

**What happened:** built, tested, and committed locally. Pushing is blocked:
the intake policy sets push=no for this class (owned-default, DEC-0202/DEC-0242); push-policy-guard.py refused 'git push origin main' live this session with no override token

**What's committed, locally, not yet pushed:**
- `6c1e02f`
- `6d5f425`
- `780d08c`

**Already verified (do not re-derive these):**
- git merge-base --is-ancestor origin/main HEAD confirms a clean fast-forward, not a merge
- local ruff check / ruff format --check / mypy agent_reach all exit 0 on main as-is
- the demo branch's one commit (f1c60f0) adds agent_reach/_ci_lint_demo.py with a single F401 unused-import violation, confirmed locally: ruff check exits 1, ruff format --check exits 0

**To land it, from your own terminal:**
```
cd '/Users/peterbeke/Developer/VS Code/Agent-Reach'
git push origin main
git push origin demo/ci-lint-gate-red-check
gh pr create --head demo/ci-lint-gate-red-check --base main --title 'demo: throwaway lint violation (do not merge)' --body 'Throwaway PR for OI-0018 — observe red lint check, then revert agent_reach/_ci_lint_demo.py and push again to observe green, then close and delete this branch.'
```

**Verify after landing:**
```
git show origin/main:.github/workflows/pytest.yml | grep -n "ruff check\|ruff format --check\|mypy agent_reach"
open the PR's Checks tab, confirm lint is red, screenshot/copy the URL
git rm agent_reach/_ci_lint_demo.py && git commit -m 'revert: remove throwaway lint violation' && git push origin demo/ci-lint-gate-red-check
confirm the same PR's lint check goes green, then: gh pr close <PR#> --delete-branch
```
