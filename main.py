import os

from PyQt5 import QtWidgets, uic, QtGui, QtCore
import pyqtgraph as pg
from functools import partial
import datetime
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel, QLineEdit

MAXVAL = 650000


class RangeSliderClass(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.minTime = 0
        self.maxTime = 0
        self.minRangeTime = 0
        self.maxRangeTime = 0

        self.sliderMin = MAXVAL
        self.sliderMax = MAXVAL

        self.setupUi(self)

    def setupUi(self, RangeSlider):
        RangeSlider.setObjectName("RangeSlider")
        RangeSlider.resize(1000, 65)
        RangeSlider.setMaximumSize(QtCore.QSize(16777215, 65))
        self.RangeBarVLayout = QtWidgets.QVBoxLayout(RangeSlider)
        self.RangeBarVLayout.setContentsMargins(5, 0, 5, 0)
        self.RangeBarVLayout.setSpacing(0)
        self.RangeBarVLayout.setObjectName("RangeBarVLayout")

        self.slidersFrame = QtWidgets.QFrame(RangeSlider)
        self.slidersFrame.setMaximumSize(QtCore.QSize(16777215, 25))
        self.slidersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.slidersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slidersFrame.setObjectName("slidersFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.slidersFrame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        ## Start Slider Widget
        self.startSlider = QtWidgets.QSlider(self.slidersFrame)
        self.startSlider.setMaximum(self.sliderMin)
        self.startSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.startSlider.setMaximumSize(QtCore.QSize(16777215, 10))

        font = QtGui.QFont()
        font.setKerning(True)

        self.startSlider.setFont(font)
        self.startSlider.setAcceptDrops(False)
        self.startSlider.setAutoFillBackground(False)
        self.startSlider.setOrientation(QtCore.Qt.Horizontal)
        self.startSlider.setInvertedAppearance(True)
        self.startSlider.setObjectName("startSlider")
        self.startSlider.setValue(MAXVAL)
        self.startSlider.valueChanged.connect(self.handleStartSliderValueChange)
        self.horizontalLayout.addWidget(self.startSlider)

        ## End Slider Widget
        self.endSlider = QtWidgets.QSlider(self.slidersFrame)
        self.endSlider.setMaximum(MAXVAL)
        self.endSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.endSlider.setMaximumSize(QtCore.QSize(16777215, 10))
        self.endSlider.setTracking(True)
        self.endSlider.setOrientation(QtCore.Qt.Horizontal)
        self.endSlider.setObjectName("endSlider")
        self.endSlider.setValue(self.sliderMax)
        self.endSlider.valueChanged.connect(self.handleEndSliderValueChange)

        # self.endSlider.sliderReleased.connect(self.handleEndSliderValueChange)

        self.horizontalLayout.addWidget(self.endSlider)

        self.RangeBarVLayout.addWidget(self.slidersFrame)

        # self.retranslateUi(RangeSlider)
        QtCore.QMetaObject.connectSlotsByName(RangeSlider)

        self.show()

    @QtCore.pyqtSlot(int)
    def handleStartSliderValueChange(self, value):
        self.startSlider.setValue(value)

    @QtCore.pyqtSlot(int)
    def handleEndSliderValueChange(self, value):
        self.endSlider.setValue(value)


class InfoWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design_window2.ui', self)


class ModelWindow(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design_model_window.ui', self)


class MainWindow(QtWidgets.QMainWindow):
    variables_with_value = {}
    plots_dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design.ui', self)
        self.dialog = InfoWindow(self)
        self.model = ModelWindow(self)
        self.Channels.setBackground(background=None)
        self.MainGraph.setBackground(background=None)
        self.FileOpen.triggered.connect(self.browse_folder)
        self.SignalInfo.triggered.connect(self.open_info)
        self.widget_cond = True
        self.opened_check = True
        self.model_1.triggered.connect(partial(self.model_button_clicked, "1"))
        self.model_2.triggered.connect(partial(self.model_button_clicked, "2"))
        self.model_3.triggered.connect(partial(self.model_button_clicked, "3"))
        self.model_4.triggered.connect(partial(self.model_button_clicked, "4"))
        self.model_5.triggered.connect(partial(self.model_button_clicked, "5"))
        self.model_6.triggered.connect(partial(self.model_button_clicked, "6"))
        self.model_7.triggered.connect(partial(self.model_button_clicked, "7"))
        self.model_8.triggered.connect(partial(self.model_button_clicked, "8"))
        self.model_9.triggered.connect(partial(self.model_button_clicked, "9"))

    def open_info(self):

        self.dialog.show()

    def fill_info_window(self, data, last_date_dt, file_name):
        list_text = ''
        start_date = data['date'].isoformat(sep=' ')
        last_date_dt = datetime.datetime.fromtimestamp(last_date_dt)
        last_date = last_date_dt.isoformat(sep=' ')
        day = last_date_dt.toordinal() - data['date'].toordinal()
        hour = last_date_dt.hour - data['date'].hour
        minute = last_date_dt.minute - data['date'].minute
        second = last_date_dt.second - data['date'].second
        self.dialog.text_info.setText("<b>Текущее состояние многоканального сигнала</b><br>"
                                      "Общее число каналов " + str(data['k']) +
                                      "<br>Общее количество отсчетов " + str(data['n']) +
                                      "<br>Частота дискретизации " + str(data['gerc']) + "(шаг между отсчетами " + str(
            1 / data['gerc']) + " сек)"
                                "<br>Дата и время начала записи - " + start_date +
                                      "<br>Дата и время окончания записи - " + last_date +
                                      "<br>Длительность: " + str(day) + " - суток, " + str(hour) + " - часов, " + str(
            minute) + " - минут, " + str(second) + " - секунд" +
                                      "<br><br><br><br><b>Информация о каналах</b>")
        self.dialog.text_info.setFont(QFont('Times', 11))
        for i in range(data['k']):
            list_text += data['Channels'][i].rstrip() + "                  Файл: " + file_name + "\n"
        self.dialog.list_info.setText(list_text)
        self.dialog.list_info.setFont(QFont('Times', 11))
        self.dialog.list_info.setAlignment(Qt.AlignLeft)
        self.dialog.list_info.setStyleSheet("background-color: white; border: 1px inset grey; min-height: 200px;")

    def browse_folder(self):
        self.opened_check = False
        path = QtWidgets.QFileDialog.getOpenFileName()
        file = path[0]
        channels_list = ["channel_0", "channel_1", "channel_2", "channel_3", "channel_4", "channel_5", "channel_6"]
        variables_list = ["k", "n", "gerc", "date", "time", "Channels"]
        variables_with_value = {}
        line_number_real = 0
        file_name = os.path.basename(file)
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
        variables_with_value['date'] = variables_with_value['date'].rstrip() + ' ' + variables_with_value[
            'time'].rstrip() + '000'
        variables_with_value['date'] = datetime.datetime.strptime(variables_with_value['date'], '%d-%m-%Y %H:%M:%S.%f')
        self.create_channels_menu(variables_with_value, channels_list, file_name)
        print(variables_with_value)

    def create_channels_menu(self, data, names, file_name):
        x_coordinates = []
        x_labels = []
        intial_date = data['date'].timestamp()
        change_value = 1 / data['gerc']
        for i in range(data['n']):
            x_value = intial_date + (change_value * i)
            x_coordinates.append(x_value)
            x_value = datetime.datetime.fromtimestamp(x_value)
            x_value = x_value.isoformat(sep=' ')
            x_labels.append(x_value)
        ticks = dict(zip(x_coordinates, x_labels))
        plots_dict = {}
        self.fill_info_window(data, x_coordinates[data['n'] - 1], file_name)
        names = ['button1', 'button2', 'button3']
        # plots_dict[data['Channels'][i]] = self.Channels.setBorder(width=3)
        for i in range(data['k']):
            plots_dict[data['Channels'][i]] = self.Channels.addPlot(x=x_coordinates, y=data['channel_' + str(i)],
                                                                    title=data['Channels'][i])
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
                                                                                   y=data['channel_' + str(i)])

            plots_dict[data['Channels'][i]].setPen(width=3)
        self.HideButton.clicked.connect(self.hideFunc)
        return 123

    def testFunc(self, x, y, name, ticks):
        Plot = self.MainGraph.addPlot(clear=True, x=x, y=y, name=name, title=name)
        self.MainGraph.nextRow()
        slider = RangeSliderClass()
        slider.minTime = x[0]
        slider.maxTime = x[len(x) - 1]
        # slider.handleStartSliderValueChange(self, )
        slider.startSlider.valueChanged.connect(partial(self.startSliderFunc, slider.startSlider.value()))
        proxy = QtGui.QGraphicsProxyWidget()
        proxy.setWidget(slider)
        self.MainGraph.addItem(proxy)
        self.MainGraph.nextRow()
        xaxis = Plot.getAxis('bottom')
        Plot = Plot.plot(clear=True, x=x, y=y, name=name).setPen(width=3)
        majorTicks = list(ticks.items())[::300]
        minorTicks = list(ticks.items())
        del minorTicks[::300]
        xaxis.setTicks([majorTicks, minorTicks])
        # self.MainGraph.setDownsampling(auto=True)
        print('testing func')

    def hideFunc(self):
        if self.widget_cond:
            self.Channels.hide()
            self.widget_cond = False
        else:
            self.Channels.show()
            print('sucess')
            self.widget_cond = True

    def startSliderFunc(self, value):
        print(value)
        return 321

    def model_button_clicked(self, model_num):
        self.model.text_hint.setText("<center>" + self.sender().text() + "</center><br>Введите данные:")
        for i in reversed(range(self.model.form.count())):
            self.model.form.removeRow(i)
        if self.opened_check:
            self.model.form.addRow(QLabel("Частота дискретизации:"), QLineEdit())
            self.model.form.addRow(QLabel("Кол-во отсчетов:"), QLineEdit())
        self.model.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
