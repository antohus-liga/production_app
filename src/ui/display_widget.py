from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
import json

from sql.manager import (
    calculate_mat_quant,
    calculate_mov_in_price,
    calculate_mov_out_price,
    calculate_pro_cost,
    calculate_pro_quant,
    calculate_prod_line_cost,
)
from ui.containers.inputs_container import InputsContainer
from ui.views.list_widget import ListWidget
from ui.views.table_widget import TableWidget


class DisplayWidget(QWidget):
    data_changed = Signal()

    def __init__(self, table_name):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.TABLE_NAME = table_name

        self.column_info = self.get_column_names()
        self.COLUMN_NAMES = list(self.column_info.keys())

        self.table = TableWidget(self)
        self.list = ListWidget(self)
        self.inputs = InputsContainer(self)

        self.table.updated.connect(self.data_changed.emit)
        self.list.updated.connect(self.data_changed.emit)

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

        self.table.load()
        self.inputs.update_combos()

    def update_views(self):
        self.table.load()
        self.list.load()

    def insert_values(self):
        db = QSqlDatabase.database()
        if not db.transaction():
            return

        try:
            self.inputs.insert_data()

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

        except Exception as e:
            db.rollback()
            QMessageBox.critical(
                None, "Operacao nao concluida", f"Insercao cancelada: {str(e)}"
            )
        finally:
            self.table.load()
            self.list.load()
            self.data_changed.emit()

    def delete_values(self):
        db = QSqlDatabase.database()
        query = QSqlQuery()

        if self.TABLE_NAME in ("clients", "suppliers", "materials", "products"):
            query.prepare(f"DELETE FROM {self.TABLE_NAME} WHERE code = ?")
        else:
            query.prepare(f"DELETE FROM {self.TABLE_NAME} WHERE nr = ?")

        if not self.switch_to_table.isEnabled():
            selection = self.table.selectionModel()
            if not selection.hasSelection():
                QMessageBox.warning(
                    self,
                    "A seleção está vazia",
                    "Selecione alguma linha para a eliminar.",
                )
                return

            rows = selection.selectedRows()
            for index in rows:
                row = index.row()
                id = self.table.model().index(row, 0).data()
                query.bindValue(0, id)
        else:
            selection = self.list.selectionModel()
            if not selection.hasSelection():
                QMessageBox.warning(
                    self,
                    "A seleção está vazia",
                    "Selecione alguma linha para a eliminar.",
                )
                return

            items = self.list.selectedItems()
            for item in items:
                id = item.data(Qt.ItemDataRole.UserRole)
                query.bindValue(0, id)

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

        except Exception as e:
            db.rollback()
            QMessageBox.critical(
                None, "Operacao nao concluida", f"Insercao cancelada: {str(e)}"
            )

        finally:
            self.table.load()
            self.list.load()
            self.data_changed.emit()

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
        return map[self.TABLE_NAME]["columns"]
