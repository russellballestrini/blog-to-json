import os
import pytest
import xmltodict

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def _load_xml(filename):
    path = os.path.join(FIXTURES_DIR, filename)
    with open(path) as f:
        return xmltodict.parse(f.read())


@pytest.fixture
def wordpress_doc():
    return _load_xml("wordpress_minimal.xml")


@pytest.fixture
def disqus_doc():
    return _load_xml("disqus_minimal.xml")


@pytest.fixture
def graphcomment_doc():
    return _load_xml("graphcomment_minimal.xml")
