from PySide6.QtWidgets import QApplication
import sys

from sql.manager import get_connection
from ui.main_window import MainWindow


app = QApplication(sys.argv)

with open("src/main.qss") as style:
    app.setStyleSheet(style.read())

get_connection()
main_window = MainWindow()
main_window.show()

app.exec()
