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
import java.util.Timer;
import javax.swing.*;

public class SnakePanel extends JPanel {
	private static final Random random = new Random();

	private final Color colourPlayer = new Color(0xe7, 0x03, 0x03);
	private final Color colourTail = new Color(0xfb, 0x41, 0x7c);
	private final Color colourApple = new Color(0x09, 0xdd, 0x01);

	private final int gridWidth, gridHeight, gridCellSize;
	private int fps;

	private Point posPlayer, posApple;
	private Optional<Direction> dirPlayer;

	private ArrayList<Point> snakeParts = new ArrayList<>();
	private boolean gameOver = false;

	private final Timer timer = new Timer();
	private final TimerTask timerTask = new TimerTask() { @Override public void run() { updateGame(); }};
	private boolean timerStarted;

	private final JFrame frame = new JFrame("Snake (Java with Swing)");

	SnakePanel(int width, int height, int gridCellSize, int fps) {
		super();

		this.setSize(width * gridCellSize, height * gridCellSize);
		this.setVisible(true);

		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(this.getSize());
		frame.addKeyListener(this);
		frame.add(this);
		frame.setVisible(true);

		this.gridWidth = width;
		this.gridHeight = height;
		this.gridCellSize = gridCellSize;
		this.fps = fps;

		this.posPlayer = new Point(random.nextInt(gridWidth), random.nextInt(gridHeight));
		this.dirPlayer = Optional.empty();

		this.posApple = new Point(0, 0);
		placeApple();

		timerStarted = false;
	}

	private void placeApple() {
		posApple = posPlayer;

		while (posApple.x == posPlayer.x && posApple.y == posPlayer.y) {
			posApple = new Point(random.nextInt(gridWidth), random.nextInt(gridHeight));
		}
	}

	private void updateGame() {
		repaint();
	}

	@Override
	public void paintComponent(Graphics g) {
		super.paintComponent(g);

		// Draw apple
		g.setColor(colourApple);
		g.fillRect(
				(int) (gridCellSize * (posApple.x + 0.15)),
				(int) (gridCellSize * (posApple.y + 0.15)),
				(int) (0.7 * gridCellSize),
				(int) (0.7 * gridCellSize)
		);

		// Draw player head
		g.setColor(colourPlayer);
		g.fillRect(
				gridCellSize * posPlayer.x,
				gridCellSize * posPlayer.y,
				gridCellSize,
				gridCellSize
		);
	}
}
