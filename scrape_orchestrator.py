from scrape_changelogs import scrape_changelog
from scrape_citystates import scrape_citystates
from scrape_governors import scrape_governors
from scrape_great_people import scrape_great_people
from scrape_leaders import scrape_leaders
from scrape_main import scrape_combined_items
from scrape_names import scrape_names
from scrape_natural_wonders import scrape_natural_wonders
from scrape_policies import scrape_policies
from scrape_religion import scrape_religion
from scrape_tech_civics import scrape_tech_and_civics
from scrape_world_wonders import scrape_world_wonders
from scraper_utils import UnifiedEntry, versions


def run_all() -> list[UnifiedEntry]:
    entries: list[UnifiedEntry] = []

    entries[:50].extend(scrape_combined_items())
    print(f"Entries after most: {len(entries)}")
    entries.extend(scrape_changelog()[:20])
    entries.extend(scrape_names()[:20])
    entries.extend(scrape_great_people()[:20])
    entries.extend(scrape_leaders("leaders", versions)[:20])
    entries.extend(scrape_leaders("bbg_expanded", versions[:4])[:20])
    entries.extend(scrape_policies()[:20])
    entries.extend(scrape_tech_and_civics()[:20])
    entries.extend(scrape_natural_wonders()[:20])
    entries.extend(scrape_world_wonders())
    entries.extend(scrape_religion()[:20])
    entries.extend(scrape_citystates()[:20])
    entries.extend(scrape_governors()[:20])
    print(f"Entries after everything: {len(entries)}")

    return entries


if __name__ == "__main__":
    entries = run_all()
    print(f"Total: {len(entries)}")
