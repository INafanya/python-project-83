from urllib.parse import urlparse

import validators


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
