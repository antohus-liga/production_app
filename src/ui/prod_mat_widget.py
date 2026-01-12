import json
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from ui.containers.inputs_container import InputsContainer
from ui.views.tree_widget import TreeWidget


class ProdMatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.TABLE_NAME = "product_materials"

        self.column_info = self.get_column_names()
        self.COLUMN_NAMES = list(self.column_info.keys())

        self.tree = TreeWidget()
        self.inputs = InputsContainer(self)

        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")

        self.add_btn.clicked.connect(self.insert_values)
        self.delete_btn.clicked.connect(self.delete_values)

        self.master_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.buttons_layout.addWidget(self.add_btn)
        self.buttons_layout.addWidget(self.delete_btn)

        self.master_layout.addWidget(self.inputs)
        self.master_layout.addLayout(self.buttons_layout)
        self.master_layout.addWidget(self.tree)

        self.setLayout(self.master_layout)

        self.inputs.update_combos()

    def get_column_names(self):
        with open("src/table_info.json") as f:
            map = json.load(f)
        return map[self.TABLE_NAME]["columns"]

    def insert_values(self):
        self.inputs.insert_data()
        self.tree.load()

    def delete_values(self):
        query = QSqlQuery()
        items = self.tree.selectedItems()
        for item in items:
            parent = item.parent()

            if parent is not None:
                query.prepare(
                    "DELETE FROM product_materials WHERE pro_code = ? AND mat_code = ?"
                )
                query.addBindValue(parent.text(0))
                query.addBindValue(item.text(0))
            else:
                query.prepare("DELETE FROM product_materials WHERE pro_code = ?")
                query.addBindValue(item.text(0))

            query.exec()

        self.tree.load()
