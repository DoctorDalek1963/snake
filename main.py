#!/usr/bin/env python

# snake - A simple snake game in Python
# Copyright (C) 2022 D. Dyson (DoctorDalek1963)

# This program is licensed under GNU GPLv3, available here:
# <https://www.gnu.org/licenses/gpl-3.0.html>

"""A simple one-file snake game."""

import enum
import sys
from random import randrange

from PyQt5.QtCore import QRect, Qt, QTimer
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPaintEvent, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow


Direction = enum.Enum('Direction', 'UP DOWN LEFT RIGHT')


class SnakeMainWindow(QMainWindow):
    """A simple main window class to contain the game."""

    grid_cell_size: int = 50
    grid_width: int = 16
    grid_height: int = 12

    colour_player: QColor = QColor(0xe7, 0x03, 0x03)  # Red
    colour_tail: QColor = QColor(0xfb, 0x41, 0x7c)  # Pink
    colour_apple: QColor = QColor(0x09, 0xdd, 0x01)  # Green

    def __init__(self):
        """Create the main window."""
        super().__init__()

        # Random position near the middle
        self.pos_player: tuple[int, int] = (randrange(1, self.grid_width - 1), randrange(1, self.grid_height - 1))

        # The direction doesn't matter because it will be set when the player first moves
        self.dir_player: Direction = Direction.UP

        self.pos_apple: tuple[int, int] = (0, 0)
        self.place_apple()

        self.snake_parts: list[tuple[int, int]] = []
        self.game_over = False

        self.setFixedSize(self.grid_cell_size * self.grid_width, self.grid_cell_size * self.grid_height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self._timer_started = False
        self.fps = 5

    def place_apple(self) -> None:
        """Place the apple in a place that isn't the same as the player position."""
        # We don't want the apple to be in the same place as the player
        self.pos_apple = self.pos_player

        while self.pos_apple == self.pos_player:
            self.pos_apple = (randrange(self.grid_width), randrange(self.grid_height))

    def update_game(self) -> None:
        """Update the game state."""
        if self.pos_player in self.snake_parts[:-1]:
            self.game_over = True
            self.timer.stop()
            self.update()
            return

        if self.pos_player == self.pos_apple:
            self.snake_parts.append(self.pos_player)
            self.place_apple()

        if self.dir_player == Direction.UP:
            self.pos_player = (self.pos_player[0], (self.pos_player[1] - 1) % self.grid_height)
        elif self.dir_player == Direction.DOWN:
            self.pos_player = (self.pos_player[0], (self.pos_player[1] + 1) % self.grid_height)
        elif self.dir_player == Direction.LEFT:
            self.pos_player = ((self.pos_player[0] - 1) % self.grid_width, self.pos_player[1])
        elif self.dir_player == Direction.RIGHT:
            self.pos_player = ((self.pos_player[0] + 1) % self.grid_width, self.pos_player[1])

        self.snake_parts = self.snake_parts[1:]
        self.snake_parts.append(self.pos_player)

        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Handle a QPaintEvent by drawing everything on the grid."""
        painter = QPainter()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)

        if self.game_over:
            font = painter.font()
            font.setPixelSize(48)
            font.setBold(True)
            painter.setFont(font)

            painter.drawText(
                QRect(0, 0, self.width(), self.height()),
                Qt.AlignCenter | Qt.AlignVCenter,
                f'GAME OVER\n\nScore: {len(self.snake_parts)}'
            )
            return

        # Draw tail
        painter.setPen(QPen(self.colour_tail))
        for part in self.snake_parts:
            painter.fillRect(
                int(part[0] * self.grid_cell_size + 0.15 * self.grid_cell_size),
                int(part[1] * self.grid_cell_size + 0.15 * self.grid_cell_size),
                int(0.7 * self.grid_cell_size),
                int(0.7 * self.grid_cell_size),
                self.colour_tail
            )

        # Draw apple
        painter.setPen(QPen(self.colour_apple))
        painter.fillRect(
            int(self.pos_apple[0] * self.grid_cell_size + 0.15 * self.grid_cell_size),
            int(self.pos_apple[1] * self.grid_cell_size + 0.15 * self.grid_cell_size),
            int(0.7 * self.grid_cell_size),
            int(0.7 * self.grid_cell_size),
            self.colour_apple
        )

        # Draw player head
        painter.setPen(QPen(self.colour_player))
        painter.fillRect(
            self.pos_player[0] * self.grid_cell_size,
            self.pos_player[1] * self.grid_cell_size,
            self.grid_cell_size,
            self.grid_cell_size,
            self.colour_player
        )

        painter.end()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle a QKeyEvent."""
        if event.key() == Qt.Key_Up and self.dir_player != Direction.DOWN:
            self.dir_player = Direction.UP
        elif event.key() == Qt.Key_Down and self.dir_player != Direction.UP:
            self.dir_player = Direction.DOWN
        elif event.key() == Qt.Key_Left and self.dir_player != Direction.RIGHT:
            self.dir_player = Direction.LEFT
        elif event.key() == Qt.Key_Right and self.dir_player != Direction.LEFT:
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
