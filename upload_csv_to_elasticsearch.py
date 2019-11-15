from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
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
csv_name = "K12_chinese_wechat_articles.csv"

previous_cache = 0

def read_csv_and_write_to_es():
    csv = pd.read_csv(csv_name)
    json_array = json.loads(csv.to_json(orient='index'))
    actions_array = []

    for x in range(0, len(json_array)):
        if x < previous_cache: continue
        print("{}/{}".format(x, len(json_array)))
        document = json_array[str(x)]
        try:
            document["发布时间"] = parser.parse(document["发布时间"])
        except:
            continue
        # es.index(index=index, doc_type="_doc", id=str(x), body=document)
        document['_id'] = str(x)
        document['_type'] = "_doc"
        document["_index"] = index
        actions_array.append(document)

    try:
        # make the bulk call, and get a response
        response = helpers.bulk(es, actions_array, chunk_size=1000, request_timeout=200)

        #response = helpers.bulk(elastic, actions, index='employees', doc_type='people')
        print ("\nRESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)

if __name__ == '__main__':
    # read_csv_and_write_to_es()
    # es.indices.delete(index=index, ignore=[400, 404])
    # res = es.search(index=index, body = {'size' : 10000,'query': {'match_all' : {}}})
    # print(res)
