from PyQt5 import QtWidgets, uic, QtGui
import pyqtgraph as pg
from functools import partial
import sys


class MainWindow(QtWidgets.QMainWindow):
    variables_with_value = {}
    plots_dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design.ui', self)
        self.Channels.setBackground(background=None)
        self.MainGraph.setBackground(background=None)
        self.FileOpen.triggered.connect(self.browse_folder)

    def browse_folder(self):
        path = QtWidgets.QFileDialog.getOpenFileName()
        file = path[0]
        channels_list = ["channel_0", "channel_1", "channel_2", "channel_3", "channel_4", "channel_5", "channel_6"]
        variables_list = ["k", "n", "gerc", "date", "time", "Channels"]
        variables_with_value = {}
        line_number_real = 0
        for i in channels_list:
            variables_with_value[i] = []
        with open(file) as f:
            for line_number, line in enumerate(f):
                if line[0] == "#":
                    continue
                else:
                    if line_number <= 11:
                        variables_with_value[variables_list[line_number_real]] = line
                        line_number_real += 1
                    else:
                        values = [float(s) for s in line.split()]
                        for i in range(int(variables_with_value['k'])):
                            variables_with_value[channels_list[i]].append(values.pop(0))

        variables_with_value['Channels'] = variables_with_value['Channels'].split(';')
        variables_with_value['k'] = int(variables_with_value['k'])
        variables_with_value['n'] = int(variables_with_value['n'])
        variables_with_value['gerc'] = float(variables_with_value['gerc'])
        self.create_channels_menu(variables_with_value, channels_list)
        print(variables_with_value)

    def create_channels_menu(self, data, names):
        x_coordinates = []
        helping_hand = [0,1,2,3,4]
        plots_dict = {}
        names = ['button1', 'button2', 'button3']
        for i in range(data['k']):
            plots_dict[data['Channels'][i]] = self.Channels.addPlot(y=data['channel_' + str(i)],
                                                                    name=data['Channels'][i], title=data['Channels'][i])
            plots_dict[data['Channels'][i]].autoBtn.clicked.connect(
                partial(self.testFunc,data['channel_' + str(i)], data['Channels'][i]))
            plots_dict[data['Channels'][i]] = plots_dict[data['Channels'][i]].plot(clear=True,
                                                                                   y=data['channel_' + str(i)],
                                                                                   name=data['Channels'][i])

            plots_dict[data['Channels'][i]].setPen(width=4.5)
            plots_dict[data['Channels'][i]].sigClicked.connect(self.unwrap_channel)
        return 123

    def testFunc(self, data, name):
        self.MainGraph.plot(clear=True, y=data, name=name).setPen(width=4.5)
        print('testing func')

    def unwrap_channel(self):
        print(123)
        # i.setPen(color='r')


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
