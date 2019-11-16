import pandas as pd
import json
from bs4 import BeautifulSoup
import urllib.request
from common import get_es_instance, given_link_get_the_sn, es_update_html_content

def read_csv_tasks(csv_name = "small_test.csv"):
    csv = pd.read_csv(csv_name)
    json_array = json.loads(csv.to_json(orient='index'))
    links = []
    for x in range(0, len(json_array)):
        document_link = json_array[str(x)]["链接"]
        links.append(document_link)
    return links

''' More tidying
Sometimes the text extracted HTML webpage may contain javascript code and some style elements.
This function removes script and style tags from HTML so that extracted text does not contain them.
'''
def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup

#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url):
    soup = None
    try:
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        res_html = mybytes.decode("utf8")
        fp.close()
        soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
        soup = remove_script(soup)
    except:
        soup = None

    return soup

def get_content_div(soup):
    img_content = soup.find("div", {"id": "img-content"}).text
    img_content = img_content.replace("\n", "")
    img_content = img_content.replace(" ", "")
    return img_content

def given_url_fetch_content_and_parse(url):
    soup = get_js_soup(url)
    if not soup: return None
    html_content = get_content_div(soup)
    return html_content

if __name__ == '__main__':
    csv_name = "K12_chinese_wechat_articles.csv"
    tasks = read_csv_tasks(csv_name)
    es = get_es_instance()
    previous_cache = 1
    for (x, task) in enumerate(tasks):
        if x < previous_cache: continue
        print("{}/{}".format(x, len(tasks)))
        html_content = given_url_fetch_content_and_parse(task)
        document_id = given_link_get_the_sn(task)
        es_update_html_content(es, document_id, html_content)
