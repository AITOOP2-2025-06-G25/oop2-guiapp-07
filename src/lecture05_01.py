import numpy as np
import cv2
from my_module.K24140.lecture05_camera_image_capture import MyVideoCapture

def lecture05_01():
    # --- 1. カメラキャプチャ実行と画像取得 ---

    # MyVideoCaptureクラスは、カメラを起動し、GUIを表示して画像キャプチャを行うと仮定します。
    # app.run()が終了する際に、キャプチャした画像データが内部に保持されているとします。
    app = MyVideoCapture()
    app.run()

    # カメラキャプチャプログラムの保存機能を使わず、get_img()で画像を取得
    # capture_img : cv2.Mat = "implement me" を置き換える
    capture_img: cv2.Mat = app.get_img() 
    
    # 画像をローカル変数に保存
    # 注意: 提出時には動作テスト用のキャプチャ画像の読み込みは削除します。
    google_img : cv2.Mat = cv2.imread('images/google.png')
    # capture_img : cv2.Mat = cv2.imread('images/camera_capture.png') # 動作テスト用なので提出時にこの行を消すこと

    # --- 2. 画像情報の確認と前処理 ---
    
    if google_img is None:
        print("エラー: 'images/google.png' が見つからないか、読み込めませんでした。")
        return
    if capture_img is None:
        print("エラー: カメラ画像が取得できませんでした。")
        return

    g_hight, g_width, g_channel = google_img.shape    # Google画像: (640, 1280, 3)を想定
    c_hight, c_width, c_channel = capture_img.shape    # カメラ画像: (480, 640, 3)を想定

    print(f"Google画像サイズ: {google_img.shape}")
    print(f"カメラ画像サイズ: {capture_img.shape}")

    # 処理後の画像を格納するための新しい画像をgoogle_imgのコピーとして作成
    # このコピーに結果を書き込みます。
    result_img = google_img.copy()

    # --- 3. 白色部分の置換処理 ---
    
    # カメラ画像をグリッド状に繰り返すための準備
    # google_imgの任意の点(y, x)に対応するカメラ画像の点(cy, cx)を計算します。
    for y in range(g_hight):
        for x in range(g_width):
            # Google画像の画素値を取得 (BGRの順)
            b, g, r = google_img[y, x]
            
            # もし画素が白色(255, 255, 255)だったら置き換える
            if (b == 255 and g == 255 and r == 255):
                # Google画像の座標(x, y)をカメラ画像のグリッド座標(cx, cy)に変換
                # 座標(0, 0)から拡大縮小なくグリッド状に並べる (タイリング処理)
                
                # カメラ画像の行/縦方向の座標 (y方向)
                # Google画像のy座標をカメラ画像の高さで割った余りが、カメラ画像内のy座標になる
                cy = y % c_hight
                
                # カメラ画像の列/横方向の座標 (x方向)
                # Google画像のx座標をカメラ画像の幅で割った余りが、カメラ画像内のx座標になる
                cx = x % c_width
                
                # カメラ画像の画素を取得 (BGRの順)
                cap_b, cap_g, cap_r = capture_img[cy, cx]

                # Google画像の白色部分をキャプチャ画像の対応する画素で置換
                # result_imgの対応する画素に書き込む
                result_img[y, x] = (cap_b, cap_g, cap_r)

    # --- 4. 書き込み処理 ---
    
    # 最終的な画像をファイルに保存
    # ファイル名: lecture05_01_学籍番号.png (学籍番号は例)
    output_filename = 'lecture05_01_K24140.png' 
    cv2.imwrite(output_filename, result_img)
    print(f"処理結果を '{output_filename}' として保存しました。")


# 実行部分 (必要に応じて追加)
if __name__ == '__main__':
    lecture05_01()