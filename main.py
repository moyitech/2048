# -*- coding = utf-8 -*-
# @Time: 2023/01/06
# @Author:MoyiTech
# @Software: PyCharm
import sys
import copy

from PyQt5 import QtGui
import settings

import core
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QDesktopWidget, QApplication, QGridLayout, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QFont


class Gui(QMainWindow):

    # 定义按键映射
    keyboard_mapping = {
        Qt.Key_Up: lambda obj: obj.up_move,
        Qt.Key_Down: lambda obj: obj.down_move,
        Qt.Key_Left: lambda obj: obj.left_move,
        Qt.Key_Right: lambda obj: obj.right_move
    }

    def __init__(self):
        super(Gui, self).__init__()
        self.central_widget = None
        self.grid = None
        self.positions = [(i, j) for i in range(0, 4) for j in range(0, 4)]
        self.init_ui()

    def init_ui(self):

        self.setWindowIcon(QIcon('damotouicon.ico'))
        self.resize(400, 400)
        self.to_center()
        self.setWindowTitle('2048 Game  by.moyi')
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet('background-color: #92877d')
        self.central_widget.setLayout(self.grid)

        self.grids_matrix = copy.deepcopy(game.map)
        for i in range(len(self.grids_matrix)):
            for j in range(len(self.grids_matrix[i])):
                text = QLabel()
                self.grids_matrix[i][j] = text
                self.grid.addWidget(text, i, j)
        print(self.grids_matrix)
        print(self.positions)
        self.load_map()

        self.show()

    def load_map(self):
        for i, j in self.positions:
            text = self.grids_matrix[i][j]  # type: QLabel
            if game.map[i][j] != 0:
                item = str(game.map[i][j])
                text.setText(item)
                text.setAlignment(Qt.AlignCenter)
                # 设置颜色、背景
                text.setStyleSheet(f'color: {settings.CELL_COLOR_DICT[item]}; '
                                   f'background-color: {settings.CELL_BACKGROUND_COLOR_DICT[item]}')
                # 设置字体、大小
                font = QFont('黑体')
                font.setPixelSize(font.pointSize() * 4)
                text.setFont(font)
            else:
                text.setText('')
                text.setStyleSheet('background-color: #9e948a')

            # text.setText()

            # self.grid.addWidget(text, i, j)
        pass

    def to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        # 如果无法移动 且无空缺 游戏结束
        if a0.key() in self.keyboard_mapping:
            if not self.keyboard_mapping[a0.key()](game)():
                if not (game.movable() or game.have_empty()):
                    QMessageBox.information(self, 'game over', "GAME OVER!", QMessageBox.Yes, QMessageBox.Yes)
                    print('Game over')
                    game.__init__()
                    game.print()
                    self.load_map()
                    return
            game.generate()
            game.print()
            self.load_map()
        # elif


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 对高分辨率的支持
    app = QApplication(sys.argv)
    game = core.Game()
    game.print()
    gui = Gui()
    # gui.keyboard_mapping[Qt.Key_Up](game)()
    # game.print()
    sys.exit(app.exec_())
