from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
)
from PySide6.QtSql import QSqlQuery


class InputsContainer(QWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.inputs: list[tuple[QLabel, QLineEdit | QComboBox | QDateEdit]] = []
        for col_name in self.master.COLUMN_NAMES:
            input_widget = QLineEdit()
            match self.master.column_info[col_name]:
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

        self.setLayout(self.grid)

    def insert_data(self):
        query = self.prepare_insertion_query()

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

    def prepare_insertion_query(self) -> QSqlQuery:
        query = QSqlQuery()
        match self.master.TABLE_NAME:
            case "clients":
                query.prepare(
                    """
                    INSERT INTO clients (
                        cli_code, first_name, last_name, cli_type, company_name,
                        country, city, phone, email, date_of_birth, nif, created_at, updated_at
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "suppliers":
                query.prepare(
                    """
                    INSERT INTO suppliers (
                        sup_code, first_name, last_name, sup_type, company_name,
                        country, city, phone, email, date_of_birth, nif, created_at, updated_at
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "materials":
                query.prepare(
                    """
                    INSERT INTO materials (
                        mat_code, name, category, base_unit, unit_price, 
                        status, created_at, updated_at
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?,
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "products":
                query.prepare(
                    """
                    INSERT INTO products (
                        pro_code, name, category, base_unit,
                        unit_price, created_at, updated_at
                    ) VALUES (
                        ?, ?, ?, ?, ?,
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "movements_in":
                query.prepare(
                    """
                    INSERT INTO movements_in (
                        mat_id, sup_id, quantity,
                        created_at, updated_at
                    ) VALUES (
                        ?, ?, ?,
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "movements_out":
                query.prepare(
                    """
                    INSERT INTO movements_out (
                        pro_id, cli_id, quantity,
                        created_at, updated_at
                    ) VALUES (
                        ?, ?, ?,
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
        return query
