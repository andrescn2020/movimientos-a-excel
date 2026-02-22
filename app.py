import streamlit as st
import io
from pathlib import Path
from extractor_movimientos import parsear_archivo, crear_excel

# --- Page Config ---
st.set_page_config(
    page_title="Comprobantes a Excel",
    page_icon="⬡",
    layout="centered"
)

# --- Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg:        #0d0f14;
    --surface:   #141720;
    --border:    #252935;
    --accent:    #e8c84a;
    --accent2:   #4ae8a0;
    --text:      #e4e8f0;
    --muted:     #6b7280;
    --danger:    #f87171;
    --radius:    10px;
}

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background-color: var(--bg) !important;
    font-family: 'Syne', sans-serif;
    color: var(--text);
}

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 680px !important;
}

h1, h2, h3, h4, p, span, div, label {
    color: var(--text) !important;
}

/* Header */
.etl-logo {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.35em;
    color: var(--accent) !important;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.8rem;
}
.etl-title {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800;
    font-size: 2.8rem !important;
    line-height: 1.4;
    color: var(--text) !important;
    text-align: center;
    margin: 0 0 0.5rem !important;
}
.etl-title span { color: var(--accent) !important; }
.etl-subtitle {
    font-size: 0.85rem;
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.05em;
    text-align: center;
}
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.8rem 0;
}

/* Cards */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}
.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: var(--accent) !important;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* File uploader */
[data-testid="stFileUploader"] > div {
    background: #0a0c10 !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: var(--accent) !important;
}
.stFileUploader label, [data-testid="stFileUploader"] label {
    color: var(--muted) !important;
}
.stFileUploader button {
    background: var(--surface) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}
.stFileUploader button:hover {
    border-color: var(--accent) !important;
}

/* Checkbox */
.stCheckbox label span { color: var(--text) !important; }
[data-testid="stCheckbox"] > label > div {
    border-color: var(--border) !important;
}

/* Main action button */
.stButton > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: #0a0c10 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    letter-spacing: 0.08em;
    height: 3.2em !important;
    margin-top: 0.5rem;
    transition: all 0.18s ease !important;
    box-shadow: 0 0 20px rgba(232,200,74,0.15);
    text-shadow: none !important;
    -webkit-text-fill-color: #0a0c10 !important;
}
.stButton > button:hover {
    background: #f5d84e !important;
    box-shadow: 0 0 30px rgba(232,200,74,0.3) !important;
    transform: translateY(-1px);
}
.stButton > button:active { transform: translateY(0); }

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--accent2) !important;
    border: 1.5px solid var(--accent2) !important;
    border-radius: var(--radius) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.06em;
    width: 100% !important;
    height: 3em !important;
    margin-top: 0.8rem;
    transition: all 0.18s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(74,232,160,0.08) !important;
    box-shadow: 0 0 20px rgba(74,232,160,0.2) !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
}
.stSuccess > div {
    background: rgba(74,232,160,0.07) !important;
    border: 1px solid rgba(74,232,160,0.25) !important;
}
.stSuccess p, .stSuccess span, .stSuccess strong { color: var(--accent2) !important; }

.stError > div {
    background: rgba(248,113,113,0.07) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
}
.stError p, .stError span { color: var(--danger) !important; }

.stWarning > div {
    background: rgba(232,200,74,0.07) !important;
    border: 1px solid rgba(232,200,74,0.25) !important;
}
.stWarning p, .stWarning span { color: var(--accent) !important; }

.stInfo > div {
    background: rgba(99,122,255,0.07) !important;
    border: 1px solid rgba(99,122,255,0.3) !important;
}
.stInfo p, .stInfo span, .stInfo strong { color: #a5b4fc !important; }

/* Spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Stats row */
.stats-row {
    display: flex;
    gap: 0.8rem;
    margin-top: 1rem;
}
.stat-chip {
    flex: 1;
    background: #0a0c10;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.7rem 0.5rem;
    text-align: center;
}
.stat-chip .stat-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent) !important;
    display: block;
}
.stat-chip .stat-lbl {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: var(--muted) !important;
    text-transform: uppercase;
    display: block;
    margin-top: 0.2rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

/* Footer */
.etl-footer {
    text-align: center;
    padding-top: 2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: var(--muted) !important;
    letter-spacing: 0.15em;
}
</style>
""", unsafe_allow_html=True)


# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div>
    <h1 class="etl-title">Movimientos a<span> Excel</span></h1>
    <p class="etl-subtitle">TXT / PRN  →  XLSX</p>
</div>
<hr class="divider">
""", unsafe_allow_html=True)


# ─── Card 01: Archivo ──────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-label">01 · Archivo fuente</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Arrastrá tu archivo o hacé click para seleccionarlo",
    type=["txt", "prn"],
    label_visibility="visible"
)
st.markdown('</div>', unsafe_allow_html=True)


# ─── Card 02: Opciones ─────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-label">02 · Opciones de exportación</div>', unsafe_allow_html=True)
con_resumenes = st.checkbox(
    "Incluir hojas de resumen",
    value=False,
    help="Genera hojas adicionales: Resumen x Impuesto, x Tipo, x Concepto, x Proveedor, Mayor x Proveedor."
)
st.markdown('</div>', unsafe_allow_html=True)


# ─── Card 03: Procesar ─────────────────────────────────────────────────────────
if uploaded_file is not None:
    filename = Path(uploaded_file.name).stem
    st.success(f"**{uploaded_file.name}** listo para procesar")

    st.markdown('<div class="card"><div class="card-label">03 · Procesar</div>', unsafe_allow_html=True)

    if st.button("⬡  Procesar Archivo"):
        try:
            with st.spinner("Analizando información..."):
                content = uploaded_file.getvalue().decode("latin-1")
                transacciones, meta = parsear_archivo(content=content)

            if not transacciones:
                st.error("No se encontraron transacciones. Verificá el formato del archivo.")
            else:
                with st.spinner("Generando Excel..."):
                    output = io.BytesIO()
                    crear_excel(transacciones, meta, output, con_resumenes=con_resumenes)
                    output.seek(0)

                st.success("✓  Proceso completado con éxito")

                # Stats chips
                from collections import Counter
                tipos = Counter(t['Tipo'] for t in transacciones)
                st.markdown(f"""
                <div class="stats-row">
                    <div class="stat-chip">
                        <span class="stat-val">{len(transacciones)}</span>
                        <span class="stat-lbl">Total</span>
                    </div>
                    <div class="stat-chip">
                        <span class="stat-val">{tipos.get('FC', 0)}</span>
                        <span class="stat-lbl">Facturas</span>
                    </div>
                    <div class="stat-chip">
                        <span class="stat-val">{tipos.get('NC', 0)}</span>
                        <span class="stat-lbl">Notas Cred.</span>
                    </div>
                    <div class="stat-chip">
                        <span class="stat-val">{tipos.get('ND', 0) + tipos.get('TF', 0) + tipos.get('TK', 0)}</span>
                        <span class="stat-lbl">Otros</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.info(
                    f"**{meta.get('tipo_reporte', 'N/A')}** · "
                    f"{meta.get('razon_social', 'Contribuyente')} · "
                    f"{meta.get('periodo', '')}"
                )

                st.download_button(
                    label="↓  Descargar Excel",
                    data=output,
                    file_name=f"{filename}_procesado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
            st.exception(e)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 1rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        color: #6b7280;
        letter-spacing: 0.12em;
    ">
        ESPERANDO ARCHIVO · PASO 01
    </div>
    """, unsafe_allow_html=True)
