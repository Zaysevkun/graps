from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('design.ui', self)
        self.FileOpen.triggered.connect(self.browse_folder)
    def browse_folder(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        f = open(file)
        k = f.readline()
        n = f.readline()
        gerc = f.readline()
        date = f.readline()
        time = f.readline()
        




def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()