from datetime import datetime, time

from pydantic import BaseModel, PositiveInt


class Cliente(BaseModel):
    id: None = None
    nome: str
    telefone: str | None = None


class Servico(BaseModel):
    id: None = None
    nome: str
    preco: float


class Atendimento(BaseModel):
    id: None = None
    cliente_id: PositiveInt
    servico_id: PositiveInt
    data_hora: datetime | None = None
    duracao: time | None = None
