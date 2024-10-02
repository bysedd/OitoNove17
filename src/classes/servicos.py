from __future__ import annotations

from typing import TYPE_CHECKING, Any

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

if TYPE_CHECKING:
    from src.database import BancoDeDados

Builder.load_string("""
<ContentAddServico>:
    orientation: "vertical"
    spacing: dp(20)
    size_hint_y: None
    height: self.minimum_height + dp(50)
<ContentEditServico>:
    orientation: "vertical"
    spacing: dp(20)
    size_hint_y: None
    height: self.minimum_height + dp(50)
""")


class TelaServicos(MDScreen):
    def __init__(self, banco: BancoDeDados, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = "tela_servicos"
        self.banco = banco
        self.selected_row = None

        layout = BoxLayout(orientation="vertical")

        self.column_data = [
            ("ID", dp(30)),
            ("Nome", dp(40)),
            ("Preço", dp(30)),
        ]

        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
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
            spacing=dp(5),
            padding=[dp(10), dp(5), dp(10), dp(5)],
        )

        btn_voltar = MDFlatButton(
            text="Voltar",
            on_release=self.voltar_menu,
            size_hint_x=1,
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
        servicos = self.banco.obter_servicos()
        self.data_tables.row_data = [
            (str(servico[0]), servico[1], f"{servico[2]:.2f}") for servico in servicos
        ]

    def adicionar(self, *_: Any) -> None:
        self.dialog = MDDialog(
            title="Adicionar Serviço",
            type="custom",
            content_cls=ContentAddServico(),
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=self.fechar_dialog),
                MDFlatButton(text="SALVAR", on_release=self.salvar_servico),
            ],
        )
        self.dialog.open()

    def fechar_dialog(self, *_: Any) -> None:
        self.dialog.dismiss()

    def salvar_servico(self, *_: Any) -> None:
        nome = self.dialog.content_cls.ids.nome.text
        preco = self.dialog.content_cls.ids.preco.text
        if nome and preco:
            try:
                preco_float = float(preco)
                self.banco.adicionar_servico(nome, preco_float)
                self.carregar()
                self.dialog.dismiss()
            except ValueError:
                # Exibir mensagem de erro
                pass
        else:
            # Exibir mensagem de erro
            pass

    def editar(self, *_: Any) -> None:
        if not self.selected_row:
            # Exibir mensagem indicando que nenhuma linha foi selecionada
            return

        row_data = self.selected_row
        _id = int(row_data[0])
        nome = row_data[1]
        preco = row_data[2]

        self.dialog = MDDialog(
            title="Editar Serviço",
            type="custom",
            content_cls=ContentEditServico(nome, preco),
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=self.fechar_dialog),
                MDFlatButton(
                    text="SALVAR",
                    on_release=lambda _: self.salvar_edicao_servico(_id),
                ),
            ],
        )
        self.dialog.open()

    def salvar_edicao_servico(self, _id: int) -> None:
        nome = self.dialog.content_cls.ids.nome.text
        preco = self.dialog.content_cls.ids.preco.text
        if nome and preco:
            try:
                preco_float = float(preco)
                self.banco.editar_servico(_id, nome, preco_float)
                self.carregar()
                self.dialog.dismiss()
            except ValueError:
                # Exibir mensagem de erro
                pass
        else:
            # Exibir mensagem de erro
            pass

    def remover(self, *_: Any) -> None:
        if not self.selected_row:
            # Exibir mensagem indicando que nenhuma linha foi selecionada
            return

        row_data = self.selected_row
        _id = int(row_data[0])
        nome = row_data[1]

        self.dialog = MDDialog(
            text=f"Tem certeza que deseja remover o serviço '{nome}'?",
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
        self.banco.remover_servico(_id)
        self.carregar()
        self.dialog.dismiss()

    def on_row_press(self, instance_table: MDDataTable, instance_row: Any) -> None:
        selected_row_index = instance_row.index // len(instance_table.column_data)
        self.selected_row = instance_table.row_data[selected_row_index]


class ContentAddServico(MDBoxLayout):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(10)
        self.ids = {}

        self.ids["nome"] = MDTextField(
            hint_text="Nome",
            required=True,
        )
        self.ids["preco"] = MDTextField(
            hint_text="Preço",
            required=True,
            input_filter="float",
        )

        self.add_widget(self.ids["nome"])
        self.add_widget(self.ids["preco"])


class ContentEditServico(MDBoxLayout):
    def __init__(self, nome: str, preco: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.ids = {}

        self.ids["nome"] = MDTextField(
            hint_text="Nome",
            text=nome,
            required=True,
        )
        self.ids["preco"] = MDTextField(
            hint_text="Preço",
            text=preco,
            required=True,
            input_filter="float",
        )

        self.add_widget(self.ids["nome"])
        self.add_widget(self.ids["preco"])
