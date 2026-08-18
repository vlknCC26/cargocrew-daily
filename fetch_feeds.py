import json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    ("Air Cargo News", "https://www.aircargonews.net/feed/"),
    ("The Loadstar", "https://theloadstar.com/feed/"),
    ("Air Cargo Week", "https://aircargoweek.com/feed/"),
    ("STAT Times", "https://www.stattimes.com/rss/latest-news"),
]
items = []
for name, url in FEEDS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (CargoCrewDailyWire)"})
        xml = urllib.request.urlopen(req, timeout=30).read()
        root = ET.fromstring(xml)
        for it in root.iter("item"):
            t = it.findtext("title") or ""
            l = it.findtext("link") or ""
            d = it.findtext("pubDate") or ""
            iso = None
            try: iso = parsedate_to_datetime(d).astimezone(timezone.utc).isoformat()
            except Exception: pass
            if t and l: items.append({"title": t.strip(), "link": l.strip(), "date": iso, "src": name})
    except Exception as e:
        print(name, "failed:", e)
items.sort(key=lambda x: x["date"] or "", reverse=True)
out = {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"), "items": items[:30]}
open("headlines.json", "w").write(json.dumps(out, ensure_ascii=False))
print("wrote", len(items), "headlines")
