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
from scraper_utils import UnifiedEntry

entries: list[UnifiedEntry] = []

entries.extend(scrape_combined_items())
print(f"Entries after most: {len(entries)}")
entries.extend(scrape_changelog())
entries.extend(scrape_names())
entries.extend(scrape_great_people())
entries.extend(scrape_leaders("leaders"))
entries.extend(scrape_leaders("bbg_expanded"))
entries.extend(scrape_policies())
entries.extend(scrape_tech_and_civics())
entries.extend(scrape_natural_wonders())
entries.extend(scrape_world_wonders())
entries.extend(scrape_religion())
entries.extend(scrape_citystates())
entries.extend(scrape_governors())
print(f"Entries after everything: {len(entries)}")
