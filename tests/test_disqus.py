from blog_to_json.disqus import (
    get_comment_dict,
    get_comments_from_post,
    disqus_xml_dict_to_normalized_dict,
)


class TestGetCommentDict:
    def test_root_comment_no_parent(self):
        comment = {
            "@dsq:id": "5001",
            "message": "Nice article!",
            "createdAt": "2019-03-02T08:30:00Z",
            "author": {"name": "Dave", "email": "dave@example.com"},
            "ipAddress": "172.16.0.1",
        }
        result = get_comment_dict(comment, "1001")
        assert result["id"] == 5001
        assert result["parent_id"] == 0
        assert result["author"] == "Dave"
        assert result["email"] == "dave@example.com"
        assert result["content"] == "Nice article!"
        assert result["author_ip"] == "172.16.0.1"
        assert isinstance(result["timestamp"], int)

    def test_reply_with_parent(self):
        comment = {
            "@dsq:id": "5002",
            "parent": {"@dsq:id": "5001"},
            "message": "I agree.",
            "createdAt": "2019-03-02T09:00:00Z",
            "author": {"name": "Eve", "email": "eve@example.com"},
            "ipAddress": "172.16.0.2",
        }
        result = get_comment_dict(comment, "1001")
        assert result["parent_id"] == 5001

    def test_missing_email(self):
        comment = {
            "@dsq:id": "5004",
            "message": "No email.",
            "createdAt": "2019-04-02T11:00:00Z",
            "author": {"name": "Frank"},
            "ipAddress": "172.16.0.3",
        }
        result = get_comment_dict(comment, "1002")
        assert result["email"] is None


class TestGetCommentsFromPost:
    def test_filters_by_thread_id(self):
        posts = [
            {
                "@dsq:id": "5001",
                "thread": {"@dsq:id": "1001"},
                "message": "yes",
                "createdAt": "2019-03-02T08:30:00Z",
                "isDeleted": "false",
                "author": {"name": "Dave", "email": "d@d.com"},
                "ipAddress": "1.1.1.1",
            },
            {
                "@dsq:id": "5004",
                "thread": {"@dsq:id": "1002"},
                "message": "other thread",
                "createdAt": "2019-04-02T11:00:00Z",
                "isDeleted": "false",
                "author": {"name": "Frank"},
                "ipAddress": "2.2.2.2",
            },
        ]
        result = get_comments_from_post("1001", posts)
        assert len(result) == 1
        assert result[0]["id"] == 5001

    def test_excludes_deleted(self):
        posts = [
            {
                "@dsq:id": "5001",
                "thread": {"@dsq:id": "1001"},
                "message": "keep",
                "createdAt": "2019-03-02T08:30:00Z",
                "isDeleted": "false",
                "author": {"name": "A"},
                "ipAddress": "1.1.1.1",
            },
            {
                "@dsq:id": "5003",
                "thread": {"@dsq:id": "1001"},
                "message": "deleted",
                "createdAt": "2019-03-02T10:00:00Z",
                "isDeleted": "true",
                "author": {"name": "Spam"},
                "ipAddress": "9.9.9.9",
            },
        ]
        result = get_comments_from_post("1001", posts)
        assert len(result) == 1
        assert result[0]["content"] == "keep"

    def test_empty_when_no_match(self):
        posts = [
            {
                "@dsq:id": "5001",
                "thread": {"@dsq:id": "1001"},
                "message": "x",
                "createdAt": "2019-03-02T08:30:00Z",
                "isDeleted": "false",
                "author": {"name": "A"},
                "ipAddress": "1.1.1.1",
            },
        ]
        result = get_comments_from_post("9999", posts)
        assert result == []


class TestDisqusNormalize:
    def test_full_parse(self, disqus_doc):
        result = disqus_xml_dict_to_normalized_dict(disqus_doc)
        # two threads
        assert len(result) == 2

    def test_thread_fields(self, disqus_doc):
        result = disqus_xml_dict_to_normalized_dict(disqus_doc)
        # find the first-post thread by checking values
        found = None
        for key, val in result.items():
            if val["title"] == "First Post":
                found = val
                break
        assert found is not None
        assert found["id"] == "1001"
        assert found["link"] == "https://example.com/first-post/"
        assert isinstance(found["timestamp"], int)
        assert found["metadata"] == {}

    def test_deleted_comments_excluded(self, disqus_doc):
        result = disqus_xml_dict_to_normalized_dict(disqus_doc)
        for key, val in result.items():
            if val["title"] == "First Post":
                # 3 posts for thread 1001, but 1 is deleted
                assert len(val["comments"]) == 2
                break

    def test_second_thread_comments(self, disqus_doc):
        result = disqus_xml_dict_to_normalized_dict(disqus_doc)
        for key, val in result.items():
            if val["title"] == "Second Post":
                assert len(val["comments"]) == 1
                assert val["comments"][0]["author"] == "Frank"
                break
