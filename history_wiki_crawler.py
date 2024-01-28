from collections import defaultdict, deque
from bs4 import BeautifulSoup
import requests

x_data_index = defaultdict(str)
base_url = 'https://en.wikipedia.org'


def crawelOnCategories(start_url, data):
    queue = deque([start_url])
    visited = set()
    contents = defaultdict(list)
    while queue:
        cur_a = queue.popleft()
        next_link = base_url + cur_a['href']
        print("Visting :", next_link)
        response = requests.get(next_link)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        if "Category" in next_link:
            subcategories = soup.find("div", id="mw-subcategories")
            pages = soup.find("div", id="mw-pages")
            if subcategories:
                for sub in subcategories.find_all("a"):
                    if sub not in visited:
                        queue.append(sub)
                        visited.add(sub)
            if pages:
                for page in pages.find_all("a"):
                    if page not in visited:
                        queue.append(page)
                        visited.add(page)
            
        else:
            body_content_div = soup.find("div", id="bodyContent")

            all_text_in_body_content = body_content_div.get_text()
            data[next_link] = all_text_in_body_content
            
    return contents
    
    
    
    
def getContentByCountryAndYear(country, year):
    start_url = '/wiki/Category:{}_in_{}'.format(year,country)
    a_tag = BeautifulSoup("<a href={}></a>".format(start_url), "html.parser").a
    a_tag["href"] = start_url
    articles = {}
    data = {(country,year) : articles}
    crawelOnCategories(a_tag,articles)
    return data

resp = getContentByCountryAndYear('Germany', '1850')
