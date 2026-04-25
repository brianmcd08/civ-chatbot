# Ad-hoc script to investigate duplicate chunks in the Chroma vector store.
# Run once during development (April 2026) to diagnose ingestion issues.
from collections import Counter

from src.schema import UnifiedEntry
from src.scraping.scrape_orchestrator import (
    run_all,  # adjust import to match your module path
)


def diagnose(entries: list[UnifiedEntry]) -> None:
    total = len(entries)
    hashes = [e.generate_hash() for e in entries]
    unique_hashes = set(hashes)

    print(f"Total entries returned : {total}")
    print(f"Unique hashes          : {len(unique_hashes)}")
    print(f"Duplicates             : {total - len(unique_hashes)}")

    if total == len(unique_hashes):
        print("\n✅ No duplicates found — safe to ingest.")
        return

    # Find which hashes collide and show example entries for each
    counts = Counter(hashes)
    collisions = {h: count for h, count in counts.items() if count > 1}

    print(f"\n⚠️  {len(collisions)} distinct hash(es) appear more than once:\n")

    hash_to_entries: dict[str, list[UnifiedEntry]] = {}
    for entry, h in zip(entries, hashes):
        hash_to_entries.setdefault(h, []).append(entry)

    for h, count in sorted(collisions.items(), key=lambda x: -x[1]):
        print(f"  Hash : {h!r}  ({count}x)")
        dupes = hash_to_entries[h]
        for i, e in enumerate(dupes):
            print(
                f"    [{i}] section={e.section!r} version={e.version!r} "
                f"name={e.name!r} description={e.description!r} "
                f"category={e.category!r} subcategory={e.subcategory!r}"
            )
        print()

    # Suggest root cause
    print("── Likely root causes ──────────────────────────────────────────")

    collision_entries = [hash_to_entries[h][0] for h in collisions]

    section_counts = Counter(str(e.section) for e in collision_entries)
    print("Collisions by section:")
    for sec, n in section_counts.most_common():
        print(f"  {sec or '(empty)'}: {n} collision(s)")

    version_counts = Counter(e.version for e in collision_entries)
    print("\nCollisions by version:")
    for ver, n in version_counts.most_common():
        print(f"  {ver or '(empty)'}: {n} collision(s)")

    empty_both = sum(1 for e in collision_entries if not e.name and not e.description)
    if empty_both:
        print(f"\n⚠️  {empty_both} collision(s) have BOTH name and description empty.")
        print("   → These will always collide — add another field to generate_hash().")

    print("\n── Suggested fixes ─────────────────────────────────────────────")
    print("1. De-dupe after scraping (fastest fix):")
    print("   seen = set()")
    print(
        "   entries = [e for e in raw if e.generate_hash() not in seen and not seen.add(e.generate_hash())]"
    )
    print()
    print("2. Strengthen generate_hash() if name/description legitimately repeat:")
    print("   include self.category or self.subcategory in hash_str")
    print()
    print("3. Index tiebreaker as a last resort:")
    print(
        "   hash_str = self.section + self.version + (self.name or self.description or '') + str(index)"
    )


if __name__ == "__main__":
    print("Fetching entries from scrape_orchestrator.run_all() …")
    entries = run_all()
    diagnose(entries)
