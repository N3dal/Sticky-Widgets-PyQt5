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


class MoreThanMainWindowException(Exception):
    pass


class MainWindow(QMainWindow):

    WIDTH, HEIGHT = (500, 500)
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


def main():

    app = QApplication(argv)

    root = MainWindow()

    root.show()

    exit(app.exec())


if __name__ == "__main__":
    main()
