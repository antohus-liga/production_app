from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
)

from ui.containers.inputs_container import InputsContainer
from sql.manager import (
    calculate_mat_quant,
    calculate_prod_line_cost,
    calculate_pro_cost,
    calculate_pro_quant,
    calculate_mov_out_price,
    calculate_mov_in_price,
)


class PopupContainer(QWidget):
    updated = Signal()

    def __init__(self, master, row=None, item=None):
        super().__init__()
        self.row = row
        self.item = item
        self.master = master
        self.TABLE_NAME = self.master.TABLE_NAME
        self.COLUMN_NAMES = self.master.COLUMN_NAMES
        self.column_info = self.master.column_info
        self.setWindowFlags(Qt.WindowType.Popup)
        self.hasNr = False

        self.inputs_container = InputsContainer(master)
        self.inputs_container.update_combos()

        self.title = QLabel("Edit")
        self.title.setStyleSheet("font: bold 20px")

        self.start = 0
        if self.TABLE_NAME in ("movements_in", "movements_out", "production_line"):
            self.start = 1
            self.hasNr = True

        if row is not None:
            for i in range(self.start, len(self.inputs_container.inputs) + self.start):
                value = self.master.model().index(row, i).data()
                input_widget = self.inputs_container.inputs[i - self.start][1]

                if isinstance(input_widget, QLineEdit):
                    input_widget.setText(value)
                elif isinstance(input_widget, QComboBox):
                    input_widget.setCurrentText(value)
                elif isinstance(input_widget, QDateEdit):
                    date_ints = value.split(sep="/")
                    d, m, y = date_ints

                    date = QDate()
                    date.setDate(int(y), int(m), int(d))
                    input_widget.setDate(date)

        elif item is not None:
            id = item.data(Qt.ItemDataRole.UserRole)
            query = QSqlQuery()

            if self.hasNr:
                query.prepare(f"SELECT * FROM {self.TABLE_NAME} WHERE nr = ?")
            else:
                query.prepare(f"SELECT * FROM {self.TABLE_NAME} WHERE code = ?")
            query.addBindValue(id)

            query.exec()

            query.first()
            values = [str(query.value(i)) for i in range(query.record().count())]
            for i in range(self.start, len(self.inputs_container.inputs) + self.start):
                value = values[i]
                input_widget = self.inputs_container.inputs[i - self.start][1]

                if isinstance(input_widget, QLineEdit):
                    input_widget.setText(value)
                elif isinstance(input_widget, QComboBox):
                    input_widget.setCurrentText(value)
                elif isinstance(input_widget, QDateEdit):
                    date_ints = value.split(sep="/")
                    d, m, y = date_ints

                    date = QDate()
                    date.setDate(int(y), int(m), int(d))
                    input_widget.setDate(date)

        self.confirm_btn = QPushButton("Confirm")
        self.cancel_btn = QPushButton("Cancel")

        self.confirm_btn.clicked.connect(self.confirm)
        self.cancel_btn.clicked.connect(lambda: self.hide())

        self.popup_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.buttons_layout.addWidget(self.confirm_btn)
        self.buttons_layout.addWidget(self.cancel_btn)

        self.popup_layout.addWidget(self.title)
        self.popup_layout.addWidget(self.inputs_container)
        self.popup_layout.addLayout(self.buttons_layout)

        self.setLayout(self.popup_layout)

    def confirm(self):
        query = QSqlQuery()
        col_val = ""
        values = []
        code = ""
        if self.row is not None:
            code = self.master.model().index(self.row, 0).data()
        elif self.item:
            code = self.item.data(Qt.ItemDataRole.UserRole)

        for i in range(len(self.inputs_container.inputs)):
            input_field = self.inputs_container.inputs[i][1]
            col_name = self.column_info[self.inputs_container.inputs[i][0].text()][
                "db_name"
            ]
            value = ""

            if isinstance(input_field, QLineEdit):
                value = input_field.text()
            elif isinstance(input_field, QComboBox):
                value = input_field.currentText()
            elif isinstance(input_field, QDateEdit):
                value = input_field.date().toString("dd/MM/yyyy")

            values.append(value)

            col_val += col_name + " = ?"
            if i < len(self.inputs_container.inputs) - 1:
                col_val += ", "

        code_or_nr = ""
        if self.hasNr:
            code_or_nr = "nr"
        else:
            code_or_nr = "code"

        query.prepare(
            f"""
            UPDATE {self.master.TABLE_NAME}
            SET updated_at = STRFTIME('%d/%m/%Y', 'now', 'localtime'), {col_val}
            WHERE {code_or_nr} = ?
        """
        )

        for value in values:
            query.addBindValue(value)

        query.addBindValue(code)
        db = QSqlDatabase.database()
        if not db.transaction():
            return

        try:
            query.exec()
            match self.TABLE_NAME:
                case "products":
                    calculate_mov_out_price()
                    calculate_prod_line_cost()
                case "materials":
                    calculate_pro_cost()
                    calculate_prod_line_cost()
                    calculate_mov_in_price()
                    calculate_mat_quant()
                case "production_line":
                    calculate_pro_quant()
                    calculate_mat_quant()
                    calculate_prod_line_cost()
                case "movements_in":
                    calculate_mat_quant()
                    calculate_mov_in_price()
                case "movements_out":
                    calculate_pro_quant()
                    calculate_mov_out_price()

            db.commit()
            self.updated.emit()

        except Exception as e:
            db.rollback()
            QMessageBox.critical(
                None, "Operation failed", f"Insertion aborted: {str(e)}"
            )

        finally:
            self.hide()
