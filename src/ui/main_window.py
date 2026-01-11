import json
from PySide6.QtWidgets import QMainWindow, QTabWidget

from ui.display_widget import DisplayWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Produção v2")

        self.db_table_names = []
        with open("src/table_info.json") as f:
            table_info = json.load(f)
            self.db_table_names = table_info.keys()
            self.table_names = [
                table_info[name]["table_name"] for name in self.db_table_names
            ]

        self.tabs = QTabWidget()
        self.display_widgets: list[DisplayWidget] = [
            DisplayWidget(table_name) for table_name in self.db_table_names
        ]

        for i in range(len(self.display_widgets)):
            self.tabs.addTab(self.display_widgets[i], self.table_names[i])

        self.setCentralWidget(self.tabs)
