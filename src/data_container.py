from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
)


class DataContainer(QWidget):
    def __init__(self, master, data):
        super().__init__()
        self.master = master

        self.setObjectName("DataContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        self.data = data
        self.master_layout = QVBoxLayout()

        self.header_layout = QHBoxLayout()
        self.data_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()

        self.name = ""
        self.data_dict = {
            "General": [],
            "Location": [],
            "Contact": [],
            "Extra": [],
            "Log": [],
        }

        for i, col in enumerate(self.master.master.COLUMN_NAMES):
            info_type = self.master.master.column_info[col]["info_type"]

            match info_type:
                case "header":
                    header = QLabel(f"#{data[i]}")
                    header.setStyleSheet("QLabel {color: gray; font: bold 14px}")
                    self.header_layout.addWidget(header)
                case "name":
                    self.name += f"{data[i]} "
                case "internal":
                    continue
                case _:
                    self.data_dict[info_type.capitalize()].append((col, data[i]))

        name_label = QLabel(self.name.strip())
        name_label.setStyleSheet("QLabel {font: bold 14px}")
        self.header_layout.addWidget(name_label)
        self.header_layout.setStretch(0, 1)
        self.header_layout.setStretch(1, 5)

        self.sep = QFrame()
        self.sep.setFrameShape(QFrame.Shape.HLine)
        self.sep.setFrameShadow(QFrame.Shadow.Sunken)
        self.sep.setObjectName("Separator")

        self.containers: list[QGridLayout] = []
        grid_row = 0
        grid_col = 0
        for info_type in self.data_dict.keys():
            if len(self.data_dict[info_type]) <= 0:
                continue

            self.containers.append(QGridLayout())
            self.containers[-1].setColumnStretch(0, 1)
            self.containers[-1].setColumnStretch(1, 6)
            self.containers[-1].addWidget(
                QLabel(info_type), 0, 0, 1, 2, Qt.AlignmentFlag.AlignLeft
            )
            container_row = 1
            for col_name, col_data in self.data_dict[info_type]:
                self.containers[-1].addWidget(
                    QLabel(f"{col_name} : {col_data}"),
                    container_row,
                    1,
                    Qt.AlignmentFlag.AlignLeft,
                )
                container_row += 1

            self.grid_layout.addLayout(self.containers[-1], grid_row, grid_col)
            grid_col += 1
            if grid_col >= 3:
                grid_col = 0
                grid_row += 1

        self.master_layout.addLayout(self.header_layout)
        self.master_layout.addWidget(self.sep)
        self.master_layout.addLayout(self.grid_layout)
        self.setLayout(self.master_layout)
