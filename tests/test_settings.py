"""Sanity checks for the Scrapy project settings."""

from scrapy.settings import Settings

from courses import settings


def test_project_identity():
    assert settings.BOT_NAME == "courses"
    assert settings.SPIDER_MODULES == ["courses.spiders"]
    assert settings.NEWSPIDER_MODULE == "courses.spiders"


def test_crawl_politeness():
    assert settings.AUTOTHROTTLE_ENABLED is True
    assert settings.CONCURRENT_REQUESTS_PER_DOMAIN == 5
    assert settings.DEPTH_LIMIT == 4
    assert settings.DOWNLOAD_TIMEOUT == 15


def test_feed_export_encoding():
    assert settings.FEED_EXPORT_ENCODING == "utf-8"


def test_ajaxcrawl_setting_removed():
    # AJAXCRAWL_ENABLED was removed along with Scrapy's AjaxCrawl middleware.
    assert not hasattr(settings, "AJAXCRAWL_ENABLED")


def test_settings_load_into_scrapy():
    loaded = Settings()
    loaded.setmodule("courses.settings")

    assert loaded.get("BOT_NAME") == "courses"
    assert loaded.getlist("SPIDER_MODULES") == ["courses.spiders"]
