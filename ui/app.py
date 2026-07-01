#!/usr/bin/env python3
"""
Agent OS Web UI — centralized command center for tools, skills, goals, and experiments.
Run: python3 app.py
Port: 4321 (or AGENT_OS_UI_PORT env var)
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, jsonify, request

HOME = Path.home()
AGENT_OS = HOME / "agent-os"
SKILLS_DIR = HOME / ".hermes" / "skills" / "productivity"
OUTPUT_DIR = AGENT_OS / "output"
JOURNAL_DIR = AGENT_OS / "journal"

app = Flask(__name__, template_folder=str(AGENT_OS / "ui" / "templates"), static_folder=str(AGENT_OS / "ui" / "static"))


def run_cmd(cmd, timeout=60):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "code": 1}


def list_skills():
    skills = []
    if not SKILLS_DIR.exists():
        return skills
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            md = (d / "SKILL.md").read_text(encoding="utf-8")
            name = re.search(r"^name:\s*(.+)$", md, re.M)
            desc = re.search(r"^description:\s*(.+)$", md, re.M)
            skills.append({
                "id": d.name,
                "name": name.group(1).strip() if name else d.name,
                "description": desc.group(1).strip() if desc else "",
                "path": str(d)
            })
    return skills


def list_projects():
    projects = []
    projects_dir = AGENT_OS / "projects"
    if not projects_dir.exists():
        return projects
    for d in sorted(projects_dir.iterdir()):
        if d.is_dir():
            ctx = d / "context.md"
            goals = d / "goals.md"
            projects.append({
                "id": d.name,
                "context": ctx.read_text(encoding="utf-8") if ctx.exists() else "",
                "goals": goals.read_text(encoding="utf-8") if goals.exists() else ""
            })
    return projects


def list_outputs():
    outputs = []
    if not OUTPUT_DIR.exists():
        return outputs
    for f in sorted(OUTPUT_DIR.iterdir(), reverse=True):
        if f.is_file():
            outputs.append({"name": f.name, "path": str(f), "mtime": f.stat().st_mtime})
    return outputs


@app.route("/")
def index():
    return render_template("index.html", port=port)


@app.route("/api/status")
def status():
    return jsonify({
        "agent_os_path": str(AGENT_OS),
        "timestamp": datetime.now().isoformat(),
        "skills_count": len(list_skills()),
        "projects_count": len(list_projects()),
        "outputs_count": len(list_outputs()),
    })


@app.route("/api/skills")
def skills():
    return jsonify(list_skills())


@app.route("/api/projects")
def projects():
    return jsonify(list_projects())


@app.route("/api/outputs")
def outputs():
    return jsonify(list_outputs())


@app.route("/api/journal/<date>")
def journal(date):
    path = JOURNAL_DIR / f"{date}.md"
    if path.exists():
        return jsonify({"date": date, "content": path.read_text(encoding="utf-8")})
    return jsonify({"date": date, "content": "No journal entry found."})


@app.route("/api/output/<path:name>")
def output_file(name):
    safe = os.path.basename(name)
    path = OUTPUT_DIR / safe
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return jsonify(data)
        except Exception:
            return jsonify({"raw": path.read_text(encoding="utf-8")})
    return jsonify({"error": "not found"}), 404


@app.route("/api/run/skill", methods=["POST"])
def run_skill():
    data = request.get_json() or {}
    skill = data.get("skill")
    args = data.get("args", [])
    script_dir = SKILLS_DIR / skill / "scripts"
    if not script_dir.exists():
        return jsonify({"error": "skill not found"}), 404
    scripts = [f for f in script_dir.iterdir() if f.is_file() and os.access(f, os.X_OK)]
    if not scripts:
        return jsonify({"error": "no executable script found"}), 404
    cmd = ["python3", str(scripts[0])] + args
    return jsonify(run_cmd(cmd, timeout=300))


@app.route("/api/run/experiment", methods=["POST"])
def run_experiment():
    data = request.get_json() or {}
    experiment = data.get("experiment")
    script = data.get("script")
    args = data.get("args", [])
    exp_script = AGENT_OS / "experiments" / experiment / "scripts" / script
    if not exp_script.exists():
        return jsonify({"error": "script not found"}), 404
    cmd = ["python3", str(exp_script)] + args
    return jsonify(run_cmd(cmd, timeout=360))


@app.route("/api/goals")
def goals():
    path = AGENT_OS / "GOALS.md"
    if path.exists():
        return jsonify({"content": path.read_text(encoding="utf-8")})
    return jsonify({"content": "No GOALS.md found."})


@app.route("/api/save/goals", methods=["POST"])
def save_goals():
    data = request.get_json() or {}
    content = data.get("content", "")
    path = AGENT_OS / "GOALS.md"
    path.write_text(content, encoding="utf-8")
    return jsonify({"ok": True})


port = int(os.environ.get("AGENT_OS_UI_PORT", "4321"))

if __name__ == "__main__":
    print(f"Agent OS UI starting on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
