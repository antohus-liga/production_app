from PySide6.QtWidgets import QApplication
from table_widget import TableWidget
from sql.manager import get_connection
import sys


app = QApplication(sys.argv)
get_connection()
clients_widget = TableWidget("clients")
clients_widget.show()
app.exec()
