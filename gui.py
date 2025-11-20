import sys
import cv2
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QMessageBox, QFrame)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, Slot

# ロジックモジュールのインポート
from logic import MyVideoCapture, composite_images

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("画像合成GUIアプリケーション")
        self.resize(900, 600)

        # --- ステータス管理用変数 ---
        self.capture_img_data = None  # カメラ画像 (OpenCV形式 BGR)
        self.result_img_data = None   # 合成結果画像 (OpenCV形式 BGR)
        self.base_image_path = 'images/google.png' # 背景画像パス

        # --- UIのセットアップ ---
        self.init_ui()

    def init_ui(self):
        """レイアウトとウィジェットの初期化"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. ステータス表示ラベル
        self.status_label = QLabel("準備完了: [写真取得]ボタンを押してください")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("background-color: #ddd; padding: 5px; border-radius: 3px;")
        main_layout.addWidget(self.status_label)

        # 2. 画像表示エリア (左右に配置)
        image_area_layout = QHBoxLayout()
        
        # 左側：カメラ画像プレビュー
        self.preview_label = self.create_image_label("カメラ画像")
        image_area_layout.addWidget(self.preview_label)

        # 右側：合成結果プレビュー
        self.result_label = self.create_image_label("合成結果")
        image_area_layout.addWidget(self.result_label)

        main_layout.addLayout(image_area_layout)

        # 3. 操作ボタンエリア
        button_layout = QHBoxLayout()

        # ボタン定義
        # (A) 写真取得ボタン
        self.btn_capture = QPushButton("📸 写真取得")
        self.btn_capture.clicked.connect(self.on_capture_click)
        self.btn_capture.setMinimumHeight(40)

        # (B) 画像合成実行ボタン
        self.btn_composite = QPushButton("✨ 画像合成実行")
        self.btn_composite.clicked.connect(self.on_composite_click)
        self.btn_composite.setMinimumHeight(40)
        self.btn_composite.setEnabled(False) # 最初は無効化

        # (C) 結果保存ボタン
        self.btn_save = QPushButton("💾 結果保存")
        self.btn_save.clicked.connect(self.on_save_click)
        self.btn_save.setMinimumHeight(40)
        self.btn_save.setEnabled(False) # 最初は無効化

        # レイアウトに追加
        button_layout.addWidget(self.btn_capture)
        button_layout.addWidget(self.btn_composite)
        button_layout.addWidget(self.btn_save)

        main_layout.addLayout(button_layout)

    def create_image_label(self, text):
        """画像表示用の共通ラベル設定"""
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFrameShape(QFrame.Box) # 枠線
        label.setStyleSheet("background-color: #f0f0f0; font-weight: bold; color: #888;")
        label.setScaledContents(True) # ウィンドウサイズに合わせて画像を伸縮
        label.setMinimumSize(320, 240)
        return label

    @Slot()
    def on_capture_click(self):
        """[写真取得]ボタンの処理"""
        try:
            self.status_label.setText("処理中: カメラに接続しています...")
            QApplication.processEvents() # UI更新を強制

            # カメラ接続と撮影
            app = MyVideoCapture()
            self.capture_img_data = app.get_img()
            app.release()

            # GUIに表示
            self.display_image(self.capture_img_data, self.preview_label)
            
            # 状態更新
            self.status_label.setText("成功: 画像を取得しました。[画像合成実行]を押してください。")
            self.btn_composite.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "カメラエラー", str(e))
            self.status_label.setText("エラー: 画像取得に失敗しました")

    @Slot()
    def on_composite_click(self):
        """[画像合成実行]ボタンの処理"""
        if self.capture_img_data is None:
            return

        try:
            self.status_label.setText("処理中: 画像合成を実行しています...")
            
            # ロジックモジュールの関数を呼び出し
            self.result_img_data = composite_images(self.base_image_path, self.capture_img_data)

            # GUIに表示
            self.display_image(self.result_img_data, self.result_label)
            
            # 状態更新
            self.status_label.setText("成功: 合成が完了しました。[結果保存]で保存できます。")
            self.btn_save.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "処理エラー", f"合成中にエラーが発生しました:\n{e}")
            self.status_label.setText("エラー: 合成処理に失敗しました")

    @Slot()
    def on_save_click(self):
        """[結果保存]ボタンの処理"""
        if self.result_img_data is None:
            return
        
        try:
            output_dir = 'output_images'
            os.makedirs(output_dir, exist_ok=True)
            save_path = os.path.join(output_dir, 'gui_result.png')
            
            # 保存実行
            cv2.imwrite(save_path, self.result_img_data)
            
            QMessageBox.information(self, "保存完了", f"画像を保存しました:\n{save_path}")
            self.status_label.setText(f"保存完了: {save_path}")
            
        except Exception as e:
            QMessageBox.warning(self, "保存エラー", str(e))

    def display_image(self, cv_img, label_widget):
        """OpenCVの画像(BGR)をPySideのQLabelに表示するヘルパー関数"""
        if cv_img is None:
            return

        # カラー変換 BGR -> RGB
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        
        # QImage作成
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # QPixmapに変換してセット
        label_widget.setPixmap(QPixmap.fromImage(qt_image))