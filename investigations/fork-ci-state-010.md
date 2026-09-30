# Investigation 010: fork CI execution state

## Observation

The fork contains the upstream GitHub Actions workflow at `.github/workflows/main.yml`. The workflow is configured to run on pushes to `main`, tags, and pull requests, with Python 3.10 through 3.15 test jobs and a 100% coverage gate.

However, GitHub currently reports no workflow runs for the fork, including after direct pushes to `main`.

## Consequence

Do not describe fork changes as CI-verified merely because the workflow file exists.

Until workflow execution is observed, distinguish:

- **repository-configured checks** — the workflow definition inherited from upstream;
- **executed checks** — currently none visible in the fork through GitHub Actions.

## Operating rule

Keep fork-specific runtime changes narrow, regression-backed, and explicitly documented. If Actions becomes active later, the existing matrix/coverage workflow should be used as the primary automated validation surface.

This is an undertaking/infrastructure observation only. It does not justify modifying the workflow configuration without evidence about why runs are absent.
