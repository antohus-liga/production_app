from PySide6.QtWidgets import (
    QTableWidget,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QTableWidgetItem,
    QMessageBox,
)
from PySide6.QtSql import QSqlQuery


class TableWidget(QWidget):
    def __init__(self, table_name):
        super().__init__()

        self.table_name = table_name
        self.column_names = self.get_column_names()

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.insert_values)

        self.inputs: list[tuple[QLabel, QLineEdit]] = [
            (QLabel(col_name), QLineEdit()) for col_name in self.column_names
        ]

        self.master_layout = QVBoxLayout()
        for label, line_edit in self.inputs:
            self.master_layout.addWidget(label)
            self.master_layout.addWidget(line_edit)
        self.master_layout.addWidget(self.add_btn)
        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        self.load_table()

    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery()
        query.exec(f"SELECT * FROM {self.table_name}")
        row = 0
        while query.next():
            self.table.insertRow(row)
            for col in range(query.record().count()):
                self.table.setItem(row, col, QTableWidgetItem(query.value(col)))

            row += 1

    def insert_values(self):
        query = QSqlQuery()
        query.prepare(f"INSERT INTO {self.table_name} VALUES(?, ?, ?, ?, ?, ?)")
        for _, line_edit in self.inputs:
            value = line_edit.text()
            if value != "":
                query.addBindValue(value)
            else:
                QMessageBox.warning(
                    self,
                    "All values must not be NULL",
                    "Make sure every field is filled",
                )
                return
        query.exec()
        self.load_table()

    def get_column_names(self):
        map = {"clients": ["Code", "Name", "City", "Country", "Phone", "Email"]}
        return map[self.table_name]
