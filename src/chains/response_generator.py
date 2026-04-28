from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.chains.rag_pipeline import rag_pipeline
from src.config import ANTHROPIC_MODEL
from src.secrets import get_secret

import os
os.environ["ANTHROPIC_API_KEY"] = get_secret("ANTHROPIC_API_KEY")


def generate_response(query: str, history: list) -> str:
    """
    The entire pipeline

    Args:
        query (str): user input

    Returns:
        str: llm output
    """

    converted_history = []
    for msg in history:
        if msg["role"] == "user":
            converted_history.append(HumanMessage(content=msg["content"]))
        else:
            converted_history.append(AIMessage(content=msg["content"]))

    llm = ChatAnthropic(model_name=ANTHROPIC_MODEL, stop=[], timeout=30)
    result = rag_pipeline(query, converted_history)

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
                MessagesPlaceholder("history"),
                ("human", "{query}"),
            ]
        )

        chain = cpt | llm | StrOutputParser()
        response = chain.invoke({"query": query, "history": history})

    return response
