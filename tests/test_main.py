import os
import pytest
import xmltodict
from blog_to_json.__main__ import get_normalized_document, default_parser

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def _read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name)) as f:
        return f.read()


class TestGetNormalizedDocument:
    def test_wordpress(self):
        xml = _read_fixture("wordpress_minimal.xml")
        result = get_normalized_document(xml, "wordpress")
        assert "hello-world" in result
        assert "no-comments" in result

    def test_disqus(self):
        xml = _read_fixture("disqus_minimal.xml")
        result = get_normalized_document(xml, "disqus")
        assert len(result) == 2

    def test_graphcomment(self):
        xml = _read_fixture("graphcomment_minimal.xml")
        result = get_normalized_document(xml, "graphcomment", "https://mysite.io")
        assert len(result) == 1

    def test_invalid_type_raises(self):
        with pytest.raises(Exception, match="invalid dump type"):
            get_normalized_document("<xml/>", "blogger")


class TestDefaultParser:
    def test_has_path_argument(self):
        parser = default_parser()
        # parser should accept 'path' positional arg
        # just verify it doesn't crash on creation
        assert parser is not None
        assert parser.description == "Convert a blog dump to JSON."
