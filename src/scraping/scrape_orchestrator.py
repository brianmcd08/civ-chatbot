from src.config import Section
from src.schema import UnifiedEntry

# Imported for dynamic dispatch via globals() in run_all()
from src.scraping.scrape_bbg_expanded import scrape_bbg_expanded  # noqa: F401
from src.scraping.scrape_buildings import scrape_buildings  # noqa: F401
from src.scraping.scrape_changelogs import scrape_changelog  # noqa: F401
from src.scraping.scrape_city_states import scrape_city_states  # noqa: F401
from src.scraping.scrape_civic_tree import scrape_civic_tree  # noqa: F401
from src.scraping.scrape_congress import scrape_congress  # noqa: F401
from src.scraping.scrape_governor import scrape_governor  # noqa: F401
from src.scraping.scrape_great_people import scrape_great_people  # noqa: F401
from src.scraping.scrape_improvements import scrape_improvements  # noqa: F401
from src.scraping.scrape_leaders import scrape_leaders  # noqa: F401
from src.scraping.scrape_misc import scrape_misc  # noqa: F401
from src.scraping.scrape_names import scrape_names  # noqa: F401
from src.scraping.scrape_natural_wonder import scrape_natural_wonder  # noqa: F401
from src.scraping.scrape_policies import scrape_policies  # noqa: F401
from src.scraping.scrape_religion import scrape_religion  # noqa: F401
from src.scraping.scrape_tech_tree import scrape_tech_tree  # noqa: F401
from src.scraping.scrape_units import scrape_units  # noqa: F401
from src.scraping.scrape_world_wonder import scrape_world_wonder  # noqa: F401


def run_all() -> list[UnifiedEntry]:
    entries: list[UnifiedEntry] = []
    for section in Section:
        scrape_fn = globals()[f"scrape_{section.value}"]
        entries.extend(scrape_fn())

    return entries


if __name__ == "__main__":
    entries = run_all()
    print(f"Total: {len(entries)}")
