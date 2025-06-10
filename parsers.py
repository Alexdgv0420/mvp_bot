import requests
from bs4 import BeautifulSoup
import json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_ozon(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=7)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Название товара
        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Товар с Ozon"

        # Парсинг JSON из <script> с window.__STATE__
        scripts = soup.find_all("script")
        state_script = next((s for s in scripts if "__STATE__" in s.text), None)

        image = price = discount = rating = delivery = "—"

        if state_script:
            try:
                json_text = state_script.string.split('window.__STATE__=')[-1].split(";</script>")[0]
                data = json.loads(json_text)

                for key in data:
                    block = data[key]
                    if isinstance(block, dict):
                        if "image" in block:
                            image = block.get("image")
                        if "finalPrice" in block:
                            price = f"{block['finalPrice']} ₽"
                        if "discount" in block:
                            discount = f"-{block['discount']}%"
                        if "rating" in block:
                            rating = f"{block['rating']} ★"
                        if "deliverySchema" in block:
                            delivery = block['deliverySchema']
            except Exception as e:
                print(f"[OZON JSON ERROR] {e}")

        return {
            "title": title,
            "utp": "Полезный и удобный товар с Ozon",
            "market": "Ozon",
            "price": price,
            "discount": discount,
            "delivery": delivery,
            "rating": rating,
            "image": image,
            "link": url
        }
    except Exception as e:
        print(f"[OZON ERROR] {e}")
        return fallback(url, "Ozon")

def parse_wildberries(url):
    try:
        product_id = url.split('/catalog/')[1].split('/')[0]
        api_url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&nm={product_id}"
        resp = requests.get(api_url, headers=HEADERS, timeout=5).json()
        data = resp['data']['products'][0]

        title = data.get("name", "Товар с Wildberries")
        price = f"{data.get('priceU', 0) // 100} ₽"
        discount = f"-{data.get('sale', 0)}%"
        rating = f"{data.get('reviewRating', 0)} ★"
        image = f"https://images.wbstatic.net/big/new/{data['id']}-1.jpg"
        delivery = "Доставка за 1–3 дня"

        return {
            "title": title,
            "utp": "Товар с хорошими отзывами, доставка из РФ",
            "market": "Wildberries",
            "price": price,
            "discount": discount,
            "delivery": delivery,
            "rating": rating,
            "image": image,
            "link": url
        }
    except Exception as e:
        print(f"[WB ERROR] {e}")
        return fallback(url, "Wildberries")

def parse_yandex_market(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=7)
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Товар с Яндекс.Маркет"

        price_tag = soup.select_one('[data-auto="mainPrice"]')
        price = price_tag.text.strip() if price_tag else "—"

        rating_tag = soup.select_one('[data-zone-name="rating"]')
        rating = rating_tag.text.strip() if rating_tag else "—"

        image_tag = soup.find("img")
        image = image_tag.get("src") if image_tag else None

        return {
            "title": title,
            "utp": "Один из хитов продаж на Я.Маркете",
            "market": "Яндекс.Маркет",
            "price": price,
            "discount": "—",
            "delivery": "Обычно 2–4 дня, из РФ",
            "rating": rating,
            "image": image,
            "link": url
        }
    except Exception as e:
        print(f"[YANDEX ERROR] {e}")
        return fallback(url, "Яндекс.Маркет")

def fallback(url, market):
    return {
        "title": f"Товар с {market}",
        "utp": "Интересный товар — посмотри сам!",
        "market": market,
        "price": "—",
        "discount": "—",
        "delivery": "—",
        "rating": "—",
        "image": None,
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
        return fallback(url, "Неизвестный маркетплейс")
