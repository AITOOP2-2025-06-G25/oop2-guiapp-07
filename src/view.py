import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
import numpy as np

class View(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  
        self.setWindowTitle("Camera GUI")
        self.resize(800, 600)

        # 中央ウィジェット
        central = QWidget()
        self.setCentralWidget(central)

        # 画像表示ラベル
        self.image_label = QLabel("ここに画像が表示されます")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(640, 480)

        # 状態ラベル
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
        central.setLayout(main_layout)

        # ボタン接続
        self.capture_btn.clicked.connect(self.controller.capture_image)
        self.compose_btn.clicked.connect(self.controller.compose_image)
        self.save_btn.clicked.connect(self.controller.save_image)

    def display_image(self, cv_img: np.ndarray):
        """QLabelに画像を表示"""
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        qimg = QImage(rgb_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg).scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.KeepAspectRatio
        )
        self.image_label.setPixmap(pixmap)

    def update_status(self, text: str):
        self.status_label.setText(text)