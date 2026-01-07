from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem
from PySide6.QtSql import QSqlQuery


class TableWidget(QTableWidget):
    def __init__(self, table_name, column_names):
        super().__init__()

        self.TABLE_NAME = table_name
        self.COLUMN_NAMES = column_names

        self.setColumnCount(len(self.COLUMN_NAMES))
        self.setHorizontalHeaderLabels(self.COLUMN_NAMES)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionsClickable(True)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)

    def load_table(self):
        self.setRowCount(0)

        query = QSqlQuery()
        query.exec(f"SELECT * FROM {self.TABLE_NAME}")
        row = 0
        while query.next():
            self.insertRow(row)
            for col in range(query.record().count()):
                self.setItem(row, col, QTableWidgetItem(str(query.value(col))))

            row += 1
