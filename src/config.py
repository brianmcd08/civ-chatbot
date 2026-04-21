from enum import StrEnum

# List of BBG versions
# versions = [
#     "7.4",
#     "7.3",
#     "7.2",
#     "7.1",
#     "6.5",
#     "6.4",
#     "6.3",
#     "6.2",
#     "6.1",
#     "6.0",
#     "5.8",
#     "5.7",
#     "5.6",
#     "base_game",
# ]


class Version(StrEnum):
    V74 = "7.4"
    V73 = "7.3"
    V72 = "7.2"
    V71 = "7.1"
    V65 = "6.5"
    V64 = "6.4"
    V63 = "6.3"
    V62 = "6.2"
    V61 = "6.1"
    V60 = "6.0"
    V58 = "5.8"
    V57 = "5.7"
    V56 = "5.6"
    VBASE = "base_game"

    @classmethod
    def to_list_of_strings(cls):
        return "\n".join([v.value for v in cls])

    @classmethod
    def get_latest_version(cls):
        return next(iter(cls))


# latest_version = versions[0]
# latest_version = Version.V74


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
