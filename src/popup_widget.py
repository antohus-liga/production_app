from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
)

from inputs_container import InputsContainer


class PopupWidget(QWidget):
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

        self.inputs_container = InputsContainer(master)
        self.title = QLabel("Edit")
        self.title.setStyleSheet("font: bold 20px")

        if row is not None:
            for i in range(len(self.inputs_container.inputs)):
                value = self.master.model().index(row, i).data()
                input_widget = self.inputs_container.inputs[i][1]

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

            query.prepare(f"SELECT * FROM {self.TABLE_NAME} WHERE code = ?")
            query.addBindValue(id)

            query.exec()

            query.first()
            values = [str(query.value(i)) for i in range(query.record().count())]
            for i in range(len(self.inputs_container.inputs)):
                value = values[i]
                input_widget = self.inputs_container.inputs[i][1]

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
        if self.row:
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

        query.prepare(
            f"""
            UPDATE {self.master.TABLE_NAME}
            SET {col_val}
            WHERE code = ?
        """
        )

        for value in values:
            query.addBindValue(value)

        query.addBindValue(code)
        query.exec()

        self.updated.emit()
        self.hide()
