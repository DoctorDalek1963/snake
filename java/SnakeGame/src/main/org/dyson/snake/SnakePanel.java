/*
 * snake - The same simple snake game in multiple languages
 * Copyright (C) 2022 D. Dyson (DoctorDalek1963)
 *
 * This program is licensed under GNU GPLv3, available here:
 * <https://www.gnu.org/licenses/gpl-3.0.html>
 */

package org.dyson.snake;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.*;
import java.util.Timer;
import javax.swing.*;

public class SnakePanel extends JPanel implements KeyListener {
	private static final Random random = new Random();

	private final Color colourPlayer = new Color(0xe7, 0x03, 0x03);
	private final Color colourTail = new Color(0xfb, 0x41, 0x7c);
	private final Color colourApple = new Color(0x09, 0xdd, 0x01);

	private final int gridWidth, gridHeight, gridCellSize;
	private int fps;

	private Point posPlayer, posApple;
	private Direction dirPlayer;

	private ArrayList<Point> snakeParts = new ArrayList<>();
	private boolean gameOver = false;

	private final Timer timer = new Timer();
	private final TimerTask timerTask = new TimerTask() { @Override public void run() { updateGame(); }};
	private boolean timerStarted;

	SnakePanel(int width, int height, int gridCellSize, int fps) {
		super();

		this.setSize(width * gridCellSize, height * gridCellSize);
		this.setVisible(true);

		JFrame frame = new JFrame("Snake (Java with Swing)");
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
		this.dirPlayer = Direction.NONE;

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

		switch (dirPlayer) {
			case UP -> posPlayer.y = (posPlayer.y - 1 + gridHeight) % gridHeight;
			case DOWN -> posPlayer.y = (posPlayer.y + 1 + gridHeight) % gridHeight;
			case LEFT -> posPlayer.x = (posPlayer.x - 1 + gridWidth) % gridWidth;
			case RIGHT -> posPlayer.x = (posPlayer.x + 1 + gridWidth) % gridWidth;
		}



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

	@Override public void keyTyped(KeyEvent e) {}

	@Override
	public void keyPressed(KeyEvent e) {
		int code = e.getKeyCode();

		if ((code == KeyEvent.VK_UP || code == KeyEvent.VK_W) && dirPlayer != Direction.DOWN) {
			dirPlayer = Direction.UP;

		} else if ((code == KeyEvent.VK_DOWN || code == KeyEvent.VK_S) && dirPlayer != Direction.UP) {
			dirPlayer = Direction.DOWN;

		} else if ((code == KeyEvent.VK_LEFT || code == KeyEvent.VK_A) && dirPlayer != Direction.RIGHT) {
			dirPlayer = Direction.LEFT;

		} else if ((code == KeyEvent.VK_RIGHT || code == KeyEvent.VK_D) && dirPlayer != Direction.LEFT) {
			dirPlayer = Direction.RIGHT;
		}

		updateGame();

		if (!timerStarted) {
			timer.scheduleAtFixedRate(timerTask, 0, 1000 / fps);
			timerStarted = true;
		}
	}

	@Override public void keyReleased(KeyEvent e) {}
}
