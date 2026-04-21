from enum import StrEnum

# List of BBG versions
versions = [
    "7.4",
    "7.3",
    "7.2",
    "7.1",
    "6.5",
    "6.4",
    "6.3",
    "6.2",
    "6.1",
    "6.0",
    "5.8",
    "5.7",
    "5.6",
    "base_game",
]

latest_version = versions[0]


# Sections
class Section(StrEnum):
    LEADERS = "leaders"
    GREATPEOPLE = "great_people"
    MISC = "misc"
    CONGRESS = "congress"
    IMPROVEMENTS = "improvements"
    UNITS = "units"
    BUILDINGS = "buildings"
    CHANGELOG = "changelog"
    CITYSTATES = "city_states"
    GOVERNORS = "governor"
    BBGEXPANDED = "bbg_expanded"
    NAMES = "names"
    NATURALWONDER = "natural_wonder"
    POLICIES = "policies"
    RELIGION = "religion"
    TECHTREE = "tech_tree"
    CIVICTREE = "civic_tree"
    WORLDWONDER = "world_wonder"
