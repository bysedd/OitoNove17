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
        # Formatando a data para exibição
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
        # Selecionar cliente
        clientes = self.banco.obter_clientes()
        cliente_id, cliente_nome = self._selecionar_item(
            "Selecionar Cliente",
            "Escolha um cliente:",
            clientes,
        )
        if cliente_id is None:
            return

        # Selecionar serviço
        servicos = self.banco.obter_servicos()
        servico_id, servico_nome = self._selecionar_item(
            "Selecionar Serviço",
            "Escolha um serviço:",
            servicos,
        )
        if servico_id is None:
            return

        # Obter data usando o método protegido
        data = self._obter_data()
        if data is None:
            return

        # Obter duração
        duracao, ok = QInputDialog.getText(
            self,
            "Adicionar Atendimento",
            "Duração (minutos):",
        )
        if not ok or not duracao:
            return

        # Confirmar antes de adicionar
        resumo = (
            f"Cliente: {cliente_nome}\n"
            f"Serviço: {servico_nome}\n"
            f"Data: {data.strftime('%d/%m/%Y')}\n"
            f"Duração: {duracao} minutos"
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
        # Implementar lógica semelhante ao adicionar, mas para editar um atendimento existente
        pass

    def remover(self) -> None:
        # Implementar lógica para remover um atendimento
        pass

    def _selecionar_item(
        self,
        titulo: str,
        label: str,
        dados: list[tuple[Any, ...]],
    ) -> tuple[int | None, str | None]:
        nomes = [item[1] for item in dados]
        nome_selecionado, ok = QInputDialog.getItem(
            self,
            titulo,
            label,
            nomes,
            editable=False,
        )
        if not ok or not nome_selecionado:
            return None, None

        id_selecionado = next(
            (item[0] for item in dados if item[1] == nome_selecionado),
            None,
        )
        return id_selecionado, nome_selecionado

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
