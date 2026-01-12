from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(("Name", "Quantity"))
        self.setColumnWidth(0, 500)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.load()

    def load(self):
        self.clear()

        query = QSqlQuery()
        query.exec(
            f"SELECT pro_code, mat_code, quantity FROM product_materials ORDER BY pro_code"
        )

        items = []
        current_product = None
        item = QTreeWidgetItem()

        while query.next():
            product = query.value(0)
            material = query.value(1)
            quantity = str(query.value(2))

            if product != current_product:
                if item.childCount() > 0:
                    items.append(item)

                current_product = product
                item = QTreeWidgetItem([product])

            item.addChild(QTreeWidgetItem([material, quantity]))

        # append last item
        if item is not None:
            items.append(item)

        self.insertTopLevelItems(0, items)
