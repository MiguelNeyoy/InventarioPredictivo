import flet as ft


def crear_sidebar(page: ft.Page, mostrar_panel, mostrar_reportes):
    sidebar_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.BLUE_700, size=30),
                        ft.Text(
                            "Predictor",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ]
                ),
                padding=ft.Padding(top=0, right=0, bottom=20, left=0),
            ),
            ft.Text(
                "MENÚ PRINCIPAL",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_400,
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.DASHBOARD),
                title=ft.Text("Panel de Control"),
                selected=True,
                on_click=mostrar_panel,
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ANALYTICS),
                title=ft.Text("Reportes"),
                on_click=mostrar_reportes,
            ),
            ft.Divider(height=20),
            ft.Container(expand=True),
        ],
        spacing=5,
        expand=True,
    )

    sidebar = ft.Container(
        content=sidebar_content,
        width=250,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.BorderRadius.only(top_right=15, bottom_right=15),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
    )

    return sidebar