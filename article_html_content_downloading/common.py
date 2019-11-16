from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
from requests_aws4auth import AWS4Auth
import boto3

def get_es_instance(index = "chinesek12_wechat_article"):
    host = 'search-chinesek12-sp2avv7lleofzv5qu5m6qkk4by.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
    region = 'us-east-2' # e.g. us-west-1

    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)
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

def given_link_get_the_sn(document_link):
    document_link_sn = document_link.find("sn") + 3
    document_id_first_round = document_link[document_link_sn:]
    document_id_stop = document_id_first_round.find("&")
    document_id = document_id_first_round[:document_id_stop]
    return document_id

def es_update_html_content(es, document_id, html_content, index="chinesek12_wechat_article"):
    # doc = es.get(index=index, id=document_id)['_source']
    # doc['文章内容'] = html_content
    # print(doc)
    # es.index(index=index, doc_type="doc",id=document_id,body=doc)
    try:
        es.update(index=index, doc_type="_doc", id=document_id, body={"doc": {'文章内容': html_content}})
        return True
    except:
        return False
if __name__ == '__main__':
    es = get_es_instance()
    print(es)
