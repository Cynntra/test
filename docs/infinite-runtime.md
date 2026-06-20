# Infinite Runtime Guide

This project cannot be kept running by ChatGPT itself. Infinite runtime means the repo contains a local supervisor and boot-service templates so your machine or server keeps the stack alive.

## Runtime stack

```text
LM Studio -> Local Daemon -> FastAPI Backend -> Browser Dashboard
```

## Infinite supervisor

Run:

```bash
python scripts/keepalive_realtime_stack.py
```

The supervisor starts:

```text
backend   FastAPI backend on 127.0.0.1:8787
daemon    LM Studio local watcher
dashboard static browser page on 127.0.0.1:8080
```

If any process exits, the supervisor restarts it with backoff.

## One-time setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Start LM Studio separately:

```bash
lms server start
```

Then run:

```bash
python scripts/keepalive_realtime_stack.py
```

Open:

```text
http://127.0.0.1:8080
```

Backend docs:

```text
http://127.0.0.1:8787/docs
```

## Service templates

### Linux systemd

Template:

```text
services/systemd/cyntra-test-realtime.service.example
```

Install outline:

```bash
cp services/systemd/cyntra-test-realtime.service.example /tmp/cyntra-test-realtime.service
# edit /tmp/cyntra-test-realtime.service and replace /ABSOLUTE/PATH/TO/Cynntra/test
sudo cp /tmp/cyntra-test-realtime.service /etc/systemd/system/cyntra-test-realtime.service
sudo systemctl daemon-reload
sudo systemctl enable cyntra-test-realtime
sudo systemctl start cyntra-test-realtime
sudo systemctl status cyntra-test-realtime
```

### macOS launchd

Template:

```text
services/launchd/com.cyntra.test.realtime.plist.example
```

Install outline:

```bash
cp services/launchd/com.cyntra.test.realtime.plist.example ~/Library/LaunchAgents/com.cyntra.test.realtime.plist
# edit the plist and replace /ABSOLUTE/PATH/TO/Cynntra/test
launchctl load ~/Library/LaunchAgents/com.cyntra.test.realtime.plist
launchctl start com.cyntra.test.realtime
```

### Windows Task Scheduler

Template:

```text
services/windows/CyntraTestRealtimeTask.xml.example
```

Install outline:

```powershell
# Edit XML paths first.
schtasks /Create /TN "Cyntra Test Realtime" /XML services\windows\CyntraTestRealtimeTask.xml.example
schtasks /Run /TN "Cyntra Test Realtime"
```

## Environment controls

```text
KEEPALIVE_RESTART_BASE_SECONDS=3
KEEPALIVE_RESTART_MAX_SECONDS=60
KEEPALIVE_CHECK_SECONDS=2
REALTIME_BACKEND_HOST=127.0.0.1
REALTIME_BACKEND_PORT=8787
REALTIME_DASHBOARD_HOST=127.0.0.1
REALTIME_DASHBOARD_PORT=8080
DAEMON_TICK_SECONDS=15
```

## Practical meaning of infinite

This setup runs indefinitely while the host machine is powered on and the service manager is active. It restarts crashed child processes and can start on login or boot depending on which service template you install.

It does not defeat shutdowns, sleep mode, OS updates, dead batteries, network outages, or LM Studio being unavailable. For stronger uptime, run it on a dedicated always-on mini PC, server, or VPS, then point the daemon/backend URLs accordingly.

## Safety

The daemon does not accept arbitrary remote commands. It only performs built-in LM Studio checks and optional predefined smoke tests.

Do not expose the backend publicly without replacing the local bearer token with real authentication and HTTPS.
