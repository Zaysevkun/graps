from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('design.ui', self)
        self.FileOpen.triggered.connect(self.browse_folder)
    def browse_folder(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        variables_list = ["k", "n", "gerc", "date", "time"]
        variables_with_value = {}
        with open(file) as f:
            for line_number, line in enumerate(f):
                variables_with_value[variables_list[line_number]] = line


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
