from datetime import date
from typing import Any

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QInputDialog,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from classes.base import TelaBase
from src.database import BancoDeDados


class TelaAtendimentos(TelaBase):
    def __init__(self, banco: BancoDeDados) -> None:
        super().__init__(
            banco,
            "Atendimentos",
            "img/atendimento.ico",
            ["ID", "Cliente", "Serviço", "Data", "Duração"],
        )

        self.carregar()

    def carregar(self) -> None:
        atendimentos = self.banco.obter_atendimentos()
        atendimentos_formatados = [
            (
                atendimento[0],
                atendimento[1],
                atendimento[2],
                date.fromisoformat(atendimento[3]).strftime("%d/%m/%Y"),
                atendimento[4],
            )
            for atendimento in atendimentos
        ]
        self._carregar_dados(atendimentos_formatados)

    def adicionar(self) -> None:
        clientes = self.banco.obter_clientes()
        cliente_id, cliente_nome = self._selecionar_item(
            "Selecionar Cliente",
            "Escolha um cliente:",
            clientes,
        )
        if not cliente_id or not cliente_nome:
            return

        servicos = self.banco.obter_servicos()
        servico_id, servico_nome = self._selecionar_item(
            "Selecionar Serviço",
            "Escolha um serviço:",
            servicos,
        )
        if not servico_id or not servico_nome:
            return

        data = self._obter_data()
        if data is None:
            return

        duracao, ok = QInputDialog.getText(
            self,
            "Adicionar Atendimento",
            "Duração (minutos):",
        )
        if not ok or not duracao:
            return

        resumo = self._resumo(
            cliente_nome,
            servico_nome,
            data.strftime("%d/%m/%Y"),
            duracao,
        )
        reply = QMessageBox.question(
            self,
            "Confirmar Atendimento",
            resumo,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.banco.adicionar_atendimento(
                cliente_id,
                servico_id,
                data,
                duracao,
            )
            self.carregar()

    def editar(self) -> None:
        linha = self.tabela.currentRow()
        if not self._validar_linha(linha):
            return

        cliente = self.tabela.item(linha, 1).text()
        servico = self.tabela.item(linha, 2).text()
        data_str: list[str] = self.tabela.item(linha, 3).text().split("/")
        data = date(
            day=int(data_str[0]),
            month=int(data_str[1]),
            year=int(data_str[2]),
        )
        duracao = int(self.tabela.item(linha, 4).text())
        self._editar_atendimento(
            cliente,
            servico,
            data,
            duracao,
        )

    def _editar_atendimento(
        self,
        cliente: str,
        servico: str,
        data: date,
        duracao: int,
    ) -> None:
        clientes = self.banco.obter_clientes()
        cliente_id, cliente_nome = self._selecionar_item(
            "Selecionar Cliente",
            "Escolha um cliente:",
            clientes,
            item_selecionado=cliente,
        )
        if not cliente_id or not cliente_nome:
            return

        servicos = self.banco.obter_servicos()
        servico_id, servico_nome = self._selecionar_item(
            "Selecionar Serviço",
            "Escolha um serviço:",
            servicos,
            item_selecionado=servico,
        )
        if not servico_id or not servico_nome:
            return

        data_dialog = DataDialog(self)
        data_dialog.date_edit.setDate(
            QDate(data.year, data.month, data.day),
        )
        if data_dialog.exec() == QDialog.DialogCode.Accepted:
            data = data_dialog.get_date()
        else:
            return

        duracao_str, ok = QInputDialog.getText(
            self,
            "Editar Atendimento",
            "Duração (minutos):",
            text=str(duracao),
        )
        if not ok or not duracao_str:
            return

        resumo = self._resumo(
            cliente_nome,
            servico_nome,
            data.strftime("%d/%m/%Y"),
            duracao_str,
        )
        reply = QMessageBox.question(
            self,
            "Confirmar Edição",
            resumo,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.banco.editar_atendimento(
                self._obter_id(),
                cliente_id,
                servico_id,
                data,
                int(duracao_str),
            )
            self.carregar()

    def remover(self) -> None:
        linha = self.tabela.currentRow()
        if not self._validar_linha(linha):
            return

        resumo = self._resumo(
            cliente=self.tabela.item(linha, 1).text(),
            servico=self.tabela.item(linha, 2).text(),
            data_str=self.tabela.item(linha, 3).text(),
            duracao=self.tabela.item(linha, 4).text(),
        )

        reply = QMessageBox.question(
            self,
            "Confirmar Remoção",
            f"Deseja realmente remover o seguinte atendimento?\n\n{resumo}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            atendimento_id = self._obter_id()
            self.banco.remover_atendimento(atendimento_id)
            self.carregar()

    @staticmethod
    def _resumo(
        cliente: str,
        servico: str,
        data_str: str,
        duracao: str,
    ) -> str:
        return (
            f"Cliente: {cliente}\n"
            f"Serviço: {servico}\n"
            f"Data: {data_str}\n"
            f"Duração: {duracao} minutos"
        )

    def _selecionar_item(
        self,
        titulo: str,
        label: str,
        dados: list[tuple[Any, ...]],
        item_selecionado: str | None = None,
    ) -> tuple[int | None, str | None]:
        nomes = [item[1] for item in dados]
        indice = nomes.index(item_selecionado) if item_selecionado in nomes else -1

        indice_atual = indice if indice != -1 else 0

        elemento, ok = QInputDialog.getItem(
            self,
            titulo,
            label,
            nomes,
            current=indice_atual,
            editable=False,
        )
        if not ok or not elemento:
            return None, None

        id_selecionado = next((item[0] for item in dados if item[1] == elemento), None)
        return id_selecionado, elemento

    def _obter_data(self) -> date | None:
        data_dialog = DataDialog(self)
        if data_dialog.exec() == QDialog.DialogCode.Accepted:
            return data_dialog.get_date()
        return None


class DataDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Selecionar Data")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.date_edit)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_date(self) -> date:
        q_date = self.date_edit.date()
        return date(q_date.year(), q_date.month(), q_date.day())
