from typing import cast

import requests
from bs4 import BeautifulSoup, Tag

from src.config import versions
from src.schema import UnifiedEntry


def parse_changelog_page(soup: BeautifulSoup, version: str) -> list[UnifiedEntry]:
    entries: list[UnifiedEntry] = []

    # All content lives inside div.chart blocks within the container
    for chart in soup.find_all("div", class_="chart"):
        current_category = ""
        current_subcategory = ""

        for tag in chart.children:
            if not isinstance(tag, Tag):
                continue  # skip NavigableString / Comment nodes

            classes = cast(list[str], tag.get("class") or [])

            # Top-level category header (h1)
            if tag.name == "h1" and "civ-name" in classes:
                current_category = tag.get_text(separator=" ", strip=True)
                current_subcategory = ""

            # Subcategory header (h2)
            elif tag.name == "h2" and "civ-name" in classes:
                current_subcategory = tag.get_text(separator=" ", strip=True)

            # Content paragraph
            elif tag.name == "p" and "civ-ability-desc" in classes:
                description = tag.get_text(separator=" ", strip=True)
                if description:
                    entries.append(
                        UnifiedEntry(
                            section="changelog",
                            version=version,
                            category=current_category,
                            subcategory=current_subcategory,
                            description=description,
                        )
                    )

    return entries


def scrape_changelog():
    changelog_versions = versions[:10]

    all_entries: list[UnifiedEntry] = []

    for version in changelog_versions:
        url = f"https://civ6bbg.github.io/en_US/changelog_{version}.html"
        response = requests.get(url)

        if not response.ok:
            print(f"WARNING: {url} not found (status {response.status_code})")
            continue

        print(f"Parsing {url}")
        soup = BeautifulSoup(response.content, "html.parser")

        page_entries = parse_changelog_page(soup, version=version)
        all_entries.extend(page_entries)

    print(f"\nTotal entries collected: {len(all_entries)}")
    return all_entries


if __name__ == "__main__":
    scrape_changelog()
