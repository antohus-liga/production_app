from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QGridLayout,
    QHBoxLayout,
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

        self.column_info = self.get_column_names()
        self.column_names = list(self.column_info.keys())

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.insert_values)

        self.inputs: list[tuple[QLabel, QLineEdit | QComboBox | QDateEdit]] = []
        for col_name in self.column_names:
            input_widget = QLineEdit()
            match self.column_info[col_name]:
                case "le":
                    input_widget = QLineEdit()
                case "cb":
                    input_widget = QComboBox()
                    input_widget.addItem("test")
                case "de":
                    input_widget = QDateEdit()
                    input_widget.setCalendarPopup(True)
                    input_widget.setDisplayFormat("dd/MM/yyyy")
                case "df":
                    continue

            self.inputs.append((QLabel(col_name), input_widget))

        self.master_layout = QVBoxLayout()

        self.grid = QGridLayout()
        row = 0
        col = 0
        for i in range(len(self.inputs)):
            widget = QWidget()

            h_layout = QHBoxLayout()
            h_layout.addWidget(self.inputs[i][0])
            h_layout.addWidget(self.inputs[i][1])
            h_layout.setStretch(0, 1)
            h_layout.setStretch(1, 3)

            widget.setLayout(h_layout)
            self.grid.addWidget(widget, row, col)

            col += 1

            if col >= 3:
                col = 0
                row += 1

        self.master_layout.addLayout(self.grid)
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
                self.table.setItem(row, col, QTableWidgetItem(str(query.value(col))))

            row += 1

    def insert_values(self):
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO clients (
                cli_code, cli_type, first_name, last_name, company_name,
                country, city, phone, email, date_of_birth, nif, created_at, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                STRFTIME('%d/%m/%Y', 'now', 'localtime')
            )
        """
        )
        for _, input_field in self.inputs:
            value = ""
            if isinstance(input_field, QLineEdit):
                value = input_field.text()
            elif isinstance(input_field, QComboBox):
                value = input_field.currentText()
            elif isinstance(input_field, QDateEdit):
                value = input_field.date().toString("dd/MM/yyyy")
            else:
                value = ""

            if value != "":
                query.addBindValue(value)
            else:
                QMessageBox.warning(
                    self,
                    "NULL value not expected",
                    "Make sure every field is filled",
                )
                query.clear()
                return
        if not query.exec():
            print(query.lastError().text())
        self.load_table()

    # df - defaulted
    # le - line edit
    # cb - combo box
    # de - date edit
    def get_column_names(self):
        map = {
            "clients": {
                "ID": "df",
                "Code": "le",
                "Type": "cb",
                "First Name": "le",
                "Last Name": "le",
                "Company Name": "le",
                "Country": "le",
                "City": "le",
                "Phone": "le",
                "Email": "le",
                "Date of Birth": "de",
                "NIF": "le",
                "Created at": "df",
                "Updated at": "df",
            }
        }
        return map[self.table_name]
