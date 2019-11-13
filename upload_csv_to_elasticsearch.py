from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import pandas as pd

host = 'search-chinesek12-sp2avv7lleofzv5qu5m6qkk4by.us-east-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-2' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)
#K12_chinese_wechat_articles
csv_name = "small_test.csv"

def read_csv(): return pd.read_csv(csv_name)

if __name__ == '__main__':
    csv = read_csv()
    # document = {
    #     "title": "Moneyball",
    #     "director": "Bennett Miller",
    #     "year": "2011"
    # }
    #
    # es.index(index="movies", doc_type="_doc", id="5", body=document)
    #
    # print(es.get(index="movies", doc_type="_doc", id="5"))
