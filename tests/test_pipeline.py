"""Tests for the Elasticsearch pipeline with a mocked client (no live ES)."""

import hashlib
from datetime import datetime
from unittest.mock import patch

import pytest

from courses.items import Course
from courses.pipelines import ElasticsearchPipeline


@pytest.fixture
def pipeline():
    with patch("courses.pipelines.Elasticsearch"):
        yield ElasticsearchPipeline()


def test_connects_to_local_elasticsearch():
    with patch("courses.pipelines.Elasticsearch") as mock_es_cls:
        ElasticsearchPipeline()

    mock_es_cls.assert_called_once_with("http://localhost:9200")


def test_get_id_hashes_id_and_title(pipeline):
    item = Course(id="CS 111", title="Intro")

    expected = hashlib.md5(b"CS 111Intro").hexdigest()
    assert pipeline.get_id(item) == expected


def test_get_id_returns_none_when_fields_missing(pipeline):
    assert pipeline.get_id(Course(title="Intro")) is None
    assert pipeline.get_id(Course(id="CS 111")) is None
    assert pipeline.get_id(Course()) is None


def test_process_item_indexes_document(pipeline):
    item = Course(id="CS 111", title="Intro", description="A course.")

    result = pipeline.process_item(item, spider=None)

    assert result is item
    assert isinstance(item["timestamp"], datetime)
    pipeline.es.index.assert_called_once()
    kwargs = pipeline.es.index.call_args.kwargs
    assert kwargs["index"] == "edu"
    assert kwargs["id"] == hashlib.md5(b"CS 111Intro").hexdigest()
    assert kwargs["document"]["title"] == "Intro"
    assert kwargs["document"]["description"] == "A course."


def test_course_item_fields():
    expected = {"site", "institute", "id", "title", "description", "credits", "category", "timestamp"}

    assert set(Course.fields) == expected
