import streamlit as st
import math

# Configuración de la interfaz
st.set_page_config(page_title="Marcos Monic - Cotizador Gyotaku", page_icon="🖼️", layout="centered")

# Estilos visuales limpios en blanco y negro (Identidad del taller)
st.markdown("""
    <style>
    .main {background-color: #ffffff;}
    h1 {color: #111111; font-family: 'Helvetica'; text-align: center; font-size: 26px; font-weight: bold;}
    .stNumberInput label, .stSelectbox label {font-size: 15px !important; font-weight: bold; color: #222222;}
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

st.title("🖼️ Cotizador de Enmarcados")
st.write("Ingrese las dimensiones de la obra para obtener su tarifa especial de taller.")

st.divider()

# 1. ENTRADAS DE DATOS (Interactivo para el cliente)
largo = st.number_input("Largo de la obra en CM:", min_value=0.0, step=0.5, value=70.0)
ancho = st.number_input("Ancho de la obra en CM:", min_value=0.0, step=0.5, value=50.0)

moldura_seleccionada = st.selectbox(
    "Seleccione el tipo de moldura:",
    ["Yenory 1\"", "Caja Pequeña"]
)

estilo_seleccionado = st.selectbox(
    "Seleccione el estilo de enmarcado:",
    ["Doble Vidrio", "Con Marialuisa (Cartón Blanco)"]
)

# 2. PROCESAMIENTO CON DATOS EXACTOS DE TU TALLER
if largo > 0 and ancho > 0:
    # Perímetro y Área base
    perimetro = 2 * (ancho + largo)
    area = ancho * largo
    
    # A. Asignación del costo de la moldura
    if moldura_seleccionada == "Yenory 1\"":
        cost_per_cm_moldura = 12.50
    else:  # Caja Pequeña
        cost_per_cm_moldura = 9.6875
        
    costo_moldura = cost_per_cm_moldura * (perimetro + 8)
    
    # B. Asignación según el estilo (Doble Vidrio vs Marialuisa)
    if estilo_seleccionado == "Doble Vidrio":
        costo_vidrio = 3.00 * area
        costo_carton = 0.00 * area
    else:  # Con Marialuisa
        costo_vidrio = 1.50 * area
        costo_carton = 0.6445 * area
        
    # C. Acabados fijos (Pintura Spray Negra)
    costo_pintura = 11.0544 * perimetro
    costo_papel_tapiz = 0.00
    
    # D. Costos Fijos e Insumos del Taller (Datos de tu AppSheet)
    costos_fijos_materiales = 21.1430
    mano_obra_empleado = 200.00
    
    # E. Complejidad (Ajustada a BAJA según tu indicación)
    if perimetro <= 140:
        factor_complejidad = 10
    else:
        factor_complejidad = 20
        
    costo_complejidad = factor_complejidad * perimetro
    
    # F. Suma total del Costo Base de Producción (Incluyendo costos fijos)
    costo_total_taller = (
        costo_moldura + 
        costo_vidrio + 
        costo_carton + 
        costo_pintura + 
        costo_papel_tapiz + 
        costos_fijos_materiales + 
        mano_obra_empleado + 
        costo_complejidad
    )
    
    # G. Multiplicador comercial (* 1.5) y redondeo al techo (CEILING) igual a AppSheet
    precio_regular = math.ceil(costo_total_taller * 1.5)
    
    # H. Aplicación del 20% de Descuento y Mínimo de ¢7,000
    precio_con_descuento = precio_regular * 0.80
    precio_final = max(7000.0, precio_con_descuento)
    
    # Redondeo final a la centena más cercana
    precio_redondeado = round(precio_final, -2)

    # 3. DESPLIEGUE DEL RESULTADO EN PANTALLA
    st.markdown(f"""
        <div class="price-box">
            <h3 style='margin:0; color:#666666; font-size: 15px; font-weight: normal;'>Tu precio especial es:</h3>
            <h1 style='margin:12px 0; color:#111111; font-size: 36px;'>¢{precio_redondeado:,.0f} Colones</h1>
            <p style='margin:0; color:#888888; font-size: 11px;'>*Incluye IVA y comisiones bancarias.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Por favor, ingrese dimensiones válidas en centímetros.")
