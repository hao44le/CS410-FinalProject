import pandas as pd
import json
from bs4 import BeautifulSoup
from common import get_es_instance, given_link_get_the_sn, es_update_html_content
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
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
def get_js_soup(url, browser):
    soup = None
    try:
        # Use the browser, it is able to get the content without being blocked by their system
        browser.get(url)
        res_html = browser.page_source
        soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
        soup = remove_script(soup)
    except:
        soup = None

    return soup

def get_content_div(soup):
    img_content = ""
    try:
        img_content = soup.find("div", {"id": "img-content"}).text
        img_content = img_content.replace("\n", "")
        img_content = img_content.replace(" ", "")
    except:
        img_content = ""
    return img_content

def given_url_fetch_content_and_parse(url, browser):
    soup = get_js_soup(url, browser)
    if not soup: return None
    html_content = get_content_div(soup)
    return html_content

if __name__ == '__main__':
    csv_name = "K12_chinese_wechat_articles.csv"
    tasks = read_csv_tasks(csv_name)
    es = get_es_instance()
    options = Options()
    # options.headless = True
    browser = webdriver.Chrome(options=options)

    previous_cache = int(sys.argv[1])
    retry_max_count = 10

    for (x, task) in enumerate(tasks):
        if x < previous_cache: continue

        html_content = given_url_fetch_content_and_parse(task, browser)
        if html_content is None:
            print("\tERROR! html_content is None!!!")
            print("\tstart from {}.   {}/{}".format(previous_cache, x, len(tasks)))
            continue
        if len(html_content) == 0:
            print("\tERROR! html_content is empty!!! {}".format(task))
            print("\tstart from {}.   {}/{}".format(previous_cache, x, len(tasks)))
            continue

        document_id = given_link_get_the_sn(task)
        print("start from {}.   {}/{}. Docuemnt length: {}. Document ID is {}".format(previous_cache, x, len(tasks), len(html_content), document_id))

        curr_retry = 0
        while curr_retry < retry_max_count:
            if es_update_html_content(es, document_id, html_content): break
            curr_retry += 1
            print("\t\tfailed to update on es. curr retry {} with max of {}".format(curr_retry, retry_max_count))
