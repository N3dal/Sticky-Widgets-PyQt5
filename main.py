#!/usr/bin/python3
# -----------------------------------------------------------------
# Description;
#
#
#
# Author:N84.
#
# Create Date:Mon Mar  4 22:24:29 2024.
# ///
# ///
# ///
# -----------------------------------------------------------------

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sys import (argv, exit)
from exceptions import *


class StickyWidget(QFrame):

    WIDTH, HEIGHT = (180, 180)
    STYLESHEET = """
        background-color: #47D7D1;
        border-radius: 5px;
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(StickyWidget.WIDTH, StickyWidget.HEIGHT)
        self.setStyleSheet(StickyWidget.STYLESHEET)

        # intial_x, intial_y = self.x(), self.y()
        self.__mouse_x, self.__mouse_y = 0, 0

        self.__enable_movement = False

    def mouseDoubleClickEvent(self, e):
        self.__enable_movement = True

        self.__mouse_x, self.__mouse_y = e.x(), e.y()

    def mouseMoveEvent(self, e):

        if not self.__enable_movement:
            return

        dx = e.windowPos().x() - self.__mouse_x
        dy = e.windowPos().y() - self.__mouse_y

        self.move(int(dx), int(dy))

    def mouseReleaseEvent(self, e):

        if self.__enable_movement:
            self.__enable_movement = False


class MainWindow(QMainWindow):

    WIDTH, HEIGHT = (800, 600)
    TITLE = "Sticky Widgets"
    STYLESHEET = """
        background-color: #F8F8F8;
    """
    windows = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if MainWindow.windows:
            # Singleton;
            raise MoreThanMainWindow(
                "You can't create more than one 'MainWidow'!!")

        MainWindow.windows.append(self)

        self.setFixedSize(MainWindow.WIDTH, MainWindow.HEIGHT)
        self.setStyleSheet(MainWindow.STYLESHEET)

        self.__setup_widgets()

    def __setup_widgets(self):

        frame = StickyWidget(parent=self)
        frame.move(100, 200)
        frame.show()


def main():

    app = QApplication(argv)

    root = MainWindow()

    root.show()

    exit(app.exec())


if __name__ == "__main__":
    main()
