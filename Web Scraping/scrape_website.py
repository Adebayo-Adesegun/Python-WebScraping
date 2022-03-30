import re
import requests
from bs4 import BeautifulSoup


def in_stock(title, topic):
    base_url = "http://books.toscrape.com/"

    status, page = get_page(base_url)

    if status:
        side_category_content = get_page_content(page, 'side_categories')

        topic_url = get_category_url(side_category_content, topic)

        if topic_url is None:
            return False


        # Assume they are multiple pages
        for elem in range(10):
            if elem == 0:
                url_inner = base_url + topic_url
            else:
                url_inner = base_url + topic_url.replace('/index.html', f'/page-{elem + 1}.html')

            status, topic_page = get_page(url_inner)

            if status is False:
                return False

            body = get_page_content(topic_page, 'row', 'ol')

            for elem in body[0].find_all('li'):
                elem_title = elem.find_all('h3')[0].find_all('a')[0].get('title').strip().lower()
                # elem_title = re.sub('[^A-Za-z0-9]+', ' ', elem_title)
                if elem_title == title.lower():
                    return True
        return False
    else:
        return False


def validate_book_exist(title, topic_content):
    for elem in topic_content:
        if elem.get_text().strip().lower() == title.lower():
            return True
    return False


def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True, response.content
    else:
        return False, None


def get_page_content(page_content, class_name, html_tag_name='div'):
    soup = BeautifulSoup(page_content, 'html.parser')
    body = soup.find_all(html_tag_name, class_=class_name)
    return body


def get_category_url(page_content, topic):
    body = page_content[0].find_all('a')
    for elem in body:
        if elem.get_text().strip().lower() == topic.lower():
            return elem['href']

    return None


# print(in_stock("the origin of species", "science"))
# print(in_stock("the origin of species", "art"))
# print(in_stock("Origin of Species", "Science"))
# print(in_stock("While You Were Mine", "Historical Fiction"))

print(in_stock("Online Marketing for Busy Authors: A Step-By-Step guide", "Self help"))