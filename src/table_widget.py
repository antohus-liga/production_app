from PySide6.QtWidgets import QTableView, QWidget
from sql.manager import get_connection


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.view = QTableView()

        db = get_connection()
