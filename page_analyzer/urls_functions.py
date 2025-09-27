import requests
from bs4 import BeautifulSoup
import validators
from urllib.parse import urlparse

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return normalized_url


def validate_url(url):
    if not url:
        return "URL не должен быть пустым"
    if len(url) > 255:
        return "Длина URL превышает 255 символов"
    if not validators.url(url):
        return "Некорректный URL"
    return None


def get_page_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, "html.parser")

        h1 = soup.find("h1")
        h1_text = h1.get_text().strip() if h1 else ""

        title = soup.find("title")
        title_text = title.get_text().strip() if title else ""

        description = soup.find("meta", attrs={"name": "description"})
        description_text = (
            description.get("content", "").strip() if description else ""
        )

        return {
            "status_code": response.status_code,
            "h1": h1_text,
            "title": title_text,
            "description": description_text,
        }
    except requests.RequestException:
        return None
