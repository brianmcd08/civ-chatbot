import requests
from bs4 import BeautifulSoup

from config import versions
from schema import UnifiedEntry

pages = [
    "tech_tree",
    "civic_tree",
]


def scrape_tech_and_civics():
    entries: list[UnifiedEntry] = []
    for page in pages:
        for version in versions:
            url = f"https://civ6bbg.github.io/en_US/{page}_{version}.html"
            response = requests.get(url)
            if not response.ok:
                print(f"{url} not found and should be!")
                continue

            print(f"Parsing {url}")
            soup = BeautifulSoup(response.content, "html.parser")

            items = soup.find_all(
                lambda tag: (  # type: ignore
                    tag.name == "div"
                    and "chart" in tag.get("class", [])
                    and tag.find("h3", class_="civ-ability-name")
                    and tag.find("p", class_="civ-ability-desc")
                )
            )

            for item in items:
                item_name = item.find("h3", class_="civ-ability-name").get_text(
                    separator=" ", strip=True
                )
                item_descr = " ".join(
                    [
                        p.get_text(separator=" ", strip=True)
                        for p in item.find_all(
                            ["p", "small"], class_="civ-ability-desc"
                        )
                    ]
                )

                entries.append(
                    UnifiedEntry(
                        section=page,
                        version=version,
                        name=item_name,
                        description=item_descr,
                    )
                )

    print(f"\nTotal entries collected: {len(entries)}")
    return entries


if __name__ == "__main__":
    entries = scrape_tech_and_civics()
    print(entries[950:1100])
