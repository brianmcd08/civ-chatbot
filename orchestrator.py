from scraper_changelog import scrape_changelog
from scraper_great_people import scrape_great_people
from scraper_main import scrape_most
from scraper_names import scrape_names
from scraper_utils import UnifiedEntry

entries: list[UnifiedEntry] = []

entries.extend(scrape_most())
print(f"Entries after most: {len(entries)}")
entries.extend(scrape_changelog())
print(f"Entries after most, changelog: {len(entries)}")
entries.extend(scrape_names())
print(f"Entries after most, changlog, names: {len(entries)}")
entries.extend(scrape_great_people())
print(f"Entries after most, changlog, names, great people: {len(entries)}")
