import pandas as pd
import os


class ExportadorDatos:
    """
    Módulo de exportación para convertir DataFrames a archivos CSV descargables.
    """

    def __init__(self, ruta_default=None):
        if ruta_default is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.ruta_default = os.path.join(base_dir, "exports")
        else:
            self.ruta_default = ruta_default

        if not os.path.exists(self.ruta_default):
            os.makedirs(self.ruta_default)

    def exportar_a_csv(self, df, nombre_archivo="reporte_inventario.csv"):
        """
        Recibe un DataFrame y lo exporta a un archivo CSV.

        Args:
            df: DataFrame de pandas con los datos a exportar.
            nombre_archivo: Nombre del archivo (incluyendo extensión .csv).

        Returns:
            str: Ruta completa del archivo generado.
        """
        if not nombre_archivo.endswith(".csv"):
            nombre_archivo += ".csv"

        ruta_completa = os.path.join(self.ruta_default, nombre_archivo)

        df.to_csv(ruta_completa, index=False, encoding="utf-8-sig")

        print(f"Archivo exportado exitosamente: {ruta_completa}")
        return ruta_completa
