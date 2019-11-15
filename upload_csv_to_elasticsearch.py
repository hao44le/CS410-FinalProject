from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import pandas as pd
import json
from dateutil import parser

host = 'search-chinesek12-sp2avv7lleofzv5qu5m6qkk4by.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-2' # e.g. us-west-1

service = 'es'
awsauth = AWS4Auth("AKIATMPP3NOWTKDPP2BX", "+qT9m84DoyWHTf1vs9e6C7exDMEKkU84Dru9O23k", region, service)
index = "chinesek12_wechat_article"
es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)
#K12_chinese_wechat_articles
csv_name = "small_test.csv"

def read_csv_and_write_to_es():
    csv = pd.read_csv(csv_name)
    json_array = json.loads(csv.to_json(orient='index'))
    for x in range(0, len(json_array)):
        document = json_array[str(x)]
        document["发布时间"] = parser.parse(document["发布时间"])
        es.index(index=index, doc_type="_doc", id=str(x), body=document)

if __name__ == '__main__':
    res = es.search(index=index, body = {'size' : 10000,'query': {'match_all' : {}}})
    print(res)
