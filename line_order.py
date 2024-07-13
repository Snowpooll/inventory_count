import requests
import os
from PIL import Image
from io import BytesIO
from utils import load_config, get_latest_directory, get_image_files

# 設定ファイルを読み込む
config = load_config('config.json')

# 設定ファイルからトークンとディレクトリパスを取得
token = config['token']
base_path = config['image_file_path']

# 最新のpredictディレクトリを取得
latest_dir = get_latest_directory(base_path)
image_files = get_image_files(latest_dir)

url = 'https://notify-api.line.me/api/notify'
message = 'ファイルパス自動取得テスト'

headers = {'Authorization': f"Bearer {token}"}
params = {'message': message}

# 最新のpredictディレクトリ内の全ての画像ファイルに対してLINE Notify APIにリクエストを送信
for image_file_path in image_files:
    with open(image_file_path, 'rb') as img_file:
        img_data = img_file.read()
        
        # 画像ファイルのサイズをチェック
        if len(img_data) > 3 * 1024 * 1024:  # 3MB
            # 画像をリサイズ
            image = Image.open(BytesIO(img_data))
            new_size = (image.width // 2, image.height // 2)
            image = image.resize(new_size, Image.LANCZOS)
            
            # リサイズした画像をバイトデータに変換
            output = BytesIO()
            image_format = image.format if image.format else 'JPEG'  # デフォルトでJPEG形式を設定
            image.save(output, format=image_format)
            img_data = output.getvalue()
        
        # ファイルデータをバイトデータとして用意
        files = {'imageFile': BytesIO(img_data)}
        files['imageFile'].name = os.path.basename(image_file_path)
        
        # LINE Notify APIにリクエストを送信
        res = requests.post(url, headers=headers, params=params, files=files)

        # レスポンスを出力
        print(f"File: {image_file_path}")
        print(res.status_code)
        print(res.text)

