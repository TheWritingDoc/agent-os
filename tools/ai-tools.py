#!/usr/bin/env python3
"""
AI Tools Command Center CLI
Quick launcher for all AI tools and capabilities.

Usage:
    python3 ai-tools.py [--category CATEGORY] [--search QUERY]

Examples:
    python3 ai-tools.py                    # Show all tools
    python3 ai-tools.py --category dev     # Show dev tools only
    python3 ai-tools.py --search deploy    # Search tools
"""

import argparse
from datetime import datetime

TOOLS = {
    "orchestration": [
        {"name": "Hermes Agent", "use": "Main AI environment", "status": "active", "command": "This chat"},
        {"name": "Hermes Skills", "use": "Reusable workflows", "status": "active", "command": "skills_list, skill_view(name)"},
        {"name": "Cron Jobs", "use": "Scheduled automation", "status": "active", "command": "cronjob(action='list')"},
        {"name": "Subagents", "use": "Parallel task delegation", "status": "active", "command": "delegate_task(goal='...')"},
    ],
    "llm": [
        {"name": "GLM/Z.AI", "use": "Primary LLM (glm-5.2)", "status": "active", "command": "ZAI_API_KEY env"},
        {"name": "OpenRouter", "use": "Fallback LLM", "status": "active", "command": "z-ai/glm-5.2"},
    ],
    "dev": [
        {"name": "Terminal", "use": "Run shell commands", "status": "active", "command": "terminal(command='...')"},
        {"name": "Browser", "use": "Test web apps / scrape", "status": "active", "command": "browser_navigate, browser_snapshot"},
        {"name": "Patch", "use": "Precise file edits", "status": "active", "command": "patch(path='...', old_string='...', new_string='...')"},
        {"name": "Execute Code", "use": "Python + Hermes tools", "status": "active", "command": "execute_code(code='...')"},
        {"name": "GitHub", "use": "Repo / PR / issues", "status": "active", "command": "github-operations skill, gh CLI"},
    ],
    "deploy": [
        {"name": "Render", "use": "Backend hosting", "status": "active", "command": "render-deploy skill"},
        {"name": "Vercel", "use": "Frontend hosting", "status": "active", "command": "vercel --prod"},
        {"name": "Supabase", "use": "Managed backend", "status": "active", "command": "Supabase dashboard / CLI"},
        {"name": "MongoDB Atlas", "use": "Managed MongoDB", "status": "active", "command": "mongosh / connection string"},
    ],
    "media": [
        {"name": "YouTube Transcript", "use": "Extract video transcripts", "status": "active", "command": "python3 ~/.hermes/skills/media/media-tools/scripts/fetch_transcript.py <url>"},
        {"name": "Image Generation", "use": "Generate images", "status": "active", "command": "image_generate(prompt='...')"},
        {"name": "Text-to-Speech", "use": "Convert text to audio", "status": "active", "command": "text_to_speech(text='...')"},
        {"name": "Open Montage", "use": "AI video generation", "status": "pending", "command": "Install open source"},
    ],
    "research": [
        {"name": "Web Search", "use": "Find docs/news/examples", "status": "active", "command": "curl search engines / RSS"},
        {"name": "RSS Fetcher", "use": "Read feeds", "status": "active", "command": "Python urllib + xml.etree"},
        {"name": "Obsidian", "use": "Knowledge base", "status": "active", "command": "obsidian skill"},
    ],
    "external": [
        {"name": "Claude Code", "use": "Terminal AI coder", "status": "pending", "command": "Install Anthropic Claude Code"},
        {"name": "Claude Desktop", "use": "Desktop AI assistant", "status": "pending", "command": "Install Anthropic app"},
        {"name": "OpenClaw", "use": "AI coding tool", "status": "pending", "command": "External install"},
    ],
    "memory": [
        {"name": "Memory", "use": "Persistent user facts", "status": "active", "command": "memory(action='add')"},
        {"name": "Fact Store", "use": "Deep structured memory", "status": "active", "command": "fact_store(action='...')"},
        {"name": "Session Search", "use": "Search past chats", "status": "active", "command": "session_search(query='...')"},
    ],
}

STATUS_EMOJI = {
    "active": "✅",
    "pending": "⏳",
    "blocked": "❌",
}


def print_all():
    print(f"\n🤖 AI Tools Command Center — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    for category, tools in TOOLS.items():
        print(f"\n{'='*60}")
        print(f"📂 {category.upper()}")
        print('='*60)
        for tool in tools:
            print(f"  {STATUS_EMOJI.get(tool['status'], '⏳')} {tool['name']}")
            print(f"     Use: {tool['use']}")
            print(f"     Command: {tool['command']}\n")


def print_category(category):
    category = category.lower()
    if category not in TOOLS:
        print(f"Unknown category: {category}")
        print(f"Available: {', '.join(TOOLS.keys())}")
        return
    print(f"\n📂 {category.upper()}\n")
    for tool in TOOLS[category]:
        print(f"  {STATUS_EMOJI.get(tool['status'], '⏳')} {tool['name']}")
        print(f"     Use: {tool['use']}")
        print(f"     Command: {tool['command']}\n")


def search_tools(query):
    query = query.lower()
    print(f"\n🔍 Search results for: '{query}'\n")
    found = 0
    for category, tools in TOOLS.items():
        for tool in tools:
            text = f"{category} {tool['name']} {tool['use']} {tool['command']}".lower()
            if query in text:
                print(f"  {STATUS_EMOJI.get(tool['status'], '⏳')} [{category}] {tool['name']}")
                print(f"     Use: {tool['use']}")
                print(f"     Command: {tool['command']}\n")
                found += 1
    if not found:
        print("  No matching tools found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Tools Command Center")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--search", "-s", help="Search tools by keyword")
    args = parser.parse_args()

    if args.search:
        search_tools(args.search)
    elif args.category:
        print_category(args.category)
    else:
        print_all()
