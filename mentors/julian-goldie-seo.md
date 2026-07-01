# Julian Goldie SEO — Operational Map

**Channel:** https://www.youtube.com/@JulianGoldieSEO  
**Focus:** AI SEO automation, Agent OS, team-of-agents workflow  
**Why we track him:** He has built a practical, non-technical "Agent OS" that automates content, SEO, and publishing.

---

## 1. Core Systems to Steal

### 1.1 Agent OS Architecture
- Multiple AI agent profiles working as a team.
- Roles: researcher, writer, video producer, judge/critic.
- Tasks enter a Kanban triage board.
- Judge reviews output before shipping.
- Agents share memory (brand, voice, goals, tools).

**Our mapping:**
- Use Hermes skills as agent profiles.
- Use cron jobs for recurring tasks.
- Use `~/agent-os/` as shared workspace/memory.
- Use a Judge skill as quality gate.

### 1.2 WordPress Oracle
- Agent logs into WordPress.
- Researches topic based on latest news.
- Writes article with internal/external links.
- Formats and publishes directly.
- Submits for indexing.

**Our mapping:**
- For WordPress sites: use WordPress REST API.
- For Vercel sites: generate MDX/HTML pages and commit to repo.
- For Sebenza: auto-generate job descriptions with SEO metadata.
- For Rugby app: auto-generate match recap pages.

### 1.3 Loop Engineering
- Fork conversation, add feature, keep iterating.
- Self-improving system that gets better daily.

**Our mapping:**
- After each experiment, update `CONTEXT.md` and skill files.
- Use git commits to snapshot iterations.
- Review what worked/didn't and feed back into next cycle.

### 1.4 Goal Mode
- Set a goal and target, walk away.
- Agent executes without constant prompting.

**Our mapping:**
- Define goals in `~/agent-os/inbox/`.
- Cron jobs or skills read goals and execute workflows.
- Judge reviews before final action.

---

## 2. Technologies He Uses

| His Tool | Our Equivalent | Status |
|----------|----------------|--------|
| Hermes Agent | Hermes Agent | ✅ Active |
| Claude Desktop | Hermes + Z.AI/GLM | ✅ Active |
| WordPress | WordPress REST API / Vercel MDX | 🔄 To integrate |
| Open Montage (video) | Image/video gen tools | ⏳ Later |
| Kanban board | Hermes todo + cron jobs | 🔄 Building |
| Shared memory | `CONTEXT.md` + Hermes memory | 🔄 Building |

---

## 3. Implementation Queue

| Priority | Tactic | Project | Status |
|----------|--------|---------|--------|
| 1 | Daily AI news + mentor brief | Agent OS | ✅ Running |
| 2 | Judge skill / quality gate | Agent OS | ⏳ Pending |
| 3 | SEO content agent | Sebenza / Rugby / new site | ⏳ Pending |
| 4 | WordPress/Vercel publishing automation | Agent OS | ⏳ Pending |
| 5 | Multi-agent Kanban workflow | Agent OS | ⏳ Pending |

---

## 4. Notes

- He emphasizes he is non-technical — systems are built by iterating with AI, not coding from scratch.
- His community is "AI Profit Boardroom" — paid community with shared templates.
- Key phrase: "set a goal, set a target, and walk away."
