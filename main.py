from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('design.ui', self)
        self.FileOpen.triggered.connect(self.browse_folder)

    def browse_folder(self):
        path = QtWidgets.QFileDialog.getOpenFileName()
        file = path[0]
        channels_list = ["channel_0", "channel_1", "channel_2", "channel_3", "channel_4", "channel_5", "channel_6"]
        variables_list = ["k", "n", "gerc", "date", "time", "Channels"]
        variables_with_value = {}
        for i in channels_list:
            variables_with_value[i] = []
        with open(file) as f:
            for line_number, line in enumerate(f):
                if line_number <= 5:
                    variables_with_value[variables_list[line_number]] = line
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
        plots_dict = {}
        for i in range(data['k']):
            plots_dict[data['Channels'][i]] = self.Channels.addPlot(y=data['channel_'+str(i)], name=data['Channels'][i], title=data['Channels'][i])
            plots_dict[data['Channels'][i]] = plots_dict[data['Channels'][i]].plot(clear=True, y=data['channel_'+str(i)], name=data['Channels'][i])
            plots_dict[data['Channels'][i]].setPen(color='r')
            #plots_dict[data['Channels'][i]].sigClicked.connect(self.unwrap_channel(data, i))

    def unwrap_channel(self, data, i):
        print(123)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
