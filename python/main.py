#!/usr/bin/env python

# snake - The same simple snake game in multiple languages
# Copyright (C) 2022 D. Dyson (DoctorDalek1963)

# This program is licensed under GNU GPLv3, available here:
# <https://www.gnu.org/licenses/gpl-3.0.html>

"""A simple one-file snake game."""

import argparse
import enum
import sys
from random import randrange

from PyQt5.QtCore import QRect, Qt, QTimer
from PyQt5.QtGui import QColor, QKeyEvent, QKeySequence, QPainter, QPaintEvent, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow


Direction = enum.Enum('Direction', 'UP DOWN LEFT RIGHT')


class SnakeMainWindow(QMainWindow):
    """A simple main window class to contain the game."""

    colour_player: QColor = QColor(0x05, 0x78, 0x12)  # Red
    colour_tail: QColor = QColor(0x6c, 0xfb, 0x4b); # Pink
    colour_apple: QColor = QColor(0xfb, 0x06, 0x06); # Green

    def __init__(self, *, width: int, height: int, grid_cell_size: int, fps: int):
        """Create the main window."""
        super().__init__()

        self.grid_width = width
        self.grid_height = height
        self.grid_cell_size = grid_cell_size
        self.fps = fps

        self.pos_player: tuple[int, int] = (randrange(self.grid_width), randrange(self.grid_height))

        # The direction doesn't matter because it will be set when the player first moves
        self.dir_player: Direction | None = None

        self.pos_apple: tuple[int, int] = (0, 0)
        self.place_apple()

        self.snake_parts: list[tuple[int, int]] = []
        self.game_over = False

        self.setFixedSize(self.grid_cell_size * self.grid_width, self.grid_cell_size * self.grid_height)
        self.setWindowTitle('Snake (Python with PyQt5)')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer_started = False

    def place_apple(self) -> None:
        """Place the apple in a place that isn't the same as the player position."""
        # We don't want the apple to be in the same place as the player
        self.pos_apple = self.pos_player

        while self.pos_apple == self.pos_player:
            self.pos_apple = (randrange(self.grid_width), randrange(self.grid_height))

    @property
    def score(self) -> str:
        """Return the player's score."""
        return str(max(0, len(self.snake_parts) - 1))

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

    def reset_game(self) -> None:
        """Reset the game."""
        self.game_over = False
        self.snake_parts = []

        self.pos_player = (randrange(self.grid_width), randrange(self.grid_height))
        self.dir_player = None
        self.place_apple()

        self.timer_started = False
        self.timer.stop()

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
                f'GAME OVER\n\nScore: {self.score}'
            )
            return

        # Draw tail
        painter.setPen(QPen(self.colour_tail))
        for part in self.snake_parts:
            painter.fillRect(
                int(part[0] * self.grid_cell_size + 0.1 * self.grid_cell_size),
                int(part[1] * self.grid_cell_size + 0.1 * self.grid_cell_size),
                int(0.8 * self.grid_cell_size),
                int(0.8 * self.grid_cell_size),
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

        painter.setPen(QPen(QColor(0, 0, 0)))

        font = painter.font()
        font.setPixelSize(24)
        painter.setFont(font)

        painter.drawText(
            QRect(10, 10, 100, 30),
            Qt.AlignLeft | Qt.AlignTop,
            f'Score: {self.score}'
        )

        painter.end()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle a QKeyEvent."""
        if event.key() in (Qt.Key_Up, Qt.Key_W) and self.dir_player != Direction.DOWN:
            self.dir_player = Direction.UP
            self.update_game()

        elif event.key() in (Qt.Key_Down, Qt.Key_S) and self.dir_player != Direction.UP:
            self.dir_player = Direction.DOWN
            self.update_game()

        elif event.key() in (Qt.Key_Left, Qt.Key_A) and self.dir_player != Direction.RIGHT:
            self.dir_player = Direction.LEFT
            self.update_game()

        elif event.key() in (Qt.Key_Right, Qt.Key_D) and self.dir_player != Direction.LEFT:
            self.dir_player = Direction.RIGHT
            self.update_game()

        elif event.matches(QKeySequence.Refresh):
            self.reset_game()
            self.update()
            return

        elif event.key() == Qt.Key_Plus:
            self.fps += 1
            self.timer.setInterval(int(1000 / self.fps))

        elif event.key() == Qt.Key_Minus:
            self.fps = max(1, self.fps - 1)
            self.timer.setInterval(int(1000 / self.fps))

        else:
            event.ignore()
            return

        if not self.timer_started:
            self.timer.start(int(1000 / self.fps))


def main() -> None:
    """Show the window."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-w',
        '--width',
        type=int,
        required=False,
        default=16
    )
    parser.add_argument(
        '-H',
        '--height',
        type=int,
        required=False,
        default=12
    )
    parser.add_argument(
        '-s',
        '--cellsize',
        type=int,
        required=False,
        default=50
    )
    parser.add_argument(
        '-f',
        '--fps',
        type=int,
        required=False,
        default=5
    )

    args = parser.parse_args()

    if args.width < 3 or args.height < 3:
        raise ValueError('Minimum board size is 3x3')

    app = QApplication([])
    window = SnakeMainWindow(
        width=args.width,
        height=args.height,
        grid_cell_size=args.cellsize,
        fps=args.fps
    )
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
