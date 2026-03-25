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
    layout="wide"
)

# =============================================================================
# CUSTOM CSS - STYLING UTAMA
# =============================================================================
st.markdown("""
<style>
    /* Header Section - Biru Laut */
    .header-container {
        background: linear-gradient(135deg, #1e88a7 0%, #0d7377 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .header-subtitle {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .header-info {
        color: #e0f7fa;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Card Styling - Menggunakan container Streamlit */
    .section-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 6px solid #1e88a7;
    }
    .card-title {
        color: #1e88a7;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1e88a7;
    }

    /* Slider Box */
    .slider-box {
        background: white;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Result Color Box */
    .result-display {
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        border: 2px solid #ccc;
        margin: 1rem 0;
    }

    /* Detail Items */
    .detail-item {
        background: white;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 4px solid #1e88a7;
    }

    /* Override Streamlit default spacing */
    .stApp > div[data-testid="stVerticalBlock"] > div.element-container {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div class="header-container">
    <div class="header-title">Simulasi Pencampuran Warna</div>
    <div class="header-subtitle">Dikembangkan oleh Felix Marcellino Henrikus, S.Si.</div>
    <div class="header-info">
        Program Studi Magister Sains Data, UKSW Salatiga<br>
        Untuk digunakan dalam pembelajaran Optika Geometri di S1 Fisika, UKSW Salatiga
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =============================================================================
# INISIALISASI SESSION STATE
# =============================================================================
if 'history' not in st.session_state:
    st.session_state.history = []

# =============================================================================
# SIDEBAR: PENGATURAN MODE
# =============================================================================
st.sidebar.header("⚙️ Konfigurasi Simulasi")
mode = st.sidebar.radio(
    "Pilih Konsep Pencampuran:",
    ["Aditif (Cahaya)", "Substraktif (Pigmen/Filter)"],
    help="Aditif: Pencampuran cahaya (RGB). Substraktif: Pencampuran pigmen atau filter cahaya (CMY)."
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Catatan Fisika:**\n\n"
    "- **Aditif:** Dasar hitam. Lampu menyala menambah intensitas cahaya.\n"
    "- **Substraktif:** Dasar putih. Lampu/Filter menyerap panjang gelombang tertentu."
)

# =============================================================================
# FUNGSI BANTUAN: HITUNG WARNA
# =============================================================================
def hitung_warna(r_lamps, g_lamps, b_lamps, c_lamps, m_lamps, y_lamps, mode):
    """Menghitung nilai RGB hasil berdasarkan mode aditif/substraktif"""
    factor = 1.0 / 3.0
    
    if "Aditif" in mode:
        # Penjumlahan cahaya
        red_val = (r_lamps + m_lamps + y_lamps) * factor
        green_val = (g_lamps + c_lamps + y_lamps) * factor
        blue_val = (b_lamps + c_lamps + m_lamps) * factor
        red_val = min(1.0, red_val)
        green_val = min(1.0, green_val)
        blue_val = min(1.0, blue_val)
        desc_mix = "Penjumlahan Vektor Cahaya"
    else:
        # Penyerapan cahaya (filter)
        absorb_r = (c_lamps + g_lamps + b_lamps) * factor
        absorb_g = (m_lamps + r_lamps + b_lamps) * factor
        absorb_b = (y_lamps + r_lamps + g_lamps) * factor
        red_val = max(0.0, 1.0 - absorb_r)
        green_val = max(0.0, 1.0 - absorb_g)
        blue_val = max(0.0, 1.0 - absorb_b)
        desc_mix = "Penyerapan Spektrum Cahaya"
    
    # Konversi ke Hex
    r_hex = int(red_val * 255)
    g_hex = int(green_val * 255)
    b_hex = int(blue_val * 255)
    color_hex = f"#{r_hex:02x}{g_hex:02x}{b_hex:02x}"
    
    return red_val, green_val, blue_val, color_hex, desc_mix

# =============================================================================
# PANEL KONTROL
# =============================================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🎨 Panel Kontrol Intensitas Lampu/Filter</div>', unsafe_allow_html=True)
st.caption("Atur jumlah unit lampu yang dinyalakan (0 - 3 unit per warna)")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown('<div class="slider-box">', unsafe_allow_html=True)
        st.markdown("**Komponen Primer & Sekunder**")
        r_lamps = st.slider("🔴 Merah (R)", 0, 3, 0, key="r")
        g_lamps = st.slider("🟢 Hijau (G)", 0, 3, 0, key="g")
        b_lamps = st.slider("🔵 Biru (B)", 0, 3, 0, key="b")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="slider-box">', unsafe_allow_html=True)
        st.markdown("**Komponen Sekunder & Primer**")
        c_lamps = st.slider("🔷 Cyan (C)", 0, 3, 0, key="c")
        m_lamps = st.slider("🟣 Magenta (M)", 0, 3, 0, key="m")
        y_lamps = st.slider("🟡 Kuning (Y)", 0, 3, 0, key="y")
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="slider-box">', unsafe_allow_html=True)
        st.markdown("**✨ Hasil Simulasi**")
        
        # Hitung warna
        red_val, green_val, blue_val, color_hex, desc_mix = hitung_warna(
            r_lamps, g_lamps, b_lamps, c_lamps, m_lamps, y_lamps, mode
        )
        
        # Tampilkan kotak warna
        st.markdown(f"""
        <div class="result-display" style="
            background: linear-gradient(135deg, {color_hex}, {color_hex});
            height: 100px;
            color: {'white' if (red_val*0.299 + green_val*0.587 + blue_val*0.114) < 0.5 else 'black'};
        ">
            {color_hex.upper()}
        </div>
        """, unsafe_allow_html=True)
        
        st.caption(f"**Model Fisika:** {desc_mix}")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.divider()

# =============================================================================
# ANALISIS KOMPONEN WARNA
# =============================================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📊 Analisis Komponen Warna</div>', unsafe_allow_html=True)

col_graph1, col_graph2 = st.columns([2, 1])

with col_graph1:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Merah (R)', 'Hijau (G)', 'Biru (B)'],
        y=[red_val, green_val, blue_val],
        marker_color=['#FF0000', '#00FF00', '#0000FF'],
        text=[f"{red_val:.2f}", f"{green_val:.2f}", f"{blue_val:.2f}"],
        textposition='auto',
    ))
    fig.update_layout(
        title="Komposisi Intensitas RGB Hasil",
        yaxis=dict(range=[0, 1.1]),
        height=400,
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_graph2:
    # Detail Nilai
    st.markdown('<div style="background: linear-gradient(135deg, #ffecd2, #fcb69f); padding: 1.2rem; border-radius: 10px; margin-bottom: 1rem;">', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.1rem; margin-bottom:0.5rem;">📋 Detail Nilai</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="detail-item"><strong>🔴 Merah:</strong> {red_val:.3f}</div>
        <div class="detail-item"><strong>🟢 Hijau:</strong> {green_val:.3f}</div>
        <div class="detail-item"><strong>🔵 Biru:</strong> {blue_val:.3f}</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Lampu
    st.markdown('<div style="background: linear-gradient(135deg, #a8edea, #fed6e3); padding: 1.2rem; border-radius: 10px;">', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.1rem; margin-bottom:0.5rem;">💡 Input Lampu</div>', unsafe_allow_html=True)
    st.write(f"**R:** {r_lamps} | **G:** {g_lamps} | **B:** {b_lamps}")
    st.write(f"**C:** {c_lamps} | **M:** {m_lamps} | **Y:** {y_lamps}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.divider()

# =============================================================================
# EKSPERIMEN DAN UNDUH DATA
# =============================================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔬 Eksperimen dan Unduh Data</div>', unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("💾 Rekam Percobaan Ini", type="primary"):
        record = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mode": mode,
            "Input_R": r_lamps, "Input_G": g_lamps, "Input_B": b_lamps,
            "Input_C": c_lamps, "Input_M": m_lamps, "Input_Y": y_lamps,
            "Output_R": round(red_val, 3),
            "Output_G": round(green_val, 3),
            "Output_B": round(blue_val, 3),
            "Hex_Color": color_hex
        }
        st.session_state.history.append(record)
        st.success("✅ Data percobaan berhasil disimpan ke memori sesi!")

with col_btn2:
    if len(st.session_state.history) > 0:
        df_history = pd.DataFrame(st.session_state.history)
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Data Percobaan (CSV)",
            data=csv,
            file_name=f"simulasi_warna_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    else:
        st.download_button(
            label="📥 Unduh Data Percobaan (CSV)",
            data="",
            file_name="simulasi_warna.csv",
            mime="text/csv",
            disabled=True
        )

# Tampilkan riwayat jika ada
if len(st.session_state.history) > 0:
    with st.expander("📜 Lihat Riwayat Percobaan"):
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("© 2026 Felix Marcellino Henrikus, S.Si. - Program Studi Magister Sains Data, UKSW Salatiga")
