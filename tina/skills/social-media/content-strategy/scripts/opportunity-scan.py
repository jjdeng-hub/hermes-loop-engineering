#!/usr/bin/env python3
"""Daily Opportunity Scan — Data Collection Script
Queries HN Algolia API for relevant topics, outputs structured JSON.
15 keyword groups covering AI + content creation + indie maker topics.
Designed as no_agent cron script feeding into LLM analysis cron job.

Usage: python3 /root/.hermes/scripts/opportunity-scan.py
Output: JSON to stdout with results sorted by points descending.

Cron: daily-opportunity-scan (c2528ec74d26), runs daily at 08:00
"""

import json, urllib.request, urllib.parse, sys
from datetime import datetime, timezone

TOPICS = [
    {"q": "AI content creator", "tags": "story", "category": "ai_content"},
    {"q": "AI video editor repurpose", "tags": "story", "category": "ai_content"},
    {"q": "AI writing tool", "tags": "story", "category": "ai_content"},
    {"q": "build in public creator", "tags": "story", "category": "indie"},
    {"q": "indie maker solopreneur", "tags": "story", "category": "indie"},
    {"q": "one person business AI", "tags": "story", "category": "indie"},
    {"q": "micro saas AI agent", "tags": "story", "category": "indie"},
    {"q": "AI agent workflow", "tags": "story", "category": "ai_tools"},
    {"q": "Hermes agent openclaw", "tags": "story", "category": "ai_tools"},
    {"q": "AI automation tool", "tags": "story", "category": "ai_tools"},
    {"q": "content marketing AI", "tags": "story", "category": "content_strategy"},
    {"q": "newsletter audience growth", "tags": "story", "category": "content_strategy"},
    {"q": "social media strategy creator", "tags": "story", "category": "content_strategy"},
    {"q": "Ask HN content creation", "tags": "story", "category": "ask_hn"},
    {"q": "Ask HN AI side project", "tags": "story", "category": "ask_hn"},
]

def query_hit(kw, tag="story", limit=10):
    params = {"query": kw, "tags": tag, "hitsPerPage": limit}
    url = f"https://hn.algolia.com/api/v1/search?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes-Scan/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return [h for h in data.get("hits", []) if h.get("points", 0) > 1]
    except Exception as e:
        print(f"  [error] {kw}: {e}", file=sys.stderr)
        return []

def main():
    all_results, seen_urls = [], set()
    for topic in TOPICS:
        for h in query_hit(topic["q"], topic["tags"]):
            url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
            if url in seen_urls:
                continue
            seen_urls.add(url)
            all_results.append({
                "title": h.get("title", ""), "url": url,
                "points": h.get("points", 0), "num_comments": h.get("num_comments", 0),
                "author": h.get("author", ""), "created_at": h.get("created_at", ""),
                "category": topic["category"], "matched_keyword": topic["q"],
                "object_id": h.get("objectID", ""),
                "hn_item_url": f"https://news.ycombinator.com/item?id={h.get('objectID','')}",
            })
    # Also fetch latest Ask HN
    try:
        ask_url = "https://hn.algolia.com/api/v1/search?tags=ask_hn&hitsPerPage=30&numericFilters=points>2"
        req = urllib.request.Request(ask_url, headers={"User-Agent": "Hermes-Scan/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            for h in json.loads(resp.read()).get("hits", []):
                title = h.get("title", "").lower()
                kws = ["content", "creator", "audience", "marketing", "side project",
                       "indie", "solo", "AI", "automation", "newsletter", "blog",
                       "build", "saas", "tool", "writer", "video", "social"]
                if any(kw in title for kw in kws):
                    url = f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
                    if url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append({
                            "title": h.get("title", ""), "url": url,
                            "points": h.get("points", 0), "num_comments": h.get("num_comments", 0),
                            "author": h.get("author", ""), "created_at": h.get("created_at", ""),
                            "category": "ask_hn_direct", "matched_keyword": "ask_hn_direct",
                            "object_id": h.get("objectID", ""), "hn_item_url": url,
                        })
    except Exception:
        pass
    output = {"scanned_at": datetime.now(timezone.utc).isoformat(),
              "total_items": len(all_results),
              "results": sorted(all_results, key=lambda x: x.get("points", 0), reverse=True)}
    json.dump(output, sys.stdout, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
