
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ur_sqlpassword",
        database="poker",
        port=3306
    )


def register_player(name):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO pokerstat
                (PNAME, HANDSPLAY, HANDSWON, TWINS, TROUND)
            VALUES (%s, 0, 0, 0, 0)
            ON DUPLICATE KEY UPDATE PNAME = PNAME
            """,
            (name,)
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()


def record_hand(name, won=False):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE pokerstat
            SET HANDSPLAY = HANDSPLAY + 1,
                HANDSWON = HANDSWON + %s
            WHERE PNAME = %s
            """,
            (int(won), name)
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()


def record_tournament(name, won=False):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE pokerstat
            SET TROUND = TROUND + 1,
                TWINS = TWINS + %s
            WHERE PNAME = %s
            """,
            (int(won), name)
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()



def get_player_stats(name):
    conn = connect_db()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT PNAME, HANDSPLAY, HANDSWON, TWINS, TROUND
            FROM pokerstat
            WHERE PNAME = %s
            """,
            (name,)
        )

        result = cursor.fetchone()

        cursor.close()
        return result  # Important: return the fetched row

    finally:
        conn.close()

