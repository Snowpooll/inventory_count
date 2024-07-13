import sqlite3

def view_detections(db_path='detections.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブルの内容を取得
    cursor.execute('SELECT * FROM detections')
    rows = cursor.fetchall()

    # カラム名を取得
    column_names = [description[0] for description in cursor.description]

    # 結果を表示
    print(f"{' | '.join(column_names)}")
    print("-" * 50)
    for row in rows:
        print(" | ".join(str(value) for value in row))

    conn.close()

if __name__ == '__main__':
    view_detections()

