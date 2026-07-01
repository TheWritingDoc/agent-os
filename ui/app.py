#!/usr/bin/env python3
"""
Agent OS Web UI — centralized command center for tools, skills, goals, and projects.
Run: python3 app.py
Port: 4321 (or AGENT_OS_UI_PORT env var)
"""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, jsonify, request

HOME = Path.home()
AGENT_OS = HOME / "agent-os"
PROJECTS_DIR = AGENT_OS / "projects"
SKILLS_DIR = HOME / ".hermes" / "skills" / "productivity"
OUTPUT_DIR = AGENT_OS / "output"
JOURNAL_DIR = AGENT_OS / "journal"
CONFIG_DIR = AGENT_OS / "config"
OBSIDIAN_VAULT = Path("/mnt/c/Users/MSI CYBORG/Documents/Obsidian Vault")

app = Flask(__name__, template_folder=str(AGENT_OS / "ui" / "templates"), static_folder=str(AGENT_OS / "ui" / "static"))
port = int(os.environ.get("AGENT_OS_UI_PORT", "4321"))


def run_cmd(cmd, cwd=None, timeout=120):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, shell=isinstance(cmd, str))
    return {"code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def list_projects():
    projects = []
    if not PROJECTS_DIR.exists():
        return projects
    for d in sorted(PROJECTS_DIR.iterdir()):
        if d.is_dir():
            ctx_file = d / "context.md"
            goals_file = d / "goals.md"
            ctx = ctx_file.read_text(encoding="utf-8") if ctx_file.exists() else ""
            goals = goals_file.read_text(encoding="utf-8") if goals_file.exists() else ""
            projects.append({
                "id": d.name,
                "name": d.name.replace("-", " ").title(),
                "path": str(d),
                "context": ctx,
                "goals": goals,
                "updated": d.stat().st_mtime,
            })
    return projects


def list_skills():
    skills = []
    if not SKILLS_DIR.exists():
        return skills
    for d in sorted(SKILLS_DIR.iterdir()):
        skill_md = d / "SKILL.md"
        if skill_md.exists():
            text = skill_md.read_text(encoding="utf-8")
            name = d.name.replace("-", " ").title()
            desc = ""
            m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            if m:
                name = m.group(1).strip()
            m = re.search(r"description:\s*(.+)", text)
            if m:
                desc = m.group(1).strip()
            elif text:
                first_p = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#") and not line.startswith("-")]
                desc = first_p[0][:120] if first_p else ""
            scripts = sorted([str(p.relative_to(d)) for p in (d / "scripts").rglob("*") if p.is_file()]) if (d / "scripts").exists() else []
            skills.append({"id": d.name, "name": name, "description": desc, "scripts": scripts, "path": str(d)})
    return skills


def list_outputs():
    outputs = []
    if not OUTPUT_DIR.exists():
        return outputs
    for f in sorted(OUTPUT_DIR.iterdir(), reverse=True):
        if f.is_file():
            outputs.append({"name": f.name, "path": str(f), "mtime": f.stat().st_mtime})
    return outputs


def load_tools():
    tools_file = CONFIG_DIR / "tools.json"
    if not tools_file.exists():
        return []
    with open(tools_file, "r", encoding="utf-8") as f:
        return json.load(f).get("tools", [])


def ensure_obsidian_dirs():
    for sub in ["Agent OS", "Projects/Sebenza", "Projects/Rugby App", "Projects/AI Lab", "Journal", "Outputs"]:
        (OBSIDIAN_VAULT / sub).mkdir(parents=True, exist_ok=True)


def sync_markdown_to_obsidian(source_path, obsidian_subdir, filename):
    ensure_obsidian_dirs()
    dest_dir = OBSIDIAN_VAULT / obsidian_subdir
    dest = dest_dir / filename
    if source_path.endswith(".md"):
        shutil.copy2(source_path, dest)
    else:
        content = Path(source_path).read_text(encoding="utf-8")
        dest.write_text(f"# {filename}\n\n```json\n{content}\n```\n", encoding="utf-8")
    return str(dest)


def sync_goals_to_obsidian():
    ensure_obsidian_dirs()
    src = AGENT_OS / "GOALS.md"
    dest = OBSIDIAN_VAULT / "Agent OS" / "GOALS.md"
    if src.exists():
        shutil.copy2(src, dest)
    return str(dest)


def sync_journal_to_obsidian(date):
    ensure_obsidian_dirs()
    src = JOURNAL_DIR / f"{date}.md"
    dest = OBSIDIAN_VAULT / "Journal" / f"{date}.md"
    if src.exists():
        shutil.copy2(src, dest)
    else:
        dest.write_text(f"# Journal: {date}\n\nNo entry for this date.\n", encoding="utf-8")
    return str(dest)


def sync_output_to_obsidian(name):
    ensure_obsidian_dirs()
    src = OUTPUT_DIR / name
    if not src.exists():
        return None
    safe_name = name.replace(".", "_") + ".md"
    dest = OBSIDIAN_VAULT / "Outputs" / safe_name
    content = src.read_text(encoding="utf-8")
    dest.write_text(f"# Output: {name}\n\n```json\n{content}\n```\n", encoding="utf-8")
    return str(dest)


def launch_tool_command(tool_id):
    for tool in load_tools():
        if tool["id"] == tool_id:
            if tool.get("url"):
                return {"ok": True, "type": "url", "url": tool["url"]}
            if tool.get("command"):
                cmd = tool["command"]
                subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {"ok": True, "type": "launch", "command": cmd}
            return {"ok": False, "error": "tool has no url or command"}
    return {"ok": False, "error": "tool not found"}


@app.route("/")
def index():
    return render_template("index.html", port=port)


@app.route("/projects")
def projects_page():
    return render_template("projects.html", port=port)


@app.route("/tools")
def tools_page():
    return render_template("tools.html", port=port)


@app.route("/skills")
def skills_page():
    return render_template("skills.html", port=port)


@app.route("/experiments")
def experiments_page():
    return render_template("experiments.html", port=port)


@app.route("/journal")
def journal_page():
    return render_template("journal.html", port=port)


@app.route("/outputs")
def outputs_page():
    return render_template("outputs.html", port=port)


@app.route("/goals")
def goals_page():
    return render_template("goals.html", port=port)


@app.route("/api/status")
def status():
    return jsonify({
        "agent_os_path": str(AGENT_OS),
        "timestamp": datetime.now().isoformat(),
        "skills_count": len(list_skills()),
        "projects_count": len(list_projects()),
        "outputs_count": len(list_outputs()),
        "tools_count": len(load_tools()),
    })


@app.route("/api/tools")
def tools():
    return jsonify(load_tools())


@app.route("/api/launch/tool", methods=["POST"])
def launch_tool():
    data = request.get_json() or {}
    tool_id = data.get("tool")
    result = launch_tool_command(tool_id)
    if result["ok"]:
        return jsonify(result)
    return jsonify(result), 400


@app.route("/api/sync/obsidian", methods=["POST"])
def sync_obsidian():
    data = request.get_json() or {}
    name = data.get("name", "")
    try:
        if name == "goals":
            path = sync_goals_to_obsidian()
            return jsonify({"ok": True, "path": path, "type": "goals"})
        if name == "journal":
            date = data.get("date") or datetime.now().strftime("%Y-%m-%d")
            path = sync_journal_to_obsidian(date)
            return jsonify({"ok": True, "path": path, "type": "journal"})
        path = sync_output_to_obsidian(name)
        if path:
            return jsonify({"ok": True, "path": path, "type": "output"})
        return jsonify({"ok": False, "error": "output not found"}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/sync/project/obsidian", methods=["POST"])
def sync_project_obsidian():
    data = request.get_json() or {}
    project_id = data.get("project")
    if not project_id:
        return jsonify({"ok": False, "error": "missing project"}), 400
    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        return jsonify({"ok": False, "error": "project not found"}), 404
    try:
        ensure_obsidian_dirs()
        dest_dir = OBSIDIAN_VAULT / "Projects" / project_id.replace("-", " ").title().replace(" ", "-")
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in project_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, dest_dir / f.name)
        # Also copy project outputs related to this project
        project_outputs_dir = dest_dir / "outputs"
        project_outputs_dir.mkdir(exist_ok=True)
        return jsonify({"ok": True, "path": str(dest_dir), "type": "project"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/projects")
def projects():
    return jsonify(list_projects())


@app.route("/api/project/<project_id>")
def project_detail(project_id):
    for p in list_projects():
        if p["id"] == project_id:
            return jsonify(p)
    return jsonify({"error": "not found"}), 404


@app.route("/api/skills")
def skills():
    return jsonify(list_skills())


@app.route("/api/run/skill", methods=["POST"])
def run_skill():
    data = request.get_json() or {}
    skill = data.get("skill")
    if not skill:
        return jsonify({"error": "missing skill"}), 400
    skill_dir = SKILLS_DIR / skill
    if not skill_dir.exists():
        return jsonify({"error": "skill not found"}), 404
    scripts = data.get("scripts") or ["scripts/run.py"]
    if isinstance(scripts, str):
        scripts = [scripts]
    results = []
    for script in scripts:
        script_path = skill_dir / script
        if script_path.exists():
            res = run_cmd(["python3", str(script_path)], cwd=str(skill_dir))
            results.append({"script": script, **res})
    return jsonify(results[0] if len(results) == 1 else {"results": results})


@app.route("/api/run/experiment", methods=["POST"])
def run_experiment():
    data = request.get_json() or {}
    experiment = data.get("experiment")
    script = data.get("script")
    args = data.get("args", [])
    if not experiment or not script:
        return jsonify({"error": "missing experiment or script"}), 400
    script_path = AGENT_OS / "experiments" / experiment / "scripts" / script
    if not script_path.exists():
        return jsonify({"error": "script not found"}), 404
    cmd = ["python3", str(script_path)] + [str(a) for a in args]
    res = run_cmd(cmd, cwd=str(script_path.parent))
    return jsonify(res)


@app.route("/api/journal/<date>")
def journal(date):
    journal_file = JOURNAL_DIR / f"{date}.md"
    if journal_file.exists():
        return jsonify({"date": date, "content": journal_file.read_text(encoding="utf-8")})
    return jsonify({"date": date, "content": "No journal entry for this date."})


@app.route("/api/outputs")
def outputs():
    return jsonify(list_outputs())


@app.route("/api/output/<name>")
def output(name):
    output_file = OUTPUT_DIR / name
    if not output_file.exists():
        return jsonify({"error": "not found"}), 404
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            content = json.load(f)
        return jsonify(content)
    except Exception:
        return jsonify({"raw": output_file.read_text(encoding="utf-8")})


@app.route("/api/goals")
def goals():
    goals_file = AGENT_OS / "GOALS.md"
    if goals_file.exists():
        return jsonify({"content": goals_file.read_text(encoding="utf-8")})
    return jsonify({"content": ""})


@app.route("/api/save/goals", methods=["POST"])
def save_goals():
    data = request.get_json() or {}
    content = data.get("content", "")
    goals_file = AGENT_OS / "GOALS.md"
    goals_file.write_text(content, encoding="utf-8")
    return jsonify({"ok": True})


if __name__ == "__main__":
    print(f"Agent OS UI starting on http://localhost:{port}", flush=True)
    app.run(host="0.0.0.0", port=port, debug=False)
