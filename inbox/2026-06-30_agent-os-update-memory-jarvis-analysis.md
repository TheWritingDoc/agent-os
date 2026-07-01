# Agent OS Update: Memory Galaxy, News Radar, Jarvis Takeover Engine

**Videos analyzed:**
1. `LSn7uFWwdFk` — Agent OS Q&A: keeping current, memory galaxy, news radar, model fusion, systems over models
2. `yVHLlnVz8Hk` — Hermes Computer Use / Takeover Engine on Windows, Linux, Mac

**Date:** 2026-06-30  
**Focus:** Operational improvements to our Agent OS.

---

## 1. New Systems Discovered

### 1.1 News Radar (24/7 Headlines)
**What Julian has:** A continuously running news radar that finds latest headlines so they never fall behind.

**Our version:**
- Already have daily morning brief cron.
- Upgrade to continuous monitoring: check RSS every 3-6 hours.
- Flag breaking stories above a relevance threshold.
- Surface them in morning brief + optionally alert via Telegram.

**Implementation:**
- Extend existing `mentor-mirror` skill.
- Add `news-radar` cron job every 3 hours.
- Store headline history in `~/agent-os/data/headlines.json`.
- Compare against previous run to detect new stories.

### 1.2 Memory Galaxy
**What Julian has:**
- Agents automatically update memory daily.
- All agents use it for context.
- Agents know who you are, your goals, your style.
- Stored in Obsidian vault.

**Our version:**
- `CONTEXT.md` is the start.
- Need daily memory updates: agent reads recent work and appends key facts.
- Use `fact_store` for structured memory.
- Use `memory` tool for high-signal facts.
- Create `memory-galaxy` skill that:
  1. Reads last 24h of work (terminal logs, files changed, output/).
  2. Extracts decisions, results, new tools, new goals.
  3. Updates `CONTEXT.md`, `fact_store`, `memory`.

**Key insight from video:** Memory should be automatic, not manual.

### 1.3 Update Agent OS Workflow
**What Julian has:**
- `update.md` markdown file in zip.
- `update-agent-os` command.
- Applies latest changes quickly.

**Our version:**
- Create `update-agent-os` skill.
- Reads `CHANGELOG.md` in `~/agent-os/`.
- Applies updates to skills, cron jobs, context files.
- Use git to version control `~/agent-os/` so updates are reversible.

### 1.4 Systems Over Models Mindset
**Quote from Alex (community member):** Instead of looking for one tool that does everything, design around specialized models, automation workflows, quality control layers.

**Julian's refinement:** It doesn't matter what Fable, Fusion, or Fugu can do. What matters is having a great system that automates every part of workflows in a quality-controlled way.

**Our takeaway:**
- Stop chasing models.
- Build interchangeable model slots.
- Focus on workflow design, quality control, and memory.

### 1.5 Token Management / Context Window Awareness
**Problem:** Free/small models hit token limits and output garbage.
**Solution:** Estimate tokens before API call; warn if prompt is too large.

**Our takeaway:**
- Add token estimation to LLM wrapper skill.
- For long transcripts/docs, chunk before sending.
- This is especially important for local models and free APIs.

### 1.6 Hermes Takeover Engine (Computer Use)
**What it does:**
- Hermes can control your computer.
- Works in background — your cursor doesn't move.
- Reads screen, clicks, types.
- Available on Mac, Windows, Linux.
- Two modes: auto (fast, basic) and agent (slower, more powerful).
- Stop button anytime.

**Use cases shown:**
- Open Obsidian, websites, apps.
- Write a note.
- Build stuff in background.

**Our assessment:**
- Powerful but potentially risky.
- Not a priority unless you need hands-free computer control.
- Could be useful for:
  - Opening project files.
  - Running local GUI apps.
  - Testing web apps visually.

**Implementation path:**
- Hermes has computer_use toolset.
- Test in a sandbox VM first.
- Start with safe actions: open browser, open Obsidian, take screenshot.
- Add approval gate before any write/click actions.

---

## 2. Refined Mental Models

### From "tools" to "systems"
| Old thinking | New thinking |
|--------------|--------------|
| Which model is best? | Which workflow is best? |
| Can this tool do X? | Can my system do X reliably? |
| One agent does everything | Specialized agents + quality control |
| I remember my workflows | Agent remembers via skills + memory |
| Manual updates | Auto-updating memory + changelog |

### Quality control layers
Every automated output should pass through:
1. Builder agent
2. Judge agent
3. Human approval (for high-stakes)
4. Memory update

---

## 3. Updated Implementation Priority

### Phase 0: Foundation ✅ DONE
- [x] `~/agent-os/` workspace
- [x] `CONTEXT.md`
- [x] Mentor maps
- [x] Technology map
- [x] Progress tracker
- [x] AI Tools Command Center
- [x] Daily morning brief

### Phase 1: Memory + Alignment (This Week)
- [ ] Create `GOALS.md`
- [ ] Create journal skill
- [ ] Create search script for `~/agent-os/`
- [ ] Build `memory-galaxy` skill (auto daily memory updates)
- [ ] Enhance morning brief with goals + journal + memory

### Phase 2: Quality + Execution (Next 2 Weeks)
- [ ] Build Judge skill with loop engineering
- [ ] Build LLM wrapper skill with token estimation
- [ ] Install Claude Code as optional executor
- [ ] Build weekly audit skill
- [ ] Build `update-agent-os` skill

### Phase 3: Content Automation (Next 2-4 Weeks)
- [ ] Build `hermes-oracle` skill
- [ ] Upgrade morning brief to 24/7 news radar
- [ ] Build `seo-content-agent`
- [ ] First experiment: publish SEO content from news

### Phase 4: Computer Use + Advanced (Later)
- [ ] Test Hermes computer_use toolset
- [ ] Build safe computer-use skill
- [ ] Multi-agent team orchestration
- [ ] Web dashboard

---

## 4. Recommended Immediate Build

The highest-leverage addition from these videos is the **Memory Galaxy** — automatic daily memory updates. This directly fixes the problem of "the agent forgets every session."

### `memory-galaxy` skill spec:

**Trigger:** Daily cron at 23:00 or on demand.

**Inputs:**
- `~/agent-os/journal/` entries from last 24h
- `~/agent-os/output/` files created
- `~/agent-os/inbox/` analysis files
- Recent terminal commands (from shell history if accessible)
- Recent git commits in tracked projects

**Outputs:**
- Updated `CONTEXT.md` (if significant changes)
- New entries in `fact_store`
- New entries in `memory`
- `~/agent-os/data/memory-log.md` audit trail

**Procedure:**
1. Collect recent activity.
2. Ask LLM: "What changed? What decisions were made? What should we remember?"
3. Extract 3-7 high-signal facts.
4. Check for conflicts with existing memory.
5. Update memory stores.
6. Log what was added/changed.

This makes the system learn from itself every day.

---

## 5. Key Takeaways

1. **Memory should be automatic.** Don't rely on manual updates.
2. **News radar > daily brief.** Continuous monitoring catches breaking trends.
3. **Systems > models.** Build interchangeable model slots and quality control.
4. **Token management matters.** Especially for free/local models.
5. **Computer use is powerful but risky.** Start small, sandbox first.
6. **Update workflow is essential.** Agent OS must be maintainable as it grows.

---

## 6. Next Action

Build the **Memory Galaxy skill** first.

Then we can enhance the morning brief to use it, and build the Oracle content engine on top.
