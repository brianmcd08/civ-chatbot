from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import src.scraping.scrape_orchestrator as scrape_orchestrator
from schema import UnifiedEntry

load_dotenv()


def get_batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]


def main():
    entries: list[UnifiedEntry] = scrape_orchestrator.run_all()

    # Initialize the embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Create a Chroma instance (In-Memory by default)
    # Use persist_directory to save data locally
    vector_store = Chroma(
        collection_name="civilization6_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",
    )

    for batch in get_batches(entries, 200):
        texts = [entry.generate_embedding_text() for entry in batch]
        metadatas = [entry.generate_metadata() for entry in batch]
        ids = [entry.generate_hash() for entry in batch]

        vector_store.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids,
        )


if __name__ == "__main__":
    main()
