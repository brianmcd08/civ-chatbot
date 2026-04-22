from langchain_core.documents import Document

from src.chains import version_extractor as ve
from src.retrieval.retriever import vectorstore_connection
from src.schema import ParsedInput


def rag_pipeline(query: str) -> list[Document]:
    """
    chain that ties everything together — Takes a raw user query,
    runs it through the version extractor, then passes the ParsedInput
    to the retriever to get relevant documents back.
    """

    extracted_values: ParsedInput = ve.version_extractor(query)
    result: list[Document] = vectorstore_connection.retrieve(
        query=extracted_values.cleaned_query, version=extracted_values.version
    )

    return result
