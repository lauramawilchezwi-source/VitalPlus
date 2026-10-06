import streamlit as st
import numpy as np
import sqlite3
from datetime import datetime
import pandas as pd
import random
from pathlib import Path


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="VitalPulse",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# RUTAS
# =========================================================

CARPETA_PROYECTO = Path(__file__).resolve().parent

DB_PATH = CARPETA_PROYECTO / "vitalpulse.db"
MANUAL_PRELIMINAR = CARPETA_PROYECTO / "MANUAL PRELIMINAR.pdf"
MANUAL_TECNICO = CARPETA_PROYECTO / "MANUAL TECNICO.pdf"


# =========================================================
# ESTILOS
# =========================================================

st.markdown(
    """
    <style>

    /* Fondo general */
    .stApp {
        background-color: #F4F8FC;
    }

    /* Texto general */
    .stApp p,
    .stApp li,
    .stApp label {
        color: #334155;
    }

    /* Títulos */
    h1 {
        color: #0B5CAD !important;
        font-weight: 700 !important;
    }

    h2 {
        color: #0B5CAD !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #174A7E !important;
        font-weight: 600 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #EAF4FC;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0B5CAD !important;
    }

    /* Botones */
    .stButton > button {
        background-color: #0B5CAD !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        min-height: 42px;
    }

    .stButton > button:hover {
        background-color: #084A8C !important;
        color: white !important;
    }

    /* Botones de formulario */
    [data-testid="stFormSubmitButton"] button {
        background-color: #0B5CAD !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* Botones de descarga */
    .stDownloadButton > button {
        background-color: #0B5CAD !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #D7E5F2;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
    }

    [data-testid="stMetricValue"] {
        color: #0B5CAD !important;
    }

    /* Contenedores */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 16px;
        border: 1px solid #D7E5F2;
    }

    /* Separadores */
    hr {
        border-color: #D7E5F2;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# BASE DE DATOS
# =========================================================

def conectar_bd():
    return sqlite3.connect(str(DB_PATH))


def crear_base_datos():

    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            fecha_registro TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mediciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nombre TEXT,
            edad INTEGER,
            spo2 INTEGER,
            bpm INTEGER,
            estado_spo2 TEXT,
            estado_bpm TEXT,
            fecha TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pruebas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_prueba TEXT,
            resultado TEXT,
            observaciones TEXT,
            fecha TEXT
        )
        """
    )

    conexion.commit()
    conexion.close()


crear_base_datos()


# =========================================================
# FUNCIONES DE BASE DE DATOS
# =========================================================

def registrar_usuario(nombre, edad):

    conexion = conectar_bd()
    cursor = conexion.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO usuarios
        (nombre, edad, fecha_registro)
        VALUES (?, ?, ?)
        """,
        (nombre, edad, fecha)
    )

    usuario_id = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return usuario_id


def registrar_medicion(
    usuario_id,
    nombre,
    edad,
    spo2,
    bpm,
    estado_spo2,
    estado_bpm
):

    conexion = conectar_bd()
    cursor = conexion.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO mediciones
        (
            usuario_id,
            nombre,
            edad,
            spo2,
            bpm,
            estado_spo2,
            estado_bpm,
            fecha
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            usuario_id,
            nombre,
            edad,
            spo2,
            bpm,
            estado_spo2,
            estado_bpm,
            fecha
        )
    )

    conexion.commit()
    conexion.close()


def obtener_mediciones():

    conexion = conectar_bd()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            nombre,
            edad,
            spo2,
            bpm,
            estado_spo2,
            estado_bpm,
            fecha
        FROM mediciones
        ORDER BY id DESC
        """,
        conexion
    )

    conexion.close()

    return df


def registrar_prueba(nombre_prueba, resultado, observaciones):

    conexion = conectar_bd()
    cursor = conexion.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO pruebas
        (
            nombre_prueba,
            resultado,
            observaciones,
            fecha
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            nombre_prueba,
            resultado,
            observaciones,
            fecha
        )
    )

    conexion.commit()
    conexion.close()


def obtener_pruebas():

    conexion = conectar_bd()

    df = pd.read_sql_query(
        """
        SELECT
            nombre_prueba,
            resultado,
            observaciones,
            fecha
        FROM pruebas
        ORDER BY id DESC
        """,
        conexion
    )

    conexion.close()

    return df


# =========================================================
# ANÁLISIS
# =========================================================

def analizar_spo2(spo2):

    if spo2 >= 95:
        return "Normal"

    elif spo2 >= 90:
        return "Revisar"

    else:
        return "Alerta"


def analizar_bpm(bpm):

    if 60 <= bpm <= 100:
        return "Normal"

    return "Revisar"


def analizar_estado_general(estado_spo2, estado_bpm):

    if estado_spo2 == "Alerta":
        return "Alerta"

    if estado_spo2 == "Revisar" or estado_bpm == "Revisar":
        return "Revisar"

    return "Normal"


# =========================================================
# RECOMENDACIONES
# =========================================================

def obtener_recomendaciones(spo2, bpm, estado_spo2, estado_bpm):

    recomendaciones = []

    if estado_spo2 == "Normal":

        recomendaciones.append(
            "La saturación de oxígeno se encuentra dentro del rango configurado para esta simulación."
        )

    elif estado_spo2 == "Revisar":

        recomendaciones.append(
            "La saturación de oxígeno está por debajo del rango normal configurado."
        )

        recomendaciones.append(
            "Se recomienda repetir la medición y verificar la correcta colocación del sensor."
        )

    else:

        recomendaciones.append(
            "La saturación de oxígeno se encuentra en un rango de alerta dentro de la simulación."
        )

        recomendaciones.append(
            "Se recomienda repetir la medición y comprobar la posición del sensor."
        )

    if estado_bpm == "Normal":

        recomendaciones.append(
            "La frecuencia cardíaca se encuentra dentro del rango configurado."
        )

    else:

        if bpm < 60:

            recomendaciones.append(
                "La frecuencia cardíaca está por debajo del rango configurado."
            )

        elif bpm > 100:

            recomendaciones.append(
                "La frecuencia cardíaca está por encima del rango configurado."
            )

        recomendaciones.append(
            "Se recomienda repetir la medición para verificar el resultado."
        )

    return recomendaciones


# =========================================================
# SIMULACIÓN
# =========================================================

def actualizar_medicion(modo):

    if modo == "Aleatorio":

        tipo = random.choices(
            [
                "normal",
                "spo2_revisar",
                "spo2_alerta",
                "bpm_bajo",
                "bpm_alto"
            ],
            weights=[
                70,
                15,
                10,
                2.5,
                2.5
            ],
            k=1
        )[0]

    else:

        tipo = modo

    # -------------------------
    # NORMAL
    # -------------------------

    if tipo == "normal":

        spo2 = random.randint(95, 100)
        bpm = random.randint(60, 100)

    # -------------------------
    # SPO2 BAJA
    # -------------------------

    elif tipo == "spo2_revisar":

        spo2 = random.randint(90, 94)
        bpm = random.randint(60, 100)

    # -------------------------
    # SPO2 CRÍTICA
    # -------------------------

    elif tipo == "spo2_alerta":

        spo2 = random.randint(85, 89)
        bpm = random.randint(60, 100)

    # -------------------------
    # BPM BAJO
    # -------------------------

    elif tipo == "bpm_bajo":

        spo2 = random.randint(95, 100)
        bpm = random.randint(45, 59)

    # -------------------------
    # BPM ALTO
    # -------------------------

    elif tipo == "bpm_alto":

        spo2 = random.randint(95, 100)
        bpm = random.randint(101, 120)

    else:

        spo2 = random.randint(95, 100)
        bpm = random.randint(60, 100)

    estado_spo2 = analizar_spo2(spo2)
    estado_bpm = analizar_bpm(bpm)

    return spo2, bpm, estado_spo2, estado_bpm


# =========================================================
# SEÑAL PPG
# =========================================================

def generar_senal_ppg(bpm, cantidad=240):

    tiempo = np.linspace(0, 8, cantidad)

    frecuencia = bpm / 60

    senal = (
        0.8 * np.sin(2 * np.pi * frecuencia * tiempo)
        + 0.20 * np.sin(4 * np.pi * frecuencia * tiempo)
        + 0.05 * np.random.randn(cantidad)
    )

    return senal


# =========================================================
# ESTADO DE LA APLICACIÓN
# =========================================================

if "monitoreo_activo" not in st.session_state:
    st.session_state.monitoreo_activo = False

if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "edad" not in st.session_state:
    st.session_state.edad = 18

if "spo2" not in st.session_state:
    st.session_state.spo2 = 98

if "bpm" not in st.session_state:
    st.session_state.bpm = 75

if "estado_spo2" not in st.session_state:
    st.session_state.estado_spo2 = "Normal"

if "estado_bpm" not in st.session_state:
    st.session_state.estado_bpm = "Normal"

if "ultima_actualizacion" not in st.session_state:
    st.session_state.ultima_actualizacion = ""


# =========================================================
# BARRA LATERAL
# =========================================================

with st.sidebar:

    st.title("💙 VitalPulse")

    st.caption(
        "Plataforma inteligente para simulación, "
        "visualización y análisis de señales biomédicas."
    )

    st.divider()

    pagina = st.radio(
        "Navegación",
        [
            "🏠 Inicio",
            "🫁 Monitoreo",
            "📊 Historial",
            "📚 Biblioteca técnica",
            "📖 Manuales",
            "🧪 Registro de pruebas"
        ]
    )

    st.divider()

    st.caption("Proyecto académico")
    st.caption("ESP32 + MAX30102 + Streamlit")


# =========================================================
# INICIO
# =========================================================

if pagina == "🏠 Inicio":

    st.title("VitalPulse")

    st.subheader(
        "Plataforma inteligente para simulación, visualización "
        "y análisis de señales biomédicas"
    )

    st.write(
        "Sistema académico desarrollado para integrar adquisición, "
        "visualización, almacenamiento y análisis básico de datos "
        "provenientes de un pulsioxímetro."
    )

    st.divider()

    # -------------------------
    # MÓDULOS
    # -------------------------

    st.subheader("Módulos principales")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.subheader("🫁 Monitoreo")

            st.write(
                "Permite visualizar valores simulados de saturación "
                "de oxígeno y frecuencia cardíaca."
            )

    with col2:

        with st.container(border=True):

            st.subheader("📈 Señales")

            st.write(
                "Genera una representación simulada de una señal "
                "fotopletismográfica (PPG)."
            )

    with col3:

        with st.container(border=True):

            st.subheader("🤖 Análisis")

            st.write(
                "Clasifica los resultados y genera recomendaciones "
                "básicas según los rangos configurados."
            )

    st.divider()

    # -------------------------
    # ESTADO DEL SISTEMA
    # -------------------------

    st.subheader("Estado del sistema")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Sistema",
            "Operativo"
        )

    with col2:
        st.metric(
            "Sensor",
            "MAX30102"
        )

    with col3:
        st.metric(
            "Controlador",
            "ESP32"
        )

    st.divider()

    # -------------------------
    # ACERCA DEL PROYECTO
    # -------------------------

    with st.container(border=True):

        st.subheader("💡 Acerca del proyecto")

        st.write(
            "VitalPulse es una plataforma académica orientada "
            "a la simulación, visualización y análisis de señales "
            "biomédicas."
        )

        st.write(
            "El sistema integra un ESP32, un sensor MAX30102 "
            "y una interfaz desarrollada con Streamlit."
        )

        st.write(
            "La plataforma permite registrar usuarios, "
            "visualizar mediciones, consultar el historial "
            "y almacenar pruebas realizadas durante "
            "el desarrollo del prototipo."
        )

    st.info(
        "Nota: las mediciones mostradas actualmente corresponden "
        "a una simulación académica y no representan una medición clínica."
    )


# =========================================================
# MONITOREO
# =========================================================

elif pagina == "🫁 Monitoreo":

    st.title("Monitoreo biomédico")

    st.write(
        "En esta sección se simulan las mediciones de SpO₂ y "
        "frecuencia cardíaca para demostrar el funcionamiento "
        "del sistema de análisis."
    )

    st.divider()

    # -------------------------
    # DATOS DEL USUARIO
    # -------------------------

    st.subheader("Datos del usuario")

    col1, col2 = st.columns(2)

    with col1:

        nombre = st.text_input(
            "Nombre",
            value=st.session_state.nombre,
            placeholder="Ingrese el nombre"
        )

    with col2:

        edad = st.number_input(
            "Edad",
            min_value=1,
            max_value=120,
            value=st.session_state.edad,
            step=1
        )

    # -------------------------
    # MODO DE SIMULACIÓN
    # -------------------------

    st.subheader("Modo de simulación")

    modo_simulacion = st.selectbox(
        "Seleccione el tipo de medición",
        [
            "Aleatorio",
            "normal",
            "spo2_revisar",
            "spo2_alerta",
            "bpm_bajo",
            "bpm_alto"
        ],
        format_func=lambda x: {
            "Aleatorio": "🎲 Aleatorio",
            "normal": "🟢 Valores normales",
            "spo2_revisar": "🟡 SpO₂ baja - Revisar",
            "spo2_alerta": "🔴 SpO₂ crítica - Alerta",
            "bpm_bajo": "🟡 BPM bajo - Revisar",
            "bpm_alto": "🟡 BPM alto - Revisar"
        }[x]
    )

    st.caption(
        "El modo aleatorio genera diferentes condiciones para "
        "demostrar el análisis automático."
    )

    # -------------------------
    # BOTONES
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:

        iniciar = st.button(
            "▶️ Iniciar monitoreo",
            use_container_width=True
        )

    with col2:

        detener = st.button(
            "⏹️ Detener monitoreo",
            use_container_width=True
        )

    if iniciar:

        if nombre.strip() == "":

            st.warning(
                "Ingrese el nombre del usuario antes de iniciar."
            )

        else:

            st.session_state.nombre = nombre.strip()
            st.session_state.edad = edad

            st.session_state.usuario_id = registrar_usuario(
                nombre.strip(),
                edad
            )

            (
                st.session_state.spo2,
                st.session_state.bpm,
                st.session_state.estado_spo2,
                st.session_state.estado_bpm
            ) = actualizar_medicion(modo_simulacion)

            st.session_state.monitoreo_activo = True

            st.session_state.ultima_actualizacion = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            st.success("Monitoreo iniciado correctamente.")

    if detener:

        st.session_state.monitoreo_activo = False

        st.info("Monitoreo detenido.")

    # -------------------------
    # MONITOREO ACTIVO
    # -------------------------

    if st.session_state.monitoreo_activo:

        st.divider()

        st.success("🟢 Monitoreo activo")

        # Actualización manual
        if st.button(
            "🔄 Generar nueva medición",
            use_container_width=True
        ):

            (
                st.session_state.spo2,
                st.session_state.bpm,
                st.session_state.estado_spo2,
                st.session_state.estado_bpm
            ) = actualizar_medicion(modo_simulacion)

            st.session_state.ultima_actualizacion = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        spo2 = st.session_state.spo2
        bpm = st.session_state.bpm

        estado_spo2 = st.session_state.estado_spo2
        estado_bpm = st.session_state.estado_bpm

        estado_general = analizar_estado_general(
            estado_spo2,
            estado_bpm
        )

        # -------------------------
        # MEDICIONES
        # -------------------------

        st.subheader("Mediciones actuales")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "SpO₂",
                f"{spo2} %"
            )

        with col2:

            st.metric(
                "Frecuencia cardíaca",
                f"{bpm} BPM"
            )

        with col3:

            st.metric(
                "Estado general",
                estado_general
            )

        st.caption(
            f"Última actualización: "
            f"{st.session_state.ultima_actualizacion}"
        )

        # -------------------------
        # ESTADO
        # -------------------------

        if estado_general == "Normal":

            st.success(
                "🟢 Estado normal: los valores están dentro "
                "de los rangos configurados."
            )

        elif estado_general == "Revisar":

            st.warning(
                "🟡 Estado revisar: uno o más valores están "
                "fuera del rango normal configurado."
            )

        else:

            st.error(
                "🔴 Estado de alerta: la SpO₂ está en un rango "
                "de alerta dentro de esta simulación."
            )

        # -------------------------
        # GRÁFICA PPG
        # -------------------------

        st.divider()

        with st.container(border=True):

            st.subheader("📈 Señal fotopletismográfica (PPG)")

            st.write(
                "Representación simulada de una señal PPG asociada "
                "a la frecuencia cardíaca obtenida."
            )

            senal = generar_senal_ppg(bpm)

            df_ppg = pd.DataFrame(
                {
                    "Señal PPG": senal
                }
            )

            st.line_chart(
                df_ppg,
                height=350
            )

        # -------------------------
        # ANÁLISIS
        # -------------------------

        st.divider()

        with st.container(border=True):

            st.subheader("🤖 Análisis inteligente")

            st.write(
                f"Clasificación de SpO₂: **{estado_spo2}**"
            )

            st.write(
                f"Clasificación de BPM: **{estado_bpm}**"
            )

            st.write(
                f"Clasificación general: **{estado_general}**"
            )

        # -------------------------
        # RECOMENDACIONES
        # -------------------------

        st.subheader("💡 Recomendaciones")

        recomendaciones = obtener_recomendaciones(
            spo2,
            bpm,
            estado_spo2,
            estado_bpm
        )

        for recomendacion in recomendaciones:

            st.info(
                recomendacion
            )

        # -------------------------
        # GUARDAR
        # -------------------------

        st.divider()

        if st.button(
            "💾 Guardar medición",
            use_container_width=True
        ):

            registrar_medicion(
                st.session_state.usuario_id,
                st.session_state.nombre,
                st.session_state.edad,
                spo2,
                bpm,
                estado_spo2,
                estado_bpm
            )

            st.success(
                "La medición fue guardada correctamente en la base de datos."
            )

    else:

        st.info(
            "Ingrese los datos del usuario y presione "
            "«Iniciar monitoreo» para comenzar."
        )


# =========================================================
# HISTORIAL
# =========================================================

elif pagina == "📊 Historial":

    st.title("Historial de mediciones")

    st.write(
        "Consulta de las mediciones almacenadas durante "
        "las pruebas del sistema."
    )

    df = obtener_mediciones()

    if df.empty:

        st.info(
            "Todavía no existen mediciones almacenadas."
        )

    else:

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total de mediciones",
                len(df)
            )

        with col2:

            st.metric(
                "SpO₂ promedio",
                f"{df['spo2'].mean():.1f} %"
            )

        with col3:

            st.metric(
                "BPM promedio",
                f"{df['bpm'].mean():.1f}"
            )

        st.divider()

        # -------------------------
        # GRÁFICA SPO2
        # -------------------------

        st.subheader("📈 Evolución de SpO₂")

        df_spo2 = df.copy()

        df_spo2["Medición"] = range(
            len(df_spo2),
            0,
            -1
        )

        df_spo2 = df_spo2.sort_values(
            "Medición"
        )

        st.line_chart(
            df_spo2.set_index("Medición")["spo2"],
            height=300
        )

        # -------------------------
        # GRÁFICA BPM
        # -------------------------

        st.subheader("❤️ Evolución de frecuencia cardíaca")

        st.line_chart(
            df_spo2.set_index("Medición")["bpm"],
            height=300
        )

        # -------------------------
        # TABLA
        # -------------------------

        st.subheader("📋 Registro")

        tabla = df.rename(
            columns={
                "id": "ID",
                "nombre": "Usuario",
                "edad": "Edad",
                "spo2": "SpO₂ (%)",
                "bpm": "BPM",
                "estado_spo2": "Estado SpO₂",
                "estado_bpm": "Estado BPM",
                "fecha": "Fecha"
            }
        )

        st.dataframe(
            tabla,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# BIBLIOTECA TÉCNICA
# =========================================================

elif pagina == "📚 Biblioteca técnica":

    st.title("Biblioteca técnica")

    st.write(
        "Información técnica de los principales componentes "
        "y conceptos utilizados en VitalPulse."
    )

    st.divider()

    with st.expander("🔵 ESP32", expanded=True):

        st.write(
            "Microcontrolador utilizado como unidad principal "
            "de control y adquisición de datos."
        )

        st.write(
            "**Función:** recibir y procesar los datos provenientes "
            "del sensor MAX30102."
        )

    with st.expander("🔴 Sensor MAX30102"):

        st.write(
            "Sensor óptico utilizado para obtener información "
            "relacionada con la señal PPG, saturación de oxígeno "
            "y frecuencia cardíaca."
        )

        st.write(
            "**Comunicación:** I²C."
        )

        st.write(
            "**Dirección utilizada:** 0x57."
        )

    with st.expander("📈 Señal PPG"):

        st.write(
            "La fotopletismografía o PPG es una técnica óptica "
            "que permite detectar cambios en el volumen sanguíneo."
        )

        st.write(
            "En VitalPulse se utiliza una señal PPG simulada "
            "para representar visualmente el comportamiento "
            "de la señal biomédica."
        )

    with st.expander("🫁 Saturación de oxígeno - SpO₂"):

        st.write(
            "La SpO₂ representa una estimación de la saturación "
            "de oxígeno en la sangre."
        )

        st.write(
            "Para esta simulación académica se configuraron "
            "los siguientes rangos:"
        )

        st.write(
            "• 95 % o superior: Normal"
        )

        st.write(
            "• 90 % a 94 %: Revisar"
        )

        st.write(
            "• Menor de 90 %: Alerta"
        )

    with st.expander("❤️ Frecuencia cardíaca"):

        st.write(
            "La frecuencia cardíaca representa el número de "
            "latidos por minuto."
        )

        st.write(
            "Para esta simulación se configuró:"
        )

        st.write(
            "• 60 a 100 BPM: Normal"
        )

        st.write(
            "• Menor de 60 o mayor de 100 BPM: Revisar"
        )

    with st.expander("💻 Software"):

        st.write(
            "La plataforma utiliza Python y Streamlit para "
            "la construcción de la interfaz."
        )

        st.write(
            "SQLite se utiliza para almacenar usuarios, "
            "mediciones y registros de pruebas."
        )

    with st.expander("🔄 Flujo general del sistema"):

        st.write(
            "MAX30102 → ESP32 → procesamiento → interfaz "
            "VitalPulse → análisis → recomendaciones → base de datos"
        )


# =========================================================
# MANUALES
# =========================================================

elif pagina == "📖 Manuales":

    st.title("Manuales")

    st.write(
        "Documentación disponible para el funcionamiento "
        "y desarrollo del proyecto."
    )

    st.divider()

    # -------------------------
    # MANUAL PRELIMINAR
    # -------------------------

    with st.container(border=True):

        st.subheader("📄 Manual preliminar")

        st.write(
            "Documento con información general para la "
            "utilización de la plataforma."
        )

        if MANUAL_PRELIMINAR.exists():

            with open(
                MANUAL_PRELIMINAR,
                "rb"
            ) as archivo:

                st.download_button(
                    label="⬇️ Descargar manual preliminar",
                    data=archivo,
                    file_name="MANUAL PRELIMINAR.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        else:

            st.warning(
                "No se encontró el archivo MANUAL PRELIMINAR.pdf "
                "en la carpeta del proyecto."
            )

    st.write("")

    # -------------------------
    # MANUAL TÉCNICO
    # -------------------------

    with st.container(border=True):

        st.subheader("📘 Manual técnico")

        st.write(
            "Documento con información técnica relacionada "
            "con el sistema y sus componentes."
        )

        if MANUAL_TECNICO.exists():

            with open(
                MANUAL_TECNICO,
                "rb"
            ) as archivo:

                st.download_button(
                    label="⬇️ Descargar manual técnico",
                    data=archivo,
                    file_name="MANUAL TECNICO.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        else:

            st.warning(
                "No se encontró el archivo MANUAL TECNICO.pdf "
                "en la carpeta del proyecto."
            )


# =========================================================
# REGISTRO DE PRUEBAS
# =========================================================

elif pagina == "🧪 Registro de pruebas":

    st.title("Registro de pruebas")

    st.write(
        "Registro de las pruebas realizadas durante el "
        "desarrollo y validación del prototipo."
    )

    st.divider()

    with st.form("formulario_prueba"):

        nombre_prueba = st.text_input(
            "Nombre de la prueba",
            placeholder="Ejemplo: Prueba de sensor MAX30102"
        )

        resultado = st.selectbox(
            "Resultado",
            [
                "Exitoso",
                "Parcial",
                "Fallido"
            ]
        )

        observaciones = st.text_area(
            "Observaciones",
            placeholder="Describa brevemente el resultado de la prueba."
        )

        enviar = st.form_submit_button(
            "💾 Registrar prueba",
            use_container_width=True
        )

        if enviar:

            if nombre_prueba.strip() == "":

                st.warning(
                    "Ingrese el nombre de la prueba."
                )

            else:

                registrar_prueba(
                    nombre_prueba.strip(),
                    resultado,
                    observaciones.strip()
                )

                st.success(
                    "La prueba fue registrada correctamente."
                )

    st.divider()

    st.subheader("📋 Pruebas registradas")

    df_pruebas = obtener_pruebas()

    if df_pruebas.empty:

        st.info(
            "Todavía no existen pruebas registradas."
        )

    else:

        tabla_pruebas = df_pruebas.rename(
            columns={
                "nombre_prueba": "Prueba",
                "resultado": "Resultado",
                "observaciones": "Observaciones",
                "fecha": "Fecha"
            }
        )

        st.dataframe(
            tabla_pruebas,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.divider()

st.caption(
    "VitalPulse · Proyecto académico de Ingeniería Biomédica · "
    "ESP32 + MAX30102 + Streamlit"
)

st.caption(
    "Las mediciones y recomendaciones mostradas corresponden "
    "a una simulación académica."
)