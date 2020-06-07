from datetime import datetime
from elasticsearch import Elasticsearch


class MediaStore():
    es_service = None

    def __init__(self):
        self.es_service = Elasticsearch([{
            "host": "elasticsearch",
            "port": 9200
        }])

    def store_tag_popularity(self, tag='', tag_posts=0, tag_popular_posts=''):
        self.es_service.indices.create(index='tag_popularity', ignore=400)
        self.es_service.index(index='tag_popularity',
                              doc_type='tag',
                              body={
                                  "tag_name": tag,
                                  "tag_posts": tag_posts,
                                  "timestamp": datetime.now(),
                                  "tag_popular_posts": tag_popular_posts
                              })
