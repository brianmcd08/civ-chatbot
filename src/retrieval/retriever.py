# Given a clean query string and an optional version string (parsed from the chain),
# return relevant Documents. This file knows nothing about LLMs or intent parsing.

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from src.config import Version


class Retriever:
    def __init__(self) -> None:
        self.vector_store = Chroma(
            collection_name="civilization6_collection",
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
            persist_directory="./chroma_langchain_db",
        )

    def retrieve(
        self, query: str, version: str | None = Version.get_latest_version()
    ) -> list[Document]:
        filter = {"bbg_version": version} if version else None
        result = self.vector_store.similarity_search(query, filter=filter)

        # Fallback: if a version-filtered search returns nothing, retry without
        # the filter so base_game or cross-version documents can still be found.
        if not result and filter is not None:
            result = self.vector_store.similarity_search(query)

        return result


vectorstore_connection = Retriever()
