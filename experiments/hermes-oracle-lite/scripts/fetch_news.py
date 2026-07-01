#!/usr/bin/env python3
"""
Fetch AI news from RSS feeds and filter for relevance.
Usage:
  python3 fetch_news.py --max 5
"""
import argparse, json, os, re
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import HTTPError

FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://www.theverge.com/rss/index.xml",
]

KEYWORDS = [
    "ai", "artificial intelligence", "agent", "llm", "model", "openai",
    "anthropic", "claude", "kimi", "glm", "job", "hiring", "rugby", "sports",
    "pwa", "supabase", "mongodb", "react", "vercel"
]

def fetch_feed(url):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as resp:
            return resp.read()
    except HTTPError as e:
        if e.code == 403:
            return None
        raise

def parse_rss(data):
    if data is None:
        return []
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []
    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        desc = item.findtext("description", default="")
        pub = item.findtext("pubDate", default="")
        items.append({"title": title, "link": link, "description": desc, "published": pub})
    return items

def score_relevance(item):
    text = (item["title"] + " " + item["description"]).lower()
    return sum(1 for kw in KEYWORDS if kw.lower() in text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=5)
    parser.add_argument("--output", default=os.path.expanduser("~/agent-os/output/hermes-oracle-news.json"))
    args = parser.parse_args()

    all_items = []
    for url in FEEDS:
        data = fetch_feed(url)
        all_items.extend(parse_rss(data))

    scored = [(score_relevance(i), i) for i in all_items]
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [item for score, item in scored[:args.max]]

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump({"fetched": datetime.now().isoformat(), "items": top}, f, indent=2)

    print(f"Saved {len(top)} items to {args.output}")

if __name__ == "__main__":
    main()
