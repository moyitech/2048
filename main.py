# -*- coding = utf-8 -*-
# @Time: 2023/01/06
# @Author:MoyiTech
# @Software: PyCharm
import sys
import copy

import settings

import core
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QDesktopWidget, QApplication, QGridLayout, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QKeyEvent


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
        # 初始化数据
        self.grids_matrix = None
        self.central_widget = None
        self.grid = None
        self.positions = [(i, j) for i in range(0, 4) for j in range(0, 4)]
        self.init_ui()

    def init_ui(self):
        # 设置窗口进本信息
        self.setWindowIcon(QIcon('damotouicon.ico'))
        self.resize(400, 400)
        self.to_center()
        self.statusBar().showMessage("score: ")
        self.setWindowTitle('2048 Game  by.moyi')

        # 配置栅格布局
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.grid)

        self.central_widget.setStyleSheet('background-color: #92877d')  # 设置背景色
        self.grids_matrix = copy.deepcopy(game.map)  # 根据 map 大小生成矩阵

        # 向矩阵填充label
        for i in range(len(self.grids_matrix)):
            for j in range(len(self.grids_matrix[i])):
                text = QLabel()
                text.setAlignment(Qt.AlignCenter)
                # 设置字体、大小
                font = QFont('黑体')
                font.setPixelSize(font.pointSize() * 4)
                text.setFont(font)
                # 加入栅格布局
                self.grids_matrix[i][j] = text
                self.grid.addWidget(text, i, j)

        self.load_map()
        self.show()

    def load_map(self):
        """
        加载游戏布局
        """
        for i, j in self.positions:
            text = self.grids_matrix[i][j]  # type: QLabel

            if game.map[i][j] != 0:
                item = str(game.map[i][j])
                text.setText(item)

                # 设置颜色、背景
                text.setStyleSheet(f'color: {settings.CELL_COLOR_DICT[item]}; '
                                   f'background-color: {settings.CELL_BACKGROUND_COLOR_DICT[item]}')

            else:
                text.setText('')
                text.setStyleSheet('background-color: #9e948a')  # 设置背景色

        self.statusBar().showMessage(f'score: {game.get_score()}')

    def to_center(self):
        """
        窗口居中
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() in self.keyboard_mapping:
            # 没移动成功，直接return 不generate
            if not self.keyboard_mapping[a0.key()](game)():
                return

            game.generate()  # 生成新块

            # 输出结果
            game.print()
            self.load_map()

            # 完成该步骤后 若不可合并或且不存在空值时结束游戏
            if game.is_game_over():
                QMessageBox.information(self, 'game over', "GAME OVER!", QMessageBox.Yes, QMessageBox.Yes)
                print('Game over')

                # 开始新的游戏
                game.__init__()
                game.print()
                self.load_map()


if __name__ == '__main__':
    # 初始化 game
    game = core.Game()
    game.print()

    # 初始化GUI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 对高分辨率的支持
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
