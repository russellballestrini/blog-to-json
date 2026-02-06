from datetime import datetime
from blog_to_json.utils import (
    make_timestamp_from_datetime,
    get_wordpress_timestamp,
    get_disqus_timestamp,
)


class TestMakeTimestamp:
    def test_returns_int(self):
        dt = datetime(2020, 1, 1, 0, 0, 0)
        result = make_timestamp_from_datetime(dt)
        assert isinstance(result, int)

    def test_epoch(self):
        dt = datetime(1970, 1, 1, 0, 0, 0)
        result = make_timestamp_from_datetime(dt)
        # mktime uses local time, so just verify it returns an int
        assert isinstance(result, int)

    def test_known_date(self):
        dt = datetime(2020, 6, 15, 12, 0, 0)
        result = make_timestamp_from_datetime(dt)
        assert result > 0


class TestGetWordpressTimestamp:
    def test_valid_format(self):
        result = get_wordpress_timestamp("2020-01-15 10:30:00")
        assert isinstance(result, int)
        assert result > 0

    def test_different_dates_differ(self):
        t1 = get_wordpress_timestamp("2020-01-01 00:00:00")
        t2 = get_wordpress_timestamp("2020-06-01 00:00:00")
        assert t2 > t1

    def test_invalid_format_raises(self):
        import pytest
        with pytest.raises(ValueError):
            get_wordpress_timestamp("01/15/2020 10:30")

    def test_midnight(self):
        result = get_wordpress_timestamp("2020-01-01 00:00:00")
        assert isinstance(result, int)


class TestGetDisqusTimestamp:
    def test_valid_format(self):
        result = get_disqus_timestamp("2019-03-01T12:00:00Z")
        assert isinstance(result, int)
        assert result > 0

    def test_different_dates_differ(self):
        t1 = get_disqus_timestamp("2019-01-01T00:00:00Z")
        t2 = get_disqus_timestamp("2019-06-01T00:00:00Z")
        assert t2 > t1

    def test_invalid_format_raises(self):
        import pytest
        with pytest.raises(ValueError):
            get_disqus_timestamp("2019-03-01 12:00:00")
