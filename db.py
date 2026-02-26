# db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("env_explorer.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS metadata (
    station   TEXT,
    name      TEXT,
    region    TEXT,
    catchment TEXT,
    lat       REAL,
    lon       REAL
);

CREATE TABLE IF NOT EXISTS readings (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    station   TEXT,
    parameter TEXT,
    date      TEXT,
    value     REAL
);

CREATE TABLE IF NOT EXISTS cache (
    station    TEXT PRIMARY KEY,
    last_fetch INTEGER
);
"""


# ------------------------------------------------------------
# Connection + Schema
# ------------------------------------------------------------

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_conn()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


# ------------------------------------------------------------
# Metadata
# ------------------------------------------------------------

def insert_metadata(rows):
    conn = get_conn()
    try:
        conn.executemany(
            "INSERT INTO metadata (station, name, region, catchment, lat, lon) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()


# ------------------------------------------------------------
# Readings
# ------------------------------------------------------------

def insert_readings(rows):
    conn = get_conn()
    try:
        conn.executemany(
            "INSERT INTO readings (station, parameter, date, value) "
            "VALUES (?, ?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()


# ------------------------------------------------------------
# Cache
# ------------------------------------------------------------

def update_cache(station: str, timestamp: int) -> None:
    conn = get_conn()
    try:
        conn.execute(
            """
            INSERT INTO cache (station, last_fetch)
            VALUES (?, ?)
            ON CONFLICT(station) DO UPDATE SET last_fetch=excluded.last_fetch
            """,
            (station, timestamp),
        )
        conn.commit()
    finally:
        conn.close()


def get_last_fetch(station: str):
    conn = get_conn()
    try:
        cur = conn.execute("SELECT last_fetch FROM cache WHERE station = ?", (station,))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def get_all_cache():
    conn = get_conn()
    try:
        cur = conn.execute("SELECT station, last_fetch FROM cache")
        return cur.fetchall()
    finally:
        conn.close()


def purge_stale_cache(cutoff_timestamp: int) -> int:
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM cache WHERE last_fetch < ?", (cutoff_timestamp,))
        deleted = cur.rowcount
        conn.commit()
        return deleted
    finally:
        conn.close()
