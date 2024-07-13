import sqlite3

def create_table():
    conn = sqlite3.connect('detections.db')
    cursor = conn.cursor()

    # テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            count INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()

