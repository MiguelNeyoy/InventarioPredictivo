import pandas as pd

# Mapeo por defecto de estrategias de suministro
ESTRATEGIA_DEFAULT = {
    # Make to Stock (MTS) - Inventario Físico
    "Hardware: SSD 240 GB": "MTS",
    "Hardware: SSD 480 GB": "MTS",
    "Hardware: SSD 1 TB": "MTS",
    "Hardware: Memoria RAM DDR4": "MTS",
    "Hardware: Fuente de Poder": "MTS",
    "Hardware: Teclado": "MTS",
    "Hardware: Carcasa HDD a USB": "MTS",
    "Hardware: Tarjeta Red WIFI PCI": "MTS",
    "Cable de Red Cat6 3m": "MTS",
    "Pasta Térmica Arctic": "MTS",
    "Memoria USB 64GB": "MTS",
    
    # Make to Order (MTO) - Compra Directa a Proveedor
    "Hardware: SSD M.2 (Bajo Pedido)": "MTO",
    "Hardware: SSD >1TB (Bajo Pedido)": "MTO",
    "Hardware: Display / Pantalla": "MTO",
    "Laptop Gaming Asus": "MTO",
    "Laptop Dell Inspiron": "MTO",
    "Tarjeta Gráfica RTX 4060": "MTO",
    "Procesador Ryzen 5": "MTO",
    "Monitor 24 Pulgadas": "MTO"
}

class LogicaNegocio:
    """
    Contiene las reglas de negocio sobre alertas de inventario.
    """

    def evaluar_stock(self, df_predicciones, stock_actual_dict, porcentaje_seguridad=0, estrategias_dict=None):
        """
        Motor de reglas de negocio para emitir alertas basadas en MTS, MTO, SVC.
        df_predicciones: DataFrame con ["Producto", "Venta_Estimada"]
        stock_actual_dict: Diccionario en forma de {"Producto": CantidadReal}
        porcentaje_seguridad: Margen adicional (%) sobre el estimado
        estrategias_dict: Mapeo personalizado {"Producto": "MTS"|"MTO"|"SVC"}
        """
        alertas = []
        
        # Unificar el mapeo de estrategias
        mapeo_estrategias = ESTRATEGIA_DEFAULT.copy()
        if estrategias_dict:
            mapeo_estrategias.update(estrategias_dict)

        for index, fila in df_predicciones.iterrows():
            articulo = fila["Producto"]
            estimado = fila["Venta_Estimada"]

            # Obtener estrategia (SVC por defecto si el nombre tiene "Servicio")
            if str(articulo).startswith("Servicio:"):
                estrategia = "SVC"
            else:
                estrategia = mapeo_estrategias.get(articulo, "MTS")

            # Inicializar valores por defecto
            stock_real = stock_actual_dict.get(articulo, 0)
            estado_alerta = False
            cantidad_a_comprar = 0
            nota_operativa = ""

            if estrategia == "MTS":
                # Make-to-Stock: Requiere inventario local
                stock_requerido = estimado * (1 + porcentaje_seguridad / 100)
                if stock_requerido > stock_real:
                    estado_alerta = True
                    cantidad_a_comprar = round(stock_requerido - stock_real)
                else:
                    estado_alerta = False
                    cantidad_a_comprar = 0
                nota_operativa = "Abastecer Almacén (MTS)"
                
            elif estrategia == "MTO":
                # Make-to-Order: Compra directa bajo demanda a proveedor (se asume stock real local irrelevante o 0)
                estado_alerta = False  # No es una alerta crítica de almacén vacío
                cantidad_a_comprar = estimado  # Pedir exactamente lo estimado al proveedor
                nota_operativa = "Compra Directa Proveedor (MTO)"
                
            elif estrategia == "SVC":
                # Servicio: Mano de obra, no hay stock ni compras físicas
                stock_real = 0
                estado_alerta = False
                cantidad_a_comprar = 0
                nota_operativa = "Mano de Obra (Servicio SVC)"

            alertas.append(
                {
                    "Producto": articulo,
                    "Estrategia": estrategia,
                    "Venta_Estimada": estimado,
                    "Stock_Actual": stock_real,
                    "Cantidad_A_Comprar": cantidad_a_comprar,
                    "Alerta_Surtir": estado_alerta,
                    "Nota_Operativa": nota_operativa
                }
            )

        return pd.DataFrame(alertas)
    