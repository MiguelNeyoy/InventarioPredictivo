import flet as ft
def main(page: ft.Page):
    l = ft.ListTile(title=ft.Text("Test"), on_click=lambda e: print("Clicked"))
    print(dir(l))
ft.app(target=main)
