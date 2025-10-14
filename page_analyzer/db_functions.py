import psycopg2
import os

from dotenv import load_dotenv
from page_analyzer.urls_functions import normalize_url
from psycopg2.extras import RealDictCursor

load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(database_url)


def get_url_id_by_name(url):
    normalized_url = normalize_url(url)
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM urls WHERE name = %s;",
            (normalized_url,),
        )
        result = cur.fetchone()
    return result[0] if result else None


def add_url(url):
    normalized_url = normalize_url(url)
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id;",
            (normalized_url,),
        )
        url_id = cur.fetchone()[0]
        conn.commit()
    return url_id


def get_all_urls():
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                u.id, u.name, u.created_at,
                lc.status_code, lc.created_at as last_check
            FROM urls u
            LEFT JOIN (
                SELECT url_id, status_code, created_at,
                        ROW_NUMBER() OVER (
                            PARTITION BY url_id ORDER BY created_at DESC
                        ) as rn
                FROM url_checks
            ) lc ON u.id = lc.url_id AND lc.rn = 1
            ORDER BY u.created_at DESC
        """)
        urls = cur.fetchall()
    return urls


def get_url_by_id(url_id):
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, name, created_at FROM urls WHERE id = %s;", (url_id,),
        )
        url = cur.fetchone()
    return url


def get_url_details(url_id):
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT id,
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    created_at
                FROM url_checks WHERE url_id = %s
                ORDER BY created_at DESC""",
                (url_id,),
        )
        checks = cur.fetchall()
    return checks


def add_url_check(url_id, check_data):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO url_checks (
                    url_id,
                    status_code,
                    h1,
                    title,
                    description
                    )
                VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                    (url_id,
                    check_data['status_code'],
                    check_data['h1'],
                    check_data['title'],
                    check_data['description']),
        )
        check_id = cur.fetchone()[0]
        conn.commit()
    return check_id
