from classes.base import TelaBase
from src.database import BancoDeDados


class TelaClientes(TelaBase):
    def __init__(self, banco: BancoDeDados) -> None:
        super().__init__(
            banco,
            "Clientes",
            "img/pessoa.ico",
            ["ID", "Nome", "Telefone"],
        )
        self.carregar()

    def carregar(self) -> None:
        clientes = self.banco.obter_clientes()
        self._carregar_dados(clientes)

    def adicionar(self) -> None:
        self._adicionar_item(
            "Adicionar Cliente",
            "Nome:",
            "Telefone:",
            self.banco.adicionar_cliente,
        )

    def editar(self) -> None:
        self._editar_item(
            "Editar Cliente",
            "Nome:",
            "Telefone:",
            lambda nome, telefone: self.banco.editar_cliente(
                self._obter_id(),
                nome,
                telefone,
            ),
        )

    def remover(self) -> None:
        self._remover_item("cliente", self.banco.remover_cliente)
