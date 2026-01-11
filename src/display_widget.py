from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from inputs_container import InputsContainer
from list_widget import ListWidget
from table_widget import TableWidget
import json


class DisplayWidget(QWidget):
    def __init__(self, table_name):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.TABLE_NAME = table_name

        self.column_info = self.get_column_names()
        self.COLUMN_NAMES = list(self.column_info.keys())

        self.table = TableWidget(self)
        self.list = ListWidget(self)
        self.inputs = InputsContainer(self)

        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")

        self.add_btn.clicked.connect(self.insert_values)
        self.delete_btn.clicked.connect(self.delete_values)

        self.switch_to_list = QPushButton("List view")
        self.switch_to_list.clicked.connect(self.toggle_view)
        self.switch_to_list.setFixedWidth(100)

        self.switch_to_table = QPushButton("Table view")
        self.switch_to_table.setDisabled(True)
        self.switch_to_table.clicked.connect(self.toggle_view)
        self.switch_to_table.setFixedWidth(100)

        self.master_layout = QVBoxLayout()
        self.toggle_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.toggle_layout.addWidget(self.switch_to_table)
        self.toggle_layout.addWidget(self.switch_to_list)
        self.toggle_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.buttons_layout.addWidget(self.add_btn)
        self.buttons_layout.addWidget(self.delete_btn)

        self.master_layout.addLayout(self.toggle_layout)
        self.master_layout.addWidget(self.inputs)
        self.master_layout.addLayout(self.buttons_layout)

        self.master_layout.addWidget(self.table)
        self.master_layout.addWidget(self.list)
        self.list.hide()

        self.setLayout(self.master_layout)

        self.table.load_table()

    def insert_values(self):
        self.inputs.insert_data()
        self.table.load_table()
        self.list.load_data()

    def delete_values(self):
        query = QSqlQuery()
        if not query.prepare(f"DELETE FROM clients WHERE cli_code = ?"):
            print(query.lastError().text())

        if not self.switch_to_table.isEnabled():
            selection = self.table.selectionModel()
            if not selection.hasSelection():
                QMessageBox.warning(
                    self, "Selection is empty", "Select any row to delete it."
                )
                return

            rows = selection.selectedRows()
            for index in rows:
                row = index.row()
                code = self.table.model().index(row, 1).data()
                query.bindValue(0, code)
                query.exec()

        self.table.load_table()
        self.list.load_data()

    def toggle_view(self):
        if self.switch_to_table.isEnabled():
            self.switch_to_table.setDisabled(True)
            self.list.hide()
            self.switch_to_list.setDisabled(False)
            self.table.show()
        else:
            self.switch_to_list.setDisabled(True)
            self.table.hide()
            self.switch_to_table.setDisabled(False)
            self.list.show()

    def get_column_names(self):
        with open("src/table_info.json") as f:
            map = json.load(f)
        return map[self.TABLE_NAME]
