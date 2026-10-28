import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urljoin
import requests
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.9679677_50.6612596_3.125725_50.6008264&locationName=Lille"
STATE_FILE = Path("seen.json")
BASE = "https://trouverunlogement.lescrous.fr"

def telegram(message):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    response = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": message}, timeout=20)
    response.raise_for_status()
    if not response.json().get("ok"):
        raise RuntimeError(f"Telegram API error: {response.text}")

def get_listings():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="fr-FR")
        page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)
        links = page.locator('a[href*="/tools/47/"]').evaluate_all("els => els.map(a => ({href:a.href, text:(a.innerText||a.getAttribute('aria-label')||'').trim()}))")
        browser.close()
    return {urljoin(BASE, x["href"]): re.sub(r"\s+", " ", x["text"]).strip() for x in links if "/search" not in x["href"] and len(x["text"].strip()) >= 5}

def main():
    listings = get_listings()
    prior = set(json.loads(STATE_FILE.read_text("utf-8"))) if STATE_FILE.exists() else set()
    if not prior:
        STATE_FILE.write_text(json.dumps(sorted(listings), ensure_ascii=False, indent=2), "utf-8")
        print(f"Initial baseline saved ({len(listings)} listings).")
        return
    new_urls = sorted(set(listings) - prior)
    for url in new_urls:
        telegram(f"🏠 Nouvelle annonce CROUS à Lille\n{listings[url]}\n{url}")
    print(f"Sent {len(new_urls)} notification(s)." if new_urls else "No new listing.")
    STATE_FILE.write_text(json.dumps(sorted(set(listings) | prior), ensure_ascii=False, indent=2), "utf-8")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Monitor failed: {exc}", file=sys.stderr)
        raise

