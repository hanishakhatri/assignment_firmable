import re
import json
import gzip
import requests
from urllib.parse import urlparse
from collections import defaultdict
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm
from setting import DB_CONFIG, CC_DATA_PREFIX, USER_AGENT, INDUSTRY_KEYWORDS_ENHANCED
import psycopg2


def connect_postgres():
    return psycopg2.connect(**DB_CONFIG)


def get_base_domain(url):
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return url


def detect_primary_industry(text, company_name="", url=""):
    text_lower = text.lower()
    company_name_lower = company_name.lower() if company_name else ""
    url_lower = url.lower() if url else ""

    industry_scores = defaultdict(int)

    for industry, keywords in INDUSTRY_KEYWORDS_ENHANCED:
        industry_scores[industry] += sum(1 for kw in keywords['content'] if kw in text_lower)
        industry_scores[industry] += sum(1 for kw in keywords['company_name'] if kw in company_name_lower) * 3
        industry_scores[industry] += sum(1 for kw in keywords['company_name'] if kw in url_lower) * 2

    domain_indicators = {
        'healthcare': ['med', 'health', 'dental', 'clinic', 'hospital', 'doctor'],
        'finance': ['bank', 'finance', 'money', 'loan', 'insurance'],
        'education': ['edu', 'school', 'university', 'college', 'academy'],
        'technology': ['tech', 'it', 'software', 'digital', 'web', 'app'],
        'legal': ['law', 'legal', 'lawyer', 'solicitor'],
        'real_estate': ['realty', 'property', 'homes', 'estate'],
        'automotive': ['auto', 'car', 'motor', 'vehicle'],
        'food_beverage': ['cafe', 'restaurant', 'bar', 'food']
    }

    if url:
        try:
            domain = urlparse(url).netloc.replace('www.', '').split('.')[0]
            for industry, indicators in domain_indicators.items():
                if any(indicator in domain.lower() for indicator in indicators):
                    industry_scores[industry] += 5
        except:
            pass

    if industry_scores:
        best_industry = max(industry_scores.items(), key=lambda x: x[1])
        if best_industry[1] > 0:
            return best_industry[0]
    return 'Unknown'


def extract_au_domains():
    print("Filtering .au domains from CDX index files...")
    company_sites = defaultdict(list)

    for file in Path('.').glob("cdx-*.gz"):
        try:
            with gzip.open(file, 'rt') as f:
                for line in tqdm(f, desc=f"Parsing {file.name}"):
                    try:
                        parts = line.split(' ', 2)
                        if len(parts) < 3:
                            continue
                        surt, timestamp, data = parts
                        record = json.loads(data)

                        url = record.get('url', '')
                        mime = record.get('mime', '')
                        status = record.get('status', '')

                        if '.au' in url and mime == 'text/html' and status.startswith('200'):
                            base_url = get_base_domain(url)
                            if base_url not in company_sites:
                                company_sites[base_url].append(record)
                    except Exception as e:
                        print(f"Error parsing line in {file.name}: {e}")
        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    return list(company_sites.values())[:40]


def fetch_html(record):
    try:
        offset = int(record['offset'])
        length = int(record['length'])
        warc_url = f"{CC_DATA_PREFIX}{record['filename']}"
        byte_range = f"bytes={offset}-{offset+length-1}"
        headers = {'User-Agent': USER_AGENT, 'Range': byte_range}

        response = requests.get(warc_url, headers=headers, stream=True, timeout=10)
        if response.status_code == 206:
            for warc_record in ArchiveIterator(response.raw):
                if warc_record.rec_type == 'response':
                    return warc_record.content_stream().read()
        else:
            print(f"Unexpected response {response.status_code} for {warc_url}")
    except Exception as e:
        print(f"Error fetching WARC HTML: {e}")
    return None


def extract_info(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        title = soup.title.string.strip() if soup.title and soup.title.string else ''
    except:
        title = ''

    text = soup.get_text(separator=' ', strip=True).lower()

    if 'one moment' in text or 'just a moment' in text:
        return {'company_name': title, 'industry': 'Unknown'}

    parts = re.split(r'\||-|\u2013|,', title)
    parts = [p.strip() for p in parts if p.strip()]

    domain = urlparse(url).netloc.replace('www.', '').split('.')[0]
    domain_clean = domain.lower().replace('-', '').replace('_', '')

    company_name = ''
    for part in parts:
        if not re.search(r'\b(home|about|contact|support|welcome|page)\b', part, re.IGNORECASE):
            part_clean = part.lower().replace(' ', '').replace('-', '')
            if domain_clean in part_clean or part_clean in domain_clean:
                company_name = part
                break

    if not company_name and parts:
        company_name = parts[0]

    industry = detect_primary_industry(text, company_name, url)

    return {
        'company_name': company_name.strip('| ').strip(),
        'industry': industry
    }


def process_record(record):
    try:
        url = record["url"]
        base_url = get_base_domain(url)
        html = fetch_html(record)
        if html:
            info = extract_info(html, base_url)
            return {
                "Website": url,
                "Company Name": info["company_name"],
                "Industry": info["industry"]
            }
    except Exception as e:
        print(f"Error processing record: {e}")
    return None


def insert_commoncrawl_record(record, conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO commoncrawl_companies (
                    url, company_name, industry
                ) VALUES (%s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """, (
                record["url"],
                record["company_name"],
                record.get("industry")
            ))
        conn.commit()
    except Exception as e:
        print(f"Failed to insert {record['url']}: {e}")
        conn.rollback()