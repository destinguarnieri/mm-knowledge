# Backend testing

Status: confirmed — Destin accepted all three stages on 2026-11-03. MON-245/246/247 and parent MON-149 are Done. Implementation committed as 7e891a59 (fix/test_harness), merged locally into feat/work as 38fc3c93 at Destin’s request. Not pushed; remote CI and live external checks have not run.

## Supported commands

Run from mm_v04/backend after installing the project environment with uv sync:

```bash
uv run pytest                         # Offline, no coverage wrapper
uv run pytest tests/helpers/          # Targeted offline tests
bash scripts/test.sh tests/helpers/   # Offline with coverage/JUnit
bash scripts/test-db.sh               # Disposable PostgreSQL with coverage/JUnit
bash scripts/test-db.sh tests/crud/test_user.py -q
bash scripts/test-external.sh --collect-only -q  # Safe external inventory; no requests
# Explicit network opt-in only:
bash scripts/test-external.sh -v
```

Shell arguments are pytest arguments, including paths, node IDs, -k, and -q; the old coverage-title positional argument is no longer supported. Paths are relative to backend. Root scripts/test.sh and scripts/test-local.sh, and backend/scripts/tests-start.sh, all delegate to offline tests. None starts or tears down the application Compose stack, invokes prestart/initial_data, or deletes volumes. Application startup scripts remain outside the test workflow.

Scripts use backend/.venv/bin/python. In a worktree without its own environment, set MM_TEST_PYTHON to an existing project interpreter. Verification here used /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/.venv/bin/python with source from /Users/destinguarnieri/.codex/worktrees/deb5/mm_v04. The runner clears inherited app/environment overrides; ordinary .env files are not read.

## Modes and boundaries

Offline is the default, including collection. Settings are synthetic; unexpected PostgreSQL, network, and unguarded subprocess activity fails. Child Python processes inherit test isolation. Explicit database or external file selection in the wrong mode fails before importing that test module.

The database runner creates a uniquely named PostgreSQL 17 Compose project, random loopback port, random test password, and tmpfs data storage. It checks ownership, mounts, and port binding before issuing a private lease; drivers verify database/user/server identity before returning connections. Migrations and every test session point to that instance. CRUD uses rollback; committed/concurrent/migration tests retain real connection semantics with per-test public-table cleanup. No existing app DB or volume is used. Owned resources are removed on normal failure/interrupt; SIGKILL or host/daemon loss can prevent cleanup. Separate invocations own separate DBs, but same-mode report directories are overwritten by the latest invocation; do not run them concurrently if retaining reports matters.

External mode allows only the inventoried public BTC candle reads through a test-only HTTPS transport: api.hyperliquid.xyz:443, POST /info, candleSnapshot payload, seven explicit intervals, bounded windows/response size/timeouts. DNS must resolve to public addresses; redirects, arbitrary sockets, database drivers, SDK websockets, account credentials, and trading methods are unavailable through that transport. These are accidental-I/O guards, not a security sandbox against malicious Python. Real exchange tests require explicit invocation; this implementation was verified with mocked transports and collection only, not live requests.

Inventory: python -m tests.support.inventory. As of this checkpoint: 155 test modules (140 offline, 14 database, 1 external), 966 static test definitions. The external module expands to eight parametrized cases. All prior assertions are preserved; the external suite swaps only its client setup/fetch boundary to the restricted public client.

## Reports and CI

Shell runners write .coverage, coverage.xml, junit.xml, and html/index.html under backend/test-results/{offline,database,external}/, including on pytest failure. Pytest exit status is preserved. Coverage measures the main pytest interpreter; child-process isolation does not imply child coverage collection. Bootstrap imports precede coverage and may produce already-imported warnings.

Test Backend CI runs offline and disposable-database modes in separate matrix jobs using Python 3.11 and frozen dependencies. Both upload distinct coverage artifacts even on test failure. Once both succeed, a separate job combines their coverage data and emits the existing coverage-html artifact for the unchanged Smokeshow workflow/check. The external workflow has only workflow_dispatch; pushes/PRs do not run it. Local union validation confirmed combined line sets exactly match both suite inputs across 355 files. Workflow YAML/structure was validated locally; remote CI was not dispatched.

## Current verification and known failures

Merge verification on feat/work (38fc3c93): 84 focused harness/identity tests and scoped Ruff pass. Full offline: 1,581 passed, 73 failed, 2 collection errors. Full database: 108 passed and the same 2 email failures. Migrations through d92e7a41c608 succeeded in the disposable instance; owned container/network cleanup verified. Compared with the older source-branch baseline below, 15 Example failures disappeared and 47 failure nodes were added in unchanged feat/work files: 41 MultiSpeedEwmacSnapshot fixtures omit trailing_annual_volatility; 6 summary-worker fixtures use the former Example THRESHOLDS payload. These are existing branch fixture mismatches, not edits made by this merge. Both code checkouts are clean.

MON-247 local CI-equivalent results: offline 1,118 passed, 41 failed, 2 collection errors; database 108 passed, 2 failed. Failure/error node sets exactly match MON-246. The 25 new offline guard/runner cases pass. All six shell entrypoints preserve argument boundaries, arbitrary-cwd behavior, and failure exit 23. External mode collects eight cases without requests; mocks verify destination/request/redirect/response limits and database blocking. Scoped Ruff, strict mypy, and diff checks pass. No disposable resources remained after the DB run.

The historical offline failures remain visible, including missing emac_v2/n_bar_breakout modules. DB failures remain the password-recovery template path and the stale app.utils.send_email patch. Coverage additionally warns about the preexisting invalid numeric annotations in app/data_models/dto/forecast.py; report generation uses --ignore-errors so the remaining report is available, excluding unparsable source. No test failure is ignored or converted into success. CI is expected to remain red until those separate defects are fixed.

See [MON-149](https://linear.app/money-machine/issue/MON-149), [MON-245](https://linear.app/money-machine/issue/MON-245), [MON-246](https://linear.app/money-machine/issue/MON-246), [MON-247](https://linear.app/money-machine/issue/MON-247), and [[sessions/current-checkpoint]].
