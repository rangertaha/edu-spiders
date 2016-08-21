# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime

from elasticsearch import Elasticsearch


class ElasticsearchPipeline(object):

    def __init__(self):
        self.es = Elasticsearch()

    def get_id(self, item):
        m = hashlib.md5()
        title = item.get('title', None)
        id = item.get('id', None)
        d = id + title
        if d:
            m.update(d)
            return m.hexdigest()

    def process_item(self, item, spider):
        id = self.get_id(item)
        item['timestamp'] = datetime.now()
        self.es.index(index="edu", doc_type="course", id=id, body=dict(item))
        return item
