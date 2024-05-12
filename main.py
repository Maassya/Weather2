import sys
from PyQt5 import QtGui
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt

from main_win import Ui_MainWindow
from api import get_weather_by_city


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()

        self.setupUi(self)
        self.show_time()

        self.configure()

        self.setWindowTitle('Погода')

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ico.png'))

    def configure(self):
        self.ok_btn.clicked.connect(self.handle_ok_btn)

        self.timer.timeout.connect(self.show_time)
        self.timer.start(500)
        self.city_img.setPixmap(QtGui.QPixmap("city.jpg").scaled(400, 400, Qt.KeepAspectRatio))

    def show_time(self):
        new_time = datetime.now().strftime('%H:%M:%S')

        hour = datetime.now().hour
        if 10 > hour >= 6:
            new_time = '🌅' + new_time
        elif hour < 14:
            new_time = '🌞' + new_time
        elif hour < 21:
            new_time = '🌆' + new_time
        else:
            new_time = '🌙' + new_time


        self.time_lbl.setText(datetime.now().strftime('%H:%M:%S'))

    def handle_ok_btn(self):
        name_city = self.search_city.text()

        try:
            resp = get_weather_by_city(name_city)
            self.temp_lbl.setText(f"{resp.temp}°C")
            self.temp_feels_lbl.setText(f"{resp.temp_feels}°C")
            self.temp_min_lbl.setText(f"{resp.temp_min}°C")
            self.temp_max_lbl.setText(f"{resp.temp_max}°C")
            self.description_lbl.setText(f"{', '.join(resp.description)}")
        except:
            msg = create_msg_error(
                self,
                "Произошла ошибка. Проверьте подключение к интернету или укажите существующий город"
            )
            msg.exec_()


def create_msg_error(parent, msg_text: str):
    msg = QtWidgets.QMessageBox(parent)
    msg.setText(msg_text)

    # msg.setWindowIcon(QtGui.QIcon("files/error.ico"))
    msg.setWindowTitle("Ошибка")
    return msg


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MyWindow()

    win.show()

    app.exec_()
