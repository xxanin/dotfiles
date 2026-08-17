#!/Users/xanin/dotfiles/newsboat/scripts/.venv/bin/python

import urllib.request
import urllib.error
from xml.sax.saxutils import escape
import sys
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0"><channel><item><title>Error</title><description>Please install BeautifulSoup: pip install beautifulsoup4</description></item></channel></rss>')
    sys.exit(1)

PL_MONTHS = {
    'stycznia': 'Jan', 'lutego': 'Feb', 'marca': 'Mar', 'kwietnia': 'Apr',
    'maja': 'May', 'czerwca': 'Jun', 'lipca': 'Jul', 'sierpnia': 'Aug',
    'września': 'Sep', 'października': 'Oct', 'listopada': 'Nov', 'grudnia': 'Dec'
}

PAGE_URL = "https://it.pracuj.pl/praca/react;kw/praca%20zdalna;wm,home-office?et=4&sc=0&its=frontend%2Cfullstack"

req = urllib.request.Request(
    PAGE_URL, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
    }
)

error_msg = None
html_content = ""

try:
    with urllib.request.urlopen(req) as response:
        html_content = response.read().decode('utf-8')
except urllib.error.HTTPError as e:
    error_msg = f"HTTP Error {e.code}: {e.reason}"
except Exception as e:
    error_msg = f"Error: {str(e)}"

print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<rss version="2.0"><channel>')
print('<title>Pracuj.pl - Remote React Jobs</title>')
print('<link>https://it.pracuj.pl</link>')
print('<description>Parsed HTML feed of Pracuj.pl</description>')

if error_msg:
    print("  <item>")
    print(f"    <title>Fetch Error: {escape(error_msg)}</title>")
    print(f"    <link>{escape(PAGE_URL)}</link>")
    print(f"    <description>Could not fetch the HTML page. {escape(error_msg)}</description>")
    print("  </item>")
else:
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Target the job card wrappers directly (this includes both regular and promoted jobs)
    job_cards = soup.find_all('div', attrs={'data-test': lambda x: x in ['default-offer', 'positioned-offer']})
    
    seen_slugs = set()
    matched_count = 0
    
    for card in job_cards:
        # Extract the explicit job ID from the container attribute
        offer_id = card.get('data-test-offerid')
        if not offer_id:
            continue
            
        # Prevent duplicates from "Oferty wyróżnione"
        if offer_id in seen_slugs:
            continue
        seen_slugs.add(offer_id)
        
        # FIX 1: Extract the actual valid URL from the anchor tag
        link_node = card.find('a', attrs={'data-test': 'link-offer-title'}) or card.find('a', attrs={'data-test': 'link-offer'})
        if link_node and link_node.get('href'):
            href = link_node.get('href')
            item_link = href if href.startswith('http') else f"https://www.pracuj.pl{href}"
        else:
            item_link = PAGE_URL # fallback
        
        # Get title
        title_node = card.find(attrs={'data-test': 'offer-title'})
        item_title = title_node.get_text(strip=True) if title_node else "Unknown Title"
        
        # Get company
        company_node = card.find(attrs={'data-test': 'text-company-name'}) or \
                       card.find(attrs={'data-test': 'section-company'})
        company = company_node.get_text(strip=True) if company_node else "Unknown Company"
        
        rss_title = f"{item_title} @ {company}" if company != "Unknown Company" else item_title
        
        # Get description / raw text
        raw_text = card.get_text(separator=' | ', strip=True)
        
        # FIX 2: Target the specific date paragraph to avoid HTML comment separator issues
        pub_date_str = ""
        date_node = card.find(attrs={'data-test': 'text-added'})
        if date_node:
            date_text = date_node.get_text(separator=' ', strip=True)
            # Find the date pattern strictly: DD Month YYYY
            date_match = re.search(r'(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})', date_text, re.IGNORECASE)
            
            if date_match:
                day = date_match.group(1).zfill(2)
                month_pl = date_match.group(2).lower()
                year = date_match.group(3)
                
                month_en = PL_MONTHS.get(month_pl, 'Jan') 
                pub_date_str = f"{day} {month_en} {year} 00:00:00 GMT"
            
        matched_count += 1
        
        print("  <item>")
        print(f"    <title>{escape(rss_title)}</title>")
        print(f"    <link>{escape(item_link)}</link>")
        print(f"    <guid isPermaLink=\"false\">{escape(offer_id)}</guid>")
        if pub_date_str:
            print(f"    <pubDate>{escape(pub_date_str)}</pubDate>")
        print(f"    <description>{escape(raw_text)}</description>")
        print("  </item>")

    if matched_count == 0:
        print("  <item>")
        print(f"    <title>Debug: Found 0 jobs</title>")
        print(f"    <link>{escape(PAGE_URL)}</link>")
        print(f"    <description>Still returning 0 jobs after analyzing debug HTML.</description>")
        print("  </item>")

print('</channel></rss>')
