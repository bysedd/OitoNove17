import logging
from collections.abc import Callable, Iterable
from typing import Any

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.database import BancoDeDados


class TelaBase(QWidget):
    def __init__(
        self,
        banco: BancoDeDados,
        titulo: str,
        icone: str,
        colunas: list[str],
    ) -> None:
        super().__init__()

        self.log = logging
        self.log.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
        )

        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon(icone))
        self.setWindowTitle(titulo)

        self.banco = banco

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(len(colunas))
        self.tabela.setHorizontalHeaderLabels(colunas)

        header = self.tabela.horizontalHeader()
        header.setStyleSheet(
            "QHeaderView::section { background-color: #4CAF50; color: white; }",
        )
        header.setStretchLastSection(True)

        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_editar = QPushButton("Editar")
        self.btn_remover = QPushButton("Remover")

        # Aplicar estilo aos botões
        for btn in (self.btn_adicionar, self.btn_editar, self.btn_remover):
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #f0f0f0;
                    color: black;
                    padding: 10px;
                    border: 1px solid #dcdcdc;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
                """,
            )

        layout_principal = QVBoxLayout()
        layout_botao = QHBoxLayout()

        layout_botao.addWidget(self.btn_adicionar)
        layout_botao.addWidget(self.btn_editar)
        layout_botao.addWidget(self.btn_remover)

        layout_principal.addWidget(self.tabela)
        layout_principal.addLayout(layout_botao)

        self.setLayout(layout_principal)

        self.btn_adicionar.clicked.connect(self.adicionar)
        self.btn_editar.clicked.connect(self.editar)
        self.btn_remover.clicked.connect(self.remover)

    def carregar(self) -> None:
        pass

    def adicionar(self) -> None:
        pass

    def editar(self) -> None:
        pass

    def remover(self) -> None:
        pass

    def _confirmar_remocao(self, msg: str) -> bool:
        reply = QMessageBox.question(
            self,
            "Confirmar Remoção",
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

    def _obter_dados_da_linha(self, row: int) -> tuple[Any, ...]:
        nome = self.tabela.item(row, 1).text()
        valor = self.tabela.item(row, 2).text()
        return nome, valor

    def _carregar_dados(self, dados: Iterable[Any]) -> None:
        self.tabela.setRowCount(0)
        for item in dados:
            self._adicionar_linha(item)

    def _adicionar_item(
        self,
        title: str,
        label1: str,
        label2: str,
        action: Callable[[str, Any], None],
    ) -> None:
        nome, ok1 = QInputDialog.getText(self, title, label1)
        if not ok1 and not nome:
            return

        segundo_input, ok2 = QInputDialog.getText(
            self,
            title,
            label2,
        )
        if ok2 and segundo_input:
            action(nome, segundo_input)
            self.carregar()

    def _validar_linha(self, linha: int) -> bool:
        if linha < 0:
            QMessageBox.warning(
                self,
                "Erro",
                "Selecione alguma linha primeiro.",
            )
            return False
        return True

    def _editar_item(
        self,
        title: str,
        label1: str,
        label2: str,
        action: Callable[[str, Any], None],
    ) -> None:
        linha = self.tabela.currentRow()
        if not self._validar_linha(linha):
            return

        dados_linha = self._obter_dados_da_linha(linha)
        nome, ok1 = QInputDialog.getText(self, title, label1, text=dados_linha[0])
        if not ok1 and not nome:
            return

        segundo_input, ok2 = QInputDialog.getText(
            self,
            title,
            label2,
            text=dados_linha[1],
        )
        if ok2 and segundo_input:
            action(nome, segundo_input)
            self.carregar()

    def _remover_item(self, tipo: str, remover_funcao: Callable[[int], None]) -> None:
        linha = self.tabela.currentRow()
        try:
            nome_item = self.tabela.item(linha, 1).text()
            if self._confirmar_remocao(
                f"Você realmente deseja remover o {tipo}: {nome_item}?",
            ):
                remover_funcao(self._obter_id())
                self.carregar()
        except AttributeError:
            self.log.warning("Selecione uma linha para remover.")

    def _adicionar_linha(self, cliente: tuple[Any, ...]) -> None:
        posicao_linha = self.tabela.rowCount()
        self.tabela.insertRow(posicao_linha)
        for i, item in enumerate(cliente):
            self.tabela.setItem(posicao_linha, i, QTableWidgetItem(str(item)))

    def _obter_id(self) -> int:
        linha = self.tabela.currentRow()
        _id = self.tabela.item(linha, 0).text()
        return int(_id)
