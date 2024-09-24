from classes.base import TelaBase
from src.database import BancoDeDados


class TelaServicos(TelaBase):
    def __init__(self, banco: BancoDeDados) -> None:
        super().__init__(banco, "Serviços", "img/corte.ico", ["ID", "Nome", "Preço"])
        self.carregar()

    def carregar(self) -> None:
        servicos = self.banco.obter_servicos()
        self._carregar_dados(servicos)

    def adicionar(self) -> None:
        self._adicionar_item(
            "Adicionar Serviço",
            "Nome:",
            "Preço:",
            self.banco.adicionar_servico,
        )

    def editar(self) -> None:
        self._editar_item(
            "Editar Serviço",
            "Nome:",
            "Preço:",
            lambda nome, preco: self.banco.editar_servico(
                self._obter_id(),
                nome,
                float(preco),
            ),
        )

    def remover(self) -> None:
        self._remover_item("serviço", self.banco.remover_servico)
