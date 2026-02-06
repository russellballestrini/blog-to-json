# blog-to-json — Terrain Report

**Date:** 2026-02-06
**Agent:** blackops
**Status:** 73 tests passing, 0 failing, 0 warnings

## What This Repo Does

Converts blog export XML dumps (WordPress, Disqus, GraphComment) into normalized JSON. Three parsers, one CLI, one output shape.

## Source Map

```
blog_to_json/
├── __init__.py          # re-exports the 3 normalizer functions
├── __main__.py          # CLI: argparse, routing, JSON output
├── utils.py             # timestamp parsing (wordpress + disqus formats)
├── wordpress.py         # WordPress XML → normalized dict
├── disqus.py            # Disqus XML → normalized dict
└── graphcomment.py      # GraphComment XML → normalized dict
```

## Test Suite

```
make test     # 73 tests in ~5s
```

### Unit Tests

| File | Tests | Covers |
|------|-------|--------|
| `test_utils.py` | 10 | timestamp parsing, format validation, error paths |
| `test_wordpress.py` | 10 | comment extraction (0/1/N), metadata, attachment skipping, full normalize |
| `test_disqus.py` | 10 | root/reply/missing-email comments, thread filtering, deleted exclusion, full normalize |
| `test_graphcomment.py` | 11 | `extract_name`, `comment_cleaner`, site filtering, attachment skipping, full normalize |
| `test_main.py` | 5 | `get_normalized_document` routing (all 3 types + invalid), parser creation |

### Integration Tests

| File | Tests | Covers |
|------|-------|--------|
| `test_integration.py` | 9 | JSON round-trip for all 3 parsers, required keys on posts/comments/threads, parent-child chains, deleted exclusion |

### Golden File Tests

| File | Tests | Covers |
|------|-------|--------|
| `test_golden.py` | 8 | Exact output match against frozen JSON for 4 real blog exports (3 WordPress + 1 Disqus), key stability checks |

### Fixtures

**Synthetic** (`tests/fixtures/`): Small hand-crafted XML for each parser. Deterministic, no PII.

**Golden** (`tests/fixtures/golden/`): Real blog exports that cannot be recreated. See `tests/fixtures/golden/README` for provenance. These are tracked in git despite the global `*.xml`/`*.json` ignore rules.

| XML | JSON | Parser | Verified |
|-----|------|--------|----------|
| `russellballestrini.wordpress.2017-09-05.xml` | `russellballestrini.wordpress.json` | wordpress | regenerated from 2017 export |
| `printableprompts.WordPress.2022-05-18.xml` | `printableprompts.json` | wordpress | exact match |
| `wingitmom.WordPress.2022-05-18.xml` | `wingitmom.com.json` | wordpress | exact match |
| `brettterpstra-...all.xml` | `brettterpstra.json` | disqus | exact match |

The 2016 russellballestrini XML is also preserved for archival but is not used in tests (the 2017 export is more complete — 13 posts gained comments between exports).

## Defect Fixed

`blog_to_json/__main__.py:43` — changed `is not` to `!=` for string comparison. Was a `SyntaxWarning` in Python 3.12, potential silent failure in other runtimes.

## Build System

```
make install-dev    # create .venv, install runtime + test deps
make test           # run pytest
make update-golden  # regenerate golden JSON (review diff before committing)
make clean          # nuke build artifacts
```

## What's Not Covered Yet

- **CLI smoke tests**: Running entry points as subprocesses (`wordpress-xml-to-json`, etc.) to test argparse + stdout end-to-end. Medium lift — needs subprocess orchestration and temp file handling.
- **GraphComment golden files**: No real GraphComment XML export exists in the repo. If one surfaces, add it to `tests/fixtures/golden/`.
- **Edge cases in real data**: The golden tests catch regressions but don't assert specific edge cases within the real exports (e.g. posts with unusual metadata, empty content, unicode). Could be mined from the golden XMLs if needed.
- **Error handling paths**: The parsers assume well-formed XML. No tests for malformed input, missing required keys, or partial exports. Low priority unless the parsers are used on untrusted input.
