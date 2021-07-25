import sqlite3 as sql


def insertUser(username, password):
    inserted = None
    try:
        conn = sql.connect("./sql/avr_users.sqlite")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
        inserted = 1

    except sql.Error as error:
        print("Failed To Read avr_users.sqlite", error)
        inserted = 0
    finally:
        if conn:
            conn.commit()
            conn.close()
            print("The SQLite connection is closed")

    return inserted


def validateUsers(username, password):

    found = None
    conn = None
    try:
        conn = sql.connect("./sql/avr_users.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users where username = ? and password = ?", (username, password))

        results = cur.fetchall()
        found = len(results)
        print("Estatus Usuario Encontrado=", found)

    except sql.Error as error:
        print("Failed To Read avr_users.sqlite", error)
        found = 0
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

    return found


#validateUsers("dosollo", "palmi4708")