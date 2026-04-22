from typing import cast

import requests
from bs4 import BeautifulSoup, Tag

from src.config import Section, Version
from src.schema import UnifiedEntry


def parse_page(soup: BeautifulSoup, version: str) -> list[UnifiedEntry]:
    """
    Parse a changelog page into one UnifiedEntry per category group.

    Previously this created one entry per <p> bullet point, which produced
    ~50-60 tiny chunks per version (median ~100 chars) with no surrounding
    context. Grouping by category means "Military Units v7.4" becomes a single
    chunk with all 17 bullet points joined — enough content for the embedding
    model to reliably retrieve it for any unit-related query.

    Subcategory is retained as metadata for the LLM but NOT used as a grouping
    key, because splitting "Military Units / Melee" and "Military Units / Ranged"
    into separate chunks would recreate the fragmentation problem.
    """

    # (category) -> list of (subcategory, bullet_text) tuples
    # We preserve subcategory in the text so the LLM can see it, but we group
    # only by category so related changes land in the same chunk.
    groups: dict[str, list[tuple[str, str]]] = {}

    current_category = ""
    current_subcategory = ""

    for chart in soup.find_all("div", class_="chart"):
        for tag in chart.children:
            if not isinstance(tag, Tag):
                continue

            classes = cast(list[str], tag.get("class") or [])

            if tag.name == "h1" and "civ-name" in classes:
                current_category = tag.get_text(separator=" ", strip=True)
                current_subcategory = ""

            elif tag.name == "h2" and "civ-name" in classes:
                current_subcategory = tag.get_text(separator=" ", strip=True)

            elif tag.name == "p" and "civ-ability-desc" in classes:
                description = tag.get_text(separator=" ", strip=True)
                if description:
                    groups.setdefault(current_category, []).append(
                        (current_subcategory, description)
                    )

    entries: list[UnifiedEntry] = []
    for category, bullets in groups.items():
        # Inline the subcategory header when it changes, so the joined text
        # reads naturally: "[Combat] bullet1 bullet2 [Recon] bullet3 ..."
        # This keeps subcategory context visible to the LLM without fragmenting.
        parts: list[str] = []
        last_sub = None
        for subcategory, text in bullets:
            if subcategory and subcategory != last_sub:
                parts.append(f"[{subcategory}]")
                last_sub = subcategory
            parts.append(text)

        entries.append(
            UnifiedEntry(
                section=Section.CHANGELOG,
                version=version,
                category=category or None,
                description=" ".join(parts),
            )
        )

    return entries


def scrape_changelog():
    changelog_versions = list(Version)[:10]

    all_entries: list[UnifiedEntry] = []

    for version in changelog_versions:
        url = f"https://civ6bbg.github.io/en_US/{Section.CHANGELOG}_{version}.html"
        response = requests.get(url)

        if not response.ok:
            print(f"WARNING: {url} not found (status {response.status_code})")
            continue

        print(f"Parsing {url}")
        soup = BeautifulSoup(response.content, "html.parser")

        page_entries = parse_page(soup, version=version)
        all_entries.extend(page_entries)

    print(f"\nTotal entries collected: {len(all_entries)}")
    return all_entries


if __name__ == "__main__":
    scrape_changelog()
