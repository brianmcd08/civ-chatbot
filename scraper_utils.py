from dataclasses import asdict, dataclass


@dataclass
class UnifiedEntry:
    """
    For storing data from all ingestion runs
    """

    section: str  # page name
    version: str  # bbg version

    name: str | None = (
        None  # e.g. "Accona Desert" or individual person name, e.g. "Boudica"
    )
    category: str | None = (
        None  # e.g. "Desert", "Mountain", "River" or top-level h1 section e.g. "Game Mechanics", "Leaders"
    )
    subcategory: str | None = None  # h2 section e.g. "Global Changes", "Combat"

    civilization: str | None = None
    description: str | None = None

    great_person_type: str | None = None  # e.g. "Great General", "Great Scientist"
    era: str | None = None  # e.g. "Classical Era"
    charges: str | None = None  # e.g. "1", "2"


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


def print_some(entries: list[UnifiedEntry]) -> None:
    """
    Preview first 3 and last 3
    """
    for e in entries[:3] + entries[-3:]:
        print(asdict(e))


if __name__ == "__main__":
    print("Run via the orchestrator!")
