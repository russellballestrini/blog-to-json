from blog_to_json.wordpress import (
    get_comment_dict,
    get_comments_from_post,
    get_metadata_from_post,
    wordpress_xml_dict_to_normalized_dict,
)


class TestGetCommentDict:
    def test_extracts_all_fields(self):
        comment = {
            "wp:comment_id": "100",
            "wp:comment_parent": "0",
            "wp:comment_author_IP": "192.168.1.1",
            "wp:comment_author": "Alice",
            "wp:comment_author_email": "alice@example.com",
            "wp:comment_content": "Great post!",
            "wp:comment_date": "2020-01-16 08:00:00",
        }
        result = get_comment_dict(comment)
        assert result["id"] == 100
        assert result["parent_id"] == 0
        assert result["author"] == "Alice"
        assert result["email"] == "alice@example.com"
        assert result["author_ip"] == "192.168.1.1"
        assert result["content"] == "Great post!"
        assert result["date"] == "2020-01-16 08:00:00"
        assert isinstance(result["timestamp"], int)

    def test_casts_ids_to_int(self):
        comment = {
            "wp:comment_id": "42",
            "wp:comment_parent": "10",
            "wp:comment_author_IP": "1.2.3.4",
            "wp:comment_author": "Test",
            "wp:comment_author_email": "t@t.com",
            "wp:comment_content": "test",
            "wp:comment_date": "2020-01-01 00:00:00",
        }
        result = get_comment_dict(comment)
        assert isinstance(result["id"], int)
        assert isinstance(result["parent_id"], int)


class TestGetCommentsFromPost:
    def test_no_comments(self):
        post = {"wp:post_id": "1"}
        assert get_comments_from_post(post) == []

    def test_single_comment_as_dict(self):
        # xmltodict returns a single comment as dict, not list
        post = {
            "wp:comment": {
                "wp:comment_id": "1",
                "wp:comment_parent": "0",
                "wp:comment_author_IP": "1.1.1.1",
                "wp:comment_author": "Solo",
                "wp:comment_author_email": "solo@example.com",
                "wp:comment_content": "Only one",
                "wp:comment_date": "2020-01-01 00:00:00",
            }
        }
        result = get_comments_from_post(post)
        assert len(result) == 1
        assert result[0]["author"] == "Solo"

    def test_multiple_comments_as_list(self):
        post = {
            "wp:comment": [
                {
                    "wp:comment_id": "1",
                    "wp:comment_parent": "0",
                    "wp:comment_author_IP": "1.1.1.1",
                    "wp:comment_author": "A",
                    "wp:comment_author_email": "a@a.com",
                    "wp:comment_content": "first",
                    "wp:comment_date": "2020-01-01 00:00:00",
                },
                {
                    "wp:comment_id": "2",
                    "wp:comment_parent": "1",
                    "wp:comment_author_IP": "2.2.2.2",
                    "wp:comment_author": "B",
                    "wp:comment_author_email": "b@b.com",
                    "wp:comment_content": "second",
                    "wp:comment_date": "2020-01-02 00:00:00",
                },
            ]
        }
        result = get_comments_from_post(post)
        assert len(result) == 2


class TestGetMetadataFromPost:
    def test_no_metadata(self):
        assert get_metadata_from_post({"wp:post_id": "1"}) == {}

    def test_extracts_metadata(self):
        post = {
            "wp:postmeta": [
                {"wp:meta_key": "_edit_last", "wp:meta_value": "1"},
                {"wp:meta_key": "_thumbnail_id", "wp:meta_value": "42"},
            ]
        }
        result = get_metadata_from_post(post)
        assert result["_edit_last"] == "1"
        assert result["_thumbnail_id"] == "42"

    def test_skips_non_dict_meta(self):
        # edge case: postmeta might contain non-dict entries
        post = {
            "wp:postmeta": [
                {"wp:meta_key": "valid", "wp:meta_value": "yes"},
                "some_string_entry",
            ]
        }
        result = get_metadata_from_post(post)
        assert result == {"valid": "yes"}


class TestWordpressNormalize:
    def test_full_parse(self, wordpress_doc):
        result = wordpress_xml_dict_to_normalized_dict(wordpress_doc)
        assert "hello-world" in result
        assert "no-comments" in result
        assert "single-comment" in result

    def test_skips_attachments(self, wordpress_doc):
        result = wordpress_xml_dict_to_normalized_dict(wordpress_doc)
        # attachment has post_name "hello-world" but should not overwrite the post
        assert result["hello-world"]["id"] == "1"

    def test_post_fields(self, wordpress_doc):
        result = wordpress_xml_dict_to_normalized_dict(wordpress_doc)
        post = result["hello-world"]
        assert post["name"] == "hello-world"
        assert post["title"] == "Hello World"
        assert post["link"] == "https://example.com/hello-world"
        assert "<p>Hello world content.</p>" in post["content"]
        assert post["date"] == "2020-01-15 10:30:00"
        assert isinstance(post["timestamp"], int)

    def test_comments_attached(self, wordpress_doc):
        result = wordpress_xml_dict_to_normalized_dict(wordpress_doc)
        comments = result["hello-world"]["comments"]
        assert len(comments) == 2
        assert comments[0]["author"] == "Alice"
        assert comments[1]["parent_id"] == 100

    def test_no_comments_post(self, wordpress_doc):
        result = wordpress_xml_dict_to_normalized_dict(wordpress_doc)
        assert result["no-comments"]["comments"] == []

    def test_single_comment_post(self, wordpress_doc):
        result = wordpress_xml_dict_to_normalized_dict(wordpress_doc)
        comments = result["single-comment"]["comments"]
        assert len(comments) == 1
        assert comments[0]["author"] == "Charlie"

    def test_metadata_extracted(self, wordpress_doc):
        result = wordpress_xml_dict_to_normalized_dict(wordpress_doc)
        meta = result["hello-world"]["metadata"]
        assert "_edit_last" in meta
        assert "_thumbnail_id" in meta
