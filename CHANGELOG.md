# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Offline pytest test suite (`tests/`) covering spider parsing against HTML
  fixtures, the Elasticsearch pipeline with a mocked client, settings sanity,
  and a `scrapy list` smoke test, with coverage reporting via pytest-cov.
- GitHub Actions CI workflow running Ruff, mypy, and the test suite on
  Python 3.12, 3.13, and 3.14.
- mypy and pytest/coverage configuration in `pyproject.toml`, plus a `dev`
  dependency group (pytest, pytest-cov, mypy).
- This changelog.
- Project metadata in `pyproject.toml`: SPDX license expression, authors,
  keywords, classifiers, and project URLs.

### Fixed

- `bhcc.mass.edu` and `extension.harvard.edu` spiders no longer raise a
  `TypeError` when the credits element is missing from a course page: the
  credits selector is extracted once and the field is set to `None` when
  absent, leaving output on well-formed pages unchanged.
- `umb.edu` spider no longer raises an `AttributeError` when the breadcrumb
  paragraph is missing from a course page; such incomplete items are skipped,
  consistent with its existing incomplete-course handling.

### Changed

- Raised the minimum supported Python version from 3.10 to 3.12
  (`requires-python = ">=3.12"`, Ruff target `py312`).
- Raised the Scrapy floor to `>=2.17,<3` and the elasticsearch client floor
  to `>=9.4,<10`.
- Rewrote the README: uv/virtualenv-based install instructions, documentation
  for all six spiders, Elasticsearch pipeline configuration, and badges.

### Removed

- The obsolete `AJAXCRAWL_ENABLED` setting (the AjaxCrawl middleware was
  deprecated and removed from Scrapy).

## [0.1.0] - 2026-06-06

First versioned state of the project. `pyproject.toml` was introduced with
version 0.1.0 in this release; everything before it was unversioned
development (2016-08-19 through 2016-10-21), which is folded in below.

### Added

- Scrapy project skeleton: `scrapy.cfg`, `courses` package with `settings.py`,
  `items.py` (the `Course` item: site, institute, id, title, description,
  credits, category, timestamp), and `pipelines.py` (2016-08-19).
- `bu.edu` spider for the Boston University academics catalog and
  `bhcc.mass.edu` spider for the Bunker Hill Community College course catalog
  (2016-08-19).
- `ElasticsearchPipeline` that indexes scraped courses into a local
  Elasticsearch `edu` index with an MD5 document id derived from the course
  id and title (2016-08-19).
- `suffolk.edu` spider for the Suffolk University course listings (2016-09-05).
- `umb.edu` spider for the University of Massachusetts Boston course catalog
  and `extension.harvard.edu` spider for the Harvard Extension School catalog
  (2016-09-18).
- `emerson.edu` spider for the Emerson College course descriptions page
  (2016-10-17).
- Sample CSV crawl output in `data/` and MIT license.
- `pyproject.toml` with project metadata, dependency floors
  (`Scrapy>=2.16,<3`, `elasticsearch>=9,<10`, `requires-python >= 3.10`), and
  Ruff lint/format configuration (2026-06-06).

### Changed

- Modernized the codebase for current Python and Scrapy (2026-06-06): removed
  Python 2 idioms (`object` base classes, coding cookies), switched selector
  calls to the `.get()`/`.getall()` API, and reorganized imports.
- Updated the Elasticsearch pipeline to the modern client API (2026-06-06):
  explicit `http://localhost:9200` endpoint, `document=` instead of the
  removed `doc_type`/`body` arguments, and a guarded `get_id()` that returns
  `None` when the course id or title is missing.
- Cleaned up `settings.py` and made the Elasticsearch pipeline opt-in
  (commented out in `ITEM_PIPELINES`) (2026-06-06).

[Unreleased]: https://github.com/rangertaha/edu-spiders/compare/e02ffc3...HEAD
[0.1.0]: https://github.com/rangertaha/edu-spiders/commits/e02ffc3
