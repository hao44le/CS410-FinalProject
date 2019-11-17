import json
from dateutil import parser
from common import get_es_instance, bulk_update, given_link_get_the_sn
import pandas as pd

#K12_chinese_wechat_articles
csv_name = "K12_chinese_wechat_articles.csv"
previous_cache = 0

def read_csv_and_write_to_es(es, index):
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

        # Use sn as the unique article id
        document_link = document["链接"]
        document_id = given_link_get_the_sn(document_link)
        if len(document_id) != 32: continue

        document['_id'] = document_id
        document['_type'] = "_doc"
        document["_index"] = index
        actions_array.append(document)

    bulk_update(es, actions_array)

if __name__ == '__main__':
    index = "chinesek12_wechat_article"

    es = get_es_instance()
    # read_csv_and_write_to_es(es, index)

    # es.indices.delete(index=index, ignore=[400, 404])

    # res = es.search(index=index, body = {'size' : 10,'query': {'match_all' : {}}})
    res = es.search(index = index, body = {"query": {"regexp" : {"文章内容" : ".+"}}})
    print(res)
    res2 = es.search(index = index, body = {"query": {"regexp" : {"文章内容" : ".+"}}}, size=10000, scroll="1m")
    print(res2)
