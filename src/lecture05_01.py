import numpy as np
import os
import cv2
from my_module.K24140.lecture05_camera_image_capture import MyVideoCapture

def lecture05_01():

    # カメラキャプチャ実行
    app = MyVideoCapture()
    app.run()

    # 画像をローカル変数に保存
    google_img : cv2.Mat = cv2.imread('images/google.png')
    capture_img : cv2.Mat = app.get_img()

    g_hight, g_width, g_channel = google_img.shape
    c_hight, c_width, c_channel = capture_img.shape
    print(google_img.shape)
    print(capture_img.shape)

    for x in range(g_width):
        for y in range(g_hight):
            g, b, r = google_img[y, x]
            # もし白色(255,255,255)だったら置き換える
            if (b, g, r) == (255, 255, 255):
                yy = y % c_hight
                xx = x % c_width
                google_img[y, x] = capture_img[yy, xx]

    os.makedirs('output_images', exist_ok=True)   
    # 書き込み処理
    app.captured_img = google_img  #保存対象を上書き
    app.write_img('output_images/lecture05_01_K21999.png')


if __name__ == "__main__":
    lecture05_01()

