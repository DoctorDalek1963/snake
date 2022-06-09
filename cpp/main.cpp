#include <algorithm>
#include <cstdlib>
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

	int getScore(void)
	{
		return std::max(0, int(snakeParts.size() - 1));
	}

	void resetGame(void)
	{
		gameOver = false;
		snakeParts.clear();

		posPlayer = {
			rand() % this->gridWidth,
			rand() % this->gridHeight
		};
		dirPlayer = std::nullopt;
		placeApple();

		timerStarted = false;
		timer->stop();
	}

	void paintEvent(QPaintEvent *)
	{
		QPainter painter(this);
		painter.setRenderHint(QPainter::Antialiasing);
		painter.setBrush(Qt::NoBrush);

		if (gameOver) {
			QFont font = painter.font();
			font.setPixelSize(48);
			font.setBold(true);
			painter.setFont(font);

			painter.drawText(
				QRect(0, 0, width(), height()),
				Qt::AlignCenter | Qt::AlignVCenter,
				QString(("GAME OVER\n\nScore: " + std::to_string(getScore())).c_str())
			);
			return;
		}

		// Draw tail
		painter.setPen(QPen(colourTail));
		for (Point part : snakeParts)
			painter.fillRect(
				int(gridCellSize * (part.x + 0.1)),
				int(gridCellSize * (part.y + 0.1)),
				int(0.8 * gridCellSize),
				int(0.8 * gridCellSize),
				colourTail
			);

		// Draw apple
		painter.setPen(QPen(colourApple));
		painter.fillRect(
			int(gridCellSize * (posApple.x + 0.15)),
			int(gridCellSize * (posApple.y + 0.15)),
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

		painter.setPen(QPen(QColor(0, 0, 0)));

		QFont font = painter.font();
		font.setPixelSize(24);
		painter.setFont(font);

		painter.drawText(
			QRect(10, 10, 100, 30),
			Qt::AlignLeft | Qt::AlignTop,
			QString(("Score: " + std::to_string(getScore())).c_str())
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

		} else if (event->matches(QKeySequence::Refresh)) {
			resetGame();
			update();
			return;

		} else if (key == Qt::Key_Plus) {
			fps++;
			timer->setInterval(int(1000 / fps));

		} else if (key == Qt::Key_Minus) {
			std::max(1, fps - 1);
			timer->setInterval(int(1000 / fps));

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
		for (int i = 0; i < int(snakeParts.size() - 1); i++)
		{
			Point part = snakeParts[i];
			if (part.x == posPlayer.x && part.y == posPlayer.y) {
				gameOver = true;
				timer->stop();
				update();
				return;
			}
		}

		if (posPlayer.x == posApple.x && posPlayer.y == posApple.y) {
			snakeParts.push_back(posPlayer);
			placeApple();
		}

		if (dirPlayer == UP) {
			posPlayer = { posPlayer.x, (posPlayer.y - 1 + gridHeight) % gridHeight };

		} else if (dirPlayer == DOWN) {
			posPlayer = { posPlayer.x, (posPlayer.y + 1 + gridHeight) % gridHeight };

		} else if (dirPlayer == LEFT) {
			posPlayer = { (posPlayer.x - 1 + gridWidth) % gridWidth, posPlayer.y };

		} else if (dirPlayer == RIGHT) {
			posPlayer = { (posPlayer.x + 1 + gridWidth) % gridWidth, posPlayer.y };
		}

		if (snakeParts.size() != 0)
			snakeParts.erase(snakeParts.begin());

		snakeParts.push_back(posPlayer);

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

// Class taken from https://stackoverflow.com/a/868894/12985838
class InputParser
{
	public:
		InputParser (int &argc, char **argv)
		{
			for (int i = 1; i < argc; ++i)
				this->tokens.push_back(std::string(argv[i]));
		}

		const std::string& getCmdOption(const std::string &option) const
		{
			std::vector<std::string>::const_iterator itr;
			itr = std::find(this->tokens.begin(), this->tokens.end(), option);

			if (itr != this->tokens.end() && ++itr != this->tokens.end())
				return *itr;

			static const std::string empty_string("");
			return empty_string;
		}

		bool cmdOptionExists(const std::string &option) const
		{
			return std::find(this->tokens.begin(), this->tokens.end(), option) != this->tokens.end();
		}

	private:
		std::vector <std::string> tokens;
};

// Function taken from https://stackoverflow.com/a/2845275/12985838
inline bool isInteger(const std::string & s)
{
	if (s.empty() || ((!isdigit(s[0])) && (s[0] != '-') && (s[0] != '+')))
		return false;

	char * p;
	strtol(s.c_str(), &p, 10);

	return (*p == 0);
}

int main(int argc, char **argv)
{
	srand(time(NULL));

	int fakeArgc = 0;
	QApplication app(fakeArgc, nullptr);

	InputParser input(argc, argv);
	const std::string &strWidth = input.getCmdOption("-w");
	const std::string &strHeight = input.getCmdOption("-H");
	const std::string &strCellsize = input.getCmdOption("-s");
	const std::string &strFps = input.getCmdOption("-f");

	int width, height, cellsize, fps;

	if (!strWidth.empty() && isInteger(strWidth))
		width = atoi(strWidth.c_str());
	else
		width = 16;

	if (!strHeight.empty() && isInteger(strHeight))
		height = atoi(strHeight.c_str());
	else
		height = 12;

	if (!strCellsize.empty() && isInteger(strCellsize))
		cellsize = atoi(strCellsize.c_str());
	else
		cellsize = 50;

	if (!strFps.empty() && isInteger(strFps))
		fps = atoi(strFps.c_str());
	else
		fps = 5;

	SnakeMainWindow window = SnakeMainWindow(width, height, cellsize, fps);
	window.show();
	return app.exec();
}
