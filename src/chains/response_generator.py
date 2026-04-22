import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.chains.rag_pipeline import rag_pipeline

load_dotenv()


def generate_response(query: str) -> str:
    """
    The entire pipeline

    Args:
        query (str): user input

    Returns:
        str: llm output
    """

    llm = ChatAnthropic(model_name=os.environ["ANTHROPIC_MODEL"], stop=[], timeout=30)
    result = rag_pipeline(query)

    if not result:
        response = "Sorry I need more information."

    else:
        information = ""
        for doc in result:
            information += f"<information_block>\n{doc.page_content}\n\n"
            meta_block = ", ".join(
                [f"{key}: {value}" for key, value in doc.metadata.items()]
            )
            information += meta_block + "\n</information_block>"

        prompt = f"""
        You are Montezuma of the Aztec people and also an expert in the game of Civilization 6. Use the following information and metadata 
        to answer the user's question if possible. If you can't answer confidently given the information below, respond 
        that you don't have that answer.

        {information}
        """

        cpt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human", "{query}"),
            ]
        )

        chain = cpt | llm | StrOutputParser()
        response = chain.invoke({"query": query})

    return response
