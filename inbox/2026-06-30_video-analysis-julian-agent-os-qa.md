# Video Analysis: Julian Goldie — Agent OS Q&A

**URL:** https://www.youtube.com/watch?v=cBWgNXSf57c  
**Topic:** Answering community questions about building Agent Operating Systems with Hermes + Claude  
**Date analyzed:** 2026-06-30

---

## 1. What the Video Is Actually About

This is a Q&A video where Julian answers member questions about his "Agent OS" system. It is **not a step-by-step build tutorial** — it is a window into how his community is implementing and customizing the system.

Key themes that come through:
- Agent OS is a **customizable orchestration layer** for AI agents.
- People in his community are building real versions: on VPS, Mac Mini, local models, etc.
- He emphasizes **model-agnostic design**, **loop engineering**, **safety**, and **focus**.

---

## 2. Core Systems Mentioned

### 2.1 Paperclip — "Full Company of AI Agents"
- A feature/module inside his Agent OS.
- Agents work together 24/7 building things.
- Output appears in a workspace/build area.

**Our mapping:**
- This is the **multi-agent execution engine**.
- We can build it with Hermes `delegate_task` + cron jobs + a shared workspace.
- Each "agent" = a skill or a subagent with a specific role.

### 2.2 AI Agent Mastermind
- Agents talk to each other.
- When they come up with good ideas, they add them to a pipeline.
- Pipeline items can be built with "one single click."

**Our mapping:**
- This is an **idea-to-implementation pipeline**.
- We can build it as:
  - `inbox/` for raw ideas
  - `strategist` agent evaluates ideas
  - `builder` agent turns approved ideas into plans/code
  - `deployer` agent ships them

### 2.3 SEO Workflow / Client Tabs
- Plug in a keyword + case study.
- Generate SEO content.
- Deploy to multiple websites.
- Can add separate tabs per client.

**Our mapping:**
- Build an **SEO content generator skill**.
- Each "client" or "project" = a config file in `projects/`.
- Output goes to WordPress, Vercel, or markdown.

### 2.4 Local AI Integration
- Example: Qwen 32B running on Mac Mini M4 Pro.
- Local models plugged into Agent OS.
- Can preview builds inside the chat.
- Free, private, can run 24/7.

**Our mapping:**
- We already use GLM/Z.AI + OpenRouter.
- For local models, we could add Ollama/lm-studio later.
- Not urgent — hosted works for now.

### 2.5 Skill Safety Process
Julian gives a 3-step process for installing third-party skills safely:
1. Read the `SKILL.md` file yourself.
2. Give the skill to Claude/AI to check it.
3. Build your own customized version instead of installing the original.

**Our mapping:**
- This is exactly why we are **building our own skills** (`mentor-mirror`, future agents).
- We never blindly install external skills.
- We review every skill before using it.

### 2.6 Loop Engineering
- Builder agent states goal and defines "done."
- Separate judge agent checks output.
- If not done, judge gives feedback.
- Loops until task is complete.

**Our mapping:**
- This is our **Judge skill** but with iteration.
- Builder + Judge loop until quality threshold met.
- Can use different models for builder and judge.

### 2.7 Model Agnosticism / Antifragility
- Don't rely on one model.
- When Fable 5 was pulled, they added Chinchilla 5.2, Kimikato 7, local models.
- Own the system so model changes don't break you.

**Our mapping:**
- We already have GLM/Z.AI + OpenRouter fallback.
- We should design skills to be **model-agnostic** (use OpenAI-compatible APIs).
- Avoid tight coupling to one provider.

### 2.8 Obsidian Memory Galaxy
- Agent OS uses Obsidian as memory.
- Each Paperclip company/team can have its own Obsidian folder.
- Custom instructions tell agents which folder to use.

**Our mapping:**
- We already use `CONTEXT.md` + `~/agent-os/`.
- We can add Obsidian integration later if needed.
- For now, markdown workspace is sufficient.

### 2.9 N8N vs Agent OS
- N8N is good for beginners to learn workflow fundamentals.
- Agent OS is for people who already understand agents and want to skip to the powerful setup.

**Our mapping:**
- We are skipping N8N.
- We build directly with Hermes skills + cron + code.

### 2.10 Agent OS Update Process
- The system comes as a zip file with an `update.md` file.
- Daily updates are applied via the update instructions.

**Our mapping:**
- We will version-control our Agent OS in GitHub.
- Updates = git pull or skill patches.
- No zip files needed.

---

## 3. Technologies Mentioned in the Video

| His Tool | Purpose | Our Equivalent | Status |
|----------|---------|----------------|--------|
| Hermes Agent | AI agent environment | Hermes Agent | ✅ |
| Claude / Codex / GPT-5 | Coding agent | Hermes + GLM/Z.AI | ✅ |
| VPS (Hostinger) | Host Agent OS | Our local/Render/Vercel setup | ✅ |
| Paperclip | Team of agents building 24/7 | `delegate_task` + cron + workspace | 🔄 |
| AI Agent Mastermind | Agents generate ideas → pipeline | inbox → strategist → builder | 🔄 |
| SEO Workflow | Keyword → case study → content → deploy | SEO/content agent skill | ⏳ |
| Open Design | AI design tool | Image gen / design tools | ⏳ |
| Grok Build | AI coding tool | External, not needed | ⏳ |
| GLM 5.2 | LLM | GLM/Z.AI | ✅ |
| Local models (Qwen 32B, North Mini Code) | Private local AI | Ollama / lm-studio later | ⏳ |
| Obsidian | Agent memory | `~/agent-os/` markdown + Obsidian skill | 🔄 |
| N8N | Beginner workflow tool | Skipping | ⏭️ |
| OpenRouter Fusion | Multi-agent + judge fusion | Our loop engineering + multi-model | 🔄 |

---

## 4. How to Recreate Our Own Version

### Phase 1: Core Agent OS Shell (Already Done)
- ✅ `~/agent-os/` workspace
- ✅ `CONTEXT.md` shared memory
- ✅ Mentor maps
- ✅ Technology map
- ✅ Progress tracker
- ✅ AI Tools Command Center

### Phase 2: Paperclip — Multi-Agent Build Engine
**Goal:** Agents working together to build things automatically.

**Implementation:**
1. Define agent roles:
   - `researcher` — finds opportunities
   - `strategist` — picks what to build
   - `builder` — writes code/plans
   - `judge` — reviews output
   - `deployer` — ships to Render/Vercel
2. Create a shared queue in `~/agent-os/inbox/`.
3. Use `delegate_task` to run agents in parallel when possible.
4. Store all outputs in `~/agent-os/output/`.
5. Use `cronjob` to trigger the loop every hour or daily.

**First experiment:**
- Drop one goal into inbox.
- Run researcher → strategist → builder → judge → deployer loop manually.
- Document what works.

### Phase 3: AI Agent Mastermind — Idea Pipeline
**Goal:** Agents generate ideas and add them to a build pipeline.

**Implementation:**
1. Researcher scans AI news + mentor videos.
2. Strategist extracts 2-3 ideas per week.
3. User approves or rejects ideas.
4. Approved ideas move to `inbox/` as goals.
5. Builder/Deployer loop executes.

**First experiment:**
- Enhance daily cron job to suggest one experiment per day.
- User replies "go" to trigger the pipeline.

### Phase 4: SEO Workflow / Client Tabs
**Goal:** Generate SEO content for multiple projects/clients.

**Implementation:**
1. Create project configs in `~/agent-os/projects/<project>/seo-config.md`.
2. SEO agent reads config + keyword + case study.
3. Generates article with metadata.
4. Publishes to:
   - WordPress (if site exists) via REST API
   - Vercel (as new page/MDX) via git commit
   - Markdown output for manual review
5. Tracks results in progress tracker.

**First experiment:**
- Pick one project (Sebenza or Rugby).
- Generate 1 SEO-optimized page.
- Publish and measure organic impressions.

### Phase 5: Loop Engineering with Judge
**Goal:** Builder + Judge iterate until quality threshold is met.

**Implementation:**
1. Builder agent produces output.
2. Judge agent checks against checklist.
3. If failed, Judge gives feedback.
4. Builder revises.
5. Loop max 3-5 iterations.
6. If passed, move to deploy.

**First experiment:**
- Use loop engineering for the SEO content agent.
- Builder writes draft → Judge reviews → Builder revises.

### Phase 6: Model Agnostic Setup
**Goal:** Not tied to one LLM provider.

**Implementation:**
1. Create a thin LLM wrapper skill.
2. Primary: GLM/Z.AI
3. Fallback: OpenRouter
4. Optional future: local models via Ollama
5. All agent skills call the wrapper, not the provider directly.

**First experiment:**
- Refactor one skill to use the wrapper.

### Phase 7: Dashboard / Mission Control
**Goal:** Visual overview of agents, tasks, builds, and status.

**Implementation:**
1. Build a simple web dashboard (React/Vite).
2. Reads from `~/agent-os/` markdown files.
3. Shows:
   - Active goals
   - Recent builds
   - Agent status
   - Mentor strategy queue
4. Host on Vercel.

**First experiment:**
- Build a read-only dashboard showing current `inbox/` and `output/`.

---

## 5. Immediate Next Steps

1. **Build Judge skill** with loop engineering.
2. **Build SEO/content agent** for first experiment.
3. **Enhance daily cron** to suggest one daily experiment.
4. **Run first Paperclip-style loop** on one goal.
5. **Add LLM wrapper skill** for model agnosticism.

---

## 6. Key Takeaways

- Agent OS is an **orchestration layer**, not a single tool.
- The power comes from **customization** — one dashboard, many agents, many workflows.
- **Model agnosticism** and **loop engineering** make the system antifragile.
- **Safety:** read skills, get AI to check them, build your own version.
- Start with **one workflow** (e.g., SEO), then expand.
