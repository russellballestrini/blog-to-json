"""CLI smoke tests: run entry points as subprocesses, verify exit code + valid JSON."""
import os
import json
import subprocess
import sys
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
GOLDEN_DIR = os.path.join(FIXTURES_DIR, "golden")
PYTHON = sys.executable


def _run_cli(module_func, *args):
    """Run a blog_to_json CLI entry point as a subprocess."""
    cmd = [PYTHON, "-c", f"from blog_to_json.__main__ import {module_func}; {module_func}()"] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=30)


class TestWordpressCLI:
    def test_exit_zero(self):
        result = _run_cli("main_wordpress", os.path.join(FIXTURES_DIR, "wordpress_minimal.xml"))
        assert result.returncode == 0, result.stderr

    def test_stdout_is_valid_json(self):
        result = _run_cli("main_wordpress", os.path.join(FIXTURES_DIR, "wordpress_minimal.xml"))
        output = json.loads(result.stdout)
        assert isinstance(output, dict)
        assert "hello-world" in output

    def test_golden_file(self):
        result = _run_cli(
            "main_wordpress",
            os.path.join(GOLDEN_DIR, "printableprompts.WordPress.2022-05-18.xml"),
        )
        assert result.returncode == 0, result.stderr
        output = json.loads(result.stdout)
        with open(os.path.join(GOLDEN_DIR, "printableprompts.json")) as f:
            expected = json.load(f)
        assert output == expected


class TestDisqusCLI:
    def test_exit_zero(self):
        result = _run_cli("main_disqus", os.path.join(FIXTURES_DIR, "disqus_minimal.xml"))
        assert result.returncode == 0, result.stderr

    def test_stdout_is_valid_json(self):
        result = _run_cli("main_disqus", os.path.join(FIXTURES_DIR, "disqus_minimal.xml"))
        output = json.loads(result.stdout)
        assert isinstance(output, dict)
        assert len(output) == 2


class TestGraphcommentCLI:
    def test_exit_zero(self):
        result = _run_cli(
            "main_graphcomment",
            os.path.join(FIXTURES_DIR, "graphcomment_minimal.xml"),
            "--host", "https://mysite.io",
        )
        assert result.returncode == 0, result.stderr

    def test_stdout_is_valid_json(self):
        result = _run_cli(
            "main_graphcomment",
            os.path.join(FIXTURES_DIR, "graphcomment_minimal.xml"),
            "--host", "https://mysite.io",
        )
        output = json.loads(result.stdout)
        assert isinstance(output, dict)
        assert len(output) == 1

    def test_default_host(self):
        # without --host it uses the default; graphcomment_minimal has no
        # posts matching the default host, so output should be empty
        result = _run_cli(
            "main_graphcomment",
            os.path.join(FIXTURES_DIR, "graphcomment_minimal.xml"),
        )
        assert result.returncode == 0, result.stderr
        output = json.loads(result.stdout)
        assert output == {}


class TestGenericCLI:
    def test_wordpress_via_type_flag(self):
        result = _run_cli(
            "main",
            os.path.join(FIXTURES_DIR, "wordpress_minimal.xml"),
            "--type", "wordpress",
        )
        assert result.returncode == 0, result.stderr
        output = json.loads(result.stdout)
        assert "hello-world" in output

    def test_disqus_via_type_flag(self):
        result = _run_cli(
            "main",
            os.path.join(FIXTURES_DIR, "disqus_minimal.xml"),
            "--type", "disqus",
        )
        assert result.returncode == 0, result.stderr
        output = json.loads(result.stdout)
        assert len(output) == 2

    def test_missing_file_exits_nonzero(self):
        result = _run_cli("main_wordpress", "/nonexistent/file.xml")
        assert result.returncode != 0

    def test_no_args_exits_nonzero(self):
        result = _run_cli("main_wordpress")
        assert result.returncode != 0
