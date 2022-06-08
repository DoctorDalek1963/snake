#include <QApplication>
#include <QMainWindow>

int main(int argc, char *argv[]) {
	QApplication app(argc, argv);

	QMainWindow window;

	window.setMinimumSize(250, 150);
	window.setWindowTitle("Simple example");
	window.show();

	return app.exec();
}
