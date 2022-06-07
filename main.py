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

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPaintEvent, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow


Direction = enum.Enum('Direction', 'UP DOWN LEFT RIGHT')


class SnakeMainWindow(QMainWindow):
    """A simple main window class to contain the game.

    The play space is a 10x10 grid.
    """

    def __init__(self):
        """Create the main window."""
        super().__init__()

        # Random position near the middle
        self.pos_player: tuple[int, int] = (randint(2, 7), randint(2, 7))

        # The direction doesn't matter because it will be set when the player first moves
        self.dir_player: Direction = Direction.UP

        self.pos_apple: tuple[int, int] = (0, 0)
        self.place_apple()

        self.length_player: int = 0
        self.grid_cell_size: int = 80
        self.colour_player: QColor = QColor(0xe7, 0x03, 0x03)  # Red
        self.colour_apple: QColor = QColor(0x09, 0xdd, 0x01)  # Green

        self.setFixedSize(self.grid_cell_size * 10, self.grid_cell_size * 10)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self._timer_started = False
        self.fps = 5

    def place_apple(self) -> None:
        """Place the apple in a place that isn't the same as the player position."""
        # We don't want the apple to be in the same place as the player
        self.pos_apple = self.pos_player
        while self.pos_apple == self.pos_player:
            self.pos_apple = (randint(0, 9), randint(0, 9))

    def update_game(self) -> None:
        """Update the game state."""
        if self.dir_player == Direction.UP:
            self.pos_player = (self.pos_player[0], (self.pos_player[1] - 1) % 10)
        elif self.dir_player == Direction.DOWN:
            self.pos_player = (self.pos_player[0], (self.pos_player[1] + 1) % 10)
        elif self.dir_player == Direction.LEFT:
            self.pos_player = ((self.pos_player[0] - 1) % 10, self.pos_player[1])
        elif self.dir_player == Direction.RIGHT:
            self.pos_player = ((self.pos_player[0] + 1) % 10, self.pos_player[1])

        self.update()

    def draw_player(self, painter: QPainter) -> None:
        """Draw the player on the grid."""
        painter.setPen(QPen(self.colour_player))
        painter.fillRect(
            self.pos_player[0] * self.grid_cell_size,
            self.pos_player[1] * self.grid_cell_size,
            self.grid_cell_size,
            self.grid_cell_size,
            self.colour_player
        )

    def draw_apple(self, painter: QPainter) -> None:
        """Draw the apple on the grid."""
        painter.setPen(QPen(self.colour_apple))
        painter.fillRect(
            int(self.pos_apple[0] * self.grid_cell_size + 0.15 * self.grid_cell_size),
            int(self.pos_apple[1] * self.grid_cell_size + 0.15 * self.grid_cell_size),
            int(0.7 * self.grid_cell_size),
            int(0.7 * self.grid_cell_size),
            self.colour_apple
        )

    def paintEvent(self, event: QPaintEvent) -> None:
        """Handle a QPaintEvent by drawing everything on the grid."""
        painter = QPainter()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)

        self.draw_apple(painter)
        self.draw_player(painter)

        painter.end()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle a QKeyEvent."""
        if event.key() == Qt.Key_Up:
            self.dir_player = Direction.UP
        elif event.key() == Qt.Key_Down:
            self.dir_player = Direction.DOWN
        elif event.key() == Qt.Key_Left:
            self.dir_player = Direction.LEFT
        elif event.key() == Qt.Key_Right:
            self.dir_player = Direction.RIGHT
        else:
            event.ignore()
            return

        if not self._timer_started:
            self.timer.start(int(1000 / self.fps))


def main() -> None:
    """."""
    app = QApplication([])
    window = SnakeMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
