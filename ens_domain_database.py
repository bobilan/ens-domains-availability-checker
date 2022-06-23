import psycopg2
from config import DB_CONFIG


def insert_available(domain, status):
    available_id = None
    sq1 = """INSERT INTO available(domains, status)
     VALUES (%s, %s) RETURNING id;"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sq1, (domain, status))
        available_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return available_id


def insert_expires_soon(domain, expiry_status, expiry_date):
    conn = None
    expiry_id = None
    sq1 = """INSERT INTO expires_soon(domains, expiry_status, expiry_date)
     VALUES (%s, %s, %s) RETURNING id;"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sq1, (domain, expiry_status, expiry_date))
        expiry_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return expiry_id


def update_reserve_list(_id):
    conn = None
    sq1 = """UPDATE reserve_list
                SET id = %s;"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sq1, (_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_from_reserve_list():
    conn = None
    row = None
    sq1 = """SELECT id FROM reserve_list ;"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sq1)
        row = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return row


def write_to_input_data(inputs):
    conn = None
    expiry_id = None
    sq1 = """INSERT INTO input_data(inputs)
     VALUES (%s) RETURNING id;"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sq1, (inputs,))
        expiry_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return expiry_id


def get_from_input_data():
    conn = None
    rows = None
    sq1 = """SELECT inputs FROM input_data ORDER BY id;"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sq1)
        rows = [r[0] for r in cur.fetchall()]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows
