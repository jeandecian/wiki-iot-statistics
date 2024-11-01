from bs4 import BeautifulSoup
import re
import requests


def get_html_text_data(path):
    BASE_URL = "https://fehmijaafar.net/wiki-iot/index.php"

    return requests.get(BASE_URL + path).text


def get_category_total_pages(category):
    text_data = get_html_text_data("/Category:" + category)
    soup = BeautifulSoup(text_data, "html.parser")
    mw_pages_div = soup.find("div", id="mw-pages")
    first_paragraph = mw_pages_div.find("p") if mw_pages_div else None

    if first_paragraph:
        numbers = re.findall(r"\d+", first_paragraph.get_text())

        if len(numbers) >= 2:
            total_pages = numbers[1]

            return category, total_pages

    return category, None


def get_total_pages():
    with open("statistics/total_pages.txt", "w") as f:
        f.write(str(get_category_total_pages("Classification")[1]))


get_total_pages()
