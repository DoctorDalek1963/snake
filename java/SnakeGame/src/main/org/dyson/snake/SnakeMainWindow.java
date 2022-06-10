/*
 * snake - The same simple snake game in multiple languages
 * Copyright (C) 2022 D. Dyson (DoctorDalek1963)
 *
 * This program is licensed under GNU GPLv3, available here:
 * <https://www.gnu.org/licenses/gpl-3.0.html>
 */

package org.dyson.snake;

import java.awt.*;
import java.util.*;
import javax.swing.*;

enum Direction { UP, DOWN, LEFT, RIGHT }

public class SnakeMainWindow extends JFrame {
	private static final Random random = new Random();
	private final int gridWidth, gridHeight, gridCellSize;
	private int fps;

	Point posPlayer, posApple;
	Optional<Direction> dirPlayer;

	ArrayList<Point> snakeParts = new ArrayList<>();
	boolean gameOver = false;

	SnakeMainWindow(int width, int height, int gridCellSize, int fps) {
		super();

		this.gridWidth = width;
		this.gridHeight = height;
		this.gridCellSize = gridCellSize;
		this.fps = fps;

		this.posPlayer = new Point(random.nextInt(gridWidth), random.nextInt(gridHeight));
		this.dirPlayer = Optional.empty();

		this.posApple = new Point(0, 0);
		placeApple();

		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setSize(gridWidth * gridCellSize, gridHeight * gridCellSize);
		setTitle("Snake (Java)");
	}

	private void placeApple() {
		posApple = posPlayer;

		while (posApple.x == posPlayer.x && posApple.y == posPlayer.y) {
			posApple = new Point(random.nextInt(gridWidth), random.nextInt(gridHeight));
		}
	}
}
