import requests
from bs4 import BeautifulSoup

from scraper_utils import UnifiedEntry, versions


def parse_citystates_page(soup: BeautifulSoup, version: str) -> list[UnifiedEntry]:
    """
    Extract city-states.
    """

    entries: list[UnifiedEntry] = []

    items = soup.find_all(
        lambda tag: (  # type: ignore
            tag.name == "div"
            and "chart" in tag.get("class", [])
            and tag.find("h2", class_="civ-name")
            and tag.find("p", class_="civ-ability-desc")
        )
    )

    for item in items:
        item_name = item.find("h2", class_="civ-name").get_text(
            separator=" ", strip=True
        )

        item_descr = item.find("p", class_="civ-ability-desc actual-text").get_text(
            separator=" ", strip=True
        )

        entries.append(
            UnifiedEntry(
                section="city-states",
                version=version,
                name=item_name,
                description=item_descr,
            )
        )

    print(f"\nTotal entries collected: {len(entries)}")
    return entries


def scrape_citystates():
    all_entries: list[UnifiedEntry] = []

    for version in versions:
        url = f"https://civ6bbg.github.io/en_US/city_states_{version}.html"
        response = requests.get(url)

        if not response.ok:
            print(f"WARNING: {url} not found (status {response.status_code})")
            continue

        print(f"Parsing {url}")
        soup = BeautifulSoup(response.content, "html.parser")

        page_entries = parse_citystates_page(soup, version=version)
        all_entries.extend(page_entries)

    print(f"\nTotal entries collected: {len(all_entries)}")
    return all_entries


if __name__ == "__main__":
    entries = scrape_citystates()
    print(entries[0])
