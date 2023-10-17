import os
import sqlite3

database_name = 'Befriend.db'

class DB:
    def __init__(self):
        if os.path.exists(database_name):
            print("Database exists!")
        else:
            print(f"Database does not exist!, create {database_name}...")
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            # 創建 User 表
            cursor.execute('''
            CREATE TABLE User (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT,
                nickname TEXT,
                password TEXT,
                img TEXT,
                self_name TEXT,
                first_name TEXT,
                last_name TEXT,
                introduction TEXT,
                interest TEXT,
                created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_time DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            ''')

            # 創建 Expired 表
            cursor.execute('''
            CREATE TABLE Expired (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                data TEXT,
                type TEXT,
                created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                expired_time DATETIME,
                updated_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES User(id)
            );
            ''')

            # 創建 log 表
            cursor.execute('''
            CREATE TABLE log (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                visit_user_id INTEGER,
                created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES User(id),
                FOREIGN KEY(visit_user_id) REFERENCES User(id)
            );
            ''')
            conn.commit()
            conn.close()
            print(f"create {database_name}... done")

    async def get_conn(self):
        return sqlite3.connect(database_name)
            


sqlite3_db = DB()