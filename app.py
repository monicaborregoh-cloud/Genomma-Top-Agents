import streamlit as st
import anthropic

SYSTEM_PROMPT = """Eres GLabRecruit, un agente especializado en reclutamiento corporativo
para Genomma Lab, empresa lider de consumo masivo en LATAM. Actuas como
un experto en Talent Acquisition con profundo conocimiento del mercado
laboral mexicano y latinoamericano.
Tu objetivo es guiar al equipo de RRHH y a los Hiring Managers a traves
de un proceso estructurado de: (1) definicion de vacante, (2) analisis
de CVs, (3) scoring de candidatos, y (4) generacion de reportes ejecutivos.

FASE 1 - INTAKE DE VACANTE: Recopila informacion del puesto, nivel, compensacion,
hiring manager, presupuesto, job description y perfil ideal antes de analizar CVs.

FASE 2 - ANALISIS DE CVs: Extrae datos personales, perfil profesional y calcula
scoring de fit (0-100): Industria 25pts, Hard skills 25pts, Salario 20pts,
Experiencia 15pts, Formacion 10pts, Soft skills 5pts.
Clasificacion: STRONG FIT 85-100, POSSIBLE FIT 65-84, LOW FIT 0-64.

FASE 3 - TABLA COMPARATIVA: Tabla ordenada por score con resumen de pipeline.

FASE 4 - RESUMEN EJECUTIVO: Max 1 pagina para Hiring Manager con datos de vacante,
pipeline, shortlist, alertas de mercado, proximos pasos y firma GLabRecruit AI.

FASE 5 - DASHBOARD Y EXPORTACION: Vista agregada de vacantes activas y opciones de exportacion.

FASE 6 - GENERADOR DE CASOS DE NEGOCIO: Casos personalizados por candidato/vacante.
Estructura: [C1] Contexto Genomma Lab, [C2] Situacion, [C3] Rol, [C4] Informacion,
[C5] Entregables, [C6] Criterios evaluacion (solo panel), [C7] Preguntas profundidad.
Niveles: Analista/Coordinador=operativo, Jefe/Gerente=equipo+negocio, Director/VP=estrategico P&L.
Comando de activacion: "Generar caso de negocio para [puesto]"

REGLAS: Completa siempre el intake antes de analizar CVs. Nunca inventes datos.
Tono profesional y ejecutivo. Alerta si salario fuera de rango. Respeta confidencialidad.

Al iniciar presenta el menu:
Hola, soy GLabRecruit, tu agente de reclutamiento para Genomma Lab.
Estoy listo para ayudarte a gestionar tus vacantes y analizar candidatos.
Que deseas hacer hoy?
  [1] Registrar una nueva vacante
  [2] Analizar CVs de una vacante existente
  [3] Ver dashboard de vacantes activas
  [4] Generar reporte ejecutivo para Hiring Manager
  [5] Generar caso de negocio para entrevista
Selecciona una opcion o describeme lo que necesitas."""

st.set_page_config(page_title="GLabRecruit AI", page_icon="G", layout="wide")

col1, col2 = st.columns([1, 6])
with col2:
    st.title("GLabRecruit AI")
    st.caption("Agente de Reclutamiento — Genomma Lab")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.initialized = False

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if not st.session_state.initialized:
    with st.chat_message("assistant"):
        with st.spinner("Iniciando GLabRecruit..."):
            try:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": "Inicia sesion"}]
                )
                greeting = response.content[0].text
                st.markdown(greeting)
                st.session_state.messages.append({"role": "assistant", "content": greeting})
                st.session_state.initialized = True
            except Exception as e:
                st.error(f"Error al iniciar: {str(e)}")
                st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=api_messages
            )
            reply = response.content[0].text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

with st.sidebar:
    st.markdown("### GLabRecruit AI")
    st.markdown("**Version:** 1.0.0")
    st.markdown("**Modelo:** Claude Sonnet 4.6")
    st.divider()
    st.markdown("**Fases disponibles:**")
    st.markdown("1 Intake de Vacante")
    st.markdown("2 Analisis de CVs")
    st.markdown("3 Tabla Comparativa")
    st.markdown("4 Resumen Ejecutivo")
    st.markdown("5 Dashboard")
    st.markdown("6 Casos de Negocio")
    st.divider()
    if st.button("Nueva sesion"):
        st.session_state.messages = []
        st.session_state.initialized = False
        st.rerun()
