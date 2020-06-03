import math
import os

from PyQt5 import QtWidgets, uic, QtGui, QtCore
import pyqtgraph as pg
from functools import partial
import datetime
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel, QLineEdit, QDialogButtonBox

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
    model_num = 0
    variables_with_value["Channels1"] = []
    variables_with_value['k1'] = 0
    variables_with_value['date1'] = ""

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
        self.HideButton.clicked.connect(self.hideFunc)
        self.widget_cond = True
        self.opened_check = True
        self.model_name = ""
        self.model_1.triggered.connect(partial(self.model_button_clicked, 1))
        self.model_2.triggered.connect(partial(self.model_button_clicked, 2))
        self.model_3.triggered.connect(partial(self.model_button_clicked, 3))
        self.model_4.triggered.connect(partial(self.model_button_clicked, 4))
        self.model_5.triggered.connect(partial(self.model_button_clicked, 5))
        self.model_6.triggered.connect(partial(self.model_button_clicked, 6))
        self.model_7.triggered.connect(partial(self.model_button_clicked, 7))
        self.model_8.triggered.connect(partial(self.model_button_clicked, 8))
        self.model_9.triggered.connect(partial(self.model_button_clicked, 9))
        self.model_func_dictionary = {"1": self.model_func_1, "2": self.model_func_2, "3": self.model_func_3,
                                      "4": self.model_func_4, "5": self.model_func_5, "6": self.model_func_6,
                                      "7": self.model_func_7, "8": self.model_func_8, "9": self.model_func_9}
        self.model.buttons.button(QDialogButtonBox.Ok).clicked.connect(partial(self.model_func))
        self.fileSave.triggered.connect(partial(self.save_func))

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
        line_number_real = 0
        file_name = os.path.basename(file)
        for i in channels_list:
            self.variables_with_value[i] = []
        with open(file) as f:
            for line_number, line in enumerate(f):
                if line[0] == "#":
                    continue
                else:
                    if line_number <= 11:
                        self.variables_with_value[variables_list[line_number_real]] = line
                        line_number_real += 1
                    else:
                        values = [float(s) for s in line.split()]
                        for i in range(int(self.variables_with_value['k'])):
                            self.variables_with_value[channels_list[i]].append(values.pop(0))

        self.variables_with_value['Channels'] = self.variables_with_value['Channels'].rstrip()
        self.variables_with_value['Channels'] = self.variables_with_value['Channels'].split(';')
        self.variables_with_value["Channels1"] = self.variables_with_value["Channels"] + self.variables_with_value["Channels1"]
        self.variables_with_value['k'] = int(self.variables_with_value['k'])
        self.variables_with_value['k1'] += self.variables_with_value['k']
        self.variables_with_value['n'] = int(self.variables_with_value['n'])
        self.variables_with_value['gerc'] = float(self.variables_with_value['gerc'])
        self.variables_with_value['date1'] = self.variables_with_value['date'].rstrip()
        self.variables_with_value['date'] = self.variables_with_value['date'].rstrip() + ' ' + self.variables_with_value[
            'time'].rstrip() + '000'
        self.variables_with_value['date'] = datetime.datetime.strptime(self.variables_with_value['date'], '%d-%m-%Y %H:%M:%S.%f')
        self.create_channels_menu(self.variables_with_value, channels_list, file_name)

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
        # plots_dict = {}
        self.fill_info_window(data, x_coordinates[data['n'] - 1], file_name)
        names = ['button1', 'button2', 'button3']
        # plots_dict[data['Channels'][i]] = self.Channels.setBorder(width=3)
        for i in range(data['k']):
            self.plots_dict[data['Channels'][i]] = self.Channels.addPlot(x=x_coordinates, y=data['channel_' + str(i)],
                                                                    title=data['Channels'][i])
            self.plots_dict[data['Channels'][i]].setDownsampling(auto=True)
            self.plots_dict[data['Channels'][i]].showAxis('right')
            self.plots_dict[data['Channels'][i]].showAxis('top')

            self.plots_dict[data['Channels'][i]].getAxis('top').setStyle(showValues=False)
            self.plots_dict[data['Channels'][i]].getAxis('left').setStyle(showValues=False)
            self.plots_dict[data['Channels'][i]].getAxis('right').setStyle(showValues=False)
            self.plots_dict[data['Channels'][i]].getAxis('bottom').setStyle(showValues=False)

            self.Channels.nextRow()
            self.plots_dict[data['Channels'][i]].autoBtn.clicked.connect(
                partial(self.testFunc, x_coordinates, data['channel_' + str(i)], data['Channels'][i], ticks))
            self.plots_dict[data['Channels'][i]] = self.plots_dict[data['Channels'][i]].plot(clear=True, x=x_coordinates,
                                                                                    y=data['channel_' + str(i)])

            self.plots_dict[data['Channels'][i]].setPen(width=3)
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
        Plot.plot(clear=True, x=x, y=y, name=name).setPen(width=3)
        if not (ticks is None):
            xaxis = Plot.getAxis('bottom')
            majorTicks = list(ticks.items())[::300]
            minorTicks = list(ticks.items())
            del minorTicks[::300]
            xaxis.setTicks([majorTicks, minorTicks])
        # self.MainGraph.setDownsampling(auto=True)
        print('testing func')

    def hideFunc(self):
        if self.widget_cond:
            self.Channels.hide()
            print('funccheckc')
            self.widget_cond = False
        else:
            self.Channels.show()
            print('sucess')
            self.widget_cond = True

    def startSliderFunc(self, value):
        print(value)
        return 321

    def model_button_clicked(self, model_num):
        self.model_num = model_num
        self.model_name = self.sender().text()
        self.model.text_hint.setText("<center>" + self.sender().text() + "</center><br>Введите данные:")
        for i in reversed(range(self.model.form.count())):
            self.model.form.removeRow(i)
        if self.opened_check:
            self.model.form.addRow(QLabel("Частота дискретизации:"), QLineEdit())
            self.model.form.addRow(QLabel("Кол-во отсчетов:"), QLineEdit())
            self.opened_check = False
        if model_num == 1 or model_num == 2:
            self.model.form.addRow(QLabel("Задержка:"), QLineEdit())
        if model_num == 3:
            self.model.form.addRow(QLabel("A(0,1):"), QLineEdit())
        if model_num == 4:
            self.model.form.addRow(QLabel("Амплитуда:"), QLineEdit())
            self.model.form.addRow(QLabel("Круговая частота[0,\u03C0]:"), QLineEdit())
            self.model.form.addRow(QLabel("Начальная фаза[0,2\u03C0]:"), QLineEdit())
        if model_num == 5 or model_num == 6:
            self.model.form.addRow(QLabel("Период"), QLineEdit())
        if model_num == 7:
            self.model.form.addRow(QLabel("Амплитуда сигнала:"), QLineEdit())
            self.model.form.addRow(QLabel("Параметр ширины огибающей:"), QLineEdit())
            if "gerc" in self.variables_with_value:
                self.model.form.addRow(QLabel("Частота несущей[0," + str(0.5 * self.variables_with_value["gerc"]) + "]:"),
                                       QLineEdit())
            else:
                self.model.form.addRow(QLabel("Частота несущей[0," + "0.5*част.дискрет." + "]:"),
                                       QLineEdit())
            self.model.form.addRow(QLabel("Начальная фаза несущей:"), QLineEdit())
        if model_num == 8:
            self.model.form.addRow(QLabel("Амплитуда сигнала:"), QLineEdit())
            self.model.form.addRow(QLabel("Частота огибающей:"), QLineEdit())
            if "gerc" in self.variables_with_value:
                self.model.form.addRow(QLabel("Частота несущей[0," + str(0.5 * self.variables_with_value["gerc"]) + "]:"),
                                       QLineEdit())
            else:
                self.model.form.addRow(QLabel("Частота несущей[0," + "0.5*част.дискрет." + "]:"),
                                       QLineEdit())
            self.model.form.addRow(QLabel("Начальная фаза несущей:"), QLineEdit())
        if model_num == 9:
            self.model.form.addRow(QLabel("Амплитуда сигнала:"), QLineEdit())
            self.model.form.addRow(QLabel("Частота огибающей:"), QLineEdit())
            if "gerc" in self.variables_with_value:
                self.model.form.addRow(QLabel("Частота несущей[0," + str(0.5 * self.variables_with_value["gerc"]) + "]:"),
                                       QLineEdit())
            else:
                self.model.form.addRow(QLabel("Частота несущей[0," + "0.5*част.дискрет." + "]:"),
                                       QLineEdit())
            self.model.form.addRow(QLabel("Начальная фаза несущей:"), QLineEdit())
            self.model.form.addRow(QLabel("Индекс глубины модуляции[0,1]:"), QLineEdit())
        self.model.show()

    def model_func(self):
        test = str(self.model_num)
        self.model_func_dictionary[str(self.model_num)]()

    def model_func_1(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        n0 = int(self.model.form.itemAt(0, 1).widget().text())
        for i in range(n):
            x_value = x_value + i / gercs
            x_coordinates.append(i)
            if i == n0:
                y_coordinates.append(1)
            else:
                y_coordinates.append(0)
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_2(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        n0 = int(self.model.form.itemAt(0, 1).widget().text())
        for i in range(n):
            x_value = x_value + i / gercs
            x_coordinates.append(i)
            if i >= n0:
                y_coordinates.append(1)
            else:
                y_coordinates.append(0)
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_3(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = float(self.model.form.itemAt(0, 1).widget().text())
        for i in range(n):
            x_value = x_value + i / gercs
            x_coordinates.append(i)
            y_coordinates.append(pow(a, i))
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_4(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = int(self.model.form.itemAt(0, 1).widget().text())
        b = float(self.model.form.itemAt(1, 1).widget().text())
        c = float(self.model.form.itemAt(2, 1).widget().text())
        for i in range(n):
            x_value = x_value + i / gercs
            x_coordinates.append(i)
            y_coordinates.append(a * math.sin(i * b + c))
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_5(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = float(self.model.form.itemAt(0, 1).widget().text())
        for i in range(n):
            x_value = x_value + i / gercs
            x_coordinates.append(i)
            if (i % a) >= (a / 2):
                y_coordinates.append(-1)
            else:
                y_coordinates.append(1)
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_6(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = int(self.model.form.itemAt(0, 1).widget().text())
        for i in range(n):
            x_value = x_value + i / gercs
            x_coordinates.append(i)
            y_coordinates.append((i % a)/a)
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_7(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = float(self.model.form.itemAt(0, 1).widget().text())
        b = float(self.model.form.itemAt(1, 1).widget().text())
        c = float(self.model.form.itemAt(2, 1).widget().text())
        d = float(self.model.form.itemAt(3, 1).widget().text())
        for i in range(n):
            t = i / gercs
            x_value = x_value + t
            x_coordinates.append(t)
            y_coordinates.append(a*math.exp(-t/b)*math.cos(2*math.pi*c*t+d))
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_8(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = float(self.model.form.itemAt(0, 1).widget().text())
        b = float(self.model.form.itemAt(1, 1).widget().text())
        c = float(self.model.form.itemAt(2, 1).widget().text())
        d = float(self.model.form.itemAt(3, 1).widget().text())
        for i in range(n):
            t = i / gercs
            x_value = x_value + t
            x_coordinates.append(t)
            y_coordinates.append(a*math.cos(2*math.pi*b*t)*math.cos(2*math.pi*c*t+d))
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_9(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = float(self.model.form.itemAt(0, 1).widget().text())
        b = float(self.model.form.itemAt(1, 1).widget().text())
        c = float(self.model.form.itemAt(2, 1).widget().text())
        d = float(self.model.form.itemAt(3, 1).widget().text())
        e = float(self.model.form.itemAt(4, 1).widget().text())
        for i in range(n):
            t = i / gercs
            x_value = x_value + t
            x_coordinates.append(t)
            y_coordinates.append(a*(1+e*math.cos(2*math.pi*b*t))*math.cos(2*math.pi*c*t+d))
        self.draw_model(x_coordinates, y_coordinates, None)

    def read_gerc_and_n(self):
        if "gerc" in self.variables_with_value:
            gercs = self.variables_with_value["gerc"]
            n = self.variables_with_value["n"]
        else:
            gercs = float(self.model.form.itemAt(0, 1).widget().text())
            n = int(self.model.form.itemAt(1, 1).widget().text())
            self.variables_with_value["gerc"] = gercs
            self.variables_with_value["n"] = n
            self.model.form.removeRow(0)
            self.model.form.removeRow(0)
        return gercs, n

    def draw_model(self, x, y, ticks):
        self.variables_with_value["k1"] += 1
        self.variables_with_value['Channels1'].append(self.model_name)
        plot = self.Channels.addPlot(x=x, y=y, title=self.model_name)
        plot.setDownsampling(auto=True)
        plot.showAxis("right")
        plot.showAxis("bottom")
        plot.getAxis('top').setStyle(showValues=False)
        plot.getAxis('bottom').setStyle(showValues=False)
        plot.getAxis('left').setStyle(showValues=False)
        plot.getAxis('right').setStyle(showValues=False)
        self.plots_dict[self.model_name] = plot.plot(clear=True, x=x, y=y, title=self.model_name)
        self.Channels.nextRow()
        plot.autoBtn.clicked.connect(
            partial(self.testFunc, x, y, self.model_name, ticks))

    def save_func(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name[0], 'w')
        text = self.generate_file()
        file.write(text)
        file.close()

    def generate_file(self):
        k = str(self.variables_with_value["k1"])
        n = str(self.variables_with_value["n"])
        gerc = str(self.variables_with_value["gerc"])
        if "date" in self.variables_with_value:
            date = self.variables_with_value["date1"]
            time = self.variables_with_value["time"].rstrip()
        else:
            date = "01-01-2000"
            time = "00:00:00.000"
        channels = ';'.join(self.variables_with_value["Channels1"])
        # channels.rstrip()
        text = "# channels number\n" \
               + k + \
               "\n# samples number\n" + n + "\n# sampling rate\n" + gerc + "\n# start date\n" + date + "\n# start " \
                                                                                                       "time\n" + \
               time + "\n# channels names\n" + channels + "\n"
        for i in range(int(n)):
            for j in range(int(k)):
                text += str(self.plots_dict[self.variables_with_value["Channels1"][j]].yData[i]) + " "
            text += "\n"
        return text

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
