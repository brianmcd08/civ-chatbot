import requests
from bs4 import BeautifulSoup

from scraper_utils import UnifiedEntry, versions

pages = [
    "city_states",
    "religion",
    "leaders",
    "governor",
    "bbg_expanded",
    "natural_wonder",
    "world_wonder",
    "buildings",
    "units",
    "improvements",
    "tech_tree",
    "civic_tree",
    "policies",
    "congress",
    "misc",
]

bbg_expanded_versions = versions[:4]


def skip(page, version):
    if page == "bbg_expanded" and version not in bbg_expanded_versions:
        return True
    return False


def scrape_most():
    entries: list[UnifiedEntry] = []
    for page in pages:
        if page in ["tech_tree", "civic_tree"]:
            civ_name_tag_name = "civ-ability-name"
            heading = "h3"
        else:
            civ_name_tag_name = "civ-name"
            heading = "h2"

        for version in versions:
            if skip(page, version):
                continue
            url = f"https://civ6bbg.github.io/en_US/{page}_{version}.html"
            response = requests.get(url)
            if not response.ok:
                print(f"{page} not found and should be!")

            print(f"Parsing {url}")
            soup = BeautifulSoup(response.content, "html.parser")

            items = soup.find_all(
                lambda tag: (  # type: ignore
                    tag.name == "div"
                    and "chart" in tag.get("class", [])
                    and tag.find(heading, class_=civ_name_tag_name)
                    and tag.find("p", class_="civ-ability-desc")
                )
            )

            for item in items:
                item_name = item.find(heading, class_=civ_name_tag_name).get_text(
                    separator=" ", strip=True
                )
                item_descr = " ".join(
                    [
                        p.get_text(separator=" ", strip=True)
                        for p in item.find_all("p", class_="civ-ability-desc")
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
    scrape_most()
