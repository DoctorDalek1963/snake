/*
 * snake - The same simple snake game in multiple languages
 * Copyright (C) 2022 D. Dyson (DoctorDalek1963)
 *
 * This program is licensed under GNU GPLv3, available here:
 * <https://www.gnu.org/licenses/gpl-3.0.html>
 */

package org.dyson.snake;

import javax.swing.*;

public class SnakeMainWindow extends JFrame {
	SnakeMainWindow(int width, int height, int gridCellSize, int fps) {
		super();

		SnakePanel snakePanel = new SnakePanel(width, height, gridCellSize, fps);

		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		setTitle("Snake (Java)");

		this.add(snakePanel);
		this.pack();

		setSize(width * gridCellSize, height * gridCellSize);
//		setResizable(false);
	}
}
