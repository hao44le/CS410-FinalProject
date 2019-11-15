from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
from requests_aws4auth import AWS4Auth

def get_es_instance(index = "chinesek12_wechat_article"):
    host = 'search-chinesek12-sp2avv7lleofzv5qu5m6qkk4by.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
    region = 'us-east-2' # e.g. us-west-1

    service = 'es'
    awsauth = AWS4Auth("AKIATMPP3NOWTKDPP2BX", "+qT9m84DoyWHTf1vs9e6C7exDMEKkU84Dru9O23k", region, service)
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    return es

def bulk_update(es, actions_array):
    try:
        # make the bulk call, and get a response
        response = helpers.bulk(es, actions_array, chunk_size=1000, request_timeout=200)
        print ("\nRESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)
