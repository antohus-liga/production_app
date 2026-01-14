import json
from PySide6.QtWidgets import QMainWindow, QTabWidget

from ui.display_widget import DisplayWidget
from ui.prod_mat_widget import ProdMatWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Produção v2")

        self.db_table_names = []
        with open("src/table_info.json") as f:
            table_info = json.load(f)
            self.db_table_names = list(table_info.keys())
            self.table_names = [
                table_info[name]["table_name"] for name in self.db_table_names
            ]
        self.db_table_names.pop()

        self.tabs = QTabWidget()
        self.display_widgets: list[DisplayWidget] = [
            DisplayWidget(table_name) for table_name in self.db_table_names
        ]
        self.prod_mat_widget = ProdMatWidget()

        for i in range(len(self.display_widgets)):
            self.tabs.addTab(self.display_widgets[i], self.table_names[i])
        self.tabs.addTab(self.prod_mat_widget, self.table_names[-1])

        self.display_widgets[0].data_changed.connect(
            self.display_widgets[5].inputs.update_combos
        )
        self.display_widgets[1].data_changed.connect(
            self.display_widgets[4].inputs.update_combos
        )
        self.display_widgets[2].data_changed.connect(self.on_materials_update)
        self.display_widgets[3].data_changed.connect(self.on_products_update)
        self.display_widgets[4].data_changed.connect(self.on_movements_in_update)
        self.display_widgets[5].data_changed.connect(self.on_movements_out_update)
        self.display_widgets[6].data_changed.connect(self.on_production_line_update)
        self.prod_mat_widget.data_changed.connect(self.on_product_materials_update)
        self.setCentralWidget(self.tabs)

    def on_products_update(self):
        self.display_widgets[5].inputs.update_combos()
        self.display_widgets[6].inputs.update_combos()
        self.prod_mat_widget.inputs.update_combos()

        self.display_widgets[5].update_views()
        self.display_widgets[6].update_views()

    def on_materials_update(self):
        self.display_widgets[4].inputs.update_combos()
        self.prod_mat_widget.inputs.update_combos()

        self.display_widgets[3].update_views()
        self.display_widgets[4].update_views()
        self.display_widgets[6].update_views()

    def on_movements_in_update(self):
        self.display_widgets[2].update_views()

    def on_movements_out_update(self):
        self.display_widgets[3].update_views()

    def on_production_line_update(self):
        self.display_widgets[2].update_views()
        self.display_widgets[3].update_views()

    def on_product_materials_update(self):
        self.display_widgets[2].update_views()
        self.display_widgets[3].update_views()
        self.display_widgets[6].update_views()
