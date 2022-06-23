import psycopg2
from config import config


def create_tables():
    """create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE expires_soon (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            domains VARCHAR(55) NOT NULL,
            expiry_status VARCHAR(100) NOT NULL,
            expiry_date DATE NOT NULL
             
            )
        """,
        """ CREATE TABLE available (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            domains VARCHAR(55) NOT NULL,
            status VARCHAR(15) NOT NULL
            )
        """,
        """
        CREATE TABLE reserve_list (
                id INTEGER PRIMARY KEY
        )
        """,
    )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()
