import streamlit as st
import pandas as pd
import math

# ======================================================
# CONFIGURACION
# ======================================================

st.set_page_config(
    page_title="Factor de Condición",
    page_icon="📋",
    layout="wide"
)

# ======================================================
# ESTILOS
# ======================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.ventana-titulo {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #1f4e79;
}

.resultado {
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

.valor-puntaje {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: #1f4e79;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* TITULO DEL CRITERIO */
label[data-testid="stWidgetLabel"] p {
    font-size: 18px !important;
    font-weight: bold !important;
}

/* OPCIONES DEL RADIO */
div[role="radiogroup"] label {
    font-size: 18px !important;
    white-space: normal !important;
    line-height: 1.4 !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# TITULO
# ======================================================

st.title("📋 Evaluación de Factor de Condición")
st.markdown("---")

# ======================================================
# DATOS GENERALES
# ======================================================

d1, d2, d3 = st.columns(3)

with d1:
    fecha = st.text_input("Fecha")

with d2:
    fase = st.text_input("Fase")

with d3:
    nivel = st.text_input("Nivel")

st.markdown("---")

# ======================================================
# VENTANAS
# ======================================================

if "num_ventanas" not in st.session_state:
    st.session_state.num_ventanas = 3

c1, c2 = st.columns(2)

with c1:
    if st.button("➕ Agregar ventana"):
        st.session_state.num_ventanas += 1

with c2:
    if st.button("🗑️ Borrar ventana"):
        if st.session_state.num_ventanas > 1:
            st.session_state.num_ventanas -= 1

st.markdown("---")

# ======================================================
# FUNCIONES
# ======================================================

def parse_coord(valor):
    if valor.strip() == "":
        return 0.0
    try:
        return round(float(valor), 3)
    except:
        return 0.0

def calcular_longitud(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

# ======================================================
# COORDENADAS
# ======================================================

num_coords = st.session_state.num_ventanas + 1
coord_cols = st.columns(num_coords)

coordenadas = []

for i in range(num_coords):

    if i == 0:
        titulo = "Inicio V1"
    elif i == num_coords - 1:
        titulo = f"Fin V{num_coords-1}"
    else:
        titulo = f"Fin V{i} / Inicio V{i+1}"

    with coord_cols[i]:

        st.markdown(
            f"""
            <h4 style="
                text-align:center;
                color:#1f4e79;
                margin-bottom:15px;
                margin-top:10px;
            ">
                {titulo}
            </h4>
            """,
            unsafe_allow_html=True
        )

        x_txt = st.text_input(
            f"E {i}",
            key=f"x_{i}",
            placeholder="0.000"
        )

        y_txt = st.text_input(
            f"N {i}",
            key=f"y_{i}",
            placeholder="0.000"
        )

        x = parse_coord(x_txt)
        y = parse_coord(y_txt)

        coordenadas.append((x, y))

# ======================================================
# LONGITUDES
# ======================================================

cols_longitudes = st.columns(st.session_state.num_ventanas)

for i in range(st.session_state.num_ventanas):

    x1, y1 = coordenadas[i]
    x2, y2 = coordenadas[i + 1]

    longitud = calcular_longitud((x1, y1), (x2, y2))

    with cols_longitudes[i]:

        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:24px;
                font-weight:bold;
                color:#1f4e79;
                margin-bottom:35px;
            ">
                L{i+1} = {longitud:.2f} m
            </div>
            """,
            unsafe_allow_html=True
        )

# ======================================================
# CRITERIOS
# ======================================================

criterios = {

    "Medias cañas (20%)": {
        "Muy Bueno (más de 80%)": 20,
        "Bueno (70-80%)": 15,
        "Bueno (60-70%)": 12,
        "Regular (50-60%)": 8,
        "Malo (30-50%)": 5,
        "Muy Malo (10-30%)": 2,
        "Muy Malo (menos de 10%)": 0
    },

    "Grietas inducidas en roca intacta (15%)": {
        "Muy Bueno (menos de 1 por m3)": 15,
        "Bueno (2 por m3)": 13,
        "Regular (3 por m3)": 7,
        "Malo (4 por m3)": 3,
        "Muy Malo (más de 5 por m3)": 0
    },

    "Discontinuidades abiertas (10%)": {
        "Muy Bueno (todo cerrado)": 10,
        "Bueno": 8,
        "Regular": 5,
        "Malo": 2,
        "Muy Malo (muchas abiertas)": 0
    },

    "Bloques inestables (20%)": {
        "Muy Bueno (sin bloques)": 20,
        "Bueno (algunos bloques pequeños)": 15,
        "Regular (bloques grandes)": 10,
        "Malo (muchos bloques)": 0
    },

    "Geometría del Talud (20%)": {
        "Muy Bueno (recto)": 20,
        "Bueno (TOE duro)": 10,
        "Regular (cresta saliente)": 5,
        "Malo (irregular)": 0
    },

    "Condición de Cresta (15%)": {
        "Muy Bueno (logrado)": 15,
        "Bueno (menos de 1m de pérdida)": 12,
        "Regular (1-2m de pérdida)": 10,
        "Malo (2-3m de pérdida)": 5,
        "Muy Malo (mayor de 3m de pérdida)": 0
    }
}

# ======================================================
# EVALUACION
# ======================================================

columnas = st.columns(st.session_state.num_ventanas)

resultados_totales = []

for idx in range(st.session_state.num_ventanas):

    ventana = f"V{idx+1}"

    i1 = idx
    i2 = idx + 1

    x1, y1 = coordenadas[i1]
    x2, y2 = coordenadas[i2]

    longitud = calcular_longitud((x1, y1), (x2, y2))

    resultados = {}

    with columnas[idx]:

        st.markdown(
            f'<div class="ventana-titulo">{ventana}</div>',
            unsafe_allow_html=True
        )

        for criterio, opciones in criterios.items():

            criterio_id = f"{ventana}_{criterio}"

            seleccion = st.radio(
                criterio,
                list(opciones.keys()),
                key=f"select_{criterio_id}"
            )

            valor_base = opciones[seleccion]

            usar_manual = st.checkbox(
                "Valor específico",
                key=f"manual_{criterio_id}"
            )

            max_valor = max(opciones.values())

            valor_final = valor_base

            if usar_manual:

                valor_manual = st.number_input(
                    "Ingrese valor",
                    min_value=0.0,
                    step=0.1,
                    format="%.1f",
                    key=f"manual_input_{criterio_id}"
                )

                if valor_manual > max_valor:

                    st.markdown(
                        """
                        <style>
                        div[data-baseweb="input"] input {
                            border: 2px solid red !important;
                            background-color: #ffe6e6 !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    st.error(f"El valor máximo permitido es {max_valor}")
                    valor_final = 0

                else:
                    valor_final = round(valor_manual, 1)

            st.markdown(
                f"""
                <div class="valor-puntaje">
                    {valor_final}
                </div>
                """,
                unsafe_allow_html=True
            )

            resultados[criterio] = valor_final

        total_fc = sum(float(v) for v in resultados.values())

        if total_fc >= 70:
            clasificacion = "BUENO"
            color = "#28a745"

        elif total_fc >= 45:
            clasificacion = "REGULAR"
            color = "#ffc107"

        else:
            clasificacion = "MALO"
            color = "#dc3545"

        st.markdown(
            f"""
            <div class="resultado" style="background-color:{color};">
                FC ({ventana}) = {total_fc:.1f}<br>
                {clasificacion}
            </div>
            """,
            unsafe_allow_html=True
        )

        resultados_totales.append({
            "VENTANA": ventana,
            "E_INICIO": x1,
            "N_INICIO": y1,
            "E_FIN": x2,
            "N_FIN": y2,
            "LONGITUD_M": round(longitud, 2),
            **resultados,
            "FACTOR_CONDICIÓN": total_fc,
            "CLASIFICACION": clasificacion
        })

# ======================================================
# EXPORTAR
# ======================================================

st.markdown("---")

df_export = pd.DataFrame(resultados_totales)

csv_texto = f"FECHA,{fecha}\nFASE,{fase}\nNIVEL,{nivel}\n\n"

csv_texto += df_export.to_csv(index=False)

st.download_button(
    "⬇ Descargar CSV",
    data=csv_texto,
    file_name="factor_condicion.csv",
    mime="text/csv"
)

