# SPEC-PRJ-001-land-ci-lint-gate — Push the already-built CI lint/type gate to GitHub and observe one real red PR check

**Source:** PLAN/HANDOFF-2026-10-02-ci-lint-typecheck-gate.md + PROJECT-LEDGER.md PRJ-001 (originally adopted from PLAN/specs/SPEC-ci-lint-typecheck-gate.md on 2026-10-02)
**Status:** READY -- accepted by founder on the Completion Status page, 2026-10-03

## Goal
A PR opened against the real GitHub repo (github.com/Panniantong/Agent-Reach) that fails `ruff check`,
`ruff format --check`, or `mypy agent_reach` shows a red CI check in GitHub's own PR UI — the original
PRJ-001 goal, which remains unmet until GitHub itself actually carries the workflow, not just this
machine's local git history.

## Done when
`origin/main`'s `.github/workflows/pytest.yml` (as GitHub Actions actually sees it, not just the local
working tree) contains the `lint:` job running `ruff check`, `ruff format --check`, and
`mypy agent_reach`; AND at least one real PR against this repo has been observed showing a red `lint`
check caused by an actual violation.

## DoD check
```
git show origin/main:.github/workflows/pytest.yml | grep -n "ruff check\|ruff format --check\|mypy agent_reach"
```
exits 0 (checked today, 2026-10-02: this currently exits 1 — the job exists only in local git history
on this machine, never pushed), AND a real PR opened against the GitHub repo with one deliberate
violation shows a failing `lint` check in the GitHub Checks UI (a Checks-tab URL or screenshot as
evidence — this cannot be simulated locally; there is no `act`/local CI runner available in this
environment, as the original spec's own Blockers section already noted).

## Fits
- `.github/workflows/pytest.yml:24` (local working tree / local `main` HEAD `6d5f425`) — the `lint:`
  job already exists here (lines 7-34), complete, and already passes clean against the pinned tool
  versions. Nothing needs to be written. The only gap is that this file state has never reached
  `origin/main`.
- `PLAN/HANDOFF-2026-10-02-ci-lint-typecheck-gate.md:5` — states explicitly: "Pushing is blocked: the
  intake policy sets push=no for this class" and hands the one remaining command
  (`git push origin main`) to the founder.
- `PROJECT-LEDGER.md:17` — currently marks PRJ-001 `DONE` (also at `PROJECT-LEDGER.md:49`,
  `Closed: 2026-10-02`). That status was declared from the local commit passing local commands, not
  from what GitHub Actions actually runs. The ledger row needs reopening, not just the push.

## Wiring
producer: `.github/workflows/pytest.yml` (the `lint:` job, on `origin/main` once pushed) -> consumer:
GitHub Actions, which renders the `lint` job as a PR check in GitHub's own UI — the literal mechanism
the goal text names ("shows a red CI check"). This producer->consumer link is currently broken, as
recorded in `PLAN/HANDOFF-2026-10-02-ci-lint-typecheck-gate.md:5`: checked this session,
`git show origin/main:.github/workflows/pytest.yml | grep -n "ruff check\|ruff format --check\|mypy agent_reach"`
exits 1 (no match), while the identical grep against the local working tree's copy of the same file
exits 0 (all three present). Local git history on a developer's machine is not a path GitHub Actions can
read — only `origin/main` (or a pushed branch/PR ref) is.

## Conflicts
- rules: `grep -n "ruff\|mypy\|lint\|push" ~/.claude/commands/CLAUDE.md` → no hits specific to this
  repo's push policy beyond the general git-mutation restriction already governing this grounding run
  itself.
- live rows: `PROJECT-LEDGER.md` currently shows PRJ-001 `DONE` and OI-0012 `WITHDRAWN` on the premise
  that the fix "closed DONE" — both are stale against the real GitHub state checked this session and
  should be reopened alongside this spec, not left as-is.
- decisions: no entry found for push policy in this repo; the policy is only documented in the HANDOFF
  file.
- in-repo: none — pushing an already-committed, already-clean set of commits conflicts with nothing
  else in flight. `git branch -vv` → only `main` exists locally, no other unpushed branch to collide
  with.

## Blast radius
Pushing `6c1e02f` and `6d5f425` is a fast-forward of `origin/main` (checked this session:
`git log origin/main -1` = `2214ac4`, a strict ancestor of local HEAD `6d5f425`; `git status` shows
`ahead 2`, not diverged — so this is a clean fast-forward, not a merge). The two commits touch 61 files,
but inspection of the largest single-file change (`agent_reach/cli.py`, 467 lines) shows the diff is
mechanical `ruff format` reformatting only — line-wrapping and blank-line insertion, no logic changes —
consistent with the commit message's own claim ("reformats 54 files... mechanical, ruff format itself").
Once pushed, every future PR against this repo gets a new `lint` check appearing in its Checks list. If
GitHub branch-protection rules are later set to require it (not visible from the local filesystem, not
checked this session — GitHub repo settings are outside what a filesystem-only grounding pass can see),
it could block a PR already in flight that hasn't run the three commands locally. This is the intended
behavior per the goal, not a defect, but the founder should know a new check will appear on push.

## Blockers
- **BLOCKER:** pushing to `origin/main` is outside what this grounding session — or any unattended
  session, per this repo's own intake policy recorded in the HANDOFF file, and per the standing rule
  against git mutations in unattended runs — is permitted to do. Not run this session (forbidden by
  both policies); control: `git log origin/main -1 --oneline` → `2214ac4`, confirming it has not
  already happened by some other path. No founder ruling is needed on *whether* to do this — the fix is
  already built, tested, and clean; this is a mechanical permissions gate, not a judgment call.
  **BLOCKED ON YOU:** only you (or a session you explicitly authorize with push access) can run
  `git push origin main` from a terminal that has it.
- **BLOCKER:** even after push, the goal's literal claim — "a PR that fails ... shows a red CI check" —
  has never actually been observed in GitHub's real Checks UI (no `act`/local runner exists in this
  environment, confirmed in the original spec's own Blockers section). Local command-line passes, which
  this session re-verified live (`ruff check agent_reach tests`, `ruff format --check agent_reach tests`,
  `mypy agent_reach` — all exit 0 against the pinned versions `ruff==0.15.1`, `mypy==1.19.1`,
  `types-requests==2.32.4.20260107`, `types-PyYAML==6.0.12.20250915` from `constraints.txt:15-18`), are
  necessary but not sufficient proof of the actual goal. **Resolved via Build order step 2 below** — a
  one-off throwaway PR with a deliberate violation is the only way to observe this, and it also requires
  push access.

## Questions
None beyond the push-access blocker above, which is a permissions fact, not an ambiguity — there is
nothing for the founder to decide, only something only the founder can execute.

## Build order
1. Founder runs `git push origin main`, landing commits `6c1e02f` and `6d5f425`. — gate: `git show origin/main:.github/workflows/pytest.yml | grep -n "ruff check\|ruff format --check\|mypy agent_reach"` exits 0.
2. Open one throwaway branch/PR with a single deliberate violation and observe GitHub's Checks UI. — gate: the PR's `lint` check shows red in GitHub's Checks tab; reverting the violation and re-pushing shows it green; then delete the throwaway branch/PR.
3. Correct `PROJECT-LEDGER.md` PRJ-001 to cite the pushed commit SHA and the real PR Checks-tab URL from step 2. — gate: the ledger row cites a real GitHub Checks observation, not just a local exit code.

## Items
- Push `6c1e02f` + `6d5f425` to `origin/main` (founder-only action; a human terminal, not an unattended
  session).
- Open and observe one throwaway PR proving a real red `lint` check on GitHub, then close it.
- Correct the PRJ-001 ledger row to cite GitHub-observed evidence instead of local-only evidence.
