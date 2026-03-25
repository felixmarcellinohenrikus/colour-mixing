import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Simulasi Pencampuran Warna", page_icon="🎨", layout="wide")

# CSS - Target Streamlit columns directly
st.markdown("""
<style>
    /* Header */
    .header-container {
        background: linear-gradient(135deg, #1e88a7 0%, #0d7377 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
    }
    .header-title { color: white; font-size: 2.5rem; font-weight: bold; margin: 0; }
    .header-subtitle { color: #ffffff; font-size: 1.3rem; margin: 0.5rem 0; }
    .header-info { color: #e0f7fa; font-size: 0.95rem; }

    /* Target column containers */
    div[data-testid="column"] > div {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Slider column background */
    .stColumn:nth-child(1) > div, .stColumn:nth-child(2) > div, .stColumn:nth-child(3) > div {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Section background using expander trick */
    div[data-testid="stExpander"] {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Result box */
    .result-box {
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #1e88a7;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header-container">
    <div class="header-title">Simulasi Pencampuran Warna</div>
    <div class="header-subtitle">Dikembangkan oleh Felix Marcellino Henrikus, S.Si.</div>
    <div class="header-info">
        Program Studi Magister Sains Data, UKSW Salatiga<br>
        Untuk pembelajaran Optika Geometri di S1 Fisika, UKSW Salatiga
    </div>
</div>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

# SIDEBAR
with st.sidebar:
    mode = st.radio("Konsep:", ["Aditif (Cahaya)", "Substraktif (Pigmen/Filter)"])
    st.info("**Aditif:** Penjumlahan cahaya\n\n**Substraktif:** Penyerapan cahaya")

# FUNGSI HITUNG
def hitung(r, g, b, c, m, y, mode):
    f = 1.0/3.0
    if "Aditif" in mode:
        R = min(1.0, (r + m + y) * f)
        G = min(1.0, (g + c + y) * f)
        B = min(1.0, (b + c + m) * f)
        desc = "Penjumlahan Spektrum Cahaya"
    else:
        R = max(0.0, 1.0 - (c + g + b) * f)
        G = max(0.0, 1.0 - (m + r + b) * f)
        B = max(0.0, 1.0 - (y + r + g) * f)
        desc = "Penyerapan Spektrum Cahaya"
    hex_col = f"#{int(R*255):02x}{int(G*255):02x}{int(B*255):02x}"
    bright = R*0.299 + G*0.587 + B*0.114
    txt = "white" if bright < 0.5 else "black"
    return R, G, B, hex_col, desc, txt

# PANEL KONTROL - Gunakan columns langsung
st.subheader("🎨 Panel Kontrol")
st.caption("Atur intensitas lampu (0 untuk terendah dan 3 untuk tertinggi)")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Komponen RGB")
    r = st.slider("🔴 Merah (R)", 0, 3, 0, key="r")
    g = st.slider("🟢 Hijau (G)", 0, 3, 0, key="g")
    b = st.slider("🔵 Biru (B)", 0, 3, 0, key="b")

with col2:
    st.markdown("#### Komponen CMY")
    c = st.slider("🔷 Cyan (C)", 0, 3, 0, key="c")
    m = st.slider("🟣 Magenta (M)", 0, 3, 0, key="m")
    y = st.slider("🟡 Kuning (Y)", 0, 3, 0, key="y")

with col3:
    st.markdown("#### Hasil Simulasi")
    R, G, B, hex_col, desc, txt = hitung(r, g, b, c, m, y, mode)
    
    st.markdown(f"""
    <div class="result-box" style="background: {hex_col};">
        <div style="color: {txt}; font-size: 2rem; font-weight: bold;">{hex_col.upper()}</div>
        <div style="color: {txt}; margin-top: 0.5rem;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ANALISIS
st.subheader("📊 Analisis Komponen")

col_g1, col_g2 = st.columns([2, 1])

with col_g1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Merah', 'Hijau', 'Biru'], y=[R, G, B], 
                         marker_color=['#FF0000', '#00FF00', '#0000FF']))
    fig.update_layout(title="Intensitas RGB", yaxis=dict(range=[0, 1.1]), 
                      height=350, template="plotly_white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col_g2:
    st.markdown("##### 📋 Detail Nilai")
    st.markdown(f'<div class="info-box">🔴 Merah: {R:.3f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">🟢 Hijau: {G:.3f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">🔵 Biru: {B:.3f}</div>', unsafe_allow_html=True)
    
    st.markdown("##### 💡 Input")
    st.markdown(f'<div class="info-box">R:{r} G:{g} B:{b}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">C:{c} M:{m} Y:{y}</div>', unsafe_allow_html=True)

st.divider()

# EKSPERIMEN
st.subheader("🔬 Eksperimen")

col_b1, col_b2 = st.columns(2)

with col_b1:
    if st.button("💾 Rekam Data", type="primary", use_container_width=True):
        st.session_state.history.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Mode": mode, "R": r, "G": g, "B": b,
            "Out_R": round(R,3), "Out_G": round(G,3), "Out_B": round(B,3),
            "Hex": hex_col
        })
        st.success("Data disimpan!")

with col_b2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.download_button("📥 Unduh CSV", df.to_csv(index=False).encode('utf-8'),
                          f"data_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv",
                          use_container_width=True)

if st.session_state.history:
    with st.expander(f"📜 Riwayat ({len(st.session_state.history)} data)"):
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

st.markdown("---")
st.caption("© 2026 Felix Marcellino Henrikus, S.Si. - UKSW Salatiga")
