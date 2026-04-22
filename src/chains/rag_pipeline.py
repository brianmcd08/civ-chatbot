from langchain_core.documents import Document

from src.chains import version_extractor as ve
from src.retrieval.retriever import vectorstore_connection
from src.schema import ParsedInput


def rag_pipeline(query: str) -> list[Document]:
    """
    Chain that ties everything together — takes a raw user query,
    runs it through the version extractor, then passes the ParsedInput
    to the retriever to get relevant documents back.

    The section_hint from the version extractor is forwarded to the
    retriever so that cross-version queries can be scoped to a single
    section instead of searching all 32k docs unfiltered.
    """

    extracted_values: ParsedInput = ve.version_extractor(query)

    # Uncomment to debug version/section extraction during development:
    # print(f"DEBUG → cleaned='{extracted_values.cleaned_query}', "
    #       f"version={extracted_values.version}, "
    #       f"section_hint={extracted_values.section_hint}")

    result: list[Document] = vectorstore_connection.retrieve(
        query=extracted_values.cleaned_query,
        version=extracted_values.version,
        section_hint=extracted_values.section_hint,
    )

    return result
