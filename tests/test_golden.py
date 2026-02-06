"""Golden file tests: verify parsers reproduce frozen output from real blog exports.

These XML files are irreplaceable — the original blogs are offline.
See tests/fixtures/golden/README for provenance.
"""
import os
import json
import pytest
import xmltodict
from blog_to_json import (
    wordpress_xml_dict_to_normalized_dict,
    disqus_xml_dict_to_normalized_dict,
)

GOLDEN_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "golden")


def _golden_path(name):
    return os.path.join(GOLDEN_DIR, name)


WORDPRESS_CASES = [
    ("russellballestrini.wordpress.2017-09-05.xml", "russellballestrini.wordpress.json"),
    ("printableprompts.WordPress.2022-05-18.xml", "printableprompts.json"),
    ("wingitmom.WordPress.2022-05-18.xml", "wingitmom.com.json"),
]

DISQUS_CASES = [
    ("brettterpstra-2019-03-01T21_42_06.627201-all.xml", "brettterpstra.json"),
]


class TestWordpressGolden:
    @pytest.mark.parametrize("xml_file,json_file", WORDPRESS_CASES)
    def test_output_matches_golden(self, xml_file, json_file):
        with open(_golden_path(xml_file)) as f:
            doc = xmltodict.parse(f.read())
        with open(_golden_path(json_file)) as f:
            expected = json.load(f)

        result = wordpress_xml_dict_to_normalized_dict(doc)
        # round-trip through JSON to normalize types (OrderedDict → dict)
        result = json.loads(json.dumps(result))

        assert len(result) == len(expected), (
            f"post count mismatch: got {len(result)}, expected {len(expected)}"
        )
        assert result == expected

    @pytest.mark.parametrize("xml_file,json_file", WORDPRESS_CASES)
    def test_post_keys_stable(self, xml_file, json_file):
        with open(_golden_path(json_file)) as f:
            expected = json.load(f)
        required = {"name", "id", "link", "title", "content", "date", "timestamp", "comments", "metadata"}
        for name, post in expected.items():
            assert required.issubset(post.keys()), f"{json_file}: post '{name}' missing keys"


class TestDisqusGolden:
    @pytest.mark.parametrize("xml_file,json_file", DISQUS_CASES)
    def test_output_matches_golden(self, xml_file, json_file):
        with open(_golden_path(xml_file)) as f:
            doc = xmltodict.parse(f.read())
        with open(_golden_path(json_file)) as f:
            expected = json.load(f)

        result = disqus_xml_dict_to_normalized_dict(doc)
        result = json.loads(json.dumps(result))

        assert len(result) == len(expected), (
            f"thread count mismatch: got {len(result)}, expected {len(expected)}"
        )
        assert result == expected

    @pytest.mark.parametrize("xml_file,json_file", DISQUS_CASES)
    def test_thread_keys_stable(self, xml_file, json_file):
        with open(_golden_path(json_file)) as f:
            expected = json.load(f)
        required = {"name", "id", "link", "title", "date", "timestamp", "comments", "metadata"}
        for name, thread in expected.items():
            assert required.issubset(thread.keys()), f"{json_file}: thread '{name}' missing keys"
