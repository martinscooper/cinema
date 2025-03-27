import os

from elasticsearch import Elasticsearch


def get_es_client():
    return Elasticsearch(
        f"https://{os.environ.get('ES_HOST', 'localhost')}:{os.environ.get('ES_PORT', 9200)}",
        verify_certs=False,
        basic_auth=("elastic", os.environ.get("ES_PASSWORD", "")),
    )


es_client = get_es_client()
