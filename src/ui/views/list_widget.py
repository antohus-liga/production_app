from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PySide6.QtSql import QSqlQuery

from ui.containers.data_container import DataContainer
from ui.containers.popup_container import PopupContainer


class ListWidget(QListWidget):
    updated = Signal()

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.TABLE_NAME = self.master.TABLE_NAME
        self.COLUMN_NAMES = self.master.COLUMN_NAMES
        self.column_info = self.master.column_info

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_popup)

        self.load()

    def load(self):
        self.clear()

        query = QSqlQuery()
        query.exec(f"SELECT * FROM {self.TABLE_NAME}")
        while query.next():
            values = [str(query.value(i)) for i in range(query.record().count())]
            item = QListWidgetItem(self)
            item.setData(Qt.ItemDataRole.UserRole, values[0])
            container = DataContainer(self, values)

            item.setSizeHint(container.sizeHint())
            self.setItemWidget(item, container)

    def show_popup(self, pos):
        item = self.itemAt(pos)
        if not item:
            return

        global_pos = self.viewport().mapToGlobal(pos)

        self.popup = PopupContainer(self, item=item)
        self.popup.move(global_pos)
        self.popup.updated.connect(lambda: self.updated.emit())

        self.popup.show()
