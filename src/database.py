import sqlite3
from datetime import date
from pathlib import Path
from typing import Any


class BancoDeDados:
    def __init__(self) -> None:
        banco = Path(__file__).parent.parent / "barbearia.sqlite"
        self.conn = sqlite3.connect(banco)
        self.cur = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self) -> None:
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT UNIQUE NOT NULL
            )
        """,
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                preco REAL NOT NULL
            )
        """,
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS atendimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                servico_id INTEGER NOT NULL,
                data TEXT,
                duracao TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (servico_id) REFERENCES servicos (id)
            )
            """,
        )
        self.conn.commit()

    def adicionar_cliente(self, nome: str, telefone: str) -> None:
        self.cur.execute(
            "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
            (nome, telefone),
        )
        self.conn.commit()

    def adicionar_servico(
        self,
        nome: str,
        preco: float,
    ) -> None:
        self.cur.execute(
            """
            INSERT INTO servicos (nome, preco) VALUES (?, ?)
            """,
            (nome, preco),
        )
        self.conn.commit()

    def adicionar_atendimento(
        self,
        cliente_id: int,
        servico_id: int,
        data: date,
        duracao: str,
    ) -> None:
        self.cur.execute(
            """
            INSERT INTO atendimentos (cliente_id, servico_id, data, duracao)
            VALUES (?, ?, ?, ?)
            """,
            (cliente_id, servico_id, data, duracao),
        )
        self.conn.commit()

    def obter_clientes(self) -> list[tuple[Any, ...]]:
        self.cur.execute("SELECT * FROM clientes")
        return self.cur.fetchall()

    def obter_servicos(self) -> list[tuple[Any, ...]]:
        self.cur.execute("SELECT * FROM servicos")
        return self.cur.fetchall()

    def obter_atendimentos(self) -> list[tuple[Any, ...]]:
        self.cur.execute(
            """
            SELECT atendimentos.id, clientes.nome, servicos.nome, atendimentos.data, atendimentos.duracao
            FROM atendimentos
            INNER JOIN clientes ON atendimentos.cliente_id = clientes.id
            INNER JOIN servicos ON atendimentos.servico_id = servicos.id
            """,
        )
        return self.cur.fetchall()

    def editar_cliente(
        self,
        _id: int,
        nome: str,
        telefone: str,
    ) -> None:
        self.cur.execute(
            """
            UPDATE clientes
            SET nome = ?, telefone = ?
            WHERE id = ?
            """,
            (nome, telefone, _id),
        )
        self.conn.commit()

    def editar_servico(
        self,
        _id: int,
        nome: str,
        preco: float,
    ) -> None:
        self.cur.execute(
            """
            UPDATE servicos
            SET nome = ?, preco = ?
            WHERE id = ?
            """,
            (nome, preco, _id),
        )
        self.conn.commit()

    def editar_atendimento(
        self,
        _id: int,
        cliente_id: int,
        servico_id: int,
        data: date,
        duracao: int,
    ) -> None:
        self.cur.execute(
            """
            UPDATE atendimentos
            SET cliente_id = ?, servico_id = ?, data = ?, duracao = ?
            WHERE id = ?
            """,
            (cliente_id, servico_id, data, duracao, _id),
        )
        self.conn.commit()

    def remover_cliente(self, _id: int) -> None:
        self.cur.execute("DELETE FROM clientes WHERE id = ?", (_id,))
        self.conn.commit()

    def remover_servico(self, _id: int) -> None:
        self.cur.execute("DELETE FROM servicos WHERE id = ?", (_id,))
        self.conn.commit()

    def remover_atendimento(self, _id: int) -> None:
        self.cur.execute("DELETE FROM atendimentos WHERE id = ?", (_id,))
        self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()
        self.cur.close()
