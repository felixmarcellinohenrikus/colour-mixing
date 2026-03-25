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
# CUSTOM CSS - MENARGETKAN CONTAINER STREAMLIT
# =============================================================================
st.markdown("""
<style>
    /* Header - Sudah benar */
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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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
        margin: 0.5rem 0;
    }

    /* SECTION CONTAINER - Menggunakan class Streamlit */
    div[data-testid="stVerticalBlock"] > div.element-container:has(.section-title) {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-left: 6px solid #1e88a7;
    }

    /* Slider Container Styling */
    .slider-wrapper {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Result Box */
    .result-display {
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .color-code {
        font-size: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }

    /* Detail & Input Boxes */
    .detail-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .input-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .info-item {
        background: white;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 4px solid #1e88a7;
    }

    /* Section Title */
    .section-title {
        color: #1e88a7;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1e88a7;
    }

    /* Override Streamlit spacing */
    .stMarkdown p {
        margin: 0.5rem 0;
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
# INISIALISASI SESSION STATE
# =============================================================================
if 'history' not in st.session_state:
    st.session_state.history = []

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.header("⚙️ Konfigurasi Simulasi")
    mode = st.radio(
        "Pilih Konsep Pencampuran:",
        ["Aditif (Cahaya)", "Substraktif (Pigmen/Filter)"],
        help="Aditif: Pencampuran cahaya (RGB). Substraktif: Pencampuran pigmen atau filter cahaya (CMY)."
    )
    
    st.markdown("---")
    st.info(
        "**Catatan Fisika:**\n\n"
        "- **Aditif:** Dasar hitam. Lampu menyala menambah intensitas cahaya.\n"
        "- **Substraktif:** Dasar putih. Lampu/Filter menyerap panjang gelombang tertentu."
    )

# =============================================================================
# FUNGSI HITUNG WARNA
# =============================================================================
def hitung_warna(r, g, b, c, m, y, mode):
    factor = 1.0 / 3.0
    
    if "Aditif" in mode:
        red_val = min(1.0, (r + m + y) * factor)
        green_val = min(1.0, (g + c + y) * factor)
        blue_val = min(1.0, (b + c + m) * factor)
        desc = "Penjumlahan Vektor Cahaya"
    else:
        red_val = max(0.0, 1.0 - (c + g + b) * factor)
        green_val = max(0.0, 1.0 - (m + r + b) * factor)
        blue_val = max(0.0, 1.0 - (y + r + g) * factor)
        desc = "Penyerapan Spektrum Cahaya"
    
    r_hex = int(red_val * 255)
    g_hex = int(green_val * 255)
    b_hex = int(blue_val * 255)
    color_hex = f"#{r_hex:02x}{g_hex:02x}{b_hex:02x}"
    
    brightness = (red_val * 0.299 + green_val * 0.587 + blue_val * 0.114)
    text_color = "white" if brightness < 0.5 else "black"
    
    return red_val, green_val, blue_val, color_hex, desc, text_color

# =============================================================================
# FUNGSI HELPER: BUAT SECTION DENGAN BACKGROUND
# =============================================================================
def create_section(title, content_func, key=None):
    """Membuat section dengan background gradient"""
    section_id = f"section_{key}" if key else "section_default"
    
    # Container dengan styling
    container = st.container()
    with container:
        # Title
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        # Content
        content_func()
        st.markdown("---")
    
    return container

# =============================================================================
# PANEL KONTROL
# =============================================================================
st.markdown('<div class="section-title">🎨 Panel Kontrol Intensitas Lampu/Filter</div>', unsafe_allow_html=True)
st.caption("Atur jumlah unit lampu yang dinyalakan (0 - 3 unit per warna)")

# Buat 3 kolom untuk slider
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    st.markdown("**Komponen Primer & Sekunder**")
    r_lamps = st.slider("🔴 Merah (R)", 0, 3, 0, key="r")
    g_lamps = st.slider("🟢 Hijau (G)", 0, 3, 0, key="g")
    b_lamps = st.slider("🔵 Biru (B)", 0, 3, 0, key="b")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    st.markdown("**Komponen Sekunder & Primer**")
    c_lamps = st.slider("🔷 Cyan (C)", 0, 3, 0, key="c")
    m_lamps = st.slider("🟣 Magenta (M)", 0, 3, 0, key="m")
    y_lamps = st.slider("🟡 Kuning (Y)", 0, 3, 0, key="y")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    st.markdown("**✨ Hasil Simulasi**")
    
    # Hitung warna
    red_val, green_val, blue_val, color_hex, desc_mix, text_color = hitung_warna(
        r_lamps, g_lamps, b_lamps, c_lamps, m_lamps, y_lamps, mode
    )
    
    # Tampilkan hasil dengan background dinamis
    st.markdown(f"""
    <div class="result-display" style="background: linear-gradient(135deg, {color_hex}, {color_hex});">
        <div class="color-code" style="color: {text_color};">{color_hex.upper()}</div>
        <div style="color: {text_color}; margin-top: 1rem;">
            <strong>Model Fisika:</strong><br>{desc_mix}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =============================================================================
# ANALISIS KOMPONEN WARNA
# =============================================================================
st.markdown('<div class="section-title">📊 Analisis Komponen Warna</div>', unsafe_allow_html=True)

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
        title="<b>Komposisi Intensitas RGB Hasil</b>",
        yaxis=dict(range=[0, 1.1], title="Intensitas (0-1)"),
        xaxis=dict(title="Komponen Warna"),
        height=400,
        template="plotly_white",
        margin=dict(t=50, b=40, l=50, r=20),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col_graph2:
    # Detail Nilai
    st.markdown('<div class="detail-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #1e88a7; margin-top: 0;">📋 Detail Nilai</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="info-item">🔴 <strong>Merah:</strong> {red_val:.3f}</div>
        <div class="info-item">🟢 <strong>Hijau:</strong> {green_val:.3f}</div>
        <div class="info-item">🔵 <strong>Biru:</strong> {blue_val:.3f}</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Lampu
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #1e88a7; margin-top: 0;">💡 Input Lampu</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="info-item">
            <strong>Primer:</strong><br>
            R: {r_lamps} | G: {g_lamps} | B: {b_lamps}
        </div>
        <div class="info-item">
            <strong>Sekunder:</strong><br>
            C: {c_lamps} | M: {m_lamps} | Y: {y_lamps}
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =============================================================================
# EKSPERIMEN DAN UNDUH DATA
# =============================================================================
st.markdown('<div class="section-title">🔬 Eksperimen dan Unduh Data</div>', unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("💾 Rekam Percobaan Ini", type="primary", use_container_width=True):
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
        st.success("✅ Data percobaan berhasil disimpan!")

with col_btn2:
    if len(st.session_state.history) > 0:
        df_history = pd.DataFrame(st.session_state.history)
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Data Percobaan (CSV)",
            data=csv,
            file_name=f"simulasi_warna_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.download_button(
            label="📥 Unduh Data Percobaan (CSV)",
            data="",
            file_name="simulasi_warna.csv",
            mime="text/csv",
            disabled=True,
            use_container_width=True
        )

# Tampilkan riwayat
if len(st.session_state.history) > 0:
    st.markdown("---")
    with st.expander(f"📜 Lihat Riwayat Percobaan ({len(st.session_state.history)} data)"):
        st.dataframe(df_history, use_container_width=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown('<p style="text-align: center; color: #888; font-size: 0.9rem;">© 2026 Felix Marcellino Henrikus, S.Si. - Program Studi Magister Sains Data, UKSW Salatiga</p>', unsafe_allow_html=True)
