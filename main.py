import sys

from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

style = """
QWidget {
    background-color: white;
    color: black;
}

QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #dcdcdc;
    padding: 5px;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #e6e6e6;
}

QTableWidget {
    background-color: white;
    gridline-color: #dcdcdc;
    border: 1px solid #dcdcdc;
}

QHeaderView::section {
    background-color: #f0f0f0;
    color: black;
    border: 1px solid #dcdcdc;
    padding: 5px;
}
"""
app.setStyleSheet(style)

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.classes.atendimentos import TelaAtendimentos
from src.classes.clientes import TelaClientes
from src.classes.servicos import TelaServicos
from src.database import BancoDeDados


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.banco = BancoDeDados()
        self.clientes = TelaClientes(self.banco)
        self.servicos = TelaServicos(self.banco)
        self.atendimentos = TelaAtendimentos(self.banco)

        self.setFixedSize(400, 200)
        self.setWindowIcon(QIcon("img/barber.ico"))
        self.setWindowTitle("Barbearia Oito Nove 17")

        btn_clientes = QPushButton("Clientes")
        btn_clientes.setFixedSize(380, 40)

        btn_servicos = QPushButton("Serviços")
        btn_servicos.setFixedSize(380, 40)

        btn_atendimentos = QPushButton("Atendimentos")
        btn_atendimentos.setFixedSize(380, 40)

        btn_clientes.clicked.connect(self.abrir_tela_clientes)
        btn_servicos.clicked.connect(self.abrir_tela_servicos)
        btn_atendimentos.clicked.connect(self.abrir_tela_atendimentos)

        layout = QVBoxLayout()
        layout.addWidget(btn_clientes)
        layout.addWidget(btn_servicos)
        layout.addWidget(btn_atendimentos)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def abrir_tela_clientes(self) -> None:
        self.clientes.show()

    def abrir_tela_servicos(self) -> None:
        self.servicos.show()

    def abrir_tela_atendimentos(self) -> None:
        self.atendimentos.show()


if __name__ == "__main__":
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
