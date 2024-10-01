# main.py

from typing import Any

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from src.classes.atendimentos import TelaAtendimentos
from src.classes.clientes import TelaClientes
from src.classes.servicos import TelaServicos
from src.database import BancoDeDados


class MainMenu(MDScreen):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = "main_menu"

        # Layout principal
        layout = BoxLayout(orientation="vertical", spacing=20, padding=40)

        # Título
        title_label = MDLabel(
            text="Barbearia Oito Nove 17",
            halign="center",
            theme_text_color="Primary",
            font_style="H4",
            size_hint=(1, 0.2),
        )

        # Botões
        btn_clientes = MDRectangleFlatButton(
            text="Clientes",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(200, 50),
            on_release=self.open_clientes,
        )

        btn_servicos = MDRectangleFlatButton(
            text="Serviços",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(200, 50),
            on_release=self.open_servicos,
        )

        btn_atendimentos = MDRectangleFlatButton(
            text="Atendimentos",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(200, 50),
            on_release=self.open_atendimentos,
        )

        # Adicionar widgets ao layout
        layout.add_widget(title_label)
        layout.add_widget(btn_clientes)
        layout.add_widget(btn_servicos)
        layout.add_widget(btn_atendimentos)

        self.add_widget(layout)

    def open_clientes(self, *args: Any) -> None:
        self.manager.current = "tela_clientes"

    def open_servicos(self, *args: Any) -> None:
        self.manager.current = "tela_servicos"

    def open_atendimentos(self, *args: Any) -> None:
        self.manager.current = "tela_atendimentos"


class MainApp(MDApp):
    def build(self) -> ScreenManager:
        self.banco = BancoDeDados()
        self.sm = ScreenManager()

        self.main_menu = MainMenu()
        self.tela_clientes = TelaClientes(self.banco)
        self.tela_servicos = TelaServicos(self.banco)
        self.tela_atendimentos = TelaAtendimentos(self.banco)

        self.sm.add_widget(self.main_menu)
        self.sm.add_widget(self.tela_clientes)
        self.sm.add_widget(self.tela_servicos)
        self.sm.add_widget(self.tela_atendimentos)

        self.sm.current = "main_menu"

        return self.sm


if __name__ == "__main__":
    MainApp().run()
