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

        self.data = data
        self.master_layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.grid_layout = QGridLayout()

        if self.master.TABLE_NAME in ("suppliers", "clients"):
            self.code = QLabel(f"#{data[1]}")
            self.code.setStyleSheet(
                """
                color: gray
            """
            )

            self.name = QLabel(f"{data[2]} {data[3]}")

        self.sep = QFrame()
        self.sep.setFrameShape(QFrame.HLine)
        self.sep.setFrameShadow(QFrame.Sunken)

        self.header_layout.addWidget(self.code)
        self.header_layout.addWidget(self.name)

        row = 0
        col = 0
        for i in range(4, len(self.data)):
            self.grid_layout.addWidget(QLabel(data[i]), row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.master_layout.addLayout(self.header_layout)
        self.master_layout.addWidget(self.sep)
        self.master_layout.addLayout(self.grid_layout)
        self.setLayout(self.master_layout)
