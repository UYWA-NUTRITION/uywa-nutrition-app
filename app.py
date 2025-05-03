import streamlit as st
import pandas as pd

# Mostrar imagen corporativa
st.image("uywa_logo.png", width=300, caption="UYWA Nutrition - Dietas húmedas para mascotas")

# Datos AAFCO actualizados
data = {
    "Nutriente": [
        "Proteína cruda (%)", "Grasa cruda (%)", "Arginina (%)", "Histidina (%)",
        "Isoleucina (%)", "Leucina (%)", "Lisina (%)", "Metionina (%)", "Metionina + Cistina (%)",
        "Fenilalanina (%)", "Fenilalanina + Tirosina (%)", "Treonina (%)", "Triptófano (%)",
        "Valina (%)", "Ácido linoleico (%)", "Calcio (%)", "Fósforo (%)", "Potasio (%)",
        "Sodio (%)", "Cloruro (%)", "Magnesio (%)", "Hierro (mg/kg)", "Cobre (mg/kg)",
        "Manganeso (mg/kg)", "Zinc (mg/kg)", "Yodo (mg/kg)", "Selenio (mg/kg)",
        "Vitamina A (UI/kg)", "Vitamina D (UI/kg)", "Vitamina E (UI/kg)", "Tiamina (mg/kg)",
        "Riboflavina (mg/kg)", "Ácido pantoténico (mg/kg)", "Niacina (mg/kg)",
        "Piridoxina (mg/kg)", "Ácido fólico (mg/kg)", "Vitamina B12 (mg/kg)", "Colina (mg/kg)"
    ],
    "Requerimiento_4000_kcal": [
        22.5, 5.5, 0.64, 0.24, 0.48, 0.85, 0.79, 0.41, 0.81, 0.56, 0.93, 0.60, 0.20,
        0.61, 1.1, 0.56, 0.4, 0.6, 0.08, 0.12, 0.06, 40, 7.3, 5, 80, 1, 0.35,
        5000, 500, 50, 2.25, 5.2, 12, 13.6, 1.5, 0.216, 0.028, 1360
    ]
}

df = pd.DataFrame(data)

def calcular_rer(peso_kg):
    return 70 * (peso_kg ** 0.75)

def calcular_mer(tipo_animal, peso_kg, estado):
    rer = calcular_rer(peso_kg)
    factores = {
        "PERRO": {
            "INTACTO": 1.8, "CASTRADO": 1.6, "PROPENSO_OBESIDAD": 1.4,
            "CACHORRO_MENOR_4M": 3.0, "CACHORRO_MAYOR_4M": 2.0,
        },
        "GATO": {
            "INTACTO": 1.4, "CASTRADO": 1.2, "PROPENSO_OBESIDAD": 1.0, "GATITO": 2.5,
        },
    }
    factor = factores[tipo_animal].get(estado)
    if not factor:
        raise ValueError("Estado no reconocido para el tipo de animal.")
    return rer * factor

# Inicializar session_state
if 'mer' not in st.session_state:
    st.session_state['mer'] = None

# App principal
st.title("Calculadora de Energía y Requerimientos Nutricionales")

tipo_animal = st.selectbox("Tipo de Animal", ["PERRO", "GATO"])
peso_kg = st.number_input("Peso (kg)", min_value=0.1, value=10.0)
if tipo_animal == "PERRO":
    estado = st.selectbox("Estado", ["INTACTO", "CASTRADO", "PROPENSO_OBESIDAD", "CACHORRO_MENOR_4M", "CACHORRO_MAYOR_4M"])
else:
    estado = st.selectbox("Estado", ["INTACTO", "CASTRADO", "PROPENSO_OBESIDAD", "GATITO"])

if st.button("Calcular MER"):
    try:
        mer = calcular_mer(tipo_animal, peso_kg, estado)
        st.session_state['mer'] = mer
        st.success(f"MER calculado: {mer:.2f} kcal/día")
    except ValueError as e:
        st.error(str(e))

if st.session_state['mer'] is not None:
    st.info(f"MER calculado previamente: {st.session_state['mer']:.2f} kcal/día")

    if st.button("Ajustar Nutrientes según MER"):
        mer = st.session_state['mer']
        df['Requerimiento ajustado'] = df['Requerimiento_4000_kcal'] * mer / 4000
        st.write("### Requerimientos ajustados")
        st.dataframe(df[['Nutriente', 'Requerimiento ajustado']])
        st.download_button("Descargar CSV", df[['Nutriente', 'Requerimiento ajustado']].to_csv(index=False), "requerimientos_ajustados.csv")
