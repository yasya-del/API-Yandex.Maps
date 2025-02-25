import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]

x = float(input())
y = float(input())


class Example(QWidget):
    def init(self):
        super().init()
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = '[https://static-maps.yandex.ru/v1?](https://static-maps.yandex.ru/v1?)'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={x}%2C{y}&spn=0,69.00619'
        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if name == 'main':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())