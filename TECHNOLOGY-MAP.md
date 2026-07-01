# Technology Map

**Purpose:** Map mentor systems to our tools, track integrations, and identify gaps.  
**Updated:** 2026-06-30

---

## 1. Our Stack vs Mentor Tools

| Capability | Julian Goldie | David Ondrej | Sean Kochel | Cyberflow10 | Our Tool | Status |
|------------|---------------|--------------|-------------|-------------|----------|--------|
| AI orchestration | Hermes Agent | TBD | TBD | TBD | Hermes Agent | ✅ |
| LLM backend | Claude + others | TBD | TBD | TBD | GLM/Z.AI (glm-5.2) + OpenRouter fallback | ✅ |
| Agent profiles | Multiple Hermes profiles | TBD | TBD | TBD | Hermes skills | 🔄 |
| Shared memory | Agent OS memory | TBD | TBD | TBD | `CONTEXT.md` + Hermes memory | 🔄 |
| Task queue / Kanban | Kanban board | TBD | TBD | TBD | Hermes todo + cron jobs | 🔄 |
| Judge / critic | Judge profile | TBD | TBD | TBD | Judge skill | ⏳ |
| Content generation | WordPress Oracle | TBD | TBD | TBD | SEO/content agent | ⏳ |
| Publishing | WordPress REST API | TBD | TBD | TBD | WordPress API / Vercel commits | ⏳ |
| Video generation | Open Montage | TBD | TBD | TBD | Image/video gen tools | ⏳ |
| Search/SEO | AI SEO workflows | TBD | TBD | TBD | SEO content agent | ⏳ |
| Deployment automation | Manual / team | TBD | TBD | TBD | Render API + Vercel CLI | ✅ |
| Code generation | Claude | TBD | TBD | TBD | Hermes coding tools | ✅ |
| Issue diagnosis | Agent OS | TBD | TBD | TBD | Debug assistant skill | ⏳ |

---

## 2. Integration Patterns

### Pattern A: Goal → Plan → Code → Deploy
**Source:** Julian Goldie Agent OS  
**Our version:**
1. Goal written to `~/agent-os/inbox/`
2. Strategist skill creates plan
3. Builder skill writes code or plan
4. Judge skill reviews
5. Deployer skill ships to Render/Vercel

### Pattern B: Research → Content → Publish → Index
**Source:** Julian Goldie WordPress Oracle  
**Our version:**
1. Researcher fetches news/trends
2. SEO/content agent writes optimized content
3. Publish to WordPress or Vercel
4. Submit for indexing (Google Indexing API or sitemap ping)

### Pattern C: Loop Engineering
**Source:** Julian Goldie  
**Our version:**
1. Ship small experiment
2. Measure result
3. Update `CONTEXT.md` and skills
4. Fork/iterate next version

---

## 3. Gap Analysis

| Gap | Impact | Priority | Plan |
|-----|--------|----------|------|
| No Judge skill | Low-quality output may ship | High | Build judge skill |
| No content agent | Can't auto-generate SEO content | High | Build SEO/content agent |
| No WordPress integration | Can't replicate WordPress Oracle | Medium | Add WordPress REST API skill |
| No multi-agent Kanban | Can't run team-of-agents workflow | Medium | Build Kanban workflow |
| No debug assistant | Issue diagnosis still manual | Medium | Build debug skill |
| No video generation pipeline | Can't replicate Open Montage | Low | Use image/video gen tools later |

---

## 4. Technology Decisions

| Decision | Rationale |
|----------|-----------|
| Use Hermes skills as agents | Already integrated, no new infra |
| Use markdown workspace | Simple, versionable, searchable |
| Use cron jobs for recurring tasks | Reliable, scheduled, observable |
| Use GLM/Z.AI as primary LLM | Already subscribed, cost-effective |
| Keep OpenRouter fallback | Resilience if Z.AI is down |
| Start with Sebenza/Rugby for content experiments | Existing projects, real data |

---

## 5. Tool Inventory

### Already Available
- Hermes Agent
- GLM/Z.AI API
- OpenRouter fallback
- Render API
- Vercel CLI
- GitHub
- Supabase
- MongoDB Atlas

### To Add
- Judge skill
- SEO/content agent
- WordPress REST API skill (if needed)
- Debug/issue diagnosis skill
- Multi-agent Kanban workflow
