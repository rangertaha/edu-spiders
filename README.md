# edu-spiders

[![CI](https://github.com/rangertaha/edu-spiders/actions/workflows/ci.yml/badge.svg)](https://github.com/rangertaha/edu-spiders/actions/workflows/ci.yml)
[![Python 3.12 | 3.13 | 3.14](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What is it

A [Scrapy](https://scrapy.org/) application that crawls course catalogs of
Boston-area educational institutes. Each spider scrapes course data (id,
title, description, credits, category) from a school's online catalog and can
write it to CSV/JSON feeds or index it directly into Elasticsearch.

## Install

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```console
$ git clone https://github.com/rangertaha/edu-spiders.git
$ cd edu-spiders
$ uv sync
```

`uv sync` creates a `.venv` and installs Scrapy and the Elasticsearch client.
Prefix commands with `uv run`, or activate the venv with
`source .venv/bin/activate`.

## Usage

List the available spiders:

```console
$ uv run scrapy list
bhcc.mass.edu
bu.edu
emerson.edu
extension.harvard.edu
suffolk.edu
umb.edu
```

Run a spider and write its output to a CSV feed (`-O` overwrites; the
`:<format>` suffix selects the exporter):

```console
$ uv run scrapy crawl bu.edu -O data/bu.edu.csv:csv
```

Crawl output is conventionally written to the `data/` directory. JSON and
JSON-lines work the same way, e.g. `-O data/bu.edu.json:json`.

### Spiders

| Spider name             | Institute                           | Start page                                                   |
| ----------------------- | ----------------------------------- | ------------------------------------------------------------ |
| `bhcc.mass.edu`         | Bunker Hill Community College       | `www.bhcc.mass.edu/catalog/courses/`                         |
| `bu.edu`                | Boston University                   | `www.bu.edu/academics/`                                      |
| `emerson.edu`           | Emerson College                     | `www.emerson.edu/academics/courses/descriptions`             |
| `extension.harvard.edu` | Harvard University Extension School | `www.extension.harvard.edu/academics/courses/course-catalog` |
| `suffolk.edu`           | Suffolk University                  | `www.suffolk.edu/college/departments.php`                    |
| `umb.edu`               | University of Massachusetts Boston  | `www.umb.edu/academics/course_catalog`                       |

Each spider is run the same way: `uv run scrapy crawl <spider name> [-O <file>:<format>]`.

## Configuration

Project-wide settings live in [`courses/settings.py`](courses/settings.py)
(AutoThrottle, download delays, depth limit, user agent, etc.). Any setting
can be overridden per run with `-s NAME=value`.

### Elasticsearch pipeline

`courses.pipelines.ElasticsearchPipeline` indexes every scraped course into
the `edu` index of an Elasticsearch node at `http://localhost:9200`, using an
MD5 hash of the course id and title as the document id. It is disabled by
default; enable it by uncommenting `ITEM_PIPELINES` in `courses/settings.py`:

```python
ITEM_PIPELINES = {
    "courses.pipelines.ElasticsearchPipeline": 300,
}
```

or per run:

```console
$ uv run scrapy crawl bu.edu -s ITEM_PIPELINES='{"courses.pipelines.ElasticsearchPipeline": 300}'
```

## Development

Install dev dependencies and run the offline test suite (no network or
Elasticsearch required):

```console
$ uv sync --group dev
$ uv run pytest --cov
```

Lint, format, and type-check:

```console
$ uvx ruff check .
$ uvx ruff format .
$ uv run mypy
```

CI runs the same checks on Python 3.12, 3.13, and 3.14. See
[CHANGELOG.md](CHANGELOG.md) for release history.
