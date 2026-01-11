from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem
from PySide6.QtSql import QSqlQuery

from ui.containers.popup_container import PopupContainer


class TableWidget(QTableWidget):
    updated = Signal()

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.COLUMN_NAMES = self.master.COLUMN_NAMES
        self.TABLE_NAME = self.master.TABLE_NAME
        self.column_info = self.master.column_info

        self.setColumnCount(len(self.COLUMN_NAMES))
        self.setHorizontalHeaderLabels(self.COLUMN_NAMES)
        self.horizontalHeader().setSectionsClickable(True)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_popup)

    def load(self):
        self.setRowCount(0)

        query = QSqlQuery()
        query.exec(f"SELECT * FROM {self.master.TABLE_NAME}")
        row = 0
        while query.next():
            self.insertRow(row)
            for col in range(query.record().count()):
                self.setItem(row, col, QTableWidgetItem(str(query.value(col))))

            row += 1
        self.resizeColumnsToContents()

    def show_popup(self, pos):
        row = self.rowAt(pos.y())
        if row < 0:
            return

        global_pos = self.viewport().mapToGlobal(pos)

        self.popup = PopupContainer(self, row=row)
        self.popup.move(global_pos)
        self.popup.updated.connect(lambda: self.updated.emit())

        self.popup.show()
