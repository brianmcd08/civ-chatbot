import os
from typing import cast

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from src.config import Version
from src.schema import ParsedInput

load_dotenv()


def version_extractor(query: str) -> ParsedInput:
    """
    1) Extract version from query by passing Version to LLM
    2) Clean query by passing to LLM

    Args:
        query (str): raw query

    Returns:
        ParsedInput: clean query and version
    """

    llm = ChatAnthropic(model_name=os.environ["ANTHROPIC_MODEL"], stop=[], timeout=30)
    structured_llm = llm.with_structured_output(ParsedInput)
    versions = Version.to_list_of_strings()

    prompt = f"""
        Extract the following from the user input:
        1) Version
        Here are the appropriate versions (default to v74 if none found):
        <Versions>
    {versions}
        </Versions>
        If the query is asking WHICH versions something appears in, or spans
        all versions (e.g. "which versions is X in?", "has X changed across versions?"),
        set version to null instead of defaulting to v74.

        2) A cleaned query: fix typos and remove explicit version references (e.g. "in v74",
        "in version 6.5"), but PRESERVE all semantic content — including the subject,
        the civilization name, the unit/building/policy name, and the nature of the question
        (e.g. "which civ", "unique unit", "what versions"). Do NOT reduce the query to
        just a bare noun; keep enough context so a vector search can find the right documents.
        """

    cpt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("human", "{query}"),
        ]
    )

    chain = cpt | structured_llm
    response = cast(ParsedInput, chain.invoke({"query": query}))
    return response
