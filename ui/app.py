#!/usr/bin/env python3
"""
Agent OS Web UI — centralized command center for tools, skills, goals, and experiments.
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
SKILLS_DIR = HOME / ".hermes" / "skills" / "productivity"
OUTPUT_DIR = AGENT_OS / "output"
JOURNAL_DIR = AGENT_OS / "journal"
CONFIG_DIR = AGENT_OS / "config"
OBSIDIAN_VAULT = Path("/mnt/c/Users/MSI CYBORG/Documents/Obsidian Vault")

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
        # JSON or other -> wrap in markdown
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
                if sys.platform.startswith("win") or "/mnt/c/" in cmd:
                    # Use wslview or direct Windows executable
                    subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {"ok": True, "type": "launch", "command": cmd}
            return {"ok": False, "error": "tool has no url or command"}
    return {"ok": False, "error": "tool not found"}


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
        "tools_count": len(load_tools()),
    })


@app.route("/api/skills")
def skills():
    return jsonify(list_skills())


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
        # Assume output file
        path = sync_output_to_obsidian(name)
        if path:
            return jsonify({"ok": True, "path": path, "type": "output"})
        return jsonify({"ok": False, "error": "output not found"}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


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
