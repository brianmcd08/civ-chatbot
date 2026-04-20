import re

import requests
from bs4 import BeautifulSoup, Comment

from src.config import versions
from src.schema import UnifiedEntry


def get_category_from_comment(chart) -> str:
    """Extract the feature category from the LOC comment preceding the h2."""

    # Matches e.g. "LOC_NAMED_DESERT_ACCONA_DESERT_NAME" -> "Desert"
    LOC_COMMENT_RE = re.compile(r"LOC_NAMED_([A-Z]+)_", re.IGNORECASE)

    for node in chart.children:
        if isinstance(node, Comment):
            m = LOC_COMMENT_RE.search(node)
            if m:
                return m.group(1).title()  # e.g. "DESERT" -> "Desert"
    return ""


def parse_names_page(soup: BeautifulSoup, version: str) -> list[UnifiedEntry]:
    entries: list[UnifiedEntry] = []

    for chart in soup.find_all("div", class_="chart"):
        h2 = chart.find("h2", class_="civ-ability-desc")
        p = chart.find("p", class_="civ-ability-desc")

        if not h2 or not p:
            continue

        name = h2.get_text(separator=" ", strip=True)
        civilization = p.get_text(separator=" ", strip=True)
        category = get_category_from_comment(chart)

        entries.append(
            UnifiedEntry(
                section="names",
                version=version,
                category=category,
                name=name,
                civilization=civilization,
            )
        )

    return entries


def scrape_names():
    all_entries: list[UnifiedEntry] = []

    for version in versions:
        url = f"https://civ6bbg.github.io/en_US/names_{version}.html"
        response = requests.get(url)

        if not response.ok:
            print(f"WARNING: {url} not found (status {response.status_code})")
            continue

        print(f"Parsing {url}")
        soup = BeautifulSoup(response.content, "html.parser")

        page_entries = parse_names_page(soup, version=version)
        all_entries.extend(page_entries)

    print(f"\nTotal entries collected: {len(all_entries)}")
    return all_entries


if __name__ == "__main__":
    scrape_names()
