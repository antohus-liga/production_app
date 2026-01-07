from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtSql import QSqlQuery
from data_container import DataContainer


class ListWidget(QListWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.TABLE_NAME = self.master.TABLE_NAME

        self.load_data()

    def load_data(self):
        self.clear()

        query = QSqlQuery()
        query.exec(f"SELECT * FROM {self.TABLE_NAME}")
        while query.next():
            item = QListWidgetItem(self)
            container = DataContainer(
                self, [str(query.value(i)) for i in range(query.record().count())]
            )

            item.setSizeHint(container.sizeHint())
            self.setItemWidget(item, container)
