# Batch Synthesis: Paperclip Team OS, Deep Seek Speed Spec, Open Tag

**Videos analyzed (4):**
- `LJjZHIbe3vA` — Agent OS Q&A: project memory isolation, community wins, updates
- `O_irkwZoQw8` — **Paperclip + Hermes update**: org-chart team of agents
- `28XmQq0tj9U` — **Deep Seek D-Spark + Deep Spec**: speculative decoding + speed
- `aZYbn8vA6dg` — **Claude Tag / Open Tag**: shared channel agents, open-source version

**Date:** 2026-07-01  
**Focus:** Operational patterns to steal and adapt.

---

## 1. Pattern: Org-Chart Team of Agents (Paperclip)

**Source video:** `O_irkwZoQw8`

### What Paperclip is:
- Open-source, self-hosted app for managing a team of AI agents.
- You "hire" agents, give them roles/titles, they report to each other.
- Set a goal at the top; every task traces back to it.
- Model-agnostic: Claude, Codex, Gemini, Cursor, Hermes, OpenClaude.
- New update: agent **team chat** — agents talk to each other in threads.

### Why it matters:
- Mirrors a real company org chart.
- Agents can collaborate and hand off work.
- Reduces single-chat bottlenecks.
- Self-hosted = privacy + control.

### Our adaptation:
We can build the same thing inside Hermes without installing Paperclip:

```
Agent team structure:
- CEO / Strategist — sets goals, prioritizes
- Researcher — gathers info
- Builder — writes code/plans
- Marketer — content/SEO
- Judge — reviews output
- Deployer — ships to production

Workflow:
1. Strategist receives goal
2. Delegates research to Researcher
3. Builder gets research, creates output
4. Judge reviews and iterates with Builder
5. Deployer ships if approved
6. All agents log to shared memory
```

Use Hermes `delegate_task` with clear roles.
Use `~/agent-os/output/` as shared workspace.
Use `cronjob` for recurring team tasks.

### Skill to build:
`agent-team` skill — defines roles, routes tasks, runs loops.

---

## 2. Pattern: Project Memory Isolation

**Source video:** `LJjZHIbe3vA`

### What Julian says:
- Community member Andrew gives each project its own notes/brain/memory.
- Julian does the same: multiple projects/businesses inside the memory galaxy.
- Agents can tell projects apart because the vault is well-organized.
- Agents sync between projects automatically.

### Our adaptation:
- Structure `~/agent-os/projects/` with one folder per project.
- Each project has: `README.md`, `context.md`, `goals.md`, `output/`.
- Agent skills accept `--project` parameter.
- When working on a project, load its `context.md` + global `CONTEXT.md`.

### Folder structure:
```
~/agent-os/projects/
├── sebenza/
│   ├── README.md
│   ├── context.md
│   ├── goals.md
│   └── output/
├── rugby-app/
│   ├── README.md
│   ├── context.md
│   ├── goals.md
│   └── output/
└── ai-lab/
    ├── README.md
    ├── context.md
    ├── goals.md
    └── output/
```

---

## 3. Pattern: Speed via Speculative Decoding (Deep Seek D-Spark)

**Source video:** `28XmQq0tj9U`

### What it is:
- D-Spark is not a new model. It's a speed layer on top of Deep Seek V4.
- Uses **speculative decoding**.
- A small fast "helper" model guesses chunks of tokens.
- A big slow model verifies/rejects guesses in parallel.
- Result: 2-3x faster generation without quality loss.

### Deep Spec:
- Deep Seek also released a spec benchmark/specification system.
- Focus on standardizing AI specs/protocols.

### Why it matters:
- Speed unlocks real-time agents (voice, live collaboration).
- Local models become more usable.
- Lower latency = better UX for interactive agents.

### Our adaptation:
- We can't directly use D-Spark unless Deep Seek exposes it.
- But we can:
  - Prefer fast/cheap models for drafting.
  - Use strong models only for verification/final polish.
  - Build `draft-verify` pattern into agent workflows.
  - Cache common outputs to reduce generation.

### Pattern to adopt:
```
Draft agent (fast/cheap) → generates first pass
Verify agent (strong) → checks and fixes
Final agent (strong) → approves for shipping
```

---

## 4. Pattern: Shared Channel Agents (Claude Tag / Open Tag)

**Source video:** `aZYbn8vA6dg`

### What Claude Tag is:
- Anthropic launched shared Claude agents inside Slack channels.
- Team can tag Claude, assign tasks, watch progress.
- Claude remembers channel context.
- Can work proactively (watch channels, flag issues).

### What Open Tag is:
- Open-source alternative from Copilot Kit team.
- Works with any model: GPT-5, Gemini, Deep Seek, local models.
- Supports Slack, Teams, Discord, Telegram, WhatsApp, Google Chat.
- Fully custom agents.

### Why it matters:
- AI becomes a teammate in existing channels.
- Not a separate tool — embedded where work happens.
- Multi-platform.

### Our adaptation:
- We already use Telegram/Discord/WhatsApp with Hermes.
- Enhance these integrations so agents can:
  - Be tagged for tasks
  - Remember channel/project context
  - Post updates proactively
  - Hand off to other agents

### Skill to build:
`channel-agent` skill — handles tagged requests, routes to right agent, posts results.

---

## 5. Combined Insight: Speed + Team + Channel = Real-Time Agent OS

Putting these together:

```
User tags @agent in Telegram:
  ↓
Channel agent parses request + loads project context
  ↓
Team strategist prioritizes and delegates
  ↓
Researcher + builder work in parallel
  ↓
Judge reviews output
  ↓
Result posted back to channel
  ↓
Memory updated automatically
```

With faster models (D-Spark-style speculative decoding) this loop becomes near real-time.

---

## 6. Updated Architecture

```
┌─────────────────────────────────────┐
│ CHANNEL LAYER                       │
│ Telegram / Discord / Slack / WhatsApp
│ @agent tagging, proactive updates   │
├─────────────────────────────────────┤
│ TEAM ORCHESTRATION                  │
│ agent-team skill                    │
│ - CEO/Strategist                    │
│ - Researcher                        │
│ - Builder                           │
│ - Marketer                          │
│ - Judge                             │
│ - Deployer                          │
├─────────────────────────────────────┤
│ SPEED LAYER                         │
│ draft-verify pattern                │
│ fast model for draft                │
│ strong model for verify             │
│ caching for common outputs          │
├─────────────────────────────────────┤
│ MEMORY LAYER                        │
│ global CONTEXT.md                   │
│ project context.md per project      │
│ journal/ + output/                  │
│ fact_store + memory                 │
├─────────────────────────────────────┤
│ EXECUTION                           │
│ Hermes + GLM/Z.AI                   │
│ OpenRouter fallback                 │
│ Local models (future)               │
└─────────────────────────────────────┘
```

---

## 7. Updated Priority List

### Phase 0: Foundation ✅ DONE
### Phase 1: Memory + Alignment (This Week)
- [ ] Create `GOALS.md`
- [ ] Create journal skill
- [ ] Create search script
- [ ] Build infinite-context-engine skill
- [ ] Enhance morning brief with goals + journal + memory

### Phase 1b: Project Isolation
- [ ] Create `~/agent-os/projects/` structure
- [ ] Move Sebenza, rugby app, AI lab into project folders
- [ ] Add `--project` parameter to agent skills

### Phase 2: Quality + Multi-Agent (Next 2 Weeks)
- [ ] Build judge skill with loop engineering
- [ ] Build llm-wrapper with model switching + token estimation
- [ ] Build council-engine
- [ ] Build agent-team skill
- [ ] Weekly audit skill

### Phase 3: Automation + Channels (Next 2-4 Weeks)
- [ ] Build channel-agent skill
- [ ] Build hermes-oracle
- [ ] Build workflow-automation
- [ ] Build seo-content-agent

### Phase 4: Speed + Local (Later)
- [ ] Draft-verify pattern
- [ ] Local model integration
- [ ] Web dashboard

---

## 8. Key Takeaways

1. **Paperclip** proves org-chart teams of agents work. We can replicate this with `delegate_task`.
2. **Project memory isolation** is critical when running multiple businesses/projects.
3. **Speed matters** — speculative decoding and draft-verify patterns make agents feel real-time.
4. **Channel agents** embed AI where work already happens (Slack, Telegram, Discord).
5. **Open-source alternatives** keep us independent of any single vendor.
6. The future is not one chatbot. It's **teams of agents embedded in channels with shared memory**.
