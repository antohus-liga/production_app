from PySide6.QtCore import QRegularExpression
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
from PySide6.QtGui import QDoubleValidator, QRegularExpressionValidator


class InputsContainer(QWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.inputs: list[tuple[QLabel, QLineEdit | QComboBox | QDateEdit]] = []
        self.relational_combos: list[tuple[str, QComboBox]] = []
        for col_name in self.master.COLUMN_NAMES:
            input_widget = QLineEdit()
            match self.master.column_info[col_name]["input_type"]:
                case "line_edit":
                    input_widget = QLineEdit()
                    match self.master.column_info[col_name]["data_type"]:
                        case "string":
                            regex = QRegularExpression(r"[A-Za-z\-\ \á\à\ã\â]+")
                            input_widget.setValidator(
                                QRegularExpressionValidator(regex)
                            )
                        case "integer":
                            regex = QRegularExpression(r"\d+")
                            input_widget.setValidator(
                                QRegularExpressionValidator(regex)
                            )
                        case "float":
                            input_widget.setValidator(
                                QDoubleValidator(bottom=0, decimals=2)
                            )
                        case "uppercase_only":
                            regex = QRegularExpression(r"[A-Z0-9]+")
                            input_widget.setValidator(
                                QRegularExpressionValidator(regex)
                            )
                    input_widget.setMaxLength(
                        self.master.column_info[col_name]["max_len"]
                    )

                case "combo_box":
                    input_widget = QComboBox()
                    values = self.master.column_info[col_name]["values"]
                    if values[0] == "query":
                        self.relational_combos.append((col_name, input_widget))
                    else:
                        input_widget.addItems(values)
                case "date_edit":
                    input_widget = QDateEdit()
                    input_widget.setCalendarPopup(True)
                    input_widget.setDisplayFormat("dd/MM/yyyy")
                case "defaulted":
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

    def update_combos(self):
        for col_name, input_widget in self.relational_combos:
            input_widget.clear()

            query_str = self.master.column_info[col_name]["values"][1]
            query = QSqlQuery()
            query.exec(query_str)

            values = []
            while query.next():
                values.append(query.value(0))

            input_widget.addItems(values)

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

            if value != "":
                query.addBindValue(value)
            else:
                QMessageBox.warning(
                    self,
                    "Valor vazio",
                    "Confirme que preencheu todos os campos",
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
                        code, first_name, last_name, cli_type, company_name,
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
                        code, first_name, last_name, sup_type, company_name,
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
                        code, name, category, base_unit, unit_price, 
                        created_at, updated_at
                    ) VALUES (
                        ?, ?, ?, ?, ?,
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "products":
                query.prepare(
                    """
                    INSERT INTO products (
                        code, name, category, base_unit,
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
                        mat_code, sup_code, quantity,
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
                        pro_code, cli_code, quantity,
                        created_at, updated_at
                    ) VALUES (
                        ?, ?, ?,
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "production_line":
                query.prepare(
                    """
                    INSERT INTO production_line (
                        pro_code, quantity,
                        created_at, updated_at
                    ) VALUES (
                        ?, ?,
                        STRFTIME('%d/%m/%Y', 'now', 'localtime'), 
                        STRFTIME('%d/%m/%Y', 'now', 'localtime')
                    )
                """
                )
            case "product_materials":
                query.prepare(
                    """
                    INSERT INTO product_materials (
                        pro_code, mat_code, quantity
                    ) VALUES (
                        ?, ?, ?
                    )
                """
                )
        return query
