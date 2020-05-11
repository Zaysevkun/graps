from PyQt5 import QtWidgets, uic, QtGui
import pyqtgraph as pg
from functools import partial
import datetime
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
        variables_with_value['date'] = variables_with_value['date'].rstrip() + ' ' + variables_with_value['time'].rstrip() + '000'
        variables_with_value['date'] = datetime.datetime.strptime(variables_with_value['date'], '%d-%m-%Y %H:%M:%S.%f')
        self.create_channels_menu(variables_with_value, channels_list)
        print(variables_with_value)

    def create_channels_menu(self, data, names):
        x_coordinates = []
        x_labels = []
        intial_date = data['date'].timestamp()
        change_value = 1/data['gerc']
        for i in range(data['n']):
            x_value = intial_date + (change_value * i)
            x_coordinates.append(x_value)
            x_value = datetime.datetime.fromtimestamp(x_value)
            x_value = x_value.isoformat(sep='T')
            x_labels.append(x_value)
        ticks = [list(zip(x_coordinates, x_labels))]
        plots_dict = {}
        names = ['button1', 'button2', 'button3']
        for i in range(data['k']):
            plots_dict[data['Channels'][i]] = self.Channels.addPlot(x=x_coordinates, y=data['channel_' + str(i)],
                                                                    name=data['Channels'][i], title=data['Channels'][i])
            plots_dict[data['Channels'][i]].setDownsampling(auto=True)
            plots_dict[data['Channels'][i]].showAxis('right')
            plots_dict[data['Channels'][i]].showAxis('top')

            plots_dict[data['Channels'][i]].getAxis('top').setStyle(showValues=False)
            plots_dict[data['Channels'][i]].getAxis('left').setStyle(showValues=False)
            plots_dict[data['Channels'][i]].getAxis('right').setStyle(showValues=False)
            plots_dict[data['Channels'][i]].getAxis('bottom').setStyle(showValues=False)

            self.Channels.nextRow()
            plots_dict[data['Channels'][i]].autoBtn.clicked.connect(
                partial(self.testFunc, x_coordinates, data['channel_' + str(i)], data['Channels'][i], ticks))
            plots_dict[data['Channels'][i]] = plots_dict[data['Channels'][i]].plot(clear=True, x=x_coordinates,
                                                                                   y=data['channel_' + str(i)],
                                                                                   name=data['Channels'][i])

            plots_dict[data['Channels'][i]].setPen(width=4.5)
            plots_dict[data['Channels'][i]].sigClicked.connect(self.unwrap_channel)
        return 123

    def testFunc(self, x, y, name, ticks):
        xaxis = self.MainGraph.getAxis('bottom')
        self.MainGraph.plot(clear=True, x=x, y=y, name=name).setPen(width=4.5)
        self.MainGraph.setDownsampling(auto=True)
        xaxis.setTicks(ticks)
        xaxis.setStyle(textFillLimits=[(0, 0.8)])
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
