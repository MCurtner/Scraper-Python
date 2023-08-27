import psycopg2


def create_database_table():
    (conn, cur) = create_conn_and_cur()

    cur.execute("""CREATE TABLE IF NOT EXISTS grocery (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        image_url VARCHAR(255),
        price VARCHAR(255),
        volume_price VARCHAR(255));
    """)
    conn.commit()
    close_cur_and_conn(cur, conn)


def insert_dummy_values():
    (conn, cur) = create_conn_and_cur()
    cur.execute("""INSERT INTO GROCERY (id, name, image_url, price, volume_price) VALUES
        (1, 'TEST', 'URL', '30', '36')
    """)
    conn.commit()
    close_cur_and_conn(cur, conn)


def insert_values(name, image_url, price, volume_price):
    (conn, cur) = create_conn_and_cur()
    try:

        cur.execute(f"""INSERT INTO GROCERY (name, image_url, price, volume_price) VALUES
           ('{name}', '{image_url}','{price}', '{volume_price}')
        """)
    except Exception as inst:
        print(inst.args)
    finally:
        conn.commit()
        close_cur_and_conn(cur, conn)


def create_conn_and_cur():
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='mysecretpassword',
                            port='5432')
    cur = conn.cursor()
    return conn, cur


def close_cur_and_conn(cur, conn):
    cur.close()
    conn.close()
