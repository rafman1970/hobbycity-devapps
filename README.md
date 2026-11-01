# HobbyCity DevApps

Shared development sandpit for HobbyCity NZ. Separate from the production repo
(`hobbycity-apps`): nothing here is pulled onto the task server or deployed.

## Rules

- **Never commit secrets.** `.env` and `credentials/` are ignored — keep keys there.
- One folder per app or experiment, e.g. `geek_portal_test/`.
- Work on a branch and open a pull request into `main`.
- Code that is ready for production gets moved into `hobbycity-apps` by Richard.
