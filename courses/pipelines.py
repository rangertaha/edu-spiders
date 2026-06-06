import hashlib
from datetime import datetime

from elasticsearch import Elasticsearch


class ElasticsearchPipeline:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")

    def get_id(self, item):
        title = item.get("title")
        course_id = item.get("id")
        if course_id and title:
            return hashlib.md5(f"{course_id}{title}".encode()).hexdigest()
        return None

    def process_item(self, item, spider):
        item["timestamp"] = datetime.now()
        self.es.index(index="edu", id=self.get_id(item), document=dict(item))
        return item
