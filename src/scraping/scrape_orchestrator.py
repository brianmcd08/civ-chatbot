from src.schema import UnifiedEntry
from src.scraping.scrape_bbg_expanded import scrape_bbg_expanded
from src.scraping.scrape_buildings import scrape_buildings
from src.scraping.scrape_changelogs import scrape_changelog
from src.scraping.scrape_citystates import scrape_citystates
from src.scraping.scrape_civic_tree import scrape_civic_tree
from src.scraping.scrape_congress import scrape_congress
from src.scraping.scrape_governors import scrape_governors
from src.scraping.scrape_great_people import scrape_great_people
from src.scraping.scrape_improvements import scrape_improvements
from src.scraping.scrape_leaders import scrape_leaders
from src.scraping.scrape_misc import scrape_misc
from src.scraping.scrape_names import scrape_names
from src.scraping.scrape_natural_wonders import scrape_natural_wonders
from src.scraping.scrape_policies import scrape_policies
from src.scraping.scrape_religion import scrape_religion
from src.scraping.scrape_tech_tree import scrape_tech_tree
from src.scraping.scrape_units import scrape_units
from src.scraping.scrape_world_wonders import scrape_world_wonders


def run_all() -> list[UnifiedEntry]:
    entries: list[UnifiedEntry] = []

    entries.extend(scrape_misc())
    print(f"Entries after misc: {len(entries)}")
    entries.extend(scrape_buildings())
    entries.extend(scrape_congress())
    entries.extend(scrape_units())
    entries.extend(scrape_improvements())
    entries.extend(scrape_changelog())
    entries.extend(scrape_names())
    entries.extend(scrape_great_people())
    entries.extend(scrape_leaders())
    entries.extend(scrape_bbg_expanded())
    entries.extend(scrape_policies())
    entries.extend(scrape_tech_tree())
    entries.extend(scrape_civic_tree())
    entries.extend(scrape_natural_wonders())
    entries.extend(scrape_world_wonders())
    entries.extend(scrape_religion())
    entries.extend(scrape_citystates())
    entries.extend(scrape_governors())
    print(f"Entries after everything: {len(entries)}")

    return entries


if __name__ == "__main__":
    entries = run_all()
    print(f"Total: {len(entries)}")
