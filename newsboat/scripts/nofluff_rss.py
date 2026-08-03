#!/Users/xanin/dotfiles/newsboat/scripts/.venv/bin/python

import feedparser
from xml.sax.saxutils import escape
import re

url = "https://nofluffjobs.com/rss"

keywords = re.compile(r"(react|next\.js|nextjs|front-?end|frontend|fullstack)", re.I)
location_re = re.compile(r"<b>Location:</b>\s*([^<]+)", re.I)

feed = feedparser.parse(url)

print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<rss version="2.0"><channel>')
print("<title>NoFluffJobs - Remote React Jobs</title>")
print("<link>https://nofluffjobs.com</link>")
print("<description>RSS feed of NoFluffJobs</description>")

for e in feed.entries:
    text = f"{e.title} {e.summary}"

    if not keywords.search(text):
        continue

    m = location_re.search(e.summary)
    location = m.group(1).strip().lower() if m else ""

    if (
        "remote" not in location
        and "poznań" not in location
        and "poznan" not in location
    ):
        continue

    print("  <item>")
    print(f"    <title>{escape(e.title)}</title>")
    print(f"    <link>{escape(e.link)}</link>")
    print(f'    <guid isPermaLink="false">{escape(e.id)}</guid>')
    print(f"    <description><![CDATA[{e.summary}]]></description>")
    if "published" in e:
        print(f"    <pubDate>{escape(e.published)}</pubDate>")
    print("  </item>")

print("</channel></rss>")
