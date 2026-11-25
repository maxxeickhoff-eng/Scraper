# Publication Audit — Books to Scrape

This file records the publication audit for this project:

- what was checked
- what was found
- which findings needed action
- what was fixed
- what remains open

It is sanitized: no secret values, keys or personal contact details appear here.

| | |
|---|---|
| Tool | Claude Code (AI coding assistant), run from the project root folder |
| Prompt | The audit prompt from the course submission guidelines (unchanged) |
| Audit 1 | 2026-11-19, read-only (no files changed, no code run) |
| Fixes | 2026-11-19, after reviewing the findings |
| Audit 2 | 2026-11-19, the same checks repeated after the fixes |
| Audit 3 | 2026-11-25, logged-out check of the public repository |

## What was checked

| Area | How |
|---|---|
| Git status | `git status --ignored`, which shows tracked, untracked and ignored files |
| Tracked files | All tracked files listed with their sizes and reviewed |
| Secrets in files | Pattern scan of every tracked file. Patterns covered: Supabase keys, GitHub tokens, JWTs, private keys, the Supabase project URL, email addresses, local user paths, and words like "password", "token" and "api key". The scan printed file names only, never values. |
| Secrets in history | The same pattern scan over **every commit** (`git grep` over `git rev-list --all`) |
| Personal data | Commit author and committer metadata (`git log`), file contents, screenshot metadata |
| Exclusions | `git check-ignore` run against typical local files: `.env` variants, virtual environments, editor folders, caches, logs |
| Configuration | Whether `.env.example` exists and contains only placeholders; permissions of the local `.env` |
| Dependencies | `requirements.txt` present and pinned; Python version documented |
| Generated files | Whether generated output (`index.html`) is tracked, and whether that is intended |
| External resources | Hosts that the HTML page loads content from |
| README | Checked against the required sections: purpose, data collection, persistence, user interaction, setup, learning, limitations and assistance |

## Audit 1: findings and decisions

"Confirmed" means the issue was verified in the files or the history. "Possible concern" means it depends on context or a judgement call.

| # | Finding | Type | Action needed? | Decision |
|---|---|---|---|---|
| 1 | No secrets in tracked files or in the history. `.env` and `.venv/` are ignored, and `.env` was never committed. | Confirmed (OK) | No | — |
| 2 | A Supabase secret key and a GitHub access token were pasted into an AI chat session during setup. They are not in the repository. | Confirmed (outside the repo) | **Yes** | Rotate both (see "Remaining items") |
| 3 | The commit metadata contains the personal email addresses of both contributors, and they become public with the repo. | Confirmed | **Yes** | Fixed: the history was rewritten to GitHub `noreply` addresses, with both contributors agreeing |
| 4 | The README is missing the **Learning** and **Limitations and assistance** sections, explains data collection only briefly, and has no screenshot. | Confirmed | **Yes** | Fixed |
| 5 | `.gitignore` misses common cases: `.env.local`/`.env.*`, `venv/`, `env/`, `.vscode/`, `.idea/`, `*.log`, `.pytest_cache/`. | Confirmed | **Yes** | Fixed |
| 6 | The README doesn't state the minimum Python version. The `supabase` package needs 3.9 or newer. | Confirmed | **Yes** | Fixed |
| 7 | The README says GitHub Pages is free, which is only true for public repositories. | Confirmed | Yes | Fixed: the claim was removed |
| 8 | `setup_supabase.py` writes `.env` with default permissions, so other local users can read it. It also writes to the current folder instead of the project folder. | Confirmed (minor) | Yes | Fixed |
| 9 | `index.html` is a generated file (about 320 KB) but is tracked. | Possible concern | No | **Kept on purpose.** It is the project's interface and lets graders view the result without a Supabase account. It is documented as generated in the README. |
| 10 | The page loads fonts from Google Fonts, so visitors' IP addresses are sent to Google. | Possible concern | No | **Accepted** and documented under Limitations. The page is opened locally; self-hosting the fonts would be the fix if it were deployed publicly. |
| 11 | The scraper sends 50 requests with no pause and the default User-Agent. | Possible concern | No | **Accepted**, because the target is a sandbox site built for scraping practice. Documented under Limitations. |
| 12 | There is no `LICENSE` file. | Possible concern | No (not required) | Left open; see "Remaining items" |
| 13 | There are no automated tests; `test_connection.py` is a manual check. | Possible concern | No | Documented under Limitations |

## Fixes made

| Finding | Fix | File |
|---|---|---|
| 4 | README rewritten with all required sections, an explanation of how the scraper works, a pipeline diagram and a screenshot | `README.md`, `docs/screenshot.png` |
| 5 | Added `.env.*` (keeping `!.env.example`), `venv/`, `env/`, `.vscode/`, `.idea/`, `*.log`, `.pytest_cache/` | `.gitignore` |
| 6 | Added "Python 3.9 or newer" to Setup | `README.md` |
| 7 | Removed the GitHub Pages claim | `README.md` |
| 8 | `.env` is now written to the project folder and set to owner-only access (`chmod 600`); the existing local `.env` was changed the same way | `setup_supabase.py` |
| 3 | The repository is configured to commit with the GitHub `noreply` address. All existing commits were rewritten (`git filter-branch --env-filter`) so that author and committer emails use each contributor's `noreply` address. A backup was taken first, and the rewrite was checked to leave every file unchanged. | Git history, `.git/config` |

## Audit 2: re-check after fixes

The same checks were repeated on every file that would be published, and on the full history.

| Check | Result |
|---|---|
| Secret patterns in files that would be published | None found |
| Secret patterns in all commits | None found |
| Email addresses or local user paths in files | None found |
| Personal email addresses in commit metadata | None. All commits use GitHub `noreply` addresses. |
| `.env`, `.env.local`, `.env.production` | Ignored |
| `.env.example` | Tracked (placeholders only) |
| `.venv/`, `venv/`, `env/`, `__pycache__/`, `.pytest_cache/`, `.vscode/`, `.idea/`, `*.log`, `.DS_Store` | Ignored |
| Local `.env` permissions | Owner-only (`-rw-------`) |
| Screenshot metadata | Only the basic image chunks (`IHDR`, `IDAT`, `IEND`); no author, path or location data |
| README sections | Purpose, Data collection, Data persistence, User interaction, Setup, Learning, Limitations and assistance: all present |

## Remaining items

Done before publishing:

- [x] **Rotate the Supabase secret key** (finding 2). A new secret key was created and stored with `setup_supabase.py`, and the old key was deleted. Verified: the old key is now rejected (HTTP 401), and the new key connects.
- [x] **Revoke the exposed GitHub token** (finding 2). Verified: the GitHub API rejects it (HTTP 401).
- [x] **Commit emails** (finding 3): the history was rewritten to `noreply` addresses.
- [x] **Force-push the rewritten history** to GitHub. Verified: GitHub's `main` matches the local rewritten history.
- [x] **Keep my email addresses private** and **Block command line pushes that expose my email** enabled in the repository owner's GitHub account.
- [ ] **Teammate re-clones** the repository and enables the same email setting. Their old local clone still holds the old history.
- [x] **Make the repository public** (see Audit 3 below).
- [ ] Optional: add a `LICENSE` (finding 12).

## Audit 3: check after publishing

This check was run without logging in to GitHub, against the now-public repository.

| Check | Result |
|---|---|
| Repository page while logged out | Opens (HTTP 200) |
| Screenshot used in the README | Publicly reachable (HTTP 200) |
| Branches on GitHub | `main` only, matching the local commit |
| `.env` in the public repository | Not present |
| Personal email addresses in commit metadata | None |
| Secret patterns in the full public history | None found |
| Files in the public repository | Only the files listed in the README's project structure |

## What could not be verified

- **GitHub features beyond the code:** releases, issues, GitHub Actions secrets and wiki pages were not checked.
- **Old commits cached by GitHub:** the commits from before the email rewrite may stay reachable for a while through their direct commit links (not through the repository). Removing them completely requires a request to GitHub Support.
- **The teammate's account settings and local clone.**
- **The live Supabase database:** only `schema.sql` and the code were checked, not policies or tables created later in the dashboard.
- **Secrets in formats** that the pattern scan doesn't cover.
- **The terms of use** of books.toscrape.com, and whether its cover images may be reused.

Finding no issues in an automated scan does not prove the project is safe.
