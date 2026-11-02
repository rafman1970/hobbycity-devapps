# HobbyCity DevApps

Shared development sandpit for HobbyCity NZ. Separate from the production repo
(`hobbycity-apps`): nothing here is pulled onto the task server or deployed.

## Setup (once per machine)

You need Python and Git for Windows installed, and to have accepted the
GitHub invite to this repo.

1. Clone the repo. Git creates the folder, so don't make it first:
   ```
   git clone https://github.com/rafman1970/hobbycity-devapps.git C:\HobbyCity-DevApps
   ```
   The first time, a GitHub sign-in window opens.
2. Install the Python packages:
   ```
   pip install -r C:\HobbyCity-DevApps\requirements.txt
   ```
3. Copy the `.env` file Richard gives you to `C:\HobbyCity-DevApps\.env`.
   It is not in the repo and must never be committed.

To get the latest changes later, in `C:\HobbyCity-DevApps` run `git pull`.

**`.env` holds production keys.** Scripts here act on the live Cin7 and
Supabase, so anything with a `--live` option makes real changes.

## Apps

- [rf_testpo](rf_testpo/README.md): create a test Bringans PO in Cin7.

## Rules

- **Never commit secrets.** `.env` and `credentials/` are ignored — keep keys there.
- One folder per app or experiment, e.g. `geek_portal_test/`.
- Work on a branch and open a pull request into `main`.
- Code that is ready for production gets moved into `hobbycity-apps` by Richard.
