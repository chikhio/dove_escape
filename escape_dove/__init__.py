import sys
from game_window import Game_Window
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QToolTip, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox, QWidget
from PyQt6.QtGui import QCloseEvent, QGuiApplication
from PyQt6.QtGui import QFont


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        QToolTip.setFont(QFont('sansSerif', 10))
        self.resize(800, 600)
        self.setWindowTitle('躲避隼隼')
        # 开始按钮
        self.start_btn = QPushButton('开始游戏', self)
        self.start_btn.setToolTip('This is <b>QWidget</b> widget')
        self.start_btn.setFixedWidth(200)
        self.start_btn.clicked.connect(self.start_game_button)
        # 退出按钮
        quit_btn = QPushButton('退出游戏', self)
        quit_btn.clicked.connect(QApplication.instance().quit)
        quit_btn.setFixedWidth(200)
        self.center()
        # 设置主界面布局
        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        v_layout.addWidget(self.start_btn)
        v_layout.addWidget(quit_btn)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout()
        central_layout.addLayout(v_layout)
        central_layout.setContentsMargins(200, 200, 200, 200)
        central_widget.setLayout(central_layout)

    def closeEvent(self, event):
        """退出提示"""
        reply = QMessageBox.question(self, '确定退出？', "你确定要退出吗？", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def start_game_button(self):
        self.game_window = Game_Window(self)
        self.game_window.show()
        self.hide()

    def center(self):
        """将窗口置于中央"""
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    mainwindow = Mainwindow()
    mainwindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
