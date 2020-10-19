import sys

from PyQt5 import QtWidgets

from src.widget.birdview import BirdView

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = BirdView()
    win.show()
    sys.exit(app.exec_())