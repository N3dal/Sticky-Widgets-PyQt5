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
from os import system


def clear() -> None:
    # only for debug;
    system("clear")


class StickyWidget(QFrame):

    WIDTH, HEIGHT = (180, 180)
    STYLESHEET = """
        background-color: #47D7D1;
        border-radius: 5px;
        border: 2px solid black;
    """

    NEARBY_THREESHOLD = 10

    class Signals(QObject):

        # send border number and the its the nearby border coordinates to the near by frame or you can say widget if its close enough;
        # tuple(self.x, self.y)
        nearby_frame = pyqtSignal(tuple)

        # send tuple with this border coordinates to the other frames or you can say widgets;
        # in our case we have four corners obviously square and we need to send every corner coordinates;
        # tuple(self.x, self.y)
        moved = pyqtSignal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(StickyWidget.WIDTH, StickyWidget.HEIGHT)
        self.setStyleSheet(StickyWidget.STYLESHEET)

        # intial_x, intial_y = self.x(), self.y()
        self.__mouse_x, self.__mouse_y = 0, 0

        self.__enable_movement = False

        self.signals = StickyWidget.Signals()

        self.borders_state = [0, 0, 0, 0]

    def check_other_moved_frames(self, coordinates: tuple) -> None:
        # print(self.x() - coordinates[0],
        #       self.y() - coordinates[1],
        #       self.x() + self.width() - coordinates[2],
        #       self.y() + self.height() - coordinates[3])
        clear()

        print(f"The Static Frame is :' {self.objectName()}'")
        self.borders_state = [self.x() - coordinates[2],
                              self.y() - coordinates[3],
                              self.x() + self.width() - coordinates[0],
                              self.y() + self.height() - coordinates[1]
                              ]

        for border_number, border_state in enumerate(self.borders_state, 1):
            if abs(border_state) <= StickyWidget.NEARBY_THREESHOLD:
                self.signals.nearby_frame.emit((border_number, border_state))
                # print(f"nearby border is: '{border_number}'")

        print(self.borders_state)

    def nearby_frame_event(self, border_data: tuple):

        border_number, nearby_border_coordinates = border_data
        print(f"The Moved Frame is: '{self.objectName()}' ")
        print(f"Border number is: '{border_number}'")

        if border_number in (1, 3):
            # dealing with x-coords
            self.move(self.x() + nearby_border_coordinates, self.y())

        if border_number in (2, 4):
            # dealing with y-coords
            self.move(self.x(), self.y() + nearby_border_coordinates)

    def mouseDoubleClickEvent(self, e):
        self.__enable_movement = True

        self.__mouse_x, self.__mouse_y = e.x(), e.y()

    def mouseMoveEvent(self, e):

        if not self.__enable_movement:
            return

        dx = e.windowPos().x() - self.__mouse_x
        dy = e.windowPos().y() - self.__mouse_y

        self.move(int(dx), int(dy))

        # and probably we need to send the id of the widget also;
        corners_coordinates = (self.x(),
                               self.y(),
                               self.x() + self.width(),
                               self.y() + self.height()
                               )

        self.signals.moved.emit(corners_coordinates)

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

        frame1 = StickyWidget(parent=self, objectName="frame1")
        frame1.move(100, 200)
        frame1.show()

        frame2 = StickyWidget(parent=self, objectName="frame2")
        frame2.move(500, 400)
        frame2.show()

        frame1.signals.moved.connect(frame2.check_other_moved_frames)
        frame2.signals.moved.connect(frame1.check_other_moved_frames)

        frame1.signals.nearby_frame.connect(frame2.nearby_frame_event)
        frame2.signals.nearby_frame.connect(frame1.nearby_frame_event)


def main():

    app = QApplication(argv)

    root = MainWindow()

    root.show()

    exit(app.exec())


if __name__ == "__main__":
    main()
