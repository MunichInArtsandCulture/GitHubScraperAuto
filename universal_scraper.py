"""
Universal Art & Culture Job Scraper with Smart Markdown Extraction and LLM Categorization.
Reduces HTML to dense, token-efficient Markdown, extracts structured job listings,
and categorizes them for Telegram export.
"""

import os
import re
import sys
import json
import asyncio
import argparse
from urllib.parse import urljoin
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import requests
from bs4 import BeautifulSoup
import trafilatura
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram categories
CATEGORIES = [
    "Art, Artist Support and Event Management",
    "Musicians and Singers",
    "Education, Pedagogical and Social",
    "Stage and Event Technology",
    "Costume, Makeup and Fashion",
    "Acting, Theater and Directing",
    "Legal and Financial",
    "Communication, PR and Press",
    "IT and Digital",
    "Customer Service, Catering and Cash Register",
    "Other"
]

CATEGORY_DESCRIPTIONS = {
    "Art, Artist Support and Event Management": "Kuratoren, Eventmanagement, Künstlerbetreuung, Ausstellungsmanagement, Regieassistenz",
    "Musicians and Singers": "Musiker, Sänger, Orchestermitglieder, Dirigenten, Chor",
    "Education, Pedagogical and Social": "Museumspädagogik, Kulturelle Bildung, Vermittlung, Sozialarbeit, Workshops",
    "Stage and Event Technology": "Bühnentechnik, Beleuchtung, Tontechnik, Veranstaltungstechnik, Requisite",
    "Costume, Makeup and Fashion": "Maskenbildner, Kostümbildner, Schneiderei, Ankleider",
    "Acting, Theater and Directing": "Schauspieler, Tänzer, Regisseure, Dramaturgen, Soufflage",
    "Legal and Financial": "Verwaltung, Finanzen, Personal, Controlling, Justiziariat",
    "Communication, PR and Press": "Marketing, Presse- und Öffentlichkeitsarbeit, Social Media, Redaktion, Grafikdesign",
    "IT and Digital": "Softwareentwicklung, IT-Support, Systemadministration, Webentwicklung",
    "Customer Service, Catering and Cash Register": "Kasse, Einlass, Besucherservice, Gästebetreuung, Gastronomie",
    "Other": "Facility Management, Hausmeister, Reinigung, Fahrer, sonstige Dienstleistungen"
}

try:
    from curl_cffi import requests as c_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False
    import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


def fetch_url(url: str, timeout: int = 15) -> Optional[str]:
    """Fetch raw HTML with browser impersonation to bypass Cloudflare/bot protections."""
    try:
        if HAS_CURL_CFFI:
            response = c_requests.get(url, impersonate="chrome124", headers=DEFAULT_HEADERS, timeout=timeout)
        else:
            import requests
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"⚠️  [Fetch Error] {url}: {e}")
        return None


def clean_html_to_dense_markdown(html: str, base_url: str) -> str:
    """
    Strips noise, boilerplate (nav, footer, ads, scripts), converts links to absolute URLs,
    and returns dense Markdown to minimize LLM token count.
    """
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    # 1. Remove non-content tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "svg", "noscript", "iframe", "form"]):
        tag.decompose()

    # 2. Remove common cookie / modal / banner elements
    for element in soup.find_all(attrs={"class": re.compile(r"(cookie|banner|modal|popup|consent|overlay|menu|navbar)", re.I)}):
        element.decompose()
    for element in soup.find_all(attrs={"id": re.compile(r"(cookie|banner|modal|popup|consent|overlay|menu|navbar)", re.I)}):
        element.decompose()

    # 3. Normalize all links to absolute URLs
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("javascript:", "mailto:", "tel:", "#")):
            a.replace_with(a.get_text(strip=True))
            continue
        abs_url = urljoin(base_url, href)
        text = a.get_text(strip=True)
        if text:
            a.replace_with(f" [{text}]({abs_url}) ")
        else:
            a.decompose()

    # 4. Extract main content container if available
    main_container = soup.find("main") or soup.find("article") or soup.find(id=re.compile(r"(content|main|jobs|stellen)", re.I)) or soup.body
    if not main_container:
        main_container = soup

    raw_text = main_container.get_text(separator="\n")

    # 5. Hybrid with trafilatura if text is very large
    trafilatura_text = trafilatura.extract(
        html,
        url=base_url,
        include_links=True,
        include_formatting=True,
        output_format="txt"
    )

    selected_text = raw_text if (raw_text and len(raw_text) < 25000) else (trafilatura_text or raw_text)

    # 6. Compress whitespace & blank lines
    lines = [line.strip() for line in selected_text.splitlines() if line.strip()]
    dense_text = "\n".join(lines)
    dense_text = re.sub(r'\n{3,}', '\n\n', dense_text)

    # Cap to max 8,000 characters (~1,800 tokens) per site to keep costs ultra-low
    if len(dense_text) > 8000:
        dense_text = dense_text[:8000] + "\n\n...[content truncated]..."

    return dense_text


def extract_jobs_with_llm(
    markdown_content: str,
    source_name: str,
    source_url: str,
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini"
) -> List[Dict[str, str]]:
    """
    Sends dense markdown to OpenAI / LLM and extracts structured job postings.
    """
    if not markdown_content or len(markdown_content.strip()) < 30:
        return []

    key = api_key or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", None)

    if not key:
        print("⚠️  OPENAI_API_KEY is not set in environment or .env file.")
        return []

    import openai

    cat_list = "\n".join([f"- {k}: ({v})" for k, v in CATEGORY_DESCRIPTIONS.items()])

    system_prompt = f"""You are an expert cultural sector job parser for Munich, Germany.
Your task is to analyze raw markdown text from an art/culture organization's career page and extract all ACTIVE JOB VACANCIES.

Available Categories (select the most accurate one):
{cat_list}

RULES:
1. Extract ONLY actual job openings, internships, apprenticeships, or open calls mentioned in the text.
2. If there are NO open positions, return an empty array: []
3. Always resolve the link: use the exact job link from markdown if present; otherwise use the source URL '{source_url}'.
4. Default Employer: '{source_name}' (unless a specific institution is explicitly named).
5. Output format must be strictly valid JSON matching this schema:
[
  {{
    "title": "Job Title (e.g. Kurator:in, Bühnentechniker:in)",
    "employer": "Institution Name",
    "link": "Full URL to apply or view details",
    "category": "Exact Category Name from the list above"
  }}
]
DO NOT output any markdown ticks or explanations, ONLY the raw JSON array.
"""

    user_prompt = f"Source Organization: {source_name}\nSource URL: {source_url}\n\nWebpage Content (Clean Markdown):\n{markdown_content}"

    try:
        if hasattr(openai, "OpenAI"):
            client = openai.OpenAI(api_key=key, base_url=base_url)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            raw_result = response.choices[0].message.content.strip()
        else:
            openai.api_key = key
            if base_url:
                openai.api_base = base_url
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            raw_result = response.choices[0].message["content"].strip()

        # Clean JSON markdown formatting
        raw_result = re.sub(r'^```json\s*', '', raw_result)
        raw_result = re.sub(r'^```\s*', '', raw_result)
        raw_result = re.sub(r'\s*```$', '', raw_result).strip()

        jobs = json.loads(raw_result)
        if isinstance(jobs, list):
            valid_jobs = []
            for j in jobs:
                if not isinstance(j, dict):
                    continue
                if j.get("category") not in CATEGORIES:
                    j["category"] = "Other"
                if not j.get("employer"):
                    j["employer"] = source_name
                if not j.get("link"):
                    j["link"] = source_url
                valid_jobs.append(j)
            return valid_jobs
    except Exception as e:
        print(f"❌ [LLM Error] {source_name}: {e}")

    return []


def get_script_dir() -> str:
    """Returns the directory containing this script."""
    return os.path.dirname(os.path.abspath(__file__))


def load_history(history_file: Optional[str] = None) -> set:
    """Loads previously seen job URLs to avoid duplicates."""
    if not history_file:
        history_file = os.path.join(get_script_dir(), "scraped_history.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data)
        except Exception:
            return set()
    return set()


def save_history(history: set, history_file: Optional[str] = None):
    """Saves seen job URLs to disk."""
    if not history_file:
        history_file = os.path.join(get_script_dir(), "scraped_history.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(list(history), f, indent=2, ensure_ascii=False)


def sync_to_google_sheet(jobs: List[Dict[str, str]], webhook_url: Optional[str] = None) -> bool:
    """
    Sends extracted jobs to Google Apps Script Webhook to write directly to Google Sheet 'Jobs' tab.
    """
    url = webhook_url or os.getenv("GOOGLE_SHEET_WEBHOOK_URL")
    if not url:
        print("ℹ️  [Google Sheet] Keine GOOGLE_SHEET_WEBHOOK_URL in .env hinterlegt. (Überspringe Google Sheet Sync)")
        return False

    if not jobs:
        print("ℹ️  [Google Sheet] Keine Jobs zu synchronisieren.")
        return True

    try:
        print(f"📡 Sende {len(jobs)} Jobs an Google Sheet...")
        resp = requests.post(url, json=jobs, timeout=30)
        if resp.status_code == 200:
            result = resp.json()
            print(f"📊 [Google Sheet Sync Erfolg] {result.get('added', len(jobs))} neue Zeilen hinzugefügt (Gesamtzeilen im Sheet: {result.get('total_rows_now', 'N/A')}).")
            return True
        else:
            print(f"⚠️  [Google Sheet Error] HTTP {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"❌ [Google Sheet Sync Fehler]: {e}")
    return False


def save_results(
    jobs: List[Dict[str, str]],
    output_txt: Optional[str] = None,
    output_json: Optional[str] = None
):
    """
    Saves extracted jobs to text format (for Telegram dispatcher) and JSON format,
    and synchronizes them to Google Sheet if configured.
    """
    script_dir = get_script_dir()
    if not output_txt:
        output_txt = os.path.join(script_dir, "categorized_jobs.txt")
    if not output_json:
        output_json = os.path.join(script_dir, "jobs.json")

    text_blocks = []
    for job in jobs:
        block = (
            f"[{job['category']}]\n"
            f"Job Title: {job['title']}\n"
            f"Employer: {job['employer']}\n"
            f"Link: {job['link']}"
        )
        text_blocks.append(block)

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n---\n".join(text_blocks))

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Gespeichert: {len(jobs)} Jobs in '{output_txt}' und '{output_json}'.")

    # Sync to Google Sheet
    sync_to_google_sheet(jobs)


def run_pipeline(
    sources_file: Optional[str] = None,
    single_url: Optional[str] = None,
    model: str = "gpt-4o-mini",
    deduplicate: bool = True
):
    """
    Runs the full scraping and extraction pipeline.
    """
    script_dir = get_script_dir()
    if not sources_file:
        sources_file = os.path.join(script_dir, "sources.json")

    if single_url:
        # Deduce friendly employer name from URL domain
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', single_url)
        domain_name = domain_match.group(1).split('.')[0].title() if domain_match else "Website"
        sources = [{"name": domain_name, "url": single_url}]
    else:
        with open(sources_file, "r", encoding="utf-8") as f:
            sources = json.load(f)

    seen_jobs = load_history() if deduplicate else set()
    new_seen_keys = set(seen_jobs)

    print(f"🚀 Starting Universal Job Scraper for {len(sources)} sources...\n")
    all_extracted_jobs = []

    for idx, src in enumerate(sources, 1):
        name = src.get("name", "Unknown")
        url = src.get("url", "")
        if not url:
            continue

        print(f"[{idx}/{len(sources)}] Fetching: {name} ({url})")
        html = fetch_url(url)
        if not html:
            continue

        dense_md = clean_html_to_dense_markdown(html, url)
        raw_size = len(html)
        dense_size = len(dense_md)
        savings = (1 - (dense_size / max(raw_size, 1))) * 100
        print(f"    ↳ Reduced: {raw_size:,} → {dense_size:,} chars ({savings:.1f}% token savings)")

        # Extract with AI
        jobs = extract_jobs_with_llm(dense_md, name, url, model=model)
        
        # Filter duplicates if requested
        added_jobs = []
        for job in jobs:
            job_key = f"{job['title']}||{job['employer']}||{job['link']}"
            if deduplicate and job_key in seen_jobs:
                continue
            added_jobs.append(job)
            new_seen_keys.add(job_key)

        print(f"    ↳ Found {len(jobs)} active listings ({len(added_jobs)} new)")
        all_extracted_jobs.extend(added_jobs)

    save_results(all_extracted_jobs)
    if deduplicate:
        save_history(new_seen_keys)


if __name__ == "__main__":
    script_dir = get_script_dir()
    default_sources = os.path.join(script_dir, "sources.json")

    parser = argparse.ArgumentParser(description="Universal Art & Culture Job Scraper")
    parser.add_argument("--sources", default=default_sources, help="Path to sources JSON file")
    parser.add_argument("--url", default=None, help="Scrape a single URL instead of full list")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model (default: gpt-4o-mini)")
    parser.add_argument("--no-dedup", action="store_true", help="Disable deduplication")
    args = parser.parse_args()

    sources_path = args.sources
    if not os.path.exists(sources_path):
        if os.path.exists("sources.json"):
            sources_path = "sources.json"
        elif os.path.exists("scraper_repo/sources.json"):
            sources_path = "scraper_repo/sources.json"

    run_pipeline(
        sources_file=sources_path,
        single_url=args.url,
        model=args.model,
        deduplicate=not args.no_dedup
    )

