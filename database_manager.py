import psycopg2


def close_cur_and_conn(cur, conn):
    """
    Close the current cursor and connection.
    :param cur: Database cursor.
    :param conn: Database connection.
    :return:
    """
    cur.close()
    conn.close()


def create_conn_and_cur():
    """
    Create the database connection and cursor objects.
    :return: Tuple containing connection and cursor.
    """
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='mysecretpassword',
                            port='5432')
    cur = conn.cursor()
    return conn, cur


def create_database_table():
    (conn, cur) = create_conn_and_cur()

    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS grocery (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            image_url VARCHAR(255),
            price VARCHAR(100),
            currency VARCHAR(255),
            volume_price VARCHAR(255),
            volume_currency VARCHAR(255),
            store VARCHAR(100));
            """)
        conn.commit()
    except Exception as inst:
        print(inst)
    finally:
        close_cur_and_conn(cur, conn)


def drop_table():
    """
    Drop the table if it exists.
    :return:
    """
    (conn, cur) = create_conn_and_cur()

    try:
        cur.execute("DROP TABLE IF EXISTS grocery")
        conn.commit()
    except Exception as inst:
        print(inst)
    finally:
        close_cur_and_conn(cur, conn)


def insert_values(name, image_url, price, currency, volume_price, volume_currency, store):
    """
    Insert the provided values into the database.
    :param name: Name of the product.
    :param image_url: Image url of the product.
    :param price:  Price string value
    :param currency: Currency string value.
    :param volume_price: Volume price string.
    :param volume_currency: Volume currency string.
    :param store: Name of store.
    :return:
    """
    # Create database connection.
    (conn, cur) = create_conn_and_cur()
    try:
        cur.execute(f"""INSERT INTO grocery (name, image_url, price, currency, volume_price, volume_currency, 
        store) VALUES ('{name}', '{image_url}','{price}', '{currency}', '{volume_price}', '{volume_currency}', 
        '{store}');
        """)
    except Exception as inst:
        print(inst)
        print(inst.args)
    finally:
        conn.commit()
        close_cur_and_conn(cur, conn)