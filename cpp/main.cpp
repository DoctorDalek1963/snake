#include <QApplication>
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

private Q_SLOTS:
	void updateGame(void)
	{
		if (dirPlayer == UP) {
			posPlayer = { posPlayer.x, (posPlayer.y - 1) % gridHeight };
		} else if (dirPlayer == DOWN) {
			posPlayer = { posPlayer.x, (posPlayer.y + 1) % gridHeight };
		} else if (dirPlayer == LEFT) {
			posPlayer = { (posPlayer.x - 1) % gridWidth, posPlayer.y };
		} else if (dirPlayer == RIGHT) {
			posPlayer = { (posPlayer.x + 1) % gridWidth, posPlayer.y };
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
