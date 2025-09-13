import re
from urllib.parse import urlparse, urlunparse


def validate_url(url):
    """URL validations"""
    if not url:
        return False, "URL is need"

    if len(url) > 255:
        return False, "URL more then 255 symbols"

    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # host
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ip address
        r"(?::\d+)?"  # port
        r"(?:/?|[/?]\S+)$", re.IGNORECASE)

    if not url_pattern.match(url):
        return False, "URL is incorrected"

    return True, ""


def normalize_url(url):
    """Normalize URL to scheme + netloc
    (ignore path, params, query, fragment)
    """
    parsed = urlparse(url)
    normalized = urlunparse((
        parsed.scheme, parsed.netloc, '', '', '', ''
    ))
    return normalized