#!/Users/xanin/dotfiles/newsboat/scripts/.venv/bin/python

import urllib.request
import urllib.error
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup

PAGE_URL = "https://justjoin.it/job-offers/remote?experience-level=mid&working-hours=full-time&keyword=react&orderBy=DESC&sortBy=newest"

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
print("<title>JustJoin.it - Remote React Jobs</title>")
print("<link>https://justjoin.it</link>")
print("<description>Parsed SSR feed of JustJoin.it</description>")

if error_msg:
    print("  <item>")
    print(f"    <title>Fetch Error: {escape(error_msg)}</title>")
    print(f"    <link>https://justjoin.it</link>")
    print(
        f"    <description>Could not fetch the HTML page. {escape(error_msg)}</description>"
    )
    print("  </item>")
else:
    soup = BeautifulSoup(html_content, "html.parser")

    job_nodes = soup.find_all("li", attrs={"data-index": True})

    seen_slugs = set()
    matched_count = 0

    for node in job_nodes:
        title_node = node.find("a", class_="offer_list_offer_title_link")

        if not title_node:
            title_node = node.find("a", class_="offer-card")

        if not title_node:
            continue

        href = title_node.get("href", "")

        item_link = href if href.startswith("http") else f"https://justjoin.it{href}"

        slug = item_link.split("/")[-1]
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        item_title = title_node.get_text(strip=True)
        if not item_title or item_title == "":
            item_title = title_node.get("title", "Unknown Job").replace(
                "View offer ", ""
            )

        company = "Unknown Company"
        img_node = node.find("img", alt=True)
        if img_node and img_node.get("alt") != "missing":
            company = img_node.get("alt")

        rss_title = f"{item_title} @ {company}"

        raw_text = node.get_text(separator=" | ", strip=True)

        matched_count += 1

        print("  <item>")
        print(f"    <title>{escape(rss_title)}</title>")
        print(f"    <link>{escape(item_link)}</link>")
        print(f'    <guid isPermaLink="false">{escape(slug)}</guid>')
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
