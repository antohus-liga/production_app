from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QMessageBox,
)
from PySide6.QtSql import QSqlQuery
from inputs_container import InputsContainer
from list_widget import ListWidget
from table_widget import TableWidget


class DisplayWidget(QWidget):
    def __init__(self, table_name):
        super().__init__()

        self.TABLE_NAME = table_name

        self.column_info = self.get_column_names()
        self.COLUMN_NAMES = list(self.column_info.keys())

        self.table = TableWidget(self)
        self.list = ListWidget(self)
        self.inputs = InputsContainer(self)

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.insert_values)

        self.master_layout = QVBoxLayout()

        self.master_layout.addWidget(self.inputs)
        self.master_layout.addWidget(self.add_btn)

        self.master_layout.addWidget(self.table)
        self.master_layout.addWidget(self.list)

        self.setLayout(self.master_layout)

        self.table.load_table()

    def insert_values(self):
        self.inputs.insert_data()
        self.table.load_table()
        self.list.load_data()

    # df - defaulted
    # le - line edit
    # cb - combo box
    # de - date edit
    def get_column_names(self):
        map = {
            "clients": {
                "ID": "df",
                "Code": "le",
                "First Name": "le",
                "Last Name": "le",
                "Type": "cb",
                "Company Name": "le",
                "Country": "le",
                "City": "le",
                "Phone": "le",
                "Email": "le",
                "Date of Birth": "de",
                "NIF": "le",
                "Created at": "df",
                "Updated at": "df",
            },
            "suppliers": {
                "ID": "df",
                "Code": "le",
                "First Name": "le",
                "Last Name": "le",
                "Type": "cb",
                "Company Name": "le",
                "Country": "le",
                "City": "le",
                "Phone": "le",
                "Email": "le",
                "Date of Birth": "de",
                "NIF": "le",
                "Created at": "df",
                "Updated at": "df",
            },
            "materials": {
                "ID": "df",
                "Code": "le",
                "Name": "le",
                "Category": "cb",
                "Quantity": "df",
                "Base unit": "cb",
                "Unit price": "le",
                "Status": "cb",
                "Created at": "df",
                "Updated at": "df",
            },
            "products": {
                "ID": "df",
                "Code": "le",
                "Name": "le",
                "Category": "cb",
                "Quantity": "df",
                "Base unit": "cb",
                "Unit price": "le",
                "Production cost": "df",
                "Created at": "df",
                "Updated at": "df",
            },
            "movements_in": {
                "Number": "df",
                "Material": "cb",
                "Supplier": "cb",
                "Quantity": "le",
                "Total price": "df",
                "Created at": "df",
                "Updated at": "df",
            },
            "movements_out": {
                "Number": "df",
                "Product": "cb",
                "Supplier": "cb",
                "Quantity": "le",
                "Total price": "df",
                "Created at": "df",
                "Updated at": "df",
            },
            "production_line": {
                "Number": "df",
                "Product": "cb",
                "Quantity": "le",
                "Total cost": "df",
                "Created at": "df",
                "Updated at": "df",
            },
        }
        return map[self.TABLE_NAME]
