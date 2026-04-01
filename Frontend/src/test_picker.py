import flet as ft

def main(page: ft.Page):
    page.title = "Test FilePicker"

    def on_result(e):
        if e.files:
            resultado.value = f"Archivo seleccionado: {e.files[0].name}"
        else:
            resultado.value = "No se seleccionó archivo"
        page.update()

    picker = ft.FilePicker(on_result=on_result)
    page.overlay.append(picker)

    resultado = ft.Text("Sin archivo seleccionado")

    page.add(
        ft.ElevatedButton(
            "Seleccionar archivo",
            on_click=lambda _: picker.pick_files(allowed_extensions=["csv"]),
        ),
        resultado,
    )

ft.app(target=main)
