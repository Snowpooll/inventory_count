# inventory_count
Detect objects with a camera and send a shopping list on LINE before inventory runs out

yoov8と学習したモデルで
指定した画像から物体検出をして在庫数が１以下になったときに  
LINE norifyで買い物リストが送信されます  
検出時の結果はsqlite3データベースに保存されます


## 動作環境
M1 MacbookAir 16GB で動作しています、  

使用にあたり
pip install -r requirements.txt  
を実行後  
create_table.py  
を実行することでデータベースが作成されます

検出したラベルと商品名を関連づけるため  
label_mapping.json  
で設定をしています。
モデルを変更したり、独自学習したモデルを使用する場合、対応する商品名を追記してください  

LINE Notifyを使うため  
config.json  
へ取得したトークンを記述してください  

config.ini  
では使用するモデルのパスと、推論に使うディレクトリを指定しているのでモデルや画像パスを変更する時に設定してください  

`python webcam_yv8.py`  
でカメラ画像での検出テストができます  

`python count_inventory_terminal.py 画像ファイル名`  
でターミナルで画像を指定し実行することができます  

`python count_inventory.py`  
でinventory_imagesフォルダに入っている画像を対象にして実行します  

`oython view_detections.py`  
で作成したデータベースの中身を閲覧することができます
