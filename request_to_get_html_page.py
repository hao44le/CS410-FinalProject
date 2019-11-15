import pandas as pd
import json
from bs4 import BeautifulSoup
import urllib.request


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
    soup = get_js_soup(task)
    if not soup: return None
    html_content = get_content_div(soup)
    return html_content

if __name__ == '__main__':
    tasks = read_csv_tasks()
    for task in tasks:
        print(task)
        html_content = given_url_fetch_content_and_parse(task)
