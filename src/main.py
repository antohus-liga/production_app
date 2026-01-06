from PySide6.QtWidgets import QApplication
from display_widget import DisplayWidget
from sql.manager import get_connection
import sys


app = QApplication(sys.argv)
get_connection()
clients_widget = DisplayWidget("movements_out")
clients_widget.show()
app.exec()
