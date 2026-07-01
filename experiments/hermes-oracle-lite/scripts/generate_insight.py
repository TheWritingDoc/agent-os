#!/usr/bin/env python3
"""
Generate a short insight/post from news, with judge retry loop.
Usage:
  python3 generate_insight.py --project sebenza --news-file ~/agent-os/output/hermes-oracle-news.json
"""
import argparse, json, os, subprocess, sys
from datetime import datetime

VAULT = os.path.expanduser("~/agent-os")
JOURNAL = os.path.join(VAULT, "journal")
ROUTER = os.path.expanduser("~/.hermes/skills/productivity/llm-router/scripts/route.py")
JUDGE = os.path.expanduser("~/.hermes/skills/productivity/judge/scripts/judge.py")

PASS_THRESHOLD = 7.0


def load_context(project):
    ctx_path = os.path.join(VAULT, "projects", project, "context.md")
    goals_path = os.path.join(VAULT, "projects", project, "goals.md")
    parts = []
    for p in [ctx_path, goals_path]:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                parts.append(f.read())
    return "\n---\n".join(parts)


def load_news(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def route(prompt, task, project):
    result = subprocess.run(
        ["python3", ROUTER, "--prompt", prompt, "--task", task, "--project", project, "--output-format", "text"],
        capture_output=True, text=True, timeout=240
    )
    try:
        data = json.loads(result.stdout)
        return data.get("output", "")
    except Exception:
        return ""


def judge(artifact, criteria, project):
    result = subprocess.run(
        ["python3", JUDGE, "--artifact", artifact, "--criteria", criteria, "--project", project],
        capture_output=True, text=True, timeout=240
    )
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"score": 0, "pass": False, "critique": "Judge failed", "improvements": []}


def generate_insight(item, project):
    context = load_context(project)
    prompt = f"""Project context:
{context}

News item:
Title: {item['title']}
Link: {item['link']}
Description: {item['description']}

Task: Write a short LinkedIn-style insight (2-3 sentences) explaining why this news matters for the project.
Rules:
- Must be directly relevant to the project's current goals.
- Must be clear and shareable.
- Must end with the link.
- Avoid forced analogies.
"""
    return route(prompt, "creative", project)


def save_to_journal(project, insight, item, score):
    os.makedirs(JOURNAL, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(JOURNAL, f"{today}.md")
    entry = f"\n## [{project.upper()}] Hermes Oracle Insight (score: {score})\n\n{insight}\n\nSource: [{item.get('title')}]({item.get('link')})\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
    return path


def try_items(items, project, criteria):
    for item in items:
        insight = generate_insight(item, project)
        if not insight:
            continue
        verdict = judge(insight, criteria, project)
        score = verdict.get("score", 0)
        if score >= PASS_THRESHOLD:
            return item, insight, verdict
    # Return best attempt even if none passed
    best = None
    for item in items:
        insight = generate_insight(item, project)
        if not insight:
            continue
        verdict = judge(insight, criteria, project)
        if best is None or verdict.get("score", 0) > best[2].get("score", 0):
            best = (item, insight, verdict)
    return best or (None, None, {"score": 0, "pass": False, "critique": "No usable items"})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, choices=["sebenza", "rugby-app", "ai-lab"])
    parser.add_argument("--news-file", default=os.path.join(VAULT, "output", "hermes-oracle-news.json"))
    parser.add_argument("--criteria", default="relevant to project goals, clear, compelling, under 100 words, no forced analogies")
    args = parser.parse_args()

    data = load_news(args.news_file)
    items = data.get("items", [])
    if not items:
        print("No news items found.")
        return

    item, insight, verdict = try_items(items, args.project, args.criteria)
    if not insight:
        print("Could not generate any insight.")
        return

    score = verdict.get("score", 0)
    passed = score >= PASS_THRESHOLD

    journal_path = None
    if passed:
        journal_path = save_to_journal(args.project, insight, item, score)

    result = {
        "project": args.project,
        "news_item": item,
        "insight": insight,
        "verdict": verdict,
        "passed": passed,
        "journal_path": journal_path,
        "timestamp": datetime.now().isoformat()
    }

    os.makedirs(os.path.join(VAULT, "output"), exist_ok=True)
    out_path = os.path.join(VAULT, "output", f"{datetime.now().strftime('%Y-%m-%d')}_hermes-oracle-{args.project}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    print(f"\n{'PASSED' if passed else 'FAILED'} — score: {score}/10", file=sys.stderr)
    if journal_path:
        print(f"Saved to journal: {journal_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
