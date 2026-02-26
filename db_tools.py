# db_tools.py
from db import get_conn


# ------------------------------------------------------------
# Count rows in each table
# ------------------------------------------------------------

def db_count_rows():
    conn = get_conn()
    cur = conn.cursor()
    tables = ["metadata", "readings", "cache"]
    result = {}

    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        result[t] = cur.fetchone()[0]

    conn.close()
    return result


# ------------------------------------------------------------
# Show last N readings
# ------------------------------------------------------------

def db_show_last_readings(limit=10):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT station, parameter, date, value FROM readings ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------
# Show stations in DB
# ------------------------------------------------------------

def db_show_stations():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT station, name, region, catchment FROM metadata LIMIT 50"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------
# VACUUM / optimize
# ------------------------------------------------------------

def db_vacuum():
    conn = get_conn()
    conn.execute("VACUUM")
    conn.commit()
    conn.close()
    return True
