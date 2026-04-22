import requests
from bs4 import BeautifulSoup

from src.config import Section, Version
from src.schema import UnifiedEntry


def scrape_units():
    entries: list[UnifiedEntry] = []
    for version in Version:
        url = f"https://civ6bbg.github.io/en_US/{Section.UNITS}_{version}.html"
        response = requests.get(url)
        if not response.ok:
            print(f"{url} not found and should be!")
            continue

        print(f"Parsing {url}")
        soup = BeautifulSoup(response.content, "html.parser")

        # Replace the items loop in both scrape_misc and scrape_units with this:
        seen: dict[str, list[str]] = {}  # name -> list of description parts

        for item in soup.find_all("div", class_="chart"):
            h2 = item.find("h2", class_="civ-name")
            if not h2:
                continue
            name = h2.get_text(separator=" ", strip=True)
            for p in item.find_all("p", class_="civ-ability-desc"):
                seen.setdefault(name, []).append(p.get_text(separator=" ", strip=True))

        for name, parts in seen.items():
            entries.append(
                UnifiedEntry(
                    section=Section.UNITS,  # Section.UNITS for scrape_units
                    version=version,
                    name=name,
                    description=" ".join(parts),
                )
            )

    print(f"\nTotal entries collected: {len(entries)}")
    return entries


if __name__ == "__main__":
    entries = scrape_units()
    print(entries[-1])
