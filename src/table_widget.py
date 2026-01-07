from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem
from PySide6.QtSql import QSqlQuery


class TableWidget(QTableWidget):
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.setColumnCount(len(self.master.COLUMN_NAMES))
        self.setHorizontalHeaderLabels(self.master.COLUMN_NAMES)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionsClickable(True)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)

    def load_table(self):
        self.setRowCount(0)

        query = QSqlQuery()
        query.exec(f"SELECT * FROM {self.master.TABLE_NAME}")
        row = 0
        while query.next():
            self.insertRow(row)
            for col in range(query.record().count()):
                self.setItem(row, col, QTableWidgetItem(str(query.value(col))))

            row += 1
