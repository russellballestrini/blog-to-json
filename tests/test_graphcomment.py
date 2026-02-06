from blog_to_json.graphcomment import (
    get_comment_dict,
    get_comments_from_post,
    get_metadata_from_post,
    comment_cleaner,
    extract_name,
    graphcomment_xml_dict_to_normalized_dict,
)


class TestExtractName:
    def test_strips_slashes(self):
        assert extract_name("https://mysite.io/blog/my-post/") == "blog_my-post"

    def test_single_segment(self):
        assert extract_name("https://mysite.io/about/") == "about"

    def test_deep_path(self):
        assert extract_name("https://mysite.io/a/b/c/") == "a_b_c"


class TestCommentCleaner:
    def test_filters_by_site(self):
        posts = [
            {"link": "https://mysite.io/post1/"},
            {"link": "https://othersite.com/post2/"},
            {"link": "https://mysite.io/post3/"},
        ]
        result = comment_cleaner(posts, "https://mysite.io")
        assert len(result) == 2

    def test_empty_list(self):
        assert comment_cleaner([], "https://mysite.io") == []

    def test_no_matches(self):
        posts = [{"link": "https://othersite.com/x/"}]
        result = comment_cleaner(posts, "https://mysite.io")
        assert result == []


class TestGetCommentDict:
    def test_extracts_fields(self):
        comment = {
            "wp:comment_id": "300",
            "wp:comment_parent": "0",
            "wp:comment_author_IP": "10.10.10.1",
            "wp:comment_author": "Gina",
            "wp:comment_author_email": "gina@example.com",
            "wp:comment_content": "GC comment here.",
            "wp:comment_date": "2021-06-02 09:00:00",
        }
        result = get_comment_dict(comment)
        assert result["id"] == "300"
        assert result["author"] == "Gina"
        assert isinstance(result["timestamp"], int)


class TestGetCommentsFromPost:
    def test_no_comments(self):
        assert get_comments_from_post({"wp:post_id": "1"}) == []

    def test_single_comment(self):
        post = {
            "wp:comment": {
                "wp:comment_id": "1",
                "wp:comment_parent": "0",
                "wp:comment_author_IP": "1.1.1.1",
                "wp:comment_author": "Test",
                "wp:comment_author_email": "t@t.com",
                "wp:comment_content": "hi",
                "wp:comment_date": "2021-01-01 00:00:00",
            }
        }
        result = get_comments_from_post(post)
        assert len(result) == 1


class TestGetMetadataFromPost:
    def test_no_metadata(self):
        assert get_metadata_from_post({"wp:post_id": "1"}) == {}

    def test_with_metadata(self):
        post = {
            "wp:postmeta": [
                {"wp:meta_key": "key1", "wp:meta_value": "val1"},
            ]
        }
        result = get_metadata_from_post(post)
        assert result["key1"] == "val1"


class TestGraphcommentNormalize:
    def test_filters_by_site(self, graphcomment_doc):
        result = graphcomment_xml_dict_to_normalized_dict(
            graphcomment_doc, "https://mysite.io"
        )
        assert len(result) == 1

    def test_skips_attachments(self, graphcomment_doc):
        result = graphcomment_xml_dict_to_normalized_dict(
            graphcomment_doc, "https://mysite.io"
        )
        # attachment has same link prefix but type=attachment
        assert len(result) == 1

    def test_post_fields(self, graphcomment_doc):
        result = graphcomment_xml_dict_to_normalized_dict(
            graphcomment_doc, "https://mysite.io"
        )
        post = list(result.values())[0]
        assert post["title"] == "My GC Post"
        assert post["link"] == "https://mysite.io/blog/my-gc-post/"
        assert post["name"] == "blog_my-gc-post"
        assert isinstance(post["timestamp"], int)

    def test_comments_attached(self, graphcomment_doc):
        result = graphcomment_xml_dict_to_normalized_dict(
            graphcomment_doc, "https://mysite.io"
        )
        post = list(result.values())[0]
        assert len(post["comments"]) == 1
        assert post["comments"][0]["author"] == "Gina"

    def test_other_site_excluded(self, graphcomment_doc):
        result = graphcomment_xml_dict_to_normalized_dict(
            graphcomment_doc, "https://mysite.io"
        )
        for post in result.values():
            assert "othersite.com" not in post["link"]
