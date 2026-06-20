# Realtime Machine Page

The Test repo includes a browser-running realtime dashboard at:

```text
docs/index.html
```

## What it does

- runs a realtime tick loop while the page is open
- tracks uptime, tick count, heartbeat, mode, and LM Studio status
- persists state in browser `localStorage`
- stores a local event log
- manages a small bot-test work queue
- copies or downloads machine snapshots as JSON
- attempts a browser-side LM Studio `/v1/models` check

## What it does not do

This is a static browser page. It does **not** run when the browser tab is closed. It does **not** create a persistent backend server. It does **not** keep running inside GitHub Pages without a viewer.

For always-on behavior, add one of these later:

```text
hosted backend
local daemon
GitHub Actions schedule
external worker
LM Studio local service wrapper
```

## GitHub Pages

GitHub Pages looks for an entry file such as `index.html`, `index.md`, or `README.md` at the top of the publishing source. This repo uses:

```text
docs/index.html
```

A GitHub Actions workflow was added at:

```text
.github/workflows/pages.yml
```

If Pages does not deploy automatically, open the repository settings and set Pages source to **GitHub Actions**.

## Local preview

From the repository root:

```bash
python -m http.server 8080 -d docs
```

Then open:

```text
http://localhost:8080
```

Local preview is recommended for LM Studio checks because browser security may block `http://localhost:1234` calls from a hosted GitHub Pages site.

## LM Studio browser check

The page attempts:

```text
GET http://localhost:1234/v1/models
```

If this fails from GitHub Pages, try local preview. Browser CORS and mixed-content rules may prevent direct checks from a public HTTPS page to a local HTTP service.

## Wisebase Routing

```text
workspace: Cyntra Coding Workspace
project: test
related_workspace: AI Bot Development
status: active
action: realtime-page
```
