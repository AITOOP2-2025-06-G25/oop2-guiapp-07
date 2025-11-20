import sys
import os
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from my_module.K24140.lecture05_camera_image_capture import MyVideoCapture


def cv2_to_qimage(cv_img: np.ndarray) -> QImage:
    """OpenCV BGR画像をQImageに変換する"""
    height, width, channel = cv_img.shape
    bytes_per_line = 3 * width
    # BGR -> RGB
    cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    return QImage(cv_img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)


class Lecture05GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lecture05 Camera GUI")
        self.resize(800, 600)

        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 画像表示用ラベル
        self.image_label = QLabel("ここに画像が表示されます")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(640, 480)

        # 処理状態ラベル
        self.status_label = QLabel("状態: 待機中")

        # ボタン
        self.capture_btn = QPushButton("写真取得")
        self.compose_btn = QPushButton("画像合成")
        self.save_btn = QPushButton("結果保存")

        # レイアウト
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.capture_btn)
        btn_layout.addWidget(self.compose_btn)
        btn_layout.addWidget(self.save_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.status_label)

        central_widget.setLayout(main_layout)

        # イベント接続
        self.capture_btn.clicked.connect(self.capture_image)
        self.compose_btn.clicked.connect(self.compose_image)
        self.save_btn.clicked.connect(self.save_image)

        # キャプチャオブジェクト
        self.capture_app = MyVideoCapture()
        self.captured_img: np.ndarray | None = None
        self.composed_img: np.ndarray | None = None

    def capture_image(self):
        self.status_label.setText("状態: カメラ起動中...")
        QApplication.processEvents()  # GUIを更新
        self.capture_app.run()
        self.captured_img = self.capture_app.get_img()
        if self.captured_img is not None:
            self.status_label.setText("状態: 写真取得完了")
            self.display_image(self.captured_img)
        else:
            self.status_label.setText("状態: 写真取得失敗")

    def compose_image(self):
        if self.captured_img is None:
            self.status_label.setText("状態: 先に写真を取得してください")
            return

        # Google画像読み込み
        google_img_path, _ = QFileDialog.getOpenFileName(
            self, "合成する画像を選択", "images", "Images (*.png *.jpg *.bmp)"
        )
        if not google_img_path:
            return

        google_img = cv2.imread(google_img_path)
        if google_img is None:
            self.status_label.setText("状態: 画像読み込み失敗")
            return

        # 合成処理
        g_h, g_w, _ = google_img.shape
        c_h, c_w, _ = self.captured_img.shape
        composed = google_img.copy()

        for y in range(g_h):
            for x in range(g_w):
                b, g, r = google_img[y, x]
                if (b, g, r) == (255, 255, 255):
                    yy = y % c_h
                    xx = x % c_w
                    composed[y, x] = self.captured_img[yy, xx]

        self.composed_img = composed
        self.status_label.setText("状態: 画像合成完了")
        self.display_image(self.composed_img)

    def save_image(self):
        if self.composed_img is None:
            self.status_label.setText("状態: 合成画像がありません")
            return

        os.makedirs('output_images', exist_ok=True)
        save_path, _ = QFileDialog.getSaveFileName(
            self, "保存先を選択", "output_images/result.png", "PNG Files (*.png)"
        )
        if save_path:
            cv2.imwrite(save_path, self.composed_img)
            self.status_label.setText(f"状態: 保存完了 ({save_path})")

    def display_image(self, cv_img: np.ndarray):
        """QLabelにOpenCV画像を表示"""
        qimg = cv2_to_qimage(cv_img)
        pixmap = QPixmap.fromImage(qimg).scaled(
            self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
        )
        self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Lecture05GUI()
    window.show()
    sys.exit(app.exec())