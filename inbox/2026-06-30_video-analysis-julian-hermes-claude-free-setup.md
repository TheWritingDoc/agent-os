# Video Analysis: Free Claude Code + Hermes Agent Setup

**URL:** https://www.youtube.com/watch?v=8PsKX5fCTJ0  
**Topic:** Free Claude Code + Hermes Agent as a powerful autonomous AI stack  
**Date analyzed:** 2026-06-30

---

## 1. Core Argument

Julian argues that **free Claude Code + Hermes Agent** is one of the most powerful free AI setups available, and most people are using AI wrong by working in isolated tabs with no shared memory.

Key contrast:
- **Wrong way:** Claude tab, ChatGPT tab, terminal, scattered files — no memory between sessions.
- **Right way:** Hermes orchestrates + Claude Code executes + Agent OS dashboard + Obsidian memory vault = one integrated system.

---

## 2. What Each Component Does

### Hermes Agent
- Free, open-source, from Nous Research (released Feb 2026).
- Autonomous agent living on your server.
- Remembers what it learns.
- Gets more capable over time.
- 26-event hook system.
- Plugin and skills marketplace.
- `claude.md` project memory.
- `memory.md` auto memory.
- Cloud-managed scheduling on Anthropic infrastructure.
- Cross-platform continuation (Telegram, Discord, Slack, WhatsApp, Signal, CLI).

**Our mapping:**
- We are already inside Hermes Agent.
- We already use skills, memory, cron jobs, and cross-platform gateways.

### Claude Code
- Anthropic's CLI coding agent.
- Reads, writes, edits, executes code locally.
- Plans, acts, iterates autonomously.
- Gets priority access to Claude's latest capabilities.

**Our mapping:**
- We can install Claude Code as a sub-agent for heavy coding tasks.
- Hermes can spawn Claude Code automatically.
- Alternative: we already use Hermes coding tools + GLM/Z.AI, but Claude Code is a stronger executor.

### Agent OS Dashboard
- Left rail: all agents (Claude, Hermes, OpenClaude, custom) with live status.
- Right rail: active goals, daily journal, memory vault search.
- Agent control room: API keys, providers, session history, skills, plugins, Kanban tasks.
- Insights panel: tool calls, tokens, models, activity patterns, peak hours.

**Our mapping:**
- We don't have a visual dashboard yet.
- This is a future build: a web dashboard reading from `~/agent-os/` and Hermes state.

### Memory Vault (Obsidian)
- Self layer records screen + microphone.
- Exports notes to Obsidian vault.
- Vault becomes a continuously growing knowledge base.
- Agents pull from vault for personalized output.
- Full-text search of past conversations.
- Two-layer compression system to prevent context drift.

**Our mapping:**
- We use `CONTEXT.md` + `~/agent-os/` markdown.
- We can add Obsidian integration and screen recording later if needed.
- Immediate priority: make `CONTEXT.md` richer and searchable.

### Skills System
- Hermes writes its own skills from experience.
- Compatible with agent-skills.io open standard.
- Skill Claw: auto-evolves, deduplicates, improves skill library.
- Post-task evolution loop.

**Our mapping:**
- We are already building custom skills (`mentor-mirror`).
- We should design skills to be composable and self-improving.
- Future: add a skill-evolution workflow.

### Automations / Hooks
- 26-event hook system triggers actions.
- New message → welcome member.
- Scheduled time → daily report.
- Task complete → next action.
- Built-in cron scheduler.

**Our mapping:**
- We use `cronjob` for scheduling.
- We can add event hooks via webhooks, Telegram bots, etc.
- Morning briefing already running.

---

## 3. Practical Workflow Described

For a community/content business like AI Profit Boardroom:
1. Wire up Agent OS.
2. Set quarterly goals in goals tracker.
3. Journal daily (voice or text).
4. Morning briefing pulls community activity, flags trends, suggests content.
5. Onboarding automation for new members.
6. Weekly audit reviews what's working.
7. After 3 months, the system knows the business deeply.

**Our mapping:**
- We don't run a community, but the same structure applies to our projects.
- Goals tracker → `CONTEXT.md` + progress tracker.
- Daily journal → voice memos or quick text notes to `~/agent-os/journal/`.
- Morning briefing → already running cron job.
- Onboarding automation → not applicable yet.
- Weekly audit → new cron job or skill.

---

## 4. Key Technologies Mentioned

| His Tool | Purpose | Our Equivalent | Status |
|----------|---------|----------------|--------|
| Hermes Agent | Orchestration | Hermes Agent | ✅ |
| Claude Code | Coding executor | Installable CLI sub-agent | ⏳ |
| Agent OS dashboard | Visual command center | Build later (React/Vercel) | ⏳ |
| Obsidian vault | Memory/knowledge base | `~/agent-os/` + Obsidian skill | 🔄 |
| Skills marketplace | Reusable skills | Custom skills + skill_view | 🔄 |
| Skill Claw | Auto-evolve skills | Future workflow | ⏳ |
| 26-event hooks | Event-driven automation | Cron + webhooks + gateways | 🔄 |
| Cross-platform gateways | Telegram/Discord/Slack/WhatsApp/Signal/CLI | Hermes gateways | ✅ |
| Self layer | Screen + mic recording | Future, optional | ⏳ |
| Goals tracker | Quarterly goals with progress bars | `CONTEXT.md` + progress tracker | 🔄 |
| Daily journal | Voice/text journal | `~/agent-os/journal/` | ⏳ |
| Morning briefing | Daily summary automation | Cron job `8065734b009f` | ✅ |

---

## 5. What We Should Steal Immediately

### 5.1 The Orchestrator + Executor Pattern
**His setup:** Hermes orchestrates → Claude Code executes.  
**Our setup:** Hermes orchestrates → Hermes coding tools / subagents execute → optionally spawn Claude Code for heavy coding.

**Action:** Install Claude Code CLI as an optional sub-agent for complex implementation tasks.

### 5.2 Daily Journal + Goals Tracker
**His setup:** Daily journal entries + quarterly goals with progress bars.  
**Our setup:** Add `~/agent-os/journal/` and a goals section to `CONTEXT.md`.

**Action:** Create a simple journal skill and update `CONTEXT.md` with active goals.

### 5.3 Memory Vault Search
**His setup:** Obsidian vault with full-text search.  
**Our setup:** Make `~/agent-os/` searchable via terminal script or Obsidian.

**Action:** Add a search script for `~/agent-os/`.

### 5.4 Morning Briefing
**His setup:** 7:00 AM summary of community activity + personal context.  
**Our setup:** Already running. Enhance it with journal review + goal progress.

**Action:** Update daily cron to read `CONTEXT.md` and recent journal entries.

### 5.5 Weekly Audit
**His setup:** Weekly review of what's working.  
**Our setup:** New weekly cron job.

**Action:** Create `weekly-audit` skill.

### 5.6 Skill Evolution
**His setup:** Skill Claw auto-improves skills from session data.  
**Our setup:** After each experiment, update skills based on what worked.

**Action:** Add a "skill retrospective" step to every experiment.

---

## 6. How to Recreate Our Own Version

### Phase 1: Install Claude Code (Optional Executor)
```bash
# Install Claude Code via Anthropic
npm install -g @anthropic-ai/claude-code

# Run in a project
claude-code
```
- Use as a sub-agent when Hermes needs heavy coding execution.
- Keep GLM/Z.AI as primary to control costs.

### Phase 2: Add Journal + Goals to Agent OS
Create:
- `~/agent-os/journal/YYYY-MM-DD.md`
- `~/agent-os/GOALS.md` with quarterly goals and progress bars

Update `CONTEXT.md` to link to active goals.

### Phase 3: Make Agent OS Searchable
Create a search script:
```bash
python3 ~/agent-os/tools/search-os.py "keyword"
```

This searches all markdown files in `~/agent-os/`.

### Phase 4: Enhance Morning Briefing
Update cron job to:
1. Read `CONTEXT.md` and `GOALS.md`.
2. Read last 7 journal entries.
3. Pull AI news.
4. Suggest one action aligned with goals.

### Phase 5: Build Weekly Audit Skill
Every Monday:
1. Review completed experiments.
2. Review active goals progress.
3. Review mentor strategies.
4. Propose adjustments.

### Phase 6: Build Agent OS Dashboard (Later)
A simple React/Vercel dashboard showing:
- Active agents/status
- Active goals + progress
- Recent journal entries
- Recent builds/output
- Memory search

---

## 7. Immediate Next Steps

1. **Add `GOALS.md`** to `~/agent-os/`.
2. **Create journal skill** for daily voice/text entries.
3. **Create search script** for `~/agent-os/`.
4. **Enhance morning briefing** to include goals + journal context.
5. **Install Claude Code** as optional heavy executor.
6. **Create weekly audit skill**.

---

## 8. Key Takeaways

- The power is not one tool — it's **orchestration + memory + execution** working together.
- Hermes is the orchestrator. Claude Code (or our existing tools) is the executor.
- Memory vault is the moat — the longer it runs, the more personalized the system becomes.
- Daily journal + goals tracker keeps the system aligned with your priorities.
- Morning briefings and weekly audits create a self-improving loop.
- We should install Claude Code as an optional executor, but keep Hermes + GLM/Z.AI as the primary cost-effective stack.
