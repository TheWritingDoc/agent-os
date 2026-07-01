# Agent OS Context

**Owner:** jason  
**Purpose:** Operational reference for improving AI setup, automation, and development workflows.  
**Updated:** 2026-06-30

---

## 1. Core Philosophy

- Mentors are **operational references**, not content to consume.
- Every mentor strategy must be mapped to a **tool, workflow, or automation** in our setup.
- Progress is measured by **capability gained**, not videos watched.
- Prefer small, shipped experiments over large plans.

---

## 2. Active Projects

| Project | Stack | Status | Primary Goal |
|---------|-------|--------|--------------|
| Sebenza | Node/Express, MongoDB, React, Vercel, Render | Active | Job/service marketplace |
| Rugby App | Supabase, React, PWA, Vercel | Active | Real-time rugby officiating + fan/coach experience |
| Agent OS | Hermes skills, cron, markdown | Building | Personal AI operating system |

---

## 3. Tech Stack

### Backend
- Node.js / Express
- MongoDB Atlas (Mongoose)
- Supabase (PostgreSQL, Auth, Realtime, Edge Functions)

### Frontend
- React 18
- Vite
- PWA

### Deployment
- Render (backend)
- Vercel (frontend)
- GitHub

### AI / LLM
- GLM/Z.AI subscription (`ZAI_API_KEY`)
- Model: `glm-5.2` via `https://open.bigmodel.cn/api/paas/v4/`
- OpenRouter fallback: `z-ai/glm-5.2`
- Hermes Agent

### Tools / Services
- Supabase Auth + RLS
- Vercel CLI
- Render API
- GitHub CLI
- Obsidian (notes/wiki)

---

## 4. Mentor Roster (Operational Mapping)

| Mentor | Channel | Focus | What We Steal |
|--------|---------|-------|---------------|
| Julian Goldie SEO | @JulianGoldieSEO | Agent OS, AI SEO automation, team-of-agents pattern | Agent roles, Kanban workflow, WordPress Oracle, loop engineering |
| David Ondrej | @DavidOndrej | TBD | TBD |
| Sean Kochel | @iamseankochel | TBD | TBD |
| Cyberflow10 | @cyberflow10 | TBD | TBD |

---

## 5. Decision Rules

1. **Test first, then recommend.**
2. **One repo per project.**
3. **Deploy early, deploy often.**
4. **No Docker, no Grok unless asked.**
5. **Prefer hosted services (Atlas, Vercel, Render, Supabase).**
6. **Keep it quick and easy.**
7. **Every experiment needs a metric.**
8. **Judge reviews before shipping.**

---

## 6. Automation Priorities

1. Daily AI news + mentor video tracking
2. SEO/content generation for projects
3. Automated testing and deployment
4. Error/issue diagnosis assistant
5. Code review / quality gate assistant

---

## 7. Known Issues / Patterns

- Render needs `trust proxy` + MongoDB connection options
- Vercel framework auto-detection can override `vercel.json`
- Git author must match GitHub account for CI deploys
- WSL paths with spaces need symlinks
- CSRF tokens required for Sebenza API testing

---

## 8. Success Metrics

- Morning brief delivered daily
- 2-3 mentor strategies adapted per month
- 1-2 automation experiments shipped per week
- Reduced time from idea to deployment
