import streamlit as st
import math

# Configuración de la interfaz
st.set_page_config(page_title="Marcos Monic - Cotizador Gyotaku VIP", page_icon="🖼️", layout="centered")

# Estilos visuales limpios y profesionales en blanco y negro
st.markdown("""
    <style>
    .main {background-color: #ffffff;}
    h1 {color: #111111; font-family: 'Helvetica'; text-align: center; font-size: 28px;}
    .stNumberInput label {font-size: 16px !important; font-weight: bold; color: #222222;}
    .price-box {
        background-color: #f9f9f9;
        padding: 24px;
        border-radius: 8px;
        border: 2px solid #111111;
        text-align: center;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🖼️ Cotizador Exclusivo - Gyotaku VIP")
st.write("Ingrese las dimensiones de la obra para obtener su tarifa especial en enmarcados de **Doble Vidrio**.")

st.divider()

# 1. ENTRADAS DE DATOS (Lo único que ve el cliente)
largo = st.number_input("Largo de la obra en CM (Lado más largo):", min_value=0.0, step=0.5, value=70.0)
ancho = st.number_input("Ancho de la obra en CM:", min_value=0.0, step=0.5, value=50.0)

# 2. CONSTANTES DE COSTOS DEL TALLER (Ocultas para el cliente)
# Moldura fija seleccionada por defecto para este estilo (ejemplo: Yenory 1" Doble)
cost_per_cm_moldura = 25.00  

# Costo del Doble Vidrio por cm²
cost_vidrio_cm2 = 3.00  

# Mano de obra base fija del empleado
mano_obra_empleado = 2000.00  

# Variables fijas del Gyotaku tradicional (Doble vidrio transparente, sin cartón, sin papel tapiz)
cost_carton_cm2 = 0.00  
cost_pintura_cm_lineal = 0.00  
cost_papeltapiz_cm_lineal = 0.00  

# 3. PROCESAMIENTO DE LA FÓRMULA MATEMÁTICA REAL DE APPSHEET
if largo > 0 and ancho > 0:
    # Perímetro y Área base
    perimetro_lineal = 2 * (ancho + largo)
    area_cm2 = ancho * largo
    
    # A. Costo de Moldura con desperdicio (+8 cm)
    costo_moldura = cost_per_cm_moldura * (perimetro_lineal + 8)
    
    # B. Costo de Materiales por Área (Doble Vidrio)
    costo_vidrio = cost_vidrio_cm2 * area_cm2
    costo_carton = cost_carton_cm2 * area_cm2
    
    # C. Costo de Acabados por Perímetro
    costo_pintura = cost_pintura_cm_lineal * perimetro_lineal
    costo_papeltapiz = cost_papeltapiz_cm_lineal * perimetro_lineal
    
    # D. Cálculo Lógico de Complejidad (Mano de Obra Variable)
    # Por defecto para doble vidrio se establece complejidad "Media" debido al peso e instalación
    complejidad_tipo = "Media" 
    
    if perimetro_lineal <= 140 and complejidad_tipo == "Baja":
        factor_complejidad = 10
    else:
        if complejidad_tipo == "Baja":
            factor_complejidad = 20
        elif complejidad_tipo == "Media":
            factor_complejidad = 40
        elif complejidad_tipo == "Alta":
            factor_complejidad = 70
        else:
            factor_complejidad = 0
            
    costo_complejidad = factor_complejidad * perimetro_lineal
    
    # E. Suma total del Costo del Taller antes del multiplicador comercial
    costo_total_taller = (
        costo_moldura + 
        costo_vidrio + 
        costo_carton + 
        costo_pintura + 
        costo_papeltapiz + 
        mano_obra_empleado + 
        costo_complejidad
    )
    
    # F. Multiplicador de Ganancia Estándar del taller (* 1.5) y redondeo al techo (CEILING)
    precio_regular_taller = math.ceil(costo_total_taller * 1.5)
    
    # 4. APLICACIÓN DE LA REGLA VIP (20% Descuento y Piso Mínimo de ¢7,000)
    precio_con_descuento = precio_regular_taller * 0.80
    
    # Filtro del MAX(7000, precio)
    precio_vip_final = max(7000, precio_con_descuento)
    
    # Redondeo final a la centena más cercana para limpieza visual del cliente
    precio_redondeado = round(precio_vip_final, -2)

    # 5. DESPLIEGUE VISUAL EN PANTALLA
    st.markdown(f"""
        <div class="price-box">
            <h3 style='margin:0; color:#666666; font-size: 16px; font-weight: normal;'>Tu Tarifa Especial VIP:</h3>
            <h1 style='margin:12px 0; color:#111111; font-size: 38px;'>¢{precio_redondeado:,.0f} Colones</h1>
            <p style='margin:0; color:#888888; font-size: 11px;'>*Tarifa para enmarcado doble vidrio. Incluye IVA y comisiones bancarias.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Por favor, ingrese dimensiones válidas en centímetros.")
