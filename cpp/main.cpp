#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <QApplication>
#include <QKeyEvent>
#include <QMainWindow>
#include <QPainter>
#include <QTimer>

enum Direction { UP, DOWN, LEFT, RIGHT };

struct Point { int x, y; };

class SnakeMainWindow : public QMainWindow
{
	const QColor colourPlayer = QColor(0xe7, 0x03, 0x03);
	const QColor colourTail = QColor(0xfb, 0x41, 0x7c);
	const QColor colourApple = QColor(0x09, 0xdd, 0x01);

	const int gridWidth, gridHeight, gridCellSize;
	int fps;

	Point posPlayer, posApple;
	std::optional<Direction> dirPlayer;

	std::vector<Point> snakeParts = std::vector<Point>();
	bool gameOver = false;

	QTimer *timer;
	bool timerStarted = false;

	void placeApple(void)
	{
		posApple = posPlayer;

		while (posApple.x == posPlayer.x && posApple.y == posPlayer.y) {
			posApple = {
				rand() % gridWidth,
				rand() % gridHeight
			};
		}
	}

	void paintEvent(QPaintEvent *)
	{
		QPainter painter(this);
		painter.setRenderHint(QPainter::Antialiasing);
		painter.setBrush(Qt::NoBrush);

		// TODO: Draw tail

		// Draw apple
		painter.setPen(QPen(colourApple));
		painter.fillRect(
			gridCellSize * int(posApple.x + 0.15),
			gridCellSize * int(posApple.y + 0.15),
			int(0.7 * gridCellSize),
			int(0.7 * gridCellSize),
			colourApple
		);

		// Draw player head
		painter.setPen(QPen(colourPlayer));
		painter.fillRect(
			posPlayer.x * gridCellSize,
			posPlayer.y * gridCellSize,
			gridCellSize,
			gridCellSize,
			colourPlayer
		);
	}

	void keyPressEvent(QKeyEvent *event)
	{
		int key = event->key();

		if ((key == Qt::Key_Up || key == Qt::Key_W) && dirPlayer != DOWN){
			dirPlayer = UP;

		} else if ((key == Qt::Key_Down || key == Qt::Key_S) && dirPlayer != UP) {
			dirPlayer = DOWN;

		} else if ((key == Qt::Key_Left || key == Qt::Key_A) && dirPlayer != RIGHT) {
			dirPlayer = LEFT;

		} else if ((key == Qt::Key_Right || key == Qt::Key_D) && dirPlayer != LEFT) {
			dirPlayer = RIGHT;

		} else {
			event->ignore();
			return;
		}

		updateGame();

		if (!timerStarted)
			timer->start(int(1000 / fps));
	}

private Q_SLOTS:
	void updateGame(void)
	{
		if (dirPlayer == UP) {
			posPlayer = { posPlayer.x, (posPlayer.y - 1 + gridHeight) % gridHeight };

		} else if (dirPlayer == DOWN) {
			posPlayer = { posPlayer.x, (posPlayer.y + 1 + gridHeight) % gridHeight };

		} else if (dirPlayer == LEFT) {
			posPlayer = { (posPlayer.x - 1 + gridWidth) % gridWidth, posPlayer.y };

		} else if (dirPlayer == RIGHT) {
			posPlayer = { (posPlayer.x + 1 + gridWidth) % gridWidth, posPlayer.y };
		}

		update();
	}

public:
	SnakeMainWindow(int width, int height, int gridCellSize, int fps)
		: gridWidth(width), gridHeight(height), gridCellSize(gridCellSize)
	{
		this->fps = fps;

		this->posPlayer = {
			rand() % this->gridWidth,
			rand() % this->gridHeight
		};
		this->dirPlayer = std::nullopt;

		this->posApple = {0, 0};
		placeApple();

		setFixedSize(this->gridCellSize * this->gridWidth, this->gridCellSize * this->gridHeight);
		setWindowTitle("Snake (C++)");

		this->timer = new QTimer(this);
		connect(this->timer, &QTimer::timeout, this, &SnakeMainWindow::updateGame);
	}
};

int main()
{
	srand(time(NULL));

	int fakeArgc = 0;
	QApplication app(fakeArgc, nullptr);

	SnakeMainWindow window = SnakeMainWindow(16, 12, 50, 5);
	window.show();
	return app.exec();
}
