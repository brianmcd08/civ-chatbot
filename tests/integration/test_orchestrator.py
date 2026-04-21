from src.config import Section
from src.scraping import scrape_orchestrator


def test_scrape_orchestrator():
    expected_sections = set(Section)
    entries = scrape_orchestrator.run_all()
    actual_sections = {entry.section for entry in entries if entry.section is not None}
    print(expected_sections - actual_sections)
    print(actual_sections)
    assert expected_sections.issubset(actual_sections)
