"""Integration tests: round-trip XML fixtures through the full pipeline."""
import os
import json
import pytest
import xmltodict
from blog_to_json.__main__ import get_normalized_document

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def _read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name)) as f:
        return f.read()


class TestWordpressRoundTrip:
    def test_output_is_json_serializable(self):
        xml = _read_fixture("wordpress_minimal.xml")
        result = get_normalized_document(xml, "wordpress")
        output = json.dumps(result, indent=2)
        roundtrip = json.loads(output)
        assert roundtrip == result

    def test_all_posts_have_required_keys(self):
        xml = _read_fixture("wordpress_minimal.xml")
        result = get_normalized_document(xml, "wordpress")
        required = {"name", "id", "link", "title", "content", "date", "timestamp", "comments", "metadata"}
        for name, post in result.items():
            assert required.issubset(post.keys()), f"post '{name}' missing keys"

    def test_all_comments_have_required_keys(self):
        xml = _read_fixture("wordpress_minimal.xml")
        result = get_normalized_document(xml, "wordpress")
        required = {"id", "parent_id", "author_ip", "author", "email", "content", "date", "timestamp"}
        for name, post in result.items():
            for comment in post["comments"]:
                assert required.issubset(comment.keys()), f"comment in '{name}' missing keys"

    def test_comment_parent_chain(self):
        xml = _read_fixture("wordpress_minimal.xml")
        result = get_normalized_document(xml, "wordpress")
        comments = result["hello-world"]["comments"]
        parent = comments[0]
        child = comments[1]
        assert child["parent_id"] == parent["id"]


class TestDisqusRoundTrip:
    def test_output_is_json_serializable(self):
        xml = _read_fixture("disqus_minimal.xml")
        result = get_normalized_document(xml, "disqus")
        output = json.dumps(result, indent=2)
        roundtrip = json.loads(output)
        assert roundtrip == result

    def test_all_threads_have_required_keys(self):
        xml = _read_fixture("disqus_minimal.xml")
        result = get_normalized_document(xml, "disqus")
        required = {"name", "id", "link", "title", "date", "timestamp", "comments", "metadata"}
        for name, thread in result.items():
            assert required.issubset(thread.keys()), f"thread '{name}' missing keys"

    def test_deleted_excluded(self):
        xml = _read_fixture("disqus_minimal.xml")
        result = get_normalized_document(xml, "disqus")
        for name, thread in result.items():
            for comment in thread["comments"]:
                assert comment["author"] != "Spam"


class TestGraphcommentRoundTrip:
    def test_output_is_json_serializable(self):
        xml = _read_fixture("graphcomment_minimal.xml")
        result = get_normalized_document(xml, "graphcomment", "https://mysite.io")
        output = json.dumps(result, indent=2)
        roundtrip = json.loads(output)
        assert roundtrip == result

    def test_site_filtering(self):
        xml = _read_fixture("graphcomment_minimal.xml")
        result = get_normalized_document(xml, "graphcomment", "https://mysite.io")
        for name, post in result.items():
            assert "mysite.io" in post["link"]
