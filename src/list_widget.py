from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PySide6.QtSql import QSqlQuery
from data_container import DataContainer


class ListWidget(QListWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.TABLE_NAME = self.master.TABLE_NAME

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.load_data()

    def load_data(self):
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
