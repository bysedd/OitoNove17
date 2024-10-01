# main.py

from typing import Any

from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar

from src.classes.atendimentos import TelaAtendimentos
from src.classes.clientes import TelaClientes
from src.classes.servicos import TelaServicos
from src.database import BancoDeDados


class MainMenu(MDScreen):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = "main_menu"

        self.md_bg_color = self.theme_cls.bg_light

        toolbar = MDTopAppBar(
            title="Barbearia Oito Nove 17",
            pos_hint={"top": 1},
            elevation=10,
        )

        layout = AnchorLayout()

        box_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint=(None, None),
            width=dp(300),
            height=dp(200),
        )

        btn_clientes = MDFillRoundFlatIconButton(
            text="Clientes",
            icon="account-group",
            text_color=self.theme_cls.primary_color,
            icon_color=self.theme_cls.primary_color,
            md_bg_color=self.theme_cls.accent_color,
            on_release=self.open_clientes,
            size_hint=(1, None),
            height=dp(50),
        )

        btn_servicos = MDFillRoundFlatIconButton(
            text="Serviços",
            icon="briefcase",
            text_color=self.theme_cls.primary_color,
            icon_color=self.theme_cls.primary_color,
            md_bg_color=self.theme_cls.accent_color,
            on_release=self.open_servicos,
            size_hint=(1, None),
            height=dp(50),
        )

        btn_atendimentos = MDFillRoundFlatIconButton(
            text="Atendimentos",
            icon="calendar-check",
            text_color=self.theme_cls.primary_color,
            icon_color=self.theme_cls.primary_color,
            md_bg_color=self.theme_cls.accent_color,
            on_release=self.open_atendimentos,
            size_hint=(1, None),
            height=dp(50),
        )

        box_layout.add_widget(btn_clientes)
        box_layout.add_widget(btn_servicos)
        box_layout.add_widget(btn_atendimentos)

        layout.add_widget(box_layout)

        self.add_widget(toolbar)
        self.add_widget(layout)

    def open_clientes(self, *_: Any) -> None:
        self.manager.current = "tela_clientes"

    def open_servicos(self, *_: Any) -> None:
        self.manager.current = "tela_servicos"

    def open_atendimentos(self, *_: Any) -> None:
        self.manager.current = "tela_atendimentos"


class MainApp(MDApp):
    def build(self) -> ScreenManager:
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"

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
