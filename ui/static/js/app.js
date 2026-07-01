const log = (msg) => {
  const el = document.getElementById('live-log');
  if (!el) return;
  el.textContent = `${new Date().toLocaleTimeString()} — ${msg}\n\n` + el.textContent;
};

const api = async (path, opts = {}) => {
  const res = await fetch(path, opts);
  return res.json();
};

// Dashboard
async function loadStatus() {
  const s = await api('/api/status');
  const cards = document.getElementById('status-cards');
  if (cards) {
    cards.innerHTML = `
      <div class="card"><div class="value">${s.skills_count}</div><div class="label">Skills</div></div>
      <div class="card"><div class="value">${s.projects_count}</div><div class="label">Projects</div></div>
      <div class="card"><div class="value">${s.outputs_count}</div><div class="label">Outputs</div></div>
      <div class="card"><div class="value">${s.tools_count}</div><div class="label">AI Tools</div></div>
    `;
  }
}

// Tools
async function loadTools() {
  const tools = await api('/api/tools');
  const el = document.getElementById('tools-list');
  if (!el) return;
  el.innerHTML = tools.map(t => {
    const action = t.url
      ? `<a href="${t.url}" target="_blank" class="btn">Open Web</a>`
      : `<button class="btn" onclick="launchTool('${t.id}')">Launch</button>`;
    return `
      <div class="list-item tool-card">
        <div class="tool-header">
          <span class="tool-icon">${t.icon}</span>
          <h4>${t.name}</h4>
        </div>
        <p>${t.description}</p>
        <div class="tool-meta">Type: ${t.type}</div>
        ${action}
      </div>
    `;
  }).join('');
}

async function launchTool(toolId) {
  log(`Launching tool: ${toolId}...`);
  const res = await api('/api/launch/tool', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tool: toolId })
  });
  log(`Launch ${toolId}: ${res.ok ? 'OK' : 'FAILED'} — ${res.message || res.error || ''}`);
}

// Skills
async function loadSkills() {
  const skills = await api('/api/skills');
  const el = document.getElementById('skills-list');
  if (!el) return;
  el.innerHTML = skills.map(s => `
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
  const el = document.getElementById('outputs-list');
  if (!el) return;
  el.innerHTML = outputs.map(o => `
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

async function syncToObsidian(name) {
  log(`Syncing ${name} to Obsidian...`);
  const res = await api('/api/sync/obsidian', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  log(`Obsidian sync: ${res.ok ? 'OK' : 'FAILED'} — ${res.path || res.error || ''}`);
}

// Goals
async function loadGoals() {
  const g = await api('/api/goals');
  const editor = document.getElementById('goals-editor');
  if (editor) editor.value = g.content;
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
