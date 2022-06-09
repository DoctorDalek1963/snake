#include <QApplication>
#include <QMainWindow>
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
		this->posApple = this->posPlayer;

		while (posApple.x == posPlayer.x && posApple.y == posPlayer.y) {
			this->posApple = {
				rand() % this->gridWidth,
				rand() % this->gridHeight
			};
		}
	}

private Q_SLOTS:
	void updateGame(void)
	{
		// TODO
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
		setWindowTitle("Snake");

		this->timer = new QTimer(this);
		connect(this->timer, &QTimer::timeout, this, &SnakeMainWindow::updateGame);
	}
};

int main()
{
	int fakeArgc = 0;
	QApplication app(fakeArgc, nullptr);

	SnakeMainWindow window = SnakeMainWindow(16, 12, 50, 5);
	window.show();
	return app.exec();
}
