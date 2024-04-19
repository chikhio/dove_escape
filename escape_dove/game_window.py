import sys
import os
from random import randint
from time import time
from dove import Dove
from monster import Monster
from PyQt6.QtGui import QPixmap, QVector2D, QCursor
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import QTimer, QPoint


class Game_Window(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('游戏')
        self.resize(800, 600)
        self.init_ui()
        self.flag = True

    def init_ui(self):
        self.game_start_time = time()
        self.create_dove()
        self.set_mouse_pos_center()
        self.move_dove()
        self.monsters = []
        self.create_monster_timer = QTimer(self)
        self.create_monster_timer.timeout.connect(
            self.check_and_create_monsters)
        self.create_monster_timer.start(1000)
        self.monster_move_timer = QTimer(self)
        self.monster_move_timer.timeout.connect(self.move_monster_step)
        self.monster_move_timer.start(15)

    def create_dove(self):
        """创建鸽子图片标签并设置初始位置。"""
        self.image_label = Dove(self)
        dove_image_path = os.path.join(
            os.path.dirname(__file__), 'image', 'dove.png')
        pixmap = QPixmap(dove_image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.move(self.size().width() // 2,
                              self.size().height() // 2)

    def set_mouse_pos_center(self):
        """将鼠标初始位置设置为窗口中心。"""
        screen_rect = QApplication.primaryScreen().geometry()
        center_x = screen_rect.width() // 2
        center_y = screen_rect.height() // 2
        QCursor.setPos(center_x, center_y)

    def move_dove(self):
        """启动定时器以持续根据鼠标光标更新鸽子位置。"""
        self.dove_initial_position = self.image_label.pos()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image_position)
        self.timer.start(1)

    def update_image_position(self):
        """根据鼠标光标更新鸽子位置。"""
        mouse_position = QCursor.pos()
        global_position = self.mapToGlobal(QPoint(0, 0))
        image_position = QPoint(mouse_position.x(
        ) - global_position.x(), mouse_position.y() - global_position.y())
        self.image_label.move(image_position)

    def check_and_create_monsters(self):
        """检测当前怪物数量，如果需要则创建新的怪物"""
        max_monsters = 10
        if len(self.monsters) < max_monsters:
            self.create_monster()

    def create_monster(self):
        """创建怪物图片标签并启动用于其移动的定时器。"""
        dove_pos = self.image_label.pos()
        monster = Monster(self)
        monster_image_path = os.path.join(os.path.dirname(
            __file__), 'image', 'falco_tinnunculus.png')
        pixmap = QPixmap(monster_image_path)
        monster.setPixmap(pixmap)
        monster.raise_()  # 提升怪物到顶层
        monster.show()    # 确保怪物是可见的
        self.monster_appearance_loc(monster)
        self.monsters.append(monster)
        monster_direction = QVector2D(dove_pos - monster.pos()).normalized()
        monster.move_direction = monster_direction
        self.distance_pos = self.dove_initial_position - monster.pos()

    def move_monster_step(self):
        """根据与鸽子的距离移动怪物。"""
        step_size = 5
        for monster in self.monsters:
            step = step_size * monster.move_direction
            new_pos = monster.pos() + QPoint(int(step.x()), int(step.y()))
            monster.move(new_pos)
        # 如果怪物到达窗口底部，则重置其位置
            if not self.rect().contains(monster.pos()):
                self.monster_appearance_loc(monster)
                dove_pos = self.image_label.pos()
                monster.move_direction = QVector2D(
                    dove_pos - monster.pos()).normalized()
            if self.check_collision(self.image_label, monster) and self.flag == True:
                self.game_over()

    def check_collision(self, dove, monster):
        """检查是否碰撞"""
        return dove.geometry().intersects(monster.geometry())

    def game_over(self):
        """游戏结束处理"""
        game_end_time = time()
        elapsed_time = game_end_time - self.game_start_time
        elapsed_minutes = int(elapsed_time//60)
        elapsed_seconds = int(elapsed_time % 60)
        self.flag = False
        QMessageBox.information(
            self, "游戏结束", f"存活{elapsed_minutes}分{elapsed_seconds}秒")
        self.close()
        if self.parent:
            self.parent.show()

    def monster_appearance_loc(self, monster):
        """随机设置怪物的初始位置在窗口边缘。"""
        x = randint(1, 4)
        if x == 1:
            monster.move(0,
                         randint(0, self.size().width()))
        elif x == 2:
            monster.move(
                self.size().width(), randint(0, self.size().height()))
        elif x == 3:
            monster.move(
                randint(0, self.size().width()),
                self.size().height()
            )
        else:
            monster.move(-monster.size().width(),
                         randint(0, self.size().height()))

    def closeEvent(self, event):
        """处理游戏窗口的关闭事件。"""
        if self.parent:
            self.parent.show()
