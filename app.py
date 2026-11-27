import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lean-CuREV Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ Lean-CuREV: Dashboard dei Risultati Sperimentali")
st.markdown(
    "Esplorazione interattiva del compromesso **efficienza / qualità** nella pulizia dei dataset di Code Review "
    "(campione di 500 commenti da `CuREV+` su GPU NVIDIA T4)."
)

st.divider()

# 1. KPI Principali (Dati dell'esperimento su 500 commenti)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Campione Analizzato", "500 commenti", "Dataset CuREV+")
col2.metric("Tempo Filtro (Fasi 1-2)", "12.45 s", "Analisi istantanea")
col3.metric("Preservati Originali", "71.2% (356)", "Stile umano intatto")
col4.metric("Riformulati (Qwen-3B)", "28.8% (144)", "1.98 s / commento")

st.divider()

# 2. Grafici di distribuzione
c_left, c_right = st.columns(2)

with c_left:
    st.subheader("Distribuzione Filtro a Imbuto")
    df_imbuto = pd.DataFrame({
        "Esito": ["Preservati Originali (71.2%)", "Selezionati per Riscrittura (28.8%)"],
        "Commenti": [356, 144]
    }).set_index("Esito")
    st.bar_chart(df_imbuto)

with c_right:
    st.subheader("Ripartizione per Pilastro Qualitativo")
    df_pilastri = pd.DataFrame({
        "Pilastro": ["Concisione (Prolissità)", "Chiarezza (Domande vaghe)", "Educatezza (Tossicità)"],
        "Commenti": [86, 58, 0]
    }).set_index("Pilastro")
    st.bar_chart(df_pilastri)

st.divider()

# 3. Ispettore Interattivo Prima vs Dopo dal file Excel
st.subheader("🔍 Confronto Qualitativo: Originale vs CuREV+ vs Lean-CuREV")

try:
    df = pd.read_excel("risultati_confronto_lean_curev_v2.xlsx")
    
    # Filtro per pilastro
    opzioni = ["Tutti"] + sorted(df["esito_filtro"].dropna().unique().tolist())
    scelta = st.selectbox("Filtra per criterio di intervento:", opzioni)
    
    df_filtrato = df if scelta == "Tutti" else df[df["esito_filtro"] == scelta]
    
    # Selettore del singolo esempio
    indice = st.slider("Seleziona l'esempio da ispezionare:", 0, len(df_filtrato) - 1, 0)
    riga = df_filtrato.iloc[indice]
    
    st.info(f"**Motivo selezione (Fase 2):** {riga['esito_filtro']}  |  **Score Tossicità:** {riga['score_tossicita']:.4f}")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("#### 🔴 Originale")
        st.warning(riga["comment"])
    with col_b:
        st.markdown("#### 🔵 Riferimento CuREV+ (70B)")
        st.info(riga["reformulated_comment"])
    with col_c:
        st.markdown("#### 🟢 Lean-CuREV (Qwen-3B)")
        st.success(riga["lean_curev_comment"])

    with st.expander("📋 Visualizza l'intera tabella comparativa"):
        st.dataframe(df_filtrato, use_container_width=True)

except FileNotFoundError:
    st.error("File `risultati_confronto_lean_curev_v2.xlsx` non trovato nella directory corrente.")
