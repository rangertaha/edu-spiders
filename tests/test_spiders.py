"""Offline tests for each spider's parsing logic, fed saved HTML fixtures."""

from courses.spiders import bhcc, bu, emerson, harvard_extension, suffolk, umb


def test_bu_parse_item(response_from):
    spider = bu.EduSpider()
    response = response_from("bu.html", "http://www.bu.edu/academics/cas/courses/cas-cs-111/")

    items = list(spider.parse_item(response))

    assert len(items) == 1
    item = items[0]
    assert item["institute"] == "Boston University"
    assert item["site"] == "www.bu.edu"
    assert item["title"] == "Introduction to Computer Science"
    assert item["id"] == "CAS CS 111"
    assert item["credits"] == "4"
    assert item["description"] == "An introduction to computer science covering programming fundamentals."


def test_umb_parse_item(response_from):
    spider = umb.EduSpider()
    response = response_from("umb.html", "https://www.umb.edu/academics/course_catalog/course_info/ugrd_CS_all_110")

    items = list(spider.parse_item(response))

    assert len(items) == 1
    item = items[0]
    assert item["institute"] == "University of Massachusetts Boston"
    assert item["site"] == "www.umb.edu"
    assert item["title"] == "Introduction to Programming"
    assert item["id"] == "CS 110"
    assert item["credits"] == "3"
    assert item["description"] == "An introductory programming course using Python."


def test_umb_skips_incomplete_course(response_from):
    spider = umb.EduSpider()
    response = response_from(
        "umb_incomplete.html", "https://www.umb.edu/academics/course_catalog/course_info/grad_CS_all_999"
    )

    items = list(spider.parse_item(response))

    assert items == []


def test_umb_missing_breadcrumb_skips_course(response_from):
    spider = umb.EduSpider()
    response = response_from(
        "umb_missing_breadcrumb.html", "https://www.umb.edu/academics/course_catalog/course_info/ugrd_CS_all_500"
    )

    items = list(spider.parse_item(response))

    assert items == []


def test_umb_clean():
    spider = umb.EduSpider()

    assert spider.clean(["3", "4"]) == "3"
    assert spider.clean([]) is None


def test_bhcc_parse_item(response_from):
    spider = bhcc.EduSpider()
    response = response_from("bhcc.html", "http://www.bhcc.mass.edu/catalog/courses/index.php?dept=ACC")

    items = list(spider.parse_item(response))

    assert len(items) == 2
    first, second = items
    assert first["institute"] == "Bunker Hill Community College"
    assert first["site"] == "www.bhcc.mass.edu"
    assert first["title"] == "Financial Accounting"
    assert first["id"] == "ACC-101"
    assert first["credits"] == "3"
    assert first["description"] == "An introduction to financial accounting principles."
    assert first["category"] == "Accounting"
    assert second["id"] == "ACC-102"
    assert second["credits"] == "4"


def test_bhcc_missing_credits_yields_none(response_from):
    spider = bhcc.EduSpider()
    response = response_from("bhcc_missing_credits.html", "http://www.bhcc.mass.edu/catalog/courses/index.php?dept=ACC")

    items = list(spider.parse_item(response))

    assert len(items) == 1
    item = items[0]
    assert item["title"] == "Accounting Seminar"
    assert item["id"] == "ACC-103"
    assert item["credits"] is None


def test_suffolk_parse_item(response_from):
    spider = suffolk.EduSpider()
    response = response_from("suffolk.html", "http://www.suffolk.edu/college/departments/12345.php")

    items = list(spider.parse_item(response))

    assert len(items) == 1
    item = items[0]
    assert item["institute"] == "Suffolk University"
    assert item["site"] == "www.suffolk.edu"
    assert item["title"] == "ACC-201 Intermediate Accounting"
    assert item["id"] == "ACC-201"
    assert item["credits"] == 4.0
    assert item["description"] == "A deeper study of accounting theory and practice."
    assert item["category"] == "Lecture"


def test_emerson_parse(response_from):
    spider = emerson.EduSpider()
    response = response_from("emerson.html", "http://www.emerson.edu/academics/courses/descriptions")

    items = list(spider.parse(response))

    assert len(items) == 2
    first, second = items
    assert first["institute"] == "Emerson College"
    assert first["site"] == "www.emerson.edu"
    assert first["title"] == "Introduction to Communication"
    assert first["credits"] == "4 credits"
    assert first["id"] == ["CC101"]
    assert first["category"] == ["CC"]
    assert "Foundations of human communication" in first["description"]
    assert second["id"] == ["JR205"]
    assert second["title"] == "News Writing"


def test_harvard_extension_parse_item(response_from):
    spider = harvard_extension.EduSpider()
    response = response_from("harvard.html", "http://www.extension.harvard.edu/academics/courses/data-science/10101")

    items = list(spider.parse_item(response))

    assert len(items) == 1
    item = items[0]
    assert item["institute"] == "Harvard University Extension School"
    assert item["site"] == "www.extension.harvard.edu"
    assert item["title"] == "Introduction to Data Science"
    assert item["id"] == "CSCI E-101"
    assert item["credits"] == "4"
    assert item["description"] == "Fundamentals of data science with hands-on projects."


def test_harvard_extension_missing_credits_yields_none(response_from):
    spider = harvard_extension.EduSpider()
    response = response_from(
        "harvard_missing_credits.html", "http://www.extension.harvard.edu/academics/courses/data-science/10102"
    )

    items = list(spider.parse_item(response))

    assert len(items) == 1
    item = items[0]
    assert item["title"] == "Introduction to Data Science"
    assert item["id"] == "CSCI E-101"
    assert item["credits"] is None
