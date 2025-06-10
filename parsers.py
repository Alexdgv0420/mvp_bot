
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_ozon(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("h1")
    img = soup.find("img")
    return {
        "title": title.text.strip() if title else "Товар с Ozon",
        "image": img["src"] if img else None,
        "link": url
    }

def parse_wildberries(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("h1")
    img = soup.find("img")
    return {
        "title": title.text.strip() if title else "Товар с WB",
        "image": img["src"] if img else None,
        "link": url
    }

def parse_yandex_market(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("h1")
    img = soup.find("img")
    return {
        "title": title.text.strip() if title else "Товар с Я.Маркета",
        "image": img["src"] if img else None,
        "link": url
    }

def parse_link(url):
    if "ozon.ru" in url:
        return parse_ozon(url)
    elif "wildberries.ru" in url:
        return parse_wildberries(url)
    elif "market.yandex" in url:
        return parse_yandex_market(url)
    else:
        return {"title": "Неизвестный магазин", "image": None, "link": url}
