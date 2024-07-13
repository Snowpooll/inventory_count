import argparse
import json
import cv2
from ultralytics import YOLO
from collections import defaultdict
from line_notify import send_line_notify  # インポートを追加
from datetime import datetime
from inventory_database_module import save_detection_to_db  # データベース保存用の関数をインポート

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description="YOLOv8 Object Detection")
parser.add_argument('image_path', type=str, help='Path to the input image file')
args = parser.parse_args()

# ラベルマッピングファイルのパス
label_mapping_path = 'label_mapping.json'

# JSONファイルからクラスラベルのマッピングを読み込み
with open(label_mapping_path, 'r', encoding='utf-8') as f:
    label_mapping = json.load(f)

# YOLOv8モデルのロード
model = YOLO('inventory_model/best.pt')  # ここで適切なモデルを選択

# 画像のロード
image = cv2.imread(args.image_path)

# 画像の検出
results = model(image, save=True, conf=0.1, iou=0.5)

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
message = f"{message}\n在庫チェックの時刻: {current_time}"

# 検出結果の表示
for line in message_lines:
    print(line)

# LINE Notifyにメッセージを送信（フィルタリングされた結果のみ）
if message_lines:
    send_line_notify(message)
    save_detection_to_db(filtered_object_counts)  # データベースに検出結果を保存
else:
    print("No objects with counts of 1 or less detected.")
