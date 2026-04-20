from src.scraping import scrape_orchestrator


def test_scrape_orchestrator():
    expected_sections = {
        "misc",
        "congress",
        "improvements",
        "units",
        "buildings",
        "changelog",
        "city_states",
        "governors",
        "leaders",
        "bbg_expanded",
        "names",
        "natural_wonder",
        "policies",
        "religion",
        "tech_tree",
        "civic_tree",
        "world_wonder",
    }

    entries = scrape_orchestrator.run_all()
    # {'bbg_expanded'}
    actual_sections = {entry.section for entry in entries if entry.section is not None}
    print(expected_sections - actual_sections)
    print(actual_sections)
    assert expected_sections.issubset(actual_sections)
