from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

import os
import src.scraping.scrape_orchestrator as scrape_orchestrator
from src.schema import UnifiedEntry

load_dotenv()


def get_batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]


def deduplicate(entries):
    groups = {}  # hash -> (entry, [versions])
    for entry in entries:
        h = entry.generate_hash()
        if h not in groups:
            groups[h] = (entry, [])
        groups[h][1].append(str(entry.version))
    return list(groups.values())


def main():
    entries: list[UnifiedEntry] = scrape_orchestrator.run_all()
    print(f"Total scraped entries: {len(entries)}")
    deduplicated_entries = deduplicate(entries)
    print(f"Total after deduplication: {len(deduplicated_entries)}")

    # Initialize the embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Initialize Pinecone and ensure index exists
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index_name = os.environ["PINECONE_INDEX_NAME"]

    if index_name not in [idx.name for idx in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print(f"Created Pinecone index: {index_name}")
    else:
        print(f"Using existing Pinecone index: {index_name}")

    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
    )

    for batch in get_batches(deduplicated_entries, 200):
        texts = [entry.generate_embedding_text() for entry, _ in batch]
        metadatas = [
            {**entry.generate_metadata(), "bbg_version": versions}
            for entry, versions in batch
        ]
        ids = [entry.generate_hash() for entry, _ in batch]
        vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        print(f"Upserted batch of {len(batch)}")

    print("Ingestion complete.")


if __name__ == "__main__":
    main()
