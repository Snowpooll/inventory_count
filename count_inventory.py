import json
import cv2
import configparser
from ultralytics import YOLO
from collections import defaultdict
from line_notify import send_line_notify  # インポートを追加
from datetime import datetime
from inventory_database_module import save_detection_to_db  # データベース保存用の関数をインポート
import os

# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('config.ini')

# 設定ファイルからモデルパスと画像ディレクトリを取得
model_path = config['Settings']['model_path']
image_directory = config['Settings']['image_directory']

# ラベルマッピングファイルのパス
label_mapping_path = 'label_mapping.json'

# JSONファイルからクラスラベルのマッピングを読み込み
with open(label_mapping_path, 'r', encoding='utf-8') as f:
    label_mapping = json.load(f)

# YOLOv8モデルのロード
model = YOLO(model_path)  # 設定ファイルからモデルパスを使用

# 画像ディレクトリ内の全画像ファイルを処理
for image_filename in os.listdir(image_directory):
    image_path = os.path.join(image_directory, image_filename)
    if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # 画像のロード
        image = cv2.imread(image_path)

        # 画像の検出
        results = model(image, save=True, conf=0.2, iou=0.5)

        # 検出結果の取得
        detections = results[0]  # 最初の結果を取得
        classes = detections.boxes.cls

        # 検出物体のカウント
        object_counts = defaultdict(int)
        for cls in classes:
            class_label = model.names[int(cls)]
            if class_label in label_mapping:
                label = label_mapping[class_label]
            else:
                label = class_label
            object_counts[label] += 1

        # 検出結果のフィルタリング（1以下のもの）
        filtered_object_counts = {label: count for label, count in object_counts.items() if count <= 1}

        # フィルタリングされた検出結果のメッセージ生成
        message_lines = [f'{label}: {count}個' for label, count in filtered_object_counts.items()]
        message = '\n'.join(message_lines)

        # 現在の時刻を取得
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"{message}\n\nMessage sent at: {current_time}"

        # 検出結果の表示
        for line in message_lines:
            print(line)

        # LINE Notifyにメッセージを送信（フィルタリングされた結果のみ）
        if message_lines:
            send_line_notify(message)
            save_detection_to_db(filtered_object_counts)  # データベースに検出結果を保存
        else:
            print("No objects with counts of 1 or less detected in file:", image_filename)
