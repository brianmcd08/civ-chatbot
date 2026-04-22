from src.retrieval.retriever import vectorstore_connection


def test_version_retrieved():
    expected_version = "7.4"
    query = "Which Great General gives you the Art of War?"
    expected_answer = "Sun Tzu"

    results = vectorstore_connection.retrieve(query=query, version=expected_version)
    assert results

    for doc in results:
        assert doc.metadata["bbg_version"] == expected_version

    assert any(expected_answer in doc.page_content for doc in results)
