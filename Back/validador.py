import pandas as pd
import os


class ValidadorDatos:
    """
    Se encarga de recibir un DataFrame crudo, validar su integridad,
    eliminar problemas y prepararlo para el motor predictivo.
    """

    def __init__(self, ruta_historico=None):
        if ruta_historico is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.ruta_historico = os.path.join(base_dir, "historico_maestro.csv")
        else:
            self.ruta_historico = ruta_historico

    def cargar_historico(self):
        """Carga el archivo histórico maestro desde el disco local."""
        if os.path.exists(self.ruta_historico):
            print(f"Cargando histórico desde: {self.ruta_historico}")
            return pd.read_csv(self.ruta_historico)
        print(f"Advertencia: No se encontró {self.ruta_historico}")
        return pd.DataFrame()

    def concatenar_historico(self, df_crudo):
        """
        Recibe el DataFrame nuevo del usuario y lo concatena con el histórico.
        Elimina duplicados manteniendo el registro más reciente.
        """
        df_historico = self.cargar_historico()

        if df_historico.empty:
            return df_crudo

        if (
            "Fecha" in df_historico.columns
            and "Producto" in df_historico.columns
            and "Cantidad" in df_historico.columns
        ):
            df_concatenado = pd.concat([df_historico, df_crudo], ignore_index=True)

            df_concatenado["ds_temp"] = pd.to_datetime(
                df_concatenado["Fecha"], errors="coerce"
            )
            df_concatenado = df_concatenado.sort_values("ds_temp", ascending=True)
            df_concatenado = df_concatenado.drop_duplicates(
                subset=["Fecha", "Producto"], keep="last"
            )
            df_concatenado = df_concatenado.drop(columns=["ds_temp"])

            print(f"Datos concatenados: {len(df_concatenado)} registros totales")
            return df_concatenado

        return df_crudo

    def validar_y_limpiar(self, df_crudo):
        """
        Recibe un DataFrame de Pandas.
        Lanza ValueError si faltan columnas requeridas o hay datos insalvables.
        Devuelve el DataFrame limpio y formateado para Prophet.
        """
        print("Validando integridad de los datos...")

        # Concatenar con histórico antes de procesar
        df_crudo = self.concatenar_historico(df_crudo)

        # 1. Validar columnas requeridas
        columnas_esperadas = {"Fecha", "Producto", "Cantidad"}
        columnas_actuales = set(df_crudo.columns)

        faltantes = columnas_esperadas - columnas_actuales
        if faltantes:
            raise ValueError(f"Faltan columnas requeridas en los datos: {faltantes}")

        # 2. Eliminar filas con valores nulos o vacíos en las columnas clave
        df_limpio = df_crudo.dropna(subset=["Fecha", "Producto", "Cantidad"]).copy()

        if df_limpio.empty:
            raise ValueError(
                "El DataFrame quedo vacio despues de limpiar valores nulos."
            )

        # 3. Validar y limpiar valores de 'Ventas'
        # Nos aseguramos de que sean numéricos (coacciona errores a NaN y luego los filtra)
        df_limpio["Cantidad"] = pd.to_numeric(df_limpio["Cantidad"], errors="coerce")
        df_limpio = df_limpio.dropna(subset=["Cantidad"])

        # Las ventas no pueden ser negativas, verificamos y/o reparamos
        # Si hubiera ventas negativas, podrías lanzar un error:
        if (df_limpio["Cantidad"] < 0).any():
            raise ValueError(
                "Se encontraron valores negativos en la columna 'Cantidad'."
            )

        # 4. Validar y convertir 'Fecha'
        try:
            df_limpio["ds"] = pd.to_datetime(df_limpio["Fecha"])
        except Exception as e:
            raise ValueError(
                f"No se pudieron convertir las fechas. Asegurate del formato correcto. Detalle: {e}"
            )

        # 5. Renombrar columnas para el modelo Prophet
        print("Preparando columnas ('ds', 'y') para el motor predictivo...")
        df_limpio = df_limpio.rename(columns={"Cantidad": "y"})

        # Seleccionamos solo las columnas que importan para el modelo
        return df_limpio[["ds", "Producto", "y"]]
