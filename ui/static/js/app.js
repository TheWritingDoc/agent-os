const log = (msg) => {
  const el = document.getElementById('live-log');
  el.textContent = `${new Date().toLocaleTimeString()} — ${msg}\n\n` + el.textContent;
};

const api = async (path, opts = {}) => {
  const res = await fetch(path, opts);
  return res.json();
};

// Navigation
for (const link of document.querySelectorAll('.nav-link')) {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    link.classList.add('active');
    document.getElementById(link.dataset.section).classList.add('active');
  });
}

// Dashboard
async function loadStatus() {
  const s = await api('/api/status');
  document.getElementById('status-cards').innerHTML = `
    <div class="card"><div class="value">${s.skills_count}</div><div class="label">Skills</div></div>
    <div class="card"><div class="value">${s.projects_count}</div><div class="label">Projects</div></div>
    <div class="card"><div class="value">${s.outputs_count}</div><div class="label">Outputs</div></div>
  `;
}

// Projects
async function loadProjects() {
  const projects = await api('/api/projects');
  document.getElementById('projects-list').innerHTML = projects.map(p => `
    <div class="list-item" onclick="viewProject('${p.id}')">
      <h4>${p.id}</h4>
      <p>${p.context.slice(0, 120).replace(/\n/g, ' ')}...</p>
    </div>
  `).join('');
}

function viewProject(id) {
  // Expand later; for now log
  log(`Selected project: ${id}`);
}

// Skills
async function loadSkills() {
  const skills = await api('/api/skills');
  document.getElementById('skills-list').innerHTML = skills.map(s => `
    <div class="list-item" onclick="runSkill('${s.id}')">
      <h4>${s.name}</h4>
      <p>${s.description}</p>
    </div>
  `).join('');
}

async function runSkill(skill) {
  log(`Running skill: ${skill}...`);
  const res = await api('/api/run/skill', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ skill })
  });
  log(`Skill ${skill} finished. Code: ${res.code}.\nStdout:\n${res.stdout.slice(0, 1000)}\nStderr:\n${res.stderr.slice(0, 500)}`);
  loadStatus();
}

// Experiments
async function runExperiment(experiment, script, args = []) {
  log(`Running experiment: ${experiment}/${script}...`);
  const res = await api('/api/run/experiment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ experiment, script, args })
  });
  log(`Experiment finished. Code: ${res.code}.\nStdout:\n${res.stdout.slice(0, 2000)}\nStderr:\n${res.stderr.slice(0, 500)}`);
  loadOutputs();
}

// Journal
async function loadJournal() {
  const date = document.getElementById('journal-date').value;
  if (!date) return;
  const j = await api(`/api/journal/${date}`);
  document.getElementById('journal-content').textContent = j.content;
}

// Outputs
async function loadOutputs() {
  const outputs = await api('/api/outputs');
  document.getElementById('outputs-list').innerHTML = outputs.map(o => `
    <div class="list-item" onclick="viewOutput('${o.name}')">
      <h4>${o.name}</h4>
      <p>${new Date(o.mtime * 1000).toLocaleString()}</p>
    </div>
  `).join('');
}

async function viewOutput(name) {
  const o = await api(`/api/output/${name}`);
  document.getElementById('output-content').textContent = JSON.stringify(o, null, 2);
}

// Goals
async function loadGoals() {
  const g = await api('/api/goals');
  document.getElementById('goals-editor').value = g.content;
}

async function saveGoals() {
  const content = document.getElementById('goals-editor').value;
  await api('/api/save/goals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content })
  });
  log('Goals saved.');
}

// Init
document.getElementById('journal-date').valueAsDate = new Date();
loadStatus();
loadProjects();
loadSkills();
loadOutputs();
loadGoals();
