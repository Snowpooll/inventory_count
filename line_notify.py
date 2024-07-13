import requests
import os
from PIL import Image
from io import BytesIO
from utils import load_config, get_latest_directory, get_image_files

def resize_image_if_needed(image_data, max_size=3 * 1024 * 1024):
    if len(image_data) > max_size:
        image = Image.open(BytesIO(image_data))
        new_size = (image.width // 2, image.height // 2)
        image = image.resize(new_size, Image.LANCZOS)

        output = BytesIO()
        image_format = image.format if image.format else 'JPEG'
        image.save(output, format=image_format)
        return output.getvalue()
    return image_data

def send_line_notify(message, config_path='config.json'):
    # 設定ファイルを読み込む
    config = load_config(config_path)

    # 設定ファイルからトークンとディレクトリパスを取得
    token = config['token']
    base_path = config['image_file_path']

    # 最新のpredictディレクトリを取得
    latest_dir = get_latest_directory(base_path)
    image_files = get_image_files(latest_dir)

    url = 'https://notify-api.line.me/api/notify'

    headers = {'Authorization': f"Bearer {token}"}
    params = {'message': message}

    # 最新のpredictディレクトリ内の全ての画像ファイルに対してLINE Notify APIにリクエストを送信
    for image_file_path in image_files:
        with open(image_file_path, 'rb') as img_file:
            img_data = img_file.read()
            img_data = resize_image_if_needed(img_data)

            # ファイルデータをバイトデータとして用意
            files = {'imageFile': BytesIO(img_data)}
            files['imageFile'].name = os.path.basename(image_file_path)

            # LINE Notify APIにリクエストを送信
            res = requests.post(url, headers=headers, params=params, files=files)

            # レスポンスを出力
            print(f"File: {image_file_path}")
            print(res.status_code)
            print(res.text)

