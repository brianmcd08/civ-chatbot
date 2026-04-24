# Given a clean query string and an optional version string (parsed from the chain),
# return relevant Documents. This file knows nothing about LLMs or intent parsing.

from typing import Any

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
        self,
        query: str,
        version: str | None = Version.get_latest_version(),
        section_hint: str | None = None,
    ) -> list[Document]:
        """
        Retrieve relevant documents for a query.

        Version-specific query (version is set):
            Filter to that version only. This keeps the search space small
            (~2,400 docs) and precision is high.

        Cross-version query (version is None):
            Previously this searched all 32k docs unfiltered, which meant
            the 17k names entries dominated the k=25 results. Now, if the
            version_extractor inferred a section_hint (e.g. "units" for a
            question about the Eagle Warrior), we filter to that section
            across all versions instead. This reduces the search space from
            32k to ~1,980 docs for units, giving the right entries a fair shot.

            If no section_hint was provided, we fall back to an unfiltered
            search but exclude the names section, which is pure lookup data
            and is never a useful result for balance questions.

        Args:
            query: cleaned query string from version_extractor
            version: BBG version string, or None for cross-version queries
            section_hint: optional section name to filter on (e.g. "units")

        Returns:
            list[Document]
        """

        chroma_filter: dict[str, Any]
        k = 25

        if version is not None and section_hint is not None:
            chroma_filter = {
                "$and": [{"bbg_version": version}, {"section": section_hint}]
            }
        elif version is not None:
            # Version-specific: filter to that version
            chroma_filter = {"bbg_version": version}
        elif section_hint is not None:
            # Cross-version with a section hint: filter to that section only
            chroma_filter = {"section": section_hint}
        else:
            # Cross-version, no hint: exclude the names section which is pure
            # lookup noise and drowns out balance-relevant results.
            # Chroma's $ne operator filters out documents where section == "names".
            chroma_filter = {"section": {"$ne": "names"}}
            k = 40

        result = self.vector_store.similarity_search(query, k=k, filter=chroma_filter)

        # Fallback: if the filtered search returned nothing at all, retry
        # completely unfiltered so we never return an empty result when docs exist.
        if not result:
            result = self.vector_store.similarity_search(query, k=25)

        return result


vectorstore_connection = Retriever()
