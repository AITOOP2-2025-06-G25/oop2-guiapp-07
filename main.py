import sys
from PySide6.QtWidgets import QApplication
from view import Lecture05View
from gui import Lecture05Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Controller 作成
    controller = Lecture05Controller()

    # View に Controller を渡して作成
    window = Lecture05View(controller)
    controller.view = window  # Controller からも View にアクセスできるように

    # ウィンドウ表示
    window.show()
    sys.exit(app.exec())