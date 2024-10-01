from __future__ import annotations

from typing import TYPE_CHECKING, Any

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

if TYPE_CHECKING:
    from src.database import BancoDeDados

Builder.load_string("""
<ContentAddAtendimento>:
    orientation: "vertical"
    spacing: dp(20)
    size_hint_y: None
    height: self.minimum_height + dp(50)

    MDLabel:
        text: "Cliente"
        size_hint_y: None
        height: dp(20)

    MDDropDownItem:
        id: cliente
        text: "Selecione o Cliente"
        on_release: root.cliente_dropdown.open()

    MDLabel:
        text: "Serviço"
        size_hint_y: None
        height: dp(20)

    MDDropDownItem:
        id: servico
        text: "Selecione o Serviço"
        on_release: root.servico_dropdown.open()

    MDTextField:
        id: data
        hint_text: "Data (dd/mm/yyyy)"
        required: True
        size_hint_y: None
        height: dp(60)

    MDTextField:
        id: duracao
        hint_text: "Duração (minutos)"
        required: True
        size_hint_y: None
        height: dp(60)
        input_filter: "int"
<ContentEditAtendimento>:
    orientation: "vertical"
    spacing: dp(20)
    size_hint_y: None
    height: self.minimum_height + dp(50)

    MDLabel:
        text: "Cliente"
        size_hint_y: None
        height: dp(20)

    MDDropDownItem:
        id: cliente
        text: "Selecione o Cliente"
        on_release: root.cliente_dropdown.open()

    MDLabel:
        text: "Serviço"
        size_hint_y: None
        height: dp(20)

    MDDropDownItem:
        id: servico
        text: "Selecione o Serviço"
        on_release: root.servico_dropdown.open()

    MDTextField:
        id: data
        hint_text: "Data (dd/mm/yyyy)"
        required: True
        size_hint_y: None
        height: dp(60)

    MDTextField:
        id: duracao
        hint_text: "Duração (minutos)"
        required: True
        size_hint_y: None
        height: dp(60)
        input_filter: "int"
""")


class TelaAtendimentos(MDScreen):
    def __init__(self, banco: BancoDeDados, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = "tela_atendimentos"
        self.banco = banco
        self.selected_row = None

        layout = BoxLayout(orientation="vertical")

        self.column_data = [
            ("ID", dp(30)),
            ("Cliente", dp(40)),
            ("Serviço", dp(40)),
            ("Data", dp(30)),
            ("Duração", dp(30)),
        ]

        self.data_tables = MDDataTable(
            size_hint=(1, 0.9),
            use_pagination=False,
            check=False,
            column_data=self.column_data,
            row_data=[],
        )

        self.data_tables.bind(on_row_press=self.on_row_press)

        layout.add_widget(self.data_tables)
        self.add_action_buttons(layout)
        self.add_widget(layout)
        self.carregar()

    def add_action_buttons(self, layout: BoxLayout) -> None:
        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(5),  # Espaçamento opcional entre os botões
            padding=[dp(10), dp(5), dp(10), dp(5)],  # Padding opcional
        )

        btn_voltar = MDFlatButton(
            text="Voltar",
            on_release=self.voltar_menu,
            size_hint_x=1,  # Cada botão terá a mesma proporção de largura
        )
        btn_adicionar = MDFlatButton(
            text="Adicionar",
            on_release=self.adicionar,
            size_hint_x=1,
        )
        btn_editar = MDFlatButton(text="Editar", on_release=self.editar, size_hint_x=1)
        btn_remover = MDFlatButton(
            text="Remover",
            on_release=self.remover,
            size_hint_x=1,
        )

        button_layout.add_widget(btn_voltar)
        button_layout.add_widget(btn_adicionar)
        button_layout.add_widget(btn_editar)
        button_layout.add_widget(btn_remover)

        layout.add_widget(button_layout)

    def voltar_menu(self, *_: Any) -> None:
        self.manager.current = "main_menu"

    def carregar(self) -> None:
        atendimentos = self.banco.obter_atendimentos()
        self.data_tables.row_data = [
            (
                str(atendimento[0]),
                atendimento[1],
                atendimento[2],
                atendimento[3],
                str(atendimento[4]),
            )
            for atendimento in atendimentos
        ]

    def adicionar(self, *_: Any) -> None:
        clientes = self.banco.obter_clientes()
        servicos = self.banco.obter_servicos()

        self.dialog = MDDialog(
            title="Adicionar Atendimento",
            type="custom",
            content_cls=ContentAddAtendimento(clientes, servicos),
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=self.fechar_dialog),
                MDFlatButton(text="SALVAR", on_release=self.salvar_atendimento),
            ],
            auto_dismiss=False,
            size_hint=(0.8, None),
            height=dp(500),
        )
        self.dialog.open()

    def salvar_atendimento(self, *_: Any) -> None:
        cliente_nome = self.dialog.content_cls.ids.cliente.text
        servico_nome = self.dialog.content_cls.ids.servico.text
        data_atendimento = self.dialog.content_cls.ids.data.text.strip()
        duracao = self.dialog.content_cls.ids.duracao.text.strip()

        if (
            all([cliente_nome, servico_nome, data_atendimento, duracao])
            and cliente_nome != "Selecione o Cliente"
            and servico_nome != "Selecione o Serviço"
        ):
            cliente_id = self.banco.obter_cliente_id_por_nome(cliente_nome)
            servico_id = self.banco.obter_servico_id_por_nome(servico_nome)
            if cliente_id and servico_id:
                self.banco.adicionar_atendimento(
                    cliente_id,
                    servico_id,
                    data_atendimento,
                    duracao,
                )
                self.carregar()
                self.dialog.dismiss()

    def fechar_dialog(self, *_: Any) -> None:
        self.dialog.dismiss()

    def editar(self, *_: Any) -> None:
        if not self.selected_row:
            # Exibir mensagem indicando que nenhuma linha foi selecionada
            return

        clientes = self.banco.obter_clientes()
        servicos = self.banco.obter_servicos()
        row_data = self.selected_row
        _id = int(row_data[0])
        data = row_data[3]
        duracao = row_data[4]

        self.dialog = MDDialog(
            title="Editar Serviço",
            type="custom",
            content_cls=ContentEditAtendimento(
                clientes,
                servicos,
                data,
                duracao,
            ),
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=self.fechar_dialog),
                MDFlatButton(
                    text="SALVAR",
                    on_release=lambda _: self.salvar_edicao_servico(_id),
                ),
            ],
        )
        self.dialog.open()

    def remover(self, *_: Any) -> None:
        if not self.selected_row:
            # Exibir mensagem indicando que nenhuma linha foi selecionada
            return

        row_data = self.selected_row
        _id = int(row_data[0])

        self.dialog = MDDialog(
            text=f"Tem certeza que deseja remover o atendimento ID {_id}?",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=self.fechar_dialog),
                MDFlatButton(
                    text="REMOVER",
                    on_release=lambda _: self.confirmar_remocao(_id),
                ),
            ],
        )
        self.dialog.open()

    def confirmar_remocao(self, _id: int) -> None:
        self.banco.remover_atendimento(_id)
        self.carregar()
        self.dialog.dismiss()

    def on_row_press(self, instance_table: MDDataTable, instance_row: Any) -> None:
        selected_row_index = instance_row.index // len(instance_table.column_data)
        self.selected_row = instance_table.row_data[selected_row_index]


class ContentAddAtendimento(MDBoxLayout):
    def __init__(
        self,
        clientes: list[tuple[str, str]],
        servicos: list[tuple[str, str]],
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.clientes = clientes
        self.servicos = servicos

        # Configurar o menu dropdown de clientes
        menu_items_clientes = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{cliente[1]}",
                "on_release": lambda x=f"{cliente[1]}": self.set_cliente_item(x),
            }
            for cliente in self.clientes
        ]
        self.cliente_dropdown = MDDropdownMenu(
            caller=self.ids.cliente,
            items=menu_items_clientes,
            width_mult=4,
        )

        # Configurar o menu dropdown de serviços
        menu_items_servicos = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{servico[1]}",
                "on_release": lambda x=f"{servico[1]}": self.set_servico_item(x),
            }
            for servico in self.servicos
        ]
        self.servico_dropdown = MDDropdownMenu(
            caller=self.ids.servico,
            items=menu_items_servicos,
            width_mult=4,
        )

    def set_cliente_item(self, text_item: str) -> None:
        self.ids.cliente.text = text_item
        self.cliente_dropdown.dismiss()

    def set_servico_item(self, text_item: str) -> None:
        self.ids.servico.text = text_item
        self.servico_dropdown.dismiss()


class ContentEditAtendimento(MDBoxLayout):
    def __init__(
        self,
        clientes: list[tuple[str, str]],
        servicos: list[tuple[str, str]],
        data: str,
        duracao: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.clientes = clientes
        self.servicos = servicos

        menu_items_clientes = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{cliente[1]}",
                "on_release": lambda x=f"{cliente[1]}": self.set_cliente_item(x),
            }
            for cliente in self.clientes
        ]
        self.cliente_dropdown = MDDropdownMenu(
            caller=self.ids.cliente,
            items=menu_items_clientes,
            width_mult=4,
        )

        menu_items_servicos = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{servico[1]}",
                "on_release": lambda x=f"{servico[1]}": self.set_servico_item(x),
            }
            for servico in self.servicos
        ]
        self.servico_dropdown = MDDropdownMenu(
            caller=self.ids.servico,
            items=menu_items_servicos,
            width_mult=4,
        )

    def set_cliente_item(self, text_item: str) -> None:
        self.ids.cliente.text = text_item
        self.cliente_dropdown.dismiss()

    def set_servico_item(self, text_item: str) -> None:
        self.ids.servico.text = text_item
        self.servico_dropdown.dismiss()
