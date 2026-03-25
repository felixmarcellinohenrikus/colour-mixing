import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# KONFIGURASI HALAMAN
# =============================================================================
st.set_page_config(
    page_title="Simulasi Pencampuran Warna",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS - MENARGETKAN STREAMLIT CONTAINERS
# =============================================================================
st.markdown("""
<style>
    /* Header */
    .header-container {
        background: linear-gradient(135deg, #1e88a7 0%, #0d7377 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
    }
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0 0 1rem 0;
    }
    .header-subtitle {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    .header-info {
        color: #e0f7fa;
        font-size: 0.95rem;
        line-height: 1.8;
    }

    /* Section Background - Target Streamlit containers */
    .section-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-left: 6px solid #1e88a7;
    }

    /* Title styling */
    .section-title {
        color: #1e88a7;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1e88a7;
    }

    /* Slider box */
    .slider-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Result box */
    .result-container {
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* Detail & Input boxes */
    .box-gradient-1 {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .box-gradient-2 {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: white;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 4px solid #1e88a7;
    }

    /* Fix Streamlit spacing */
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    
    .stMarkdown p {
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Simulasi Pencampuran Warna</h1>
    <div class="header-subtitle">Dikembangkan oleh Felix Marcellino Henrikus, S.Si.</div>
    <div class="header-info">
        Program Studi Magister Sains Data, UKSW Salatiga<br>
        Untuk digunakan dalam pembelajaran Optika Geometri di S1 Fisika, UKSW Salatiga
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================
if 'history' not in st.session_state:
    st.session_state.history = []

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    mode = st.radio(
        "Konsep Pencampuran:",
        ["Aditif (Cahaya)", "Substraktif (Pigmen/Filter)"]
    )
    st.info("**Aditif:** Penjumlahan cahaya\n\n**Substraktif:** Penyerapan cahaya")

# =============================================================================
# FUNGSI HITUNG WARNA
# =============================================================================
def hitung_warna(r, g, b, c, m, y, mode):
    factor = 1.0 / 3.0
    
    if "Aditif" in mode:
        red = min(1.0, (r + m + y) * factor)
        green = min(1.0, (g + c + y) * factor)
        blue = min(1.0, (b + c + m) * factor)
        desc = "Penjumlahan Vektor Cahaya"
    else:
        red = max(0.0, 1.0 - (c + g + b) * factor)
        green = max(0.0, 1.0 - (m + r + b) * factor)
        blue = max(0.0, 1.0 - (y + r + g) * factor)
        desc = "Penyerapan Spektrum Cahaya"
    
    hex_color = f"#{int(red*255):02x}{int(green*255):02x}{int(blue*255):02x}"
    brightness = red * 0.299 + green * 0.587 + blue * 0.114
    text_col = "white" if brightness < 0.5 else "black"
    
    return red, green, blue, hex_color, desc, text_col

# =============================================================================
# PANEL KONTROL - MENGGUNAKAN CONTAINER
# =============================================================================
# Container utama dengan background
panel_container = st.container()
with panel_container:
    # Background wrapper
    st.markdown('<div style="background: linear-gradient(135deg, #f5f7fa, #c3cfe2); padding: 2rem; border-radius: 15px; margin: 1rem 0; border-left: 6px solid #1e88a7;">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🎨 Panel Kontrol Intensitas Lampu/Filter</div>', unsafe_allow_html=True)
    st.caption("Atur jumlah unit lampu (0-3 unit per warna)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown("**Komponen Primer & Sekunder**")
        r = st.slider("🔴 Merah (R)", 0, 3, 0, key="r")
        g = st.slider("🟢 Hijau (G)", 0, 3, 0, key="g")
        b = st.slider("🔵 Biru (B)", 0, 3, 0, key="b")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown("**Komponen Sekunder & Primer**")
        c = st.slider("🔷 Cyan (C)", 0, 3, 0, key="c")
        m = st.slider("🟣 Magenta (M)", 0, 3, 0, key="m")
        y = st.slider("🟡 Kuning (Y)", 0, 3, 0, key="y")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown("**✨ Hasil Simulasi**")
        
        red_val, green_val, blue_val, color_hex, desc_mix, txt_col = hitung_warna(
            r, g, b, c, m, y, mode
        )
        
        st.markdown(f"""
        <div class="result-container" style="background: {color_hex};">
            <div style="color: {txt_col}; font-size: 2rem; font-weight: bold;">{color_hex.upper()}</div>
            <div style="color: {txt_col}; margin-top: 1rem;">{desc_mix}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =============================================================================
# ANALISIS
# =============================================================================
analysis_container = st.container()
with analysis_container:
    st.markdown('<div style="background: linear-gradient(135deg, #f5f7fa, #c3cfe2); padding: 2rem; border-radius: 15px; margin: 1rem 0; border-left: 6px solid #1e88a7;">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📊 Analisis Komponen Warna</div>', unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns([2, 1])
    
    with col_g1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Merah', 'Hijau', 'Biru'],
            y=[red_val, green_val, blue_val],
            marker_color=['#FF0000', '#00FF00', '#0000FF'],
            text=[f"{red_val:.2f}", f"{green_val:.2f}", f"{blue_val:.2f}"],
        ))
        fig.update_layout(
            title="Komposisi RGB",
            yaxis=dict(range=[0, 1.1]),
            height=350,
            template="plotly_white",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_g2:
        st.markdown('<div class="box-gradient-1">', unsafe_allow_html=True)
        st.markdown("**📋 Detail Nilai**")
        st.markdown(f"""
        <div class="info-box">🔴 Merah: {red_val:.3f}</div>
        <div class="info-box">🟢 Hijau: {green_val:.3f}</div>
        <div class="info-box">🔵 Biru: {blue_val:.3f}</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="box-gradient-2">', unsafe_allow_html=True)
        st.markdown("**💡 Input Lampu**")
        st.markdown(f"""
        <div class="info-box">R:{r} G:{g} B:{b}</div>
        <div class="info-box">C:{c} M:{m} Y:{y}</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =============================================================================
# EKSPERIMEN
# =============================================================================
exp_container = st.container()
with exp_container:
    st.markdown('<div style="background: linear-gradient(135deg, #f5f7fa, #c3cfe2); padding: 2rem; border-radius: 15px; margin: 1rem 0; border-left: 6px solid #1e88a7;">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🔬 Eksperimen dan Unduh Data</div>', unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        if st.button("💾 Rekam Data", type="primary", use_container_width=True):
            record = {
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Mode": mode,
                "R": r, "G": g, "B": b,
                "C": c, "M": m, "Y": y,
                "Out_R": round(red_val, 3),
                "Out_G": round(green_val, 3),
                "Out_B": round(blue_val, 3),
                "Hex": color_hex
            }
            st.session_state.history.append(record)
            st.success("Data disimpan!")
    
    with col_b2:
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Unduh CSV",
                data=csv,
                file_name=f"data_warna_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    if st.session_state.history:
        with st.expander(f"📜 Riwayat ({len(st.session_state.history)} data)"):
            st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("© 2026 Felix Marcellino Henrikus, S.Si. - UKSW Salatiga")
