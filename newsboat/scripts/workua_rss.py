#!/Users/xanin/dotfiles/newsboat/scripts/.venv/bin/python

import urllib.request
import urllib.error
from xml.sax.saxutils import escape
import re
from bs4 import BeautifulSoup

# Map Ukrainian months to English abbreviations for RSS <pubDate> standard (RFC 822)
UKR_MONTHS = {
    "січня": "Jan",
    "лютого": "Feb",
    "березня": "Mar",
    "квітня": "Apr",
    "травня": "May",
    "червня": "Jun",
    "липня": "Jul",
    "серпня": "Aug",
    "вересня": "Sep",
    "жовтня": "Oct",
    "листопада": "Nov",
    "грудня": "Dec",
}

PAGE_URL = "https://www.work.ua/jobs-remote-react/"

req = urllib.request.Request(
    PAGE_URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    },
)

error_msg = None
html_content = ""

try:
    with urllib.request.urlopen(req) as response:
        html_content = response.read().decode("utf-8")
except urllib.error.HTTPError as e:
    error_msg = f"HTTP Error {e.code}: {e.reason}"
except Exception as e:
    error_msg = f"Error: {str(e)}"

print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<rss version="2.0"><channel>')
print("<title>Work.ua - Remote React Jobs</title>")
print("<link>https://www.work.ua</link>")
print("<description>Parsed HTML feed of Work.ua</description>")

if error_msg:
    print("  <item>")
    print(f"    <title>Fetch Error: {escape(error_msg)}</title>")
    print(f"    <link>https://www.work.ua</link>")
    print(
        f"    <description>Could not fetch the HTML page. {escape(error_msg)}</description>"
    )
    print("  </item>")
else:
    soup = BeautifulSoup(html_content, "html.parser")

    job_nodes = soup.find_all("div", class_=lambda c: c and "job-link" in c.split())

    seen_slugs = set()
    matched_count = 0

    for node in job_nodes:
        h2_node = node.find("h2")
        if not h2_node:
            continue

        title_node = h2_node.find("a")
        if not title_node:
            continue

        href = title_node.get("href", "")
        item_link = href if href.startswith("http") else f"https://www.work.ua{href}"

        slug = item_link.strip("/").split("/")[-1]
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        item_title = title_node.get_text(strip=True)

        title_attr = title_node.get("title", "")
        pub_date_str = ""

        date_match = re.search(
            r"вакансія від (\d{1,2})\s+([^\s]+)\s+(\d{4})", title_attr, re.IGNORECASE
        )
        if date_match:
            day = date_match.group(1).zfill(2)
            month_ua = date_match.group(2).lower()
            year = date_match.group(3)

            month_en = UKR_MONTHS.get(month_ua, "Jan")
            pub_date_str = f"{day} {month_en} {year} 00:00:00 GMT"

        company = "Unknown Company"
        img_node = node.find(
            "img", class_=lambda c: c and "preview-img-logo" in c.split()
        )
        if img_node and img_node.get("alt"):
            company = img_node.get("alt").replace(" logo", "").strip()

        rss_title = (
            f"{item_title} @ {company}" if company != "Unknown Company" else item_title
        )

        desc_node = node.find("p", class_=lambda c: c and "ellipsis" in c)
        if desc_node:
            raw_text = desc_node.get_text(separator=" ", strip=True)
        else:
            raw_text = node.get_text(separator=" | ", strip=True)[:300]

        matched_count += 1

        print("  <item>")
        print(f"    <title>{escape(rss_title)}</title>")
        print(f"    <link>{escape(item_link)}</link>")
        print(f'    <guid isPermaLink="false">{escape(slug)}</guid>')
        if pub_date_str:
            print(f"    <pubDate>{escape(pub_date_str)}</pubDate>")
        print(f"    <description>{escape(raw_text)}</description>")
        print("  </item>")

    if matched_count == 0:
        print("  <item>")
        print(f"    <title>Debug: Found 0 jobs</title>")
        print(f"    <link>{escape(PAGE_URL)}</link>")
        print(
            f"    <description>The page loaded and BeautifulSoup parsed it, but no matching list items were found.</description>"
        )
        print("  </item>")

print("</channel></rss>")
