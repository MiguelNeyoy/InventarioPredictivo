import flet as ft


def crear_kpi_cards(df_metricas=None):
    mae = "N/A"
    rmse = "N/A"

    if df_metricas is not None and not df_metricas.empty:
        mae = f"{df_metricas['MAE'].mean():.2f}" if "MAE" in df_metricas.columns else "N/A"
        rmse = f"{df_metricas['RMSE'].mean():.2f}" if "RMSE" in df_metricas.columns else "N/A"

    tarjetas = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("MAE", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_600),
                        ft.Text(mae, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                    ],
                    spacing=5,
                ),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                expand=True,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("RMSE", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_600),
                        ft.Text(rmse, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                    ],
                    spacing=5,
                ),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                expand=True,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            ),
        ],
        spacing=20,
    )

    return tarjetas