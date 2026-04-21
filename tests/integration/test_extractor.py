from src.chains.version_extractor import version_extractor
from src.schema import ParsedInput


def test_extractor_no_version_specified():
    expected_version = "7.4"

    query = "Whech Great Gneral gives you the Art of War?"
    results = version_extractor(query)

    assert isinstance(results, ParsedInput)
    assert results.version == expected_version
    assert expected_version not in results.cleaned_query


def test_extractor_version_specified():
    expected_version = "7.2"

    query = "Whech Great Gneral gives you the Art of War in 7.2?"
    results = version_extractor(query)

    assert isinstance(results, ParsedInput)
    assert results.version == expected_version
    assert expected_version not in results.cleaned_query


def test_extractor_version_oddly_specified():
    expected_version = "7.2"

    query = "Which Great Gneral gives you the Art frl War in seven.two?"
    results = version_extractor(query)

    assert isinstance(results, ParsedInput)
    assert results.version == expected_version
    assert "seven.two" not in results.cleaned_query
