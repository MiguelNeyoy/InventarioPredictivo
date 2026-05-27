import os
import re
import pandas as pd
import unicodedata

# Diccionario de Expresiones Regulares para Clasificación Semántica (Mapa de Servicios y Insumos)
CATEGORIAS_REGEX = {
    # ─── SERVICIOS (SVC) ───
    "Servicio: Formateo": r"\b(formateo|formatear|pantallazo azul|sistema operativo|reinstalar|windows|os install)\b",
    "Servicio: Limpieza Estandar": r"\b(limpieza|mantenimiento)\b(?!.*(gamer|all in one|aio))",
    "Servicio: Limpieza Gamer/AIO": r"\b(limpieza|mantenimiento).*(gamer|all in one|aio)",
    "Servicio: Programas Basicos": r"\b(programas basicos|paquete de programas|office|pdf|winrar)\b",
    "Servicio: Programas Especialidad": r"\b(autocad|revit|photoshop|indesign|illustrator|solidworks)\b",
    "Servicio: Cambio Fuente Poder": r"\b(cambio|reemplazo|instalacion).*(fuente de poder|power supply|psu)",
    "Servicio: Cambio Teclado": r"\b(cambio|reemplazo|instalacion).*(teclado|keyboard)",
    "Servicio: Reparacion Bisagras/Display": r"\b(pantalla|display|bisagra|bisagras)\b",
    "Servicio: Diagnostico Humedad/Plaga": r"\b(mojado|agua|plaga|cucarachas|limpieza por humedad)\b",
    "Servicio: Equipo Lento (Diagnostico)": r"\b(lento|lenta|traba|se congela|optimizar|rendimiento bajo)\b",
    "Servicio: Actualizacion BIOS": r"\b(bios|actualizar bios|update bios)\b",
    "Servicio: Ensamble Completo": r"\b(ensamble completo|armar pc|armado de pc|ensamble)\b",
    
    # ─── HARDWARE (MTS / MTO) ───
    "Hardware: SSD 240 GB": r"\b(ssd\s*240\s*g[bo]|ssd\s*240|solido\s*240)\b",
    "Hardware: SSD 480 GB": r"\b(ssd\s*480\s*g[bo]|ssd\s*480|solido\s*480)\b",
    "Hardware: SSD 1 TB": r"\b(ssd\s*1\s*t[bo]|ssd\s*1000|ssd\s*960|solido\s*1tb)\b",
    "Hardware: SSD M.2 (Bajo Pedido)": r"\b(m\.2|nvme|ssd\s*m2)\b",
    "Hardware: SSD >1TB (Bajo Pedido)": r"\b(ssd\s*2tb|ssd\s*mayor almacenamiento)\b",
    "Hardware: Tarjeta Red WIFI PCI": r"\b(tarjeta wifi|pci wifi|adaptador de red wifi)\b",
    "Hardware: Memoria RAM DDR4": r"\b(ram|memoria ram|ddr4|ddr3)\b",
    "Hardware: Fuente de Poder": r"\b(fuente de poder|fuente certificada|psu)\b",
    "Hardware: Teclado": r"\b(teclado|keyboard)\b",
    "Hardware: Display / Pantalla": r"\b(display|pantalla|screen)\b",
    "Hardware: Carcasa HDD a USB": r"\b(carcasa|case hdd|adaptador hdd)\b"
}

# Regex para detectar gastos operativos que deben ser excluidos del análisis de ventas
GASTOS_REGEX = r"\b(nomina|renta|prestamo|tarjeta|internet|secretaria|mercadolibre|osiris|marilu|benjamin|miguel)\b"

MESES_ESPANOL = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

def normalizar_texto(texto):
    """Limpia el texto libre eliminando acentos, caracteres especiales y convirtiendo a minúsculas."""
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    # Eliminar acentos
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    # Eliminar caracteres raros pero conservar letras, números y espacios
    texto = re.sub(r'[^a-z0-9\s\.\+/*\-]', '', texto)
    return texto.strip()

def parsear_fecha_espanol(fecha_str):
    """Parsea fechas escritas en texto en español (ej. '15 DE ENERO 2023') a datetime de Pandas."""
    if not isinstance(fecha_str, str):
        try:
            return pd.to_datetime(fecha_str)
        except:
            return pd.NaT
            
    fecha_clean = normalizar_texto(fecha_str).lower()
    # Buscar patrones tipo: "15 de enero 2023" o "15 enero 2023" o "16  de enero 2023"
    match = re.search(r'(\d+)\s+(?:de\s+)?([a-z]+)\s+(?:de\s+)?(\d{4})', fecha_clean)
    if match:
        dia = match.group(1).zfill(2)
        mes_txt = match.group(2)
        anio = match.group(3)
        
        mes = MESES_ESPANOL.get(mes_txt, "01")
        return pd.to_datetime(f"{anio}-{mes}-{dia}")
    
    try:
        return pd.to_datetime(fecha_str)
    except:
        return pd.NaT

def extraer_cantidad(texto, val_cant=None):
    """Busca patrones de cantidad incrustados (ej. '2 x', '2 unidades', 'x2') con fallback a 1."""
    if val_cant is not None and pd.notna(val_cant):
        try:
            return int(float(val_cant))
        except:
            pass
    
    texto = str(texto).lower()
    
    # Buscar si inicia con número seguido de palabra (ej. "2 cpu", "4 laptops")
    match_start = re.match(r'^\s*(\d+)\s+(cpu|laptop|pc|pantalla|teclado|memoria|disco)', texto)
    if match_start:
        return int(match_start.group(1))
        
    # Buscar patrones tipo "2 x" o "x 2"
    match_x = re.search(r'\b(\d+)\s*x\b|\bx\s*(\d+)\b', texto)
    if match_x:
        val = match_x.group(1) or match_x.group(2)
        return int(val)
        
    # Buscar patrones como "2 unidades", "2 pz", "2 ssd"
    match_units = re.search(r'\b(\d+)\s*(unidad|unidades|pz|pzs|ssd|ram|disco|teclado|fuente|pantalla|display)\b', texto)
    if match_units:
        return int(match_units.group(1))
        
    return 1

def procesar_hoja(df_crudo, nombre_hoja):
    """Procesa una única hoja del libro de Excel, extrayendo y clasificando transacciones."""
    # --- DETECTOR DINÁMICO DE CABECERA (Header Offset) ---
    header_idx = None
    for idx, row in df_crudo.iterrows():
        row_vals = [normalizar_texto(str(val)) for val in row.values]
        has_fecha = any("fecha" in val for val in row_vals)
        has_servicio = any("servicio" in val or "concepto" in val or "descripcion" in val for val in row_vals)
        if has_fecha and has_servicio:
            header_idx = idx
            break
            
    if header_idx is not None:
        columnas_reales = df_crudo.iloc[header_idx].values
        df_crudo.columns = [str(c).strip() for c in columnas_reales]
        df_crudo = df_crudo.iloc[header_idx + 1:].reset_index(drop=True)
    else:
        df_crudo.columns = [str(c).strip() for c in df_crudo.columns]
        
    df_crudo.columns = [c.lower() for c in df_crudo.columns]
    
    col_fecha = next((c for c in ["fecha de venta", "fecha", "date"] if c in df_crudo.columns), None)
    col_desc = next((c for c in ["tipo de servicio", "descripcion", "concepto", "detalle"] if c in df_crudo.columns), None)
    col_cant = next((c for c in ["cantidad", "unidades", "qty"] if c in df_crudo.columns), None)
    
    if not col_fecha or not col_desc:
        # Si la hoja no tiene estructura de ventas, la omitimos
        return [], []
        
    registros_hardware = []
    registros_servicios = []
    
    for idx, fila in df_crudo.iterrows():
        fecha_raw = fila[col_fecha]
        desc_raw = fila[col_desc]
        cant_raw = fila[col_cant] if col_cant else None
        
        if pd.isna(fecha_raw) or pd.isna(desc_raw):
            continue
            
        desc_limpia = normalizar_texto(str(desc_raw))
        
        # ⚠️ FILTRO DE GASTOS OPERATIVOS
        if re.search(GASTOS_REGEX, desc_limpia):
            continue
            
        fecha_dt = parsear_fecha_espanol(fecha_raw)
        if pd.isna(fecha_dt):
            continue
            
        fecha_str = fecha_dt.strftime("%Y-%m-%d")
        cantidad = extraer_cantidad(desc_limpia, cant_raw)
        
        coincidencias = []
        for cat, patron in CATEGORIAS_REGEX.items():
            if re.search(patron, desc_limpia):
                coincidencias.append(cat)
                
        # LÓGICA ESPECIAL A: Ensambles / Armados (Receta BOM)
        if any("ensamble" in cat.lower() for cat in coincidencias):
            for comp in ["Hardware: SSD 1 TB", "Hardware: Memoria RAM DDR4", "Hardware: Fuente de Poder", "Hardware: Teclado"]:
                registros_hardware.append({
                    "Fecha": fecha_str,
                    "Producto": comp,
                    "Ventas": 1
                })
            registros_servicios.append({
                "Fecha": fecha_str,
                "Producto": "Servicio: Ensamble Completo",
                "Ventas": 1
            })
            continue
            
        # LÓGICA ESPECIAL B: Correlación Diagnóstico Lento ➔ Oportunidad SSD
        if any("lento" in cat.lower() for cat in coincidencias):
            registros_servicios.append({
                "Fecha": fecha_str,
                "Producto": "Servicio: Equipo Lento (Diagnostico)",
                "Ventas": 1
            })
            registros_hardware.append({
                "Fecha": fecha_str,
                "Producto": "Hardware: SSD 240 GB",
                "Ventas": 1
            })
            continue
            
        # LÓGICA ESPECIAL C: Desglose de Paquetes SSD con Formateo incluido
        if any("ssd" in cat.lower() and not "pedido" in cat.lower() for cat in coincidencias):
            for cat in coincidencias:
                if "hardware" in cat.lower():
                    registros_hardware.append({
                        "Fecha": fecha_str,
                        "Producto": cat,
                        "Ventas": cantidad
                    })
            registros_servicios.append({
                "Fecha": fecha_str,
                "Producto": "Servicio: Formateo",
                "Ventas": 1
            })
            continue
            
        # Mapeo estándar
        tiene_hardware = False
        tiene_servicio = False
        
        for cat in coincidencias:
            if "hardware" in cat.lower():
                registros_hardware.append({
                    "Fecha": fecha_str,
                    "Producto": cat,
                    "Ventas": cantidad
                })
                tiene_hardware = True
            elif "servicio" in cat.lower():
                registros_servicios.append({
                    "Fecha": fecha_str,
                    "Producto": cat,
                    "Ventas": cantidad
                })
                tiene_servicio = True
                
        # Clasificar como no identificado si no coincide con ninguna regex pero tiene marca
        if not tiene_hardware and not tiene_servicio:
            if any(brand in desc_limpia for brand in ["hp", "dell", "lenovo", "asus", "acer", "toshiba", "macbook"]):
                registros_servicios.append({
                    "Fecha": fecha_str,
                    "Producto": "Servicio: Limpieza Estandar",
                    "Ventas": 1
                })
                
    return registros_hardware, registros_servicios

def ejecutar_etl():
    """Ejecuta el pipeline ETL procesando todas las hojas del Excel real."""
    print("=== INICIANDO PIPELINE ETL MULTI-HOJA DE ALTA PRECISIÓN ===")
    
    excel_path = "/home/chili/Documents/InventarioPredictivo/ArchivosCSV/VENTAS PCYLAP 2023.xlsx"
    output_dir = "/home/chili/Documents/InventarioPredictivo/ArchivosCSV"
    
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"No se encontró el archivo Excel de ventas de PCYLAP en: {excel_path}")
        
    print(f"[ETL] Cargando libro de Excel completo: {excel_path}")
    xls = pd.ExcelFile(excel_path, engine="openpyxl")
    hojas = xls.sheet_names
    print(f"[ETL] Total hojas detectadas: {len(hojas)}")
    
    if len(hojas) == 0:
        raise ValueError("El archivo Excel no contiene hojas de datos.")
        
    # La última hoja es el "mes actual"
    hoja_mes_actual = hojas[-1]
    hojas_historicas = hojas[:-1]
    
    print(f"[ETL] Mes Actual: '{hoja_mes_actual}'")
    print(f"[ETL] Rango Histórico: Enero 2023 → '{hojas_historicas[-1]}'")
    
    # ─── 1. PROCESAR HISTÓRICO ───
    hw_hist_list = []
    sv_hist_list = []
    
    for hoja in hojas_historicas:
        df_hoja = pd.read_excel(excel_path, sheet_name=hoja, header=None, engine="openpyxl")
        hw_rows, sv_rows = procesar_hoja(df_hoja, hoja)
        hw_hist_list.extend(hw_rows)
        sv_hist_list.extend(sv_rows)
        
    df_hw_hist = pd.DataFrame(hw_hist_list)
    df_sv_hist = pd.DataFrame(sv_hist_list)
    
    # Consolidar histórico de hardware
    if not df_hw_hist.empty:
        df_hw_hist = df_hw_hist.groupby(["Fecha", "Producto"])["Ventas"].sum().reset_index()
        df_hw_hist = df_hw_hist.sort_values("Fecha")
        path_hw = os.path.join(output_dir, "historico_maestro.csv")
        df_hw_hist.to_csv(path_hw, index=False, encoding="utf-8-sig")
        print(f"[ETL] Histórico Maestro exportado: {path_hw} ({len(df_hw_hist)} registros)")
        
    # Consolidar histórico de servicios
    if not df_sv_hist.empty:
        df_sv_hist = df_sv_hist.groupby(["Fecha", "Producto"])["Ventas"].sum().reset_index()
        df_sv_hist = df_sv_hist.sort_values("Fecha")
        path_sv = os.path.join(output_dir, "historico_servicios.csv")
        df_sv_hist.to_csv(path_sv, index=False, encoding="utf-8-sig")
        print(f"[ETL] Histórico Servicios exportado: {path_sv} ({len(df_sv_hist)} registros)")
        
    # ─── 2. PROCESAR MES ACTUAL ───
    df_actual_raw = pd.read_excel(excel_path, sheet_name=hoja_mes_actual, header=None, engine="openpyxl")
    hw_act, sv_act = procesar_hoja(df_actual_raw, hoja_mes_actual)
    
    # El mes actual mezcla transacciones de hardware y servicio en el formato esperado por el Predictor
    all_actual = hw_act + sv_act
    df_actual = pd.DataFrame(all_actual)
    
    if not df_actual.empty:
        df_actual = df_actual.groupby(["Fecha", "Producto"])["Ventas"].sum().reset_index()
        df_actual = df_actual.sort_values("Fecha")
        
        # Guardar en ventas_mes_actual.csv
        path_actual = os.path.join(output_dir, "ventas_mes_actual.csv")
        df_actual.to_csv(path_actual, index=False, encoding="utf-8-sig")
        print(f"[ETL] Ventas Mes Actual exportado: {path_actual} ({len(df_actual)} registros)")
    else:
        # Fallback vacío
        df_actual = pd.DataFrame(columns=["Fecha", "Producto", "Ventas"])
        path_actual = os.path.join(output_dir, "ventas_mes_actual.csv")
        df_actual.to_csv(path_actual, index=False, encoding="utf-8-sig")
        print(f"[ETL] Mes actual vacío. Creado CSV de fallback.")
        
    print("=== PIPELINE ETL PROCESADO EXITOSAMENTE ===")

if __name__ == "__main__":
    ejecutar_etl()
