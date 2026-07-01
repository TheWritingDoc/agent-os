# AI Tools Command Center

**Purpose:** Single view of all AI tools on this PC, with exact commands and when to use each.  
**Owner:** jason  
**Updated:** 2026-07-01

---

## Core Principle

No more hunting for the right tool. Every AI tool installed on this machine is listed here with:
- What it does
- When to use it
- Exact command to invoke it
- Current status

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Installed and ready |
| ⚠️ | Installed but needs config/testing |
| ❓ | Mentioned but status unknown |

---

## 1. Code Generation / Coding Agents

### Claude Desktop
- **What:** GUI version of Claude
- **Use for:** Chat, brainstorming, document analysis, quick tasks
- **Invoke:** `claude-desktop` or application launcher
- **Path:** Windows desktop app (check Start Menu)
- **When to use:** When you want a chat interface or need to paste large context
- **Status:** ✅ Installed

### OpenCode
- **What:** CLI coding assistant
- **Use for:** Code help, refactoring, explanations
- **Invoke:** `opencode`
- **Path:** `/home/msicyborg/.npm-global/bin/opencode`
- **When to use:** Lightweight coding Q&A and edits
- **Status:** ✅ Installed

### OpenClaw
- **What:** CLI coding agent (Claude Code alternative)
- **Use for:** Code generation, editing, debugging from terminal
- **Invoke:** `openclaw` or `claw`
- **Path:** `/mnt/c/Users/MSI CYBORG/.local/node/node-v22.19.0-win-x64/openclaw`
- **When to use:** Quick terminal-based coding when you don't want browser/IDE
- **Status:** ✅ Installed

### Claude Code (Subscription)
- **What:** Anthropic's official CLI coding agent
- **Use for:** Heavy coding tasks, large refactors, complex debugging
- **Invoke:** `claude` or `claude code`
- **Path:** `/home/msicyborg/.npm-global/bin/claude`
- **When to use:** Mission-critical code, when you want the strongest model
- **Status:** ✅ Installed + subscribed

### Kimi Code CLI
- **What:** Kimi coding agent in terminal
- **Use for:** Code generation, project edits, debugging with Kimi models
- **Invoke:** `kimi` or `kimi-cli` (both at `~/.local/bin/kimi.exe`, `~/.local/bin/kimi-cli.exe`)
- **Config:** `~/.kimi/config.toml`
- **Default model:** `kimi-code/kimi-for-coding`
- **Available models:** `kimi-k2.5`, `kimi-k2-thinking`, `kimi-k2-turbo-preview`, etc.
- **When to use:** When you want Kimi's coding model specifically; strong for coding tasks
- **Status:** ✅ Installed + subscribed

### Pi Agent (Pi Coding Agent)
- **What:** Pi coding agent CLI
- **Use for:** Coding tasks, project edits
- **Invoke:** `pi` (at `/mnt/c/Users/MSI CYBORG/node-v24.18.0-win-x64/pi`)
- **Package:** `@earendil-works/pi-coding-agent`
- **When to use:** Alternative CLI coding agent
- **Status:** ✅ Installed

---

## 2. Agent Orchestration

### Hermes Agent
- **What:** Main agent environment (this chat)
- **Use for:** Orchestration, multi-step tasks, automation, memory, skills, cron
- **Invoke:** This chat interface / `hermes`
- **When to use:** When you want an agent that remembers, schedules, and delegates
- **Status:** ✅ Active

### Hermes Skills
- **What:** Reusable procedural memory
- **Use for:** Deployment, research, mentor tracking, automation
- **Invoke:**
  - List: `skills_list`
  - View: `skill_view(name)`
  - Our skills: `mentor-mirror`, `deployer`, `media-tools`
- **Status:** ✅ Active

### Hermes Cron Jobs
- **What:** Scheduled automation
- **Invoke:**
  - List: `cronjob(action='list')`
  - Run now: `cronjob(action='run', job_id='...')`
- **Active jobs:**
  - `Daily AI Morning Brief` (ID: `8065734b009f`) — 07:00 daily
- **Status:** ✅ Active

---

## 3. LLM Providers

### GLM / Z.AI (GLM-5.2 subscription)
- **What:** Primary LLM provider
- **Model:** `glm-5.2`
- **Use for:** General coding, reasoning, planning
- **Access:** Via `ZAI_API_KEY`, base URL `https://open.bigmodel.cn/api/paas/v4/`
- **When to use:** Default coding and reasoning tasks
- **Status:** ✅ Active + subscribed

### Kimi Coding Plan (subscription)
- **What:** Kimi coding model subscription
- **Use for:** Coding tasks via Kimi Code CLI or API
- **Invoke:** `kimi` / `kimi-cli`
- **Models available:** `kimi-k2.5`, `kimi-k2-thinking`, `kimi-for-coding`
- **When to use:** When Kimi outperforms others for a specific task
- **Status:** ✅ Subscribed + installed

### OpenRouter / Other Providers
- **What:** Fallback provider
- **Use for:** When Z.AI/Kimi unavailable
- **Access:** OpenRouter API key
- **When to use:** Fallback only
- **Status:** ✅ Available

---

## 4. Terminal / Session Management

### tmux
- **What:** Terminal multiplexer
- **Use for:** Persistent terminal sessions, split panes, session management
- **Invoke:** `tmux new -s <name>` / `tmux attach -t <name>`
- **When to use:** Long-running processes, multiple terminal workspaces
- **Status:** ✅ Installed

### Terminal (Hermes)
- **What:** Shell access inside Hermes
- **Use for:** Commands, installs, git, deployments
- **Invoke:** `terminal(command='...')`
- **Status:** ✅ Active

---

## 5. Browser / Web Tools

### Hermes Browser Tools
- **What:** Web navigation and interaction
- **Use for:** Testing deployed apps, scraping, UI verification
- **Invoke:**
  - `browser_navigate(url='...')`
  - `browser_snapshot()`
  - `browser_click(ref='@e1')`
  - `browser_type(ref='@e1', text='...')`
  - `browser_console(expression='...')`
- **Status:** ✅ Active

---

## 6. Memory / Knowledge

### ~/agent-os/ Vault
- **What:** Local markdown knowledge base
- **Use for:** Project context, mentor maps, progress tracking, journal
- **Path:** `/home/msicyborg/agent-os/`
- **When to use:** Shared memory across all agents and sessions
- **Status:** ✅ Active

### Hermes memory Tool
- **What:** Persistent facts across Hermes sessions
- **Use for:** User preferences, stable facts, important reminders
- **Invoke:** `memory(target='memory' or 'user', operations=[...])`
- **Status:** ✅ Active

### fact_store Tool
- **What:** Deep structured memory with reasoning
- **Use for:** Entity relationships, compositional queries
- **Invoke:** `fact_store(action='add' | 'search' | 'probe' | 'reason', ...)`
- **Status:** ✅ Active

---

## 7. Automation / Scheduling

### Hermes cronjob Tool
- **What:** Schedule recurring jobs
- **Use for:** Daily briefs, periodic checks, background work
- **Invoke:** `cronjob(action='create' | 'list' | 'run' | 'update', ...)`
- **Status:** ✅ Active

### cron (system)
- **What:** Linux cron scheduler
- **Use for:** System-level scheduled scripts
- **Invoke:** `crontab -e`
- **Status:** ✅ Available

---

## 8. Quick Selection Guide

| I want to... | Tool to use |
|--------------|-------------|
| Heavy coding / complex refactor | `claude` (Claude Code) |
| Quick terminal coding | `openclaw` or `opencode` |
| Coding with Kimi model | `kimi` (Kimi Code CLI) |
| Alternative CLI agent | `pi` |
| Chat / brainstorm / documents | Claude Desktop or Hermes |
| Run multi-step automation | Hermes Agent |
| Schedule recurring work | `cronjob` or `crontab` |
| Persistent terminal session | `tmux` |
| Test a deployed web app | Hermes browser tools |
| Search/deploy repo | Hermes `github-operations` skill or `gh` CLI |
| Remember something long-term | `memory` / `fact_store` |
| Access project context | `~/agent-os/CONTEXT.md` or project `context.md` |
| Get daily AI news | Morning brief cron job |

---

## 9. Tool Layer Architecture

```
┌──────────────────────────────────────────┐
│ USER INTERFACE LAYER                     │
│ Hermes Chat | Claude Desktop | tmux      │
├──────────────────────────────────────────┤
│ CODING AGENTS                            │
│ Claude Code | OpenClaw | Kimi | OpenCode │
├──────────────────────────────────────────┤
│ ORCHESTRATION                            │
│ Hermes Agent + skills + cron             │
├──────────────────────────────────────────┤
│ MODEL PROVIDERS                          │
│ GLM/Z.AI (glm-5.2) | Kimi | OpenRouter   │
├──────────────────────────────────────────┤
│ MEMORY                                   │
│ ~/agent-os/ vault | memory | fact_store  │
├──────────────────────────────────────────┤
│ EXECUTION                                │
│ Terminal | Browser | Git | Deploy        │
└──────────────────────────────────────────┘
```

---

## 10. Suggested Workflow

1. **Plan / orchestrate** in Hermes (this chat)
2. **Heavy coding** with Claude Code or Kimi Code CLI
3. **Quick edits / exploration** with OpenClaw or OpenCode
4. **Chat / documents** in Claude Desktop
5. **Long-running sessions** in tmux
6. **Remember everything** via `~/agent-os/` vault + `memory`
7. **Automate** via Hermes skills + cron

---

## 11. Unknowns to Verify

- [x] Exact command for **Pi Agent** → `pi`
- [x] Exact command for **Kimi Code CLI** → `kimi` / `kimi-cli`
- [x] Whether **OpenClaw** is `claw` or `openclaw` → `openclaw`
- [ ] Whether **OpenCode** requires any API key setup
- [ ] Whether **Claude Desktop** auto-starts on Windows
- [ ] Whether **Pi** has credentials configured

To verify remaining items, run in terminal:
```bash
opencode --help
pi --help
```

---

## 12. How to Add a New Tool

1. Install the tool
2. Add a section here
3. Add it to the quick selection guide
4. Update the tool layer architecture
5. Test the exact command
6. Update `AI-TOOLS-DASHBOARD.md`
