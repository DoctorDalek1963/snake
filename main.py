#!/usr/bin/env python

# snake - A simple snake game in Python
# Copyright (C) 2022 D. Dyson (DoctorDalek1963)

# This program is licensed under GNU GPLv3, available here:
# <https://www.gnu.org/licenses/gpl-3.0.html>

"""A simple one-file snake game."""

import enum
import sys
import random
from random import randint

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPaintEvent, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow


Direction = enum.Enum('Direction', 'UP DOWN LEFT RIGHT')


class SnakeMainWindow(QMainWindow):
    """A simple main window class to contain the game.

    The play space is a 10x10 grid.
    """

    def __init__(self):
        """Create the main window."""
        super().__init__()
        # Random position near the middle and random direction
        self.pos_player: tuple[int, int] = (randint(2, 7), randint(2, 7))
        self.dir_player: Direction = random.choice(list(Direction))

        self.pos_apple: tuple[int, int] = (0, 0)
        self.place_apple()

        self.grid_cell_size: int = 80
        self.colour_player: QColor = QColor(0xe7, 0x03, 0x03)  # Red
        self.colour_apple: QColor = QColor(0x09, 0xdd, 0x01)  # Green

        self.setFixedSize(self.grid_cell_size * 10, self.grid_cell_size * 10)

    def place_apple(self) -> None:
        """Place the apple in a place that isn't the same as the player position."""
        # We don't want the apple to be in the same place as the player
        self.pos_apple = self.pos_player
        while self.pos_apple == self.pos_player:
            self.pos_apple = (randint(0, 9), randint(0, 9))

    def draw_player(self, painter: QPainter) -> None:
        """Draw the player on the grid."""
        painter.setPen(QPen(self.colour_player))
        painter.drawRect(
            self.pos_player[0] * self.grid_cell_size,
            self.pos_player[1] * self.grid_cell_size,
            self.grid_cell_size,
            self.grid_cell_size
        )

    def draw_apple(self, painter: QPainter) -> None:
        """Draw the apple on the grid."""
        painter.setPen(QPen(self.colour_apple))
        painter.drawRect(
            self.pos_apple[0] * self.grid_cell_size,
            self.pos_apple[1] * self.grid_cell_size,
            self.grid_cell_size,
            self.grid_cell_size
        )

    def paintEvent(self, event: QPaintEvent) -> None:
        """Handle a QPaintEvent by drawing everything on the grid."""
        painter = QPainter()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)

        self.draw_player(painter)
        self.draw_apple(painter)

        painter.end()
        event.accept()


def main() -> None:
    """."""
    app = QApplication([])
    window = SnakeMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
