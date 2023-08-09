import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from opengl_widget import OpenGLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("3D Editor")

        self.opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
