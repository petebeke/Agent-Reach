# SPEC-cut-pending-release — Ship the release that's already sitting on main

**Source:** PLAN/dumps/202610011705-estate-intake-onboarding.md
**Status:** READY

## Goal
A GitHub Release exists whose tag matches the current state of `main`, so (a) `agent-reach doctor` /
`agent-reach check-update` on every install still pinned to v1.5.0 (2026-06-11) correctly reports "update
available" instead of silently reporting "up to date" while missing two new channels and a security fix,
and (b) `CHANGELOG.md` names what actually shipped.

## Done when
`pyproject.toml` and `agent_reach/__init__.py` both read `1.6.0`, `CHANGELOG.md` has a dated `## [1.6.0]`
section (promoted from `## [Unreleased]`, with the merges since `v1.5.0` folded in), a `v1.6.0` git tag
points at that commit, and a GitHub Release named `v1.6.0` exists for it.

## DoD check
```
python3 -c "import tomllib,re; d=tomllib.load(open('pyproject.toml','rb')); v=d['project']['version']; \
import agent_reach; assert v == agent_reach.__version__ == '1.6.0', (v, agent_reach.__version__)"
grep -q '^## \[1.6.0\]' CHANGELOG.md
git tag --points-at v1.6.0 | grep -q v1.6.0
gh api repos/Panniantong/agent-reach/releases/latest --jq .tag_name | grep -q '^v1\.6\.0$'
```
All four must exit 0. The fourth call is the one that matters functionally — it is exactly the endpoint
`_cmd_check_update` polls (`agent_reach/cli.py:2273`), so it is also the regression check: run it again
after any future merge batch to catch the next time this drifts.

## Fits
- `pyproject.toml:3` — `version = "1.5.0"` → `"1.6.0"`
- `agent_reach/__init__.py:4` — `__version__ = "1.5.0"` → `"1.6.0"`
- `CHANGELOG.md:9` — `## [Unreleased]` heading; its current body (Boss直聘 fix + feature) becomes the seed
  of the new `## [1.6.0]` section, extended with the other unreleased work (see Blast radius)
- `agent_reach/cli.py:2273` (`_cmd_check_update`) and `:2338` (the `doctor` call site) — both read
  `GET /repos/Panniantong/Agent-Reach/releases/latest` and compare `tag_name` to `__version__` via
  `_is_newer_version` (`agent_reach/cli.py:2250`). This is the live consumer that makes "no release since
  v1.5.0" a functional gap, not cosmetic — confirmed no other workflow or script touches `releases/`:
  `grep -rn "releases" agent_reach/ .github/` → only the two cli.py call sites above.
- `CLAUDE.md:4` — "gives AI agents read/search access to 13 internet platforms" is stale; actual count is
  16, enumerated in `README.md:104-121` (the 支持的平台 table) and matching 1:1 with
  `ls agent_reach/channels/*.py` minus `base.py`, `_opencli_site.py`, `mcporter.py` (helpers, not platforms).
- `CLAUDE.md:40` — "Version in THREE places must match: `pyproject.toml`, `__init__.py`,
  `tests/test_cli.py`" is false as written: `tests/test_cli.py` carries no version literal that must be
  edited. Checked — `grep -n "1\.5\.0" tests/test_cli.py` returns only two unrelated fixtures inside
  `TestIsNewerVersion` (`:427`, `:466-477`) that exercise the comparison function with arbitrary version
  strings, not the live package version; `test_version` (`tests/test_cli.py:18`) only asserts the string
  `"Agent Reach v"` is present, never a specific number. A future session trusting this line would edit a
  file that needs no edit.

## Wiring
This is a release action, not new code — nothing to wire in the usual producer→consumer sense. The thing
that "calls" the result is external: any already-installed `agent-reach` binary whose `check-update` /
`doctor` path hits `agent_reach/cli.py:2273` against GitHub's API. Verified reachable: the DoD check's
4th command hits the same real endpoint.

## Conflicts
- rules: `grep -n "release\|changelog\|version bump" ~/.claude/commands/CLAUDE.md` → no hits; no standing
  rule governs how this repo cuts a release, so this spec sets no precedent beyond itself.
- live rows: ledger has zero project rows yet (`PROJECT-LEDGER.md` — PRJ-000 only, this is the first
  onboarding pass for this repo), so nothing here conflicts with an existing open item.
- decisions: `grep -n "agent.reach\|Agent Reach" ~/.claude/DECISIONS.md` → no hits.

## Blast radius
Touches only `pyproject.toml`, `agent_reach/__init__.py`, `CHANGELOG.md`, `CLAUDE.md`, plus a new git tag
and GitHub Release — no runtime code changes, so no test should flip. Enumerated the one place version
strings are read at runtime (`agent_reach/cli.py`, see Fits) and confirmed no test asserts a literal
current-version string that this would break: `grep -n "1\.5\.0\|__version__ ==" tests/*.py` → the only
`1.5.0` hits are the `_is_newer_version` fixtures already covered above, which take version strings as
*parameters*, not as an assertion against the live package version.
The CHANGELOG body for `[1.6.0]` must actually enumerate the merged work — positive control that there is
real content to summarize: `git log --oneline v1.5.0..HEAD | wc -l` → 95 commits, including two new
channels (`feat(channels): add facebook and instagram opencli support`, `feat: 新增 Boss直聘 channel`)
and a security hardening commit (`fix(security): harden local credential handling`). Writing "no changes"
would be false.

## Blockers
- **BLOCKER:** creating a GitHub Release (not just a git tag) requires an authenticated `gh` CLI or
  equivalent GitHub API credential in whatever environment runs the Build order below —
  `gh issue list --repo Panniantong/agent-reach --state open --limit 1` → `gh not available or not authed`
  (checked this session); control: `which git` → present, so the tag itself is not blocked, only the
  Release object is. **Resolved:** no founder ruling needed — this is an environment/auth precondition
  for the execution session, not a product decision; the execution session runs under the repo's own
  full edit/commit/push authority and only needs `gh auth login` or a `GITHUB_TOKEN` to proceed.

## Questions
None. The version number (1.6.0, a minor bump) follows the repo's own unbroken pattern — every prior tag
from v1.1.0 through v1.5.0 bumped minor for added channels/features (confirmed via `git tag` + CHANGELOG
headers), and this batch adds two new channels, so there is no genuine ambiguity for him to resolve.

## Build order
1. Bump `pyproject.toml:3` and `agent_reach/__init__.py:4` to `1.6.0` — gate: DoD check command 1 exits 0
2. Rewrite `CHANGELOG.md:9` `## [Unreleased]` as `## [1.6.0] - <today's date>`, keep its existing Boss直聘 content, and add entries for the other unreleased merges (facebook/instagram opencli support, the security-hardening commit, and any other user-facing change in `git log v1.5.0..HEAD`) — gate: DoD check command 2 exits 0
3. Fix `CLAUDE.md:4` ("13" → "16") and `CLAUDE.md:40` (drop the false `tests/test_cli.py` claim, state accurately that only `pyproject.toml` and `agent_reach/__init__.py` must match) — gate: `grep -c "16 internet platforms" CLAUDE.md` returns 1
4. Commit steps 1-3 — gate: `git log -1 --name-only` shows exactly those four files
5. Tag the commit `v1.6.0` and push the tag — gate: DoD check command 3 exits 0
6. Create a GitHub Release for `v1.6.0` (`gh release create v1.6.0 --notes-file <(sed -n '/## \[1.6.0\]/,/## \[1\.3\.1\]/p' CHANGELOG.md)` or equivalent) — gate: DoD check command 4 exits 0

## Items
- Bump version in `pyproject.toml` and `agent_reach/__init__.py` to 1.6.0
- Promote `CHANGELOG.md`'s `[Unreleased]` section to a dated `[1.6.0]` section, backfilled with the other
  95 commits' user-facing changes since v1.5.0
- Fix the stale "13 internet platforms" and "three places must match" lines in `CLAUDE.md`
- Tag `v1.6.0` and publish a matching GitHub Release so `_cmd_check_update` (`agent_reach/cli.py:2273`)
  starts reporting it to existing installs
