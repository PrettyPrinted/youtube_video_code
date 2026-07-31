"""
Scrapes D.R. Horton home listings for a given area page, e.g.
https://www.drhorton.com/nevada/las-vegas

Two steps are needed because the site splits the data across two sources:
1. The area page's community list comes from a JSON API
   (https://www.drhorton.com/api/comms/direct{area_path}).
2. Each community's individual "available homes" (quick move-in homes) are
   server-rendered on that community's own page, so each one is scraped
   separately.

Install dependencies with:
    pip install requests
"""

import re
import time
from html.parser import HTMLParser

import requests
import sqlite3
from datetime import date

BASE_URL = "https://www.drhorton.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

PROXIES = {
    "http": "YOUR_PROXY_URL",
    "https": "YOUR_PROXY_URL",
}


class _HomeCardParser(HTMLParser):
    """Extracts (address, price) pairs from <a class="available-home-card"> blocks."""

    def __init__(self):
        super().__init__()
        self.in_card = False
        self.anchor_depth = 0
        self.current_tag = None
        self.price_text = ""
        self.name_text = ""
        self.homes = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "available-home-card" in (attrs.get("class") or ""):
            self.in_card = True
            self.anchor_depth = 0
            self.price_text = ""
            self.name_text = ""
            return
        if self.in_card and tag == "a":
            self.anchor_depth += 1
        if self.in_card and tag in ("h2", "h3"):
            self.current_tag = tag

    def handle_endtag(self, tag):
        if tag == "a":
            if self.in_card and self.anchor_depth > 0:
                self.anchor_depth -= 1
            elif self.in_card:
                self._finish_card()
        if tag in ("h2", "h3"):
            self.current_tag = None

    def handle_data(self, data):
        if not self.in_card:
            return
        if self.current_tag == "h2":
            self.price_text += data
        elif self.current_tag == "h3":
            self.name_text += data

    def _finish_card(self):
        price_match = re.search(r"\$[\d,]+", self.price_text)
        name = self.name_text.strip()
        if price_match and name:
            price = int(price_match.group(0).replace("$", "").replace(",", ""))
            self.homes.append({"name": name, "price": price})
        self.in_card = False


def _get_communities(session, area_path):
    """Return the list of community dicts for an area, e.g. '/nevada/las-vegas'."""
    resp = session.get(f"{BASE_URL}/api/comms/direct{area_path}", timeout=15, proxies=PROXIES)
    resp.raise_for_status()
    return resp.json().get("CommunityData", [])


def _get_community_homes(session, community_path, community_name):
    """Parse the quick move-in home cards on a single community's page."""
    resp = session.get(f"{BASE_URL}{community_path}", timeout=15, proxies=PROXIES)
    resp.raise_for_status()

    parser = _HomeCardParser()
    parser.feed(resp.text)

    return [
        {"name": home["name"], "community": community_name, "price": home["price"]}
        for home in parser.homes
    ]


def get_home_listings(area_path="/nevada/las-vegas", delay=0.5):
    """
    Return a list of dicts (name, community, price) for every quick move-in
    home listed under the given D.R. Horton area page.
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    listings = []
    for community in _get_communities(session, area_path):
        community_name = community.get("commName")
        community_path = community.get("commPageLink")
        if not community_path:
            continue

        try:
            listings.extend(
                _get_community_homes(session, community_path, community_name)
            )
        except requests.RequestException as exc:
            print(f"Skipping '{community_name}': {exc}")

        time.sleep(delay)  # be polite between requests

    return listings


if __name__ == "__main__":
    conn = sqlite3.connect("homes.db")
    cursor = conn.cursor()
    
    homes = get_home_listings()
    #print(f"Found {len(homes)} homes\n")
    for home in homes:
        cursor.execute(
            "INSERT INTO homes (name, community, price, date) VALUES (?, ?, ?, ?)", 
            (home['name'], home['community'], home['price'], date.today()))

    conn.commit()
    cursor.close()
    conn.close()