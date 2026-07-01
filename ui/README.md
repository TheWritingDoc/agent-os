# Agent OS UI

Centralized web command center for Agent OS tools, skills, goals, and experiments.

## Run

```bash
cd ~/agent-os/ui
python3 app.py
```

Open: **http://localhost:4321**

## Features

- Dashboard with skill/project/output counts
- Projects browser
- Skills launcher
- Experiments runner (Hermes Oracle Lite)
- Journal viewer
- Outputs viewer (JSON)
- Goals editor

## Port

Default: **4321**

Override with env var:

```bash
AGENT_OS_UI_PORT=8080 python3 app.py
```
