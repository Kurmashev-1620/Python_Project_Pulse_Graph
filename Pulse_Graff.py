import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer
import time

app = QtWidgets.QApplication([])
ui = uic.loadUi('Pulse_Graff.ui')
ui.setWindowTitle('Pulse Graff')

serial = QSerialPort()
serial.setBaudRate(230400)

portList = []
ports = QSerialPortInfo().availablePorts()

for port in ports:
    portList.append(port.portName())

ui.comboBox.addItems(portList)

LenGraph = 2000

ListX = list(range(LenGraph))
ListY = [0] * LenGraph

# Настройка графика
plotWidget = pg.PlotWidget()
layout = QtWidgets.QVBoxLayout()
ui.graph.setLayout(layout)
layout.addWidget(plotWidget)
curve = plotWidget.plot()

# Порог для определения всплесков
threshold = 600

# Переменные для подсчета пульса
last_peak_time = 0
peak_times = []

def serial_open():
    serial.setPortName(ui.comboBox.currentText())
    serial.open(QIODevice.ReadOnly)

def serial_close():
    serial.close()

def calculate_bpm():
    global peak_times
    current_time = time.time()
    # Удаляем устаревшие значения
    peak_times = [t for t in peak_times if current_time - t < 60]
    bpm = len(peak_times)
    ui.pulseLabel.setText(f'Pulse: {bpm} BPM')

def serial_read():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()

    if rxs.isdigit():
        new_data = int(rxs)
        global ListY, last_peak_time

        ListY = ListY[1:] + [new_data]
        curve.setData(ListX, ListY)

        if new_data > threshold and (time.time() - last_peak_time) > 0.5:
            last_peak_time = time.time()
            peak_times.append(last_peak_time)
            calculate_bpm()

serial.readyRead.connect(serial_read)
ui.OPEN_Button.clicked.connect(serial_open)
ui.CLOSE_Button.clicked.connect(serial_close)

# Таймер для периодического обновления пульса
timer = QTimer()
timer.timeout.connect(calculate_bpm)
timer.start(1000)  # Обновляем каждую секунду

ui.show()
app.exec()

git remote add origin https://github.com/Kurmashev-1620/Python_Project_Pulse_Graph.git
