import os

import psycopg2
from dotenv import load_dotenv

from .urls import normalize_url

load_dotenv()


def get_connection():
    """Get DB connection"""
    database_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(database_url)


def init_db():
    """Initialize DB"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name varchar(255) NOT NULL UNIQUE,
                created_at timestamp DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
    finally:
        cursor.close()
        conn.close()


def add_url(url):
    """Add URL to DB"""
    normalized_url = normalize_url(url)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check URL in DB
        cursor.execute(
            "SELECT id FROM urls WHERE name = %s", (normalized_url,)
        )

        existing = cursor.fetchone()
        if existing:
            return existing[0]

        # Add new URL
        cursor.execute(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id",
            (normalized_url,),
        )
        url_id = cursor.fetchone()[0]

        conn.commit()
        return url_id
    finally:
        cursor.close()
        conn.close()


def get_url_by_id(url_id):
    """Get URL by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_all_urls():
    """Get all URLs with last check information"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                u.id, u.name, u.created_at,
                lc.status_code, lc.created_at as last_check_date
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

        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


