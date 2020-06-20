import math
import os

import numpy
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import pyqtgraph as pg
from functools import partial
import datetime
import sys
import random
from decimal import Decimal

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel, QLineEdit, QDialogButtonBox, QCheckBox, QComboBox

MAXVAL = 650000


class SpecWindow(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design/design_spec.ui', self)


class InfoWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design/design_info.ui', self)


class ModelWindow(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design/design_model_window.ui', self)


class StatWindow(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design/design_stat.ui', self)
        self.hystogram.setBackground(background=None)
        self.hystogram.showAxis("left", show=False)
        self.hystogram.showAxis("bottom", show=False)


class MainWindow(QtWidgets.QMainWindow):
    variables_with_value = {}
    plots_dict = {}
    model_num = 0
    variables_with_value["Channels1"] = []
    variables_with_value['k1'] = 0
    variables_with_value['date1'] = ""
    spec_dict_a = []
    spec_dict_p = []
    spec_plot = []
    spec_plot_lg = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        # pg.setConfigOption('background', 'w')
        uic.loadUi('design/design.ui', self)
        self.dialog = InfoWindow(self)
        self.model = ModelWindow(self)
        self.stat = StatWindow(self)
        self.spec = SpecWindow(self)
        self.Channels.setBackground(background=None)
        self.MainGraph.setBackground(background=None)
        self.FileOpen.triggered.connect(self.browse_folder)
        self.SignalInfo.triggered.connect(self.open_info)
        self.HideButton.clicked.connect(self.hideFunc)
        self.widget_cond = True
        self.opened_check = True
        self.model_name = ""
        self.spec.grid.itemAt(2).widget().clicked.connect(partial(self.do_it_func))
        self.model_1.triggered.connect(partial(self.model_button_clicked, 1))
        self.model_2.triggered.connect(partial(self.model_button_clicked, 2))
        self.model_3.triggered.connect(partial(self.model_button_clicked, 3))
        self.model_4.triggered.connect(partial(self.model_button_clicked, 4))
        self.model_5.triggered.connect(partial(self.model_button_clicked, 5))
        self.model_6.triggered.connect(partial(self.model_button_clicked, 6))
        self.model_7.triggered.connect(partial(self.model_button_clicked, 7))
        self.model_8.triggered.connect(partial(self.model_button_clicked, 8))
        self.model_9.triggered.connect(partial(self.model_button_clicked, 9))
        self.model_10.triggered.connect(partial(self.model_button_clicked, 10))
        self.model_11.triggered.connect(partial(self.model_button_clicked, 11))
        self.model_12.triggered.connect(partial(self.model_button_clicked, 12))
        self.superpos.triggered.connect(partial(self.model_button_clicked, 13))
        self.stats.triggered.connect(partial(self.model_button_clicked, 14))
        self.spectr.triggered.connect(partial(self.spec_func))
        self.spec.type.currentIndexChanged.connect(partial(self.change_type_func))
        self.spec.mode.currentIndexChanged.connect(partial(self.change_mode_func))
        self.model_func_dictionary = {"1": self.model_func_1, "2": self.model_func_2, "3": self.model_func_3,
                                      "4": self.model_func_4, "5": self.model_func_5, "6": self.model_func_6,
                                      "7": self.model_func_7, "8": self.model_func_8, "9": self.model_func_9,
                                      "10": self.model_func_10, "11": self.model_func_11, "12": self.model_func_12,
                                      "13": self.superpos_func, "14": self.stat_func}
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
        self.variables_with_value["Channels1"] = self.variables_with_value["Channels"] + self.variables_with_value[
            "Channels1"]
        self.variables_with_value['k'] = int(self.variables_with_value['k'])
        self.variables_with_value['k1'] += self.variables_with_value['k']
        self.variables_with_value['n'] = int(self.variables_with_value['n'])
        self.variables_with_value['gerc'] = float(self.variables_with_value['gerc'])
        self.variables_with_value['date1'] = self.variables_with_value['date'].rstrip()
        self.variables_with_value['date'] = self.variables_with_value['date'].rstrip() + ' ' + \
                                            self.variables_with_value[
                                                'time'].rstrip() + '000'
        self.variables_with_value['date'] = datetime.datetime.strptime(self.variables_with_value['date'],
                                                                       '%d-%m-%Y %H:%M:%S.%f')
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
            # self.plots_dict[data["Channels"][i]].setMouseEnabled(x=False, y=False)
            self.plots_dict[data['Channels'][i]].getAxis('top').setStyle(showValues=False)
            self.plots_dict[data['Channels'][i]].getAxis('left').setStyle(showValues=False)
            self.plots_dict[data['Channels'][i]].getAxis('right').setStyle(showValues=False)
            self.plots_dict[data['Channels'][i]].getAxis('bottom').setStyle(showValues=False)

            self.Channels.nextRow()
            self.plots_dict[data['Channels'][i]].autoBtn.clicked.connect(
                partial(self.unwrap_graph, x_coordinates, data['channel_' + str(i)], data['Channels'][i], ticks))
            self.plots_dict[data['Channels'][i]] = self.plots_dict[data['Channels'][i]].plot(clear=True,
                                                                                             x=x_coordinates,
                                                                                             y=data[
                                                                                                 'channel_' + str(i)])

            self.plots_dict[data['Channels'][i]].setPen(width=3)
        return 123

    def unwrap_graph(self, x, y, name, ticks):
        Plot = self.MainGraph.addPlot(clear=True, x=x, y=y, name=name, title=name)
        view = Plot.getViewBox()
        # view.setMouseMode(pg.ViewBox.RectMode)
        view.setMouseEnabled(x=True, y=False)
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
                self.model.form.addRow(
                    QLabel("Частота несущей[0," + str(0.5 * self.variables_with_value["gerc"]) + "]:"),
                    QLineEdit())
            else:
                self.model.form.addRow(QLabel("Частота несущей[0," + "0.5*част.дискрет." + "]:"),
                                       QLineEdit())
            self.model.form.addRow(QLabel("Начальная фаза несущей:"), QLineEdit())
        if model_num == 8:
            self.model.form.addRow(QLabel("Амплитуда сигнала:"), QLineEdit())
            self.model.form.addRow(QLabel("Частота огибающей:"), QLineEdit())
            if "gerc" in self.variables_with_value:
                self.model.form.addRow(
                    QLabel("Частота несущей[0," + str(0.5 * self.variables_with_value["gerc"]) + "]:"),
                    QLineEdit())
            else:
                self.model.form.addRow(QLabel("Частота несущей[0," + "0.5*част.дискрет." + "]:"),
                                       QLineEdit())
            self.model.form.addRow(QLabel("Начальная фаза несущей:"), QLineEdit())
        if model_num == 9:
            self.model.form.addRow(QLabel("Амплитуда сигнала:"), QLineEdit())
            self.model.form.addRow(QLabel("Частота огибающей:"), QLineEdit())
            if "gerc" in self.variables_with_value:
                self.model.form.addRow(
                    QLabel("Частота несущей[0," + str(0.5 * self.variables_with_value["gerc"]) + "]:"),
                    QLineEdit())
            else:
                self.model.form.addRow(QLabel("Частота несущей[0," + "0.5*част.дискрет." + "]:"),
                                       QLineEdit())
            self.model.form.addRow(QLabel("Начальная фаза несущей:"), QLineEdit())
            self.model.form.addRow(QLabel("Индекс глубины модуляции[0,1]:"), QLineEdit())
        if model_num == 10:
            self.model.form.addRow(QLabel("a:"), QLineEdit())
            self.model.form.addRow(QLabel("b:"), QLineEdit())
        if model_num == 11:
            self.model.form.addRow(QLabel("среднее \u03B1:"), QLineEdit())
            self.model.form.addRow(QLabel("дисперсия \u03C3:"), QLineEdit())
        if model_num == 12:
            self.model.form.addRow(QLabel("дисперсия \u03C3:"), QLineEdit())
            self.model.form.addRow(QLabel("P:"), QLineEdit())
            self.model.form.addRow(QLabel("Q:"), QLineEdit())
            self.model.form.addRow(QLabel("a(a1,a2,...):"), QLineEdit())
            self.model.form.addRow(QLabel("b(b1,b2,...):"), QLineEdit())
        if model_num == 13:
            combo = QComboBox()
            types = ["суперпозиция с произвольными коэффициентами", "мультипликативная суперпозиция"]
            self.model.form.addRow(QLabel("тип:"), combo)
            combo.addItems(types)
            self.model.form.addRow(QLabel("a(a0,a1,a2,...):"), QLineEdit())
            for i in range(self.variables_with_value["k1"]):
                self.model.form.addRow(QLabel(self.variables_with_value["Channels1"][i] + ":"), QCheckBox())
        if model_num == 14:
            combo = QComboBox()
            self.model.form.addRow(QLabel("Сигнал:"), combo)
            combo.addItems(self.variables_with_value["Channels1"])
            self.model.form.addRow(QLabel("K:"), QLineEdit())
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
        a = float(self.model.form.itemAt(0, 1).widget().text())
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
            y_coordinates.append((i % a) / a)
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
            y_coordinates.append(a * math.exp(-t / b) * math.cos(2 * math.pi * c * t + d))
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
            y_coordinates.append(a * math.cos(2 * math.pi * b * t) * math.cos(2 * math.pi * c * t + d))
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
            y_coordinates.append(a * (1 + e * math.cos(2 * math.pi * b * t)) * math.cos(2 * math.pi * c * t + d))
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_10(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        a = float(self.model.form.itemAt(0, 1).widget().text())
        b = float(self.model.form.itemAt(1, 1).widget().text())
        for i in range(n):
            t = i / gercs
            x_value = x_value + t
            x_coordinates.append(t)
            y_coordinates.append(a + (b - a) * random.random())
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_11(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        alpha = float(self.model.form.itemAt(0, 1).widget().text())
        sigma = float(self.model.form.itemAt(1, 1).widget().text())
        sigma = math.sqrt(sigma)
        for i in range(n):
            eta = 0
            t = i / gercs
            x_value = x_value + t
            x_coordinates.append(t)
            for j in range(12):
                eta += random.random()
            eta -= 6
            y_coordinates.append(alpha + (sigma * eta))
        self.draw_model(x_coordinates, y_coordinates, None)

    def model_func_12(self):
        x_coordinates = []
        y_coordinates = []
        x_value = 0
        eta = 0
        eta_list = []
        eta = []
        gercs, n = self.read_gerc_and_n()
        sigma = float(self.model.form.itemAt(0, 1).widget().text())
        sigma = math.sqrt(sigma)
        p = int(self.model.form.itemAt(1, 1).widget().text())
        q = int(self.model.form.itemAt(2, 1).widget().text())
        a = str(self.model.form.itemAt(3, 1).widget().text()).split(",")
        b = str(self.model.form.itemAt(4, 1).widget().text()).split(",")
        for i in range(n):
            p_sum = 0
            q_sum = 0
            eta_temp = 0
            t = i / gercs
            x_value = x_value + t
            x_coordinates.append(t)
            for j in range(12):
                eta_temp += random.random()
            eta_temp -= 6
            eta.append(eta_temp * sigma)
            for j in range(1, p):
                if i - j >= 0 and i != 0:
                    p_sum += float(a[j]) * eta[i - j]
            for j in range(1, q):
                if i - j >= 0 and i != 0:
                    q_sum += float(b[j]) * y_coordinates[i - j]
            y_coordinates.append(eta[i] + p_sum + q_sum)
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
            partial(self.unwrap_graph, x, y, self.model_name, ticks))

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

    def superpos_func(self):
        # self.model_name = self.model.form.itemAt(0, 1).widget().currentText() + "(" +
        x_coordinates = []
        y_coordinates = []
        checkboxes = []
        x_value = 0
        gercs, n = self.read_gerc_and_n()
        superpos_type = self.model.form.itemAt(0, 1).widget().currentIndex()
        a = str(self.model.form.itemAt(1, 1).widget().text()).split(",")
        for i in range(self.variables_with_value["k1"]):
            checkboxes.append(self.model.form.itemAt(i + 2, 1).widget().isChecked())
        for i in range(n):
            y_value = float(a[0])
            x_value = x_value + i / gercs
            x_coordinates.append(i)
            if superpos_type == 0:
                counter = 1
                for j in range(self.variables_with_value["k1"]):
                    if checkboxes[j]:
                        y_value += float(a[counter]) * self.plots_dict[self.variables_with_value["Channels1"][j]].yData[
                            i]
                        counter += 1
            else:
                for j in range(self.variables_with_value["k1"]):
                    if checkboxes[j]:
                        y_value *= self.plots_dict[self.variables_with_value["Channels1"][j]].yData[i]
            y_coordinates.append(y_value)
        self.draw_model(x_coordinates, y_coordinates, None)

    def stat_func(self):
        avg = 0
        disp = 0
        asym = 0
        exc = 0
        for i in reversed(range(self.stat.form.count())):
            self.stat.form.removeRow(i)

        self.stat.text_hint.setText(self.model.form.itemAt(0, 1).widget().currentText())
        n = self.model.form.itemAt(0, 1).widget().currentIndex()
        k = int(self.model.form.itemAt(1, 1).widget().text())
        for i in range(self.variables_with_value["n"]):
            avg += self.plots_dict[self.variables_with_value["Channels1"][n]].yData[i]
        avg = avg / self.variables_with_value["n"]
        # avg = float('{:.2f}'.format(avg))
        self.stat.form.addRow(QLabel("Среднее:"), QLabel(str(avg)))

        for i in range(self.variables_with_value["n"]):
            disp += pow(self.plots_dict[self.variables_with_value["Channels1"][n]].yData[i] - avg, 2)
        disp = disp / self.variables_with_value["n"]
        disp = float('{:.2f}'.format(disp))
        self.stat.form.addRow(QLabel("Дисперсия:"), QLabel(str(disp)))

        srko = math.sqrt(disp)
        srko = float('{:.2f}'.format(srko))
        self.stat.form.addRow(QLabel("Среднеквадратичное отклонение:"), QLabel(str(srko)))

        var = srko / avg
        var = float('{:.2f}'.format(var))
        self.stat.form.addRow(QLabel("Коэф. вариации:"), QLabel(str(var)))

        for i in range(self.variables_with_value["n"]):
            asym += pow(self.plots_dict[self.variables_with_value["Channels1"][n]].yData[i] - avg, 3)
        asym = asym / self.variables_with_value["n"] / pow(srko, 3)
        asym = float('{:.2f}'.format(asym))
        self.stat.form.addRow(QLabel("Коэф. ассиметрии:"), QLabel(str(asym)))

        for i in range(self.variables_with_value["n"]):
            exc += pow(self.plots_dict[self.variables_with_value["Channels1"][n]].yData[i] - avg, 4)
        exc = exc / self.variables_with_value["n"] / pow(srko, 4)
        exc = exc - 3
        exc = float('{:.2f}'.format(exc))
        testtest = str(exc)
        self.stat.form.addRow(QLabel("Коэф. эксцесса:"), QLabel(str(exc)))

        minim = min(self.plots_dict[self.variables_with_value["Channels1"][n]].yData)
        minim = float('{:.2f}'.format(minim))
        self.stat.form.addRow(QLabel("минимальное знач. сигнала:"), QLabel(str(minim)))

        maxim = max(self.plots_dict[self.variables_with_value["Channels1"][n]].yData)
        maxim = float('{:.2f}'.format(maxim))
        self.stat.form.addRow(QLabel("максим. знач. сигнала:"), QLabel(str(maxim)))

        data = self.plots_dict[self.variables_with_value["Channels1"][n]].yData
        data.sort()
        kwan_n = int(0.05 * self.variables_with_value["n"])
        kwan1 = data[kwan_n]
        self.stat.form.addRow(QLabel("Квантиль 0.05:"), QLabel(str(kwan1)))

        kwan_n = int(0.95 * self.variables_with_value["n"])
        kwan2 = data[kwan_n]
        self.stat.form.addRow(QLabel("Квантиль 0.95:"), QLabel(str(kwan2)))

        kwan_n = int(0.5 * self.variables_with_value["n"])
        med = data[kwan_n]
        self.stat.form.addRow(QLabel("Медиана:"), QLabel(str(med)))

        dots = []
        hysto = [0 for x in range(k)]
        temp_dot = minim
        h = (maxim - minim) / k
        for i in range(k + 1):
            dots.append(temp_dot + h * i)
        for i in range(self.variables_with_value["n"]):
            for j in range(1, k + 1):
                if dots[j] >= data[i] >= dots[j - 1]:
                    hysto[j - 1] += 1
                    break
        bg = pg.BarGraphItem(x=range(k), height=hysto, width=1)
        self.stat.hystogram.clear()
        self.stat.hystogram.addItem(bg)
        self.stat.hystogram.setMouseEnabled(x=False, y=False)
        self.stat.show()

    def spec_func(self):
        self.spec.grid.itemAt(0).widget().addItems(self.variables_with_value["Channels1"])
        self.spec.show()

    def do_it_func(self):
        x_coordinates = []
        x_value = 0
        tip = self.spec.type.currentIndex()
        md = self.spec.mode.currentIndex()
        ch = self.spec.grid.itemAt(0).widget().currentIndex()
        ch_name = self.spec.grid.itemAt(0).widget().currentText()
        h0 = self.spec.grid.itemAt(1).widget().currentIndex()
        l = self.spec.grid.itemAt(3).widget().text()
        coord = self.plots_dict[self.variables_with_value["Channels1"][ch]].yData
        y_coordinates_a = numpy.fft.rfft(coord)
        y_coordinates_p = numpy.fft.rfft(coord)
        if h0 == 1:
            y_coordinates_a[0] = 0
            y_coordinates_p[0] = 0
        elif h0 == 2:
            y_coordinates_a[0] = abs(y_coordinates_a[1])
            y_coordinates_p[0] = abs(y_coordinates_p[1])
        for i in range(len(y_coordinates_a)):
            t = i / (self.variables_with_value["gerc"] * self.variables_with_value["n"])
            x_value = x_value + t
            x_coordinates.append(t)
            y_coordinates_a[i] = t * abs(y_coordinates_a[i])
            y_coordinates_p[i] = pow(t, 2) * pow(abs(y_coordinates_p[i]), 2)
        y_coordinates_a = y_coordinates_a.real
        y_coordinates_p = y_coordinates_p.real
        if l != "" and l != 0:
            l = int(l)
            mlt = 1 / ((2 * l) + 1)
            for j in range(len(y_coordinates_a)):
                summ_a = 0
                summ_p = 0
                for i in range(-l, l):
                    if j + i < len(y_coordinates_a):
                        summ_a += y_coordinates_a[abs(j + i)]
                        summ_p += y_coordinates_p[abs(j + i)]
                y_coordinates_a[j] = summ_a * mlt
                y_coordinates_p[j] = summ_p * mlt

        y_coordinates_a_lg = []
        for i in range(len(y_coordinates_a)):
            if y_coordinates_a[i] > 0:
                y_coordinates_a_lg.append(math.log10(y_coordinates_a[i]) * 20)
            else:
                y_coordinates_a_lg.append(y_coordinates_a[i])

        plot = self.spec.specGraph.addPlot()
        plot.setLabels(left=ch_name, bottom="Частота(гц)")
        plot_a = plot.plot(x=x_coordinates, y=y_coordinates_a,
                           title=self.variables_with_value["Channels1"][ch] + "_a")
        plot_p = plot.plot(x=x_coordinates, y=y_coordinates_p,
                           title=self.variables_with_value["Channels1"][ch] + "_p", pen={'color': "FF0"})
        plot_lg = plot.plot(x=x_coordinates, y=y_coordinates_a_lg,
                            title=self.variables_with_value["Channels1"][ch] + "_lg", pen={'color': "F0F"})
        self.spec_plot.append(plot)
        self.spec_dict_a.append(plot_a)
        self.spec_dict_p.append(plot_p)
        self.spec_plot_lg.append(plot_lg)
        if md == 0:
            if tip == 0:
                plot_p.hide()
                plot_lg.hide()
            else:
                plot_a.hide()
                plot_lg.hide()
        else:
            plot_p.hide()
            plot_a.hide()
        self.spec.specGraph.nextRow()

    def change_type_func(self):
        tip = self.spec.type.currentIndex()
        md = self.spec.mode.currentIndex()
        if len(self.spec_dict_a) != 0 and md == 0:
            for i in range(len(self.spec_dict_a)):
                if tip == 0:
                    self.spec_dict_a[i].show()
                    self.spec_dict_p[i].hide()
                else:
                    self.spec_dict_a[i].hide()
                    self.spec_dict_p[i].show()
                self.spec_plot[i].autoRange()

    def change_mode_func(self):
        md = self.spec.mode.currentIndex()
        if len(self.spec_dict_a) != 0:
            if md == 0:
                self.change_type_func()
                for i in range(len(self.spec_dict_a)):
                    self.spec_plot_lg[i].hide()
            else:
                self.hide_all_exep_lg()
                for i in range(len(self.spec_dict_a)):
                    self.spec_plot_lg[i].show()
                    self.spec_plot[i].autoRange()

    def hide_all_exep_lg(self):
        for i in range(len(self.spec_dict_a)):
            self.spec_dict_a[i].hide()
            self.spec_dict_p[i].hide()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
