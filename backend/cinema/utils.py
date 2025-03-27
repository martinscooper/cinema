from elasticsearch import Elasticsearch
from fastapi import HTTPException


def verify_es_connection(es: Elasticsearch):
    try:
        es.info()
    except Exception:
        raise HTTPException(400, "Failed to connect to elastic search")
