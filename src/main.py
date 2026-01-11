from PySide6.QtWidgets import QApplication
import sys

from ui.display_widget import DisplayWidget
from sql.manager import get_connection


app = QApplication(sys.argv)

with open("src/main.qss") as style:
    app.setStyleSheet(style.read())

get_connection()
clients_widget = DisplayWidget("clients")
clients_widget.show()

app.exec()
