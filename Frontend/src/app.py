import sys
import os
import flet as ft

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from views.dashboard import crear_vista_dashboard


def main(page: ft.Page):
    
    page.title = "Estación de Análisis Centralizada"
    page.bgcolor = "#F4F6F8"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1280
    page.window_height = 800

    page.add(crear_vista_dashboard(page))


ft.run(main)