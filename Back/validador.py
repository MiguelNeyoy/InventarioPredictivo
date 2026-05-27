import pandas as pd
import os


class ValidadorDatos:
    """
    Se encargado de recibir un DataFrame crudo, validar su integridad,
    eliminar problemas y prepararlo para el motor predictivo.
    """

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path_hw = os.path.join(base_dir, "..", "ArchivosCSV", "historico_maestro.csv")
        csv_path_sv = os.path.join(base_dir, "..", "ArchivosCSV", "historico_servicios.csv")
        
        df_hw = pd.read_csv(csv_path_hw) if os.path.exists(csv_path_hw) else pd.DataFrame(columns=["Fecha", "Producto", "Ventas"])
        df_sv = pd.read_csv(csv_path_sv) if os.path.exists(csv_path_sv) else pd.DataFrame(columns=["Fecha", "Producto", "Ventas"])
        
        self.df_historico = pd.concat([df_hw, df_sv], ignore_index=True)
        self.df_historico["ds"] = pd.to_datetime(self.df_historico["Fecha"])
        self.df_historico["y"] = pd.to_numeric(self.df_historico["Ventas"], errors="coerce").fillna(0)
        
        # Limpieza de Outliers (ej. RAM de 241 unidades en un solo día)
        cleaned_rows = []
        for prod, group in self.df_historico.groupby("Producto"):
            group = group.copy()
            median_val = group["y"].median()
            if pd.isna(median_val) or median_val <= 0:
                median_val = 1
            threshold = max(10.0, median_val * 10.0)
            # Reemplazar valores atípicos con la mediana
            group.loc[group["y"] > threshold, "y"] = median_val
            cleaned_rows.append(group)
            
        if cleaned_rows:
            self.df_historico = pd.concat(cleaned_rows, ignore_index=True)

    def validar_y_limpiar(self, df_crudo):
        """
        Recibe un DataFrame de Pandas.
        Lanza ValueError si faltan columnas requeridas o hay datos insalvables.
        Devuelve el DataFrame limpio y formateado para Prophet.
        """

        # 1. Validar columnas requeridas
        columnas_esperadas = {"Fecha", "Producto", "Ventas"}
        columnas_actuales = set(df_crudo.columns)

        faltantes = columnas_esperadas - columnas_actuales
        if faltantes:
            raise ValueError(f"Faltan columnas requeridas en los datos: {faltantes}")

        # 2. Eliminar filas con valores nulos o vacíos en las columnas clave
        df_limpio = df_crudo.dropna(subset=["Fecha", "Producto", "Ventas"]).copy()

        if df_limpio.empty:
            raise ValueError(
                "El DataFrame quedo vacio despues de limpiar valores nulos."
            )

        # 3. Validar y limpiar valores de 'Ventas'
        # Nos aseguramos de que sean numéricos (coacciona errores a NaN y luego los filtra)
        df_limpio["Ventas"] = pd.to_numeric(df_limpio["Ventas"], errors="coerce")
        df_limpio = df_limpio.dropna(subset=["Ventas"])

        # Las ventas no pueden ser negativas, verificamos y/o reparamos
        # Si hubiera ventas negativas, podrías lanzar un error:
        if (df_limpio["Ventas"] < 0).any():
            raise ValueError("Se encontraron valores negativos en la columna 'Ventas'.")

        # 4. Validar y convertir 'Fecha'
        try:
            df_limpio["ds"] = pd.to_datetime(df_limpio["Fecha"])
        except Exception as e:
            raise ValueError(
                f"No se pudieron convertir las fechas. Asegurate del formato correcto. Detalle: {e}"
            )

        # 5. Renombrar columnas para el modelo Prophet
        df_limpio = df_limpio.rename(columns={"Ventas": "y"})

        df_usuario = df_limpio[["ds", "Producto", "y"]].copy()
        df_usuario["Fuente"] = "usuario"

        df_historico = self.df_historico[["ds", "Producto", "y"]].copy()
        df_historico["Fuente"] = "historico"

        df_unificado = pd.concat([df_historico, df_usuario], ignore_index=True)
        df_unificado = df_unificado.drop_duplicates(
            subset=["ds", "Producto"], keep="last"
        )
        df_unificado = df_unificado.drop(columns=["Fuente"])
        return df_unificado, df_usuario
