from PySide6.QtWidgets import QApplication
from table_widget import TableWidget
import sys


app = QApplication(sys.argv)
widget = TableWidget()
widget.show()
app.exec()
