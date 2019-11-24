from elasticsearch import helpers, Elasticsearch
import csv
import sys
from common import get_es_instance

es = get_es_instance()

with open(sys.argv[1]) as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index=sys.argv[2], doc_type='doc')
