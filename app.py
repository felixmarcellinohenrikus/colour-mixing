import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Simulasi Pencampuran Warna",
    page_icon="🎨",
    layout="wide"
)

# --- HEADER SESUAI PERMINTAAN ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #1E3A8A; font-family: sans-serif;">Simulasi Pencampuran Warna</h1>
    <h3 style="color: #555; font-family: sans-serif;">Dikembangkan oleh Felix Marcellino Henrikus, S.Si.</h3>
    <p style="color: #777; font-family: sans-serif;">
        Program Studi Magister Sains Data, UKSW Salatiga<br>
        Untuk digunakan dalam pembelajaran Optika Geometri di S1 Fisika, UKSW Salatiga
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- INISIALISASI SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: PENGATURAN MODE ---
st.sidebar.header("Konfigurasi Simulasi")
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

# --- INPUT KOMPONEN WARNA ---
st.subheader("Panel Kontrol Intensitas Lampu/Filter")
st.caption("Atur jumlah unit lampu yang dinyalakan (0 - 3 unit per warna)")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Komponen Primer & Sekunder")
    r_lamps = st.slider("Merah (R)", 0, 3, 0, key="r")
    g_lamps = st.slider("Hijau (G)", 0, 3, 0, key="g")
    b_lamps = st.slider("Biru (B)", 0, 3, 0, key="b")

with col2:
    st.markdown("### Komponen Sekunder & Primer")
    c_lamps = st.slider("Cyan (C)", 0, 3, 0, key="c")
    m_lamps = st.slider("Magenta (M)", 0, 3, 0, key="m")
    y_lamps = st.slider("Kuning (Y)", 0, 3, 0, key="y")

with col3:
    st.markdown("### Hasil Simulasi")
    # --- LOGIKA FISIKA ---
    # Normalisasi: 3 lampu = Intensitas Maksimum (1.0)
    factor = 1.0 / 3.0
    
    if "Aditif" in mode:
        # Model Aditif: Penjumlahan Cahaya
        # R contributes to Red
        # G contributes to Green
        # B contributes to Blue
        # C (Cyan) = Green + Blue
        # M (Magenta) = Red + Blue
        # Y (Yellow) = Red + Green
        
        red_val = (r_lamps + m_lamps + y_lamps) * factor
        green_val = (g_lamps + c_lamps + y_lamps) * factor
        blue_val = (b_lamps + c_lamps + m_lamps) * factor
        
        # Clamping 0-1
        red_val = min(1.0, red_val)
        green_val = min(1.0, green_val)
        blue_val = min(1.0, blue_val)
        
        bg_color = "black"
        text_color = "white"
        desc_mix = "Penjumlahan Vektor Cahaya"

    else:
        # Model Substraktif: Penyerapan Cahaya (Filter)
        # Dasar Putih (1, 1, 1)
        # Cyan menyerap Merah
        # Magenta menyerap Hijau
        # Kuning menyerap Biru
        # Filter Merah menyerap Hijau & Biru
        # Filter Hijau menyerap Merah & Biru
        # Filter Biru menyerap Merah & Hijau
        
        # Perhitungan Penyerapan
        absorb_r = (c_lamps + g_lamps + b_lamps) * factor
        absorb_g = (m_lamps + r_lamps + b_lamps) * factor
        absorb_b = (y_lamps + r_lamps + g_lamps) * factor
        
        red_val = max(0.0, 1.0 - absorb_r)
        green_val = max(0.0, 1.0 - absorb_g)
        blue_val = max(0.0, 1.0 - absorb_b)
        
        bg_color = "white"
        text_color = "black"
        desc_mix = "Penyerapan Spektrum Cahaya"

    # Konversi ke Hex untuk display
    r_hex = int(red_val * 255)
    g_hex = int(green_val * 255)
    b_hex = int(blue_val * 255)
    color_hex = f"#{r_hex:02x}{g_hex:02x}{b_hex:02x}"
    
    # Tampilan Warna
    st.markdown(
        f"""
        <div style="
            background-color: {color_hex};
            height: 150px;
            border-radius: 10px;
            border: 2px solid #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            color: {text_color};
            font-weight: bold;
            font-size: 1.2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            {color_hex.upper()}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <p style="font-size: 14px; color: #555;">
        <strong>Model Fisika:</strong> {desc_mix}
    </p>
    """, unsafe_allow_html=True)

st.divider()

# --- GRAFIK KOMPONEN RGB ---
st.subheader("Analisis Komponen Warna")
col_graph1, col_graph2 = st.columns([2, 1])

with col_graph1:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Merah (R)', 'Hijau (G)', 'Biru (B)'],
        y=[red_val, green_val, blue_val],
        marker_color=['#FF0000', '#00FF00', '#0000FF'],
        text=[f"{red_val:.2f}", f"{green_val:.2f}", f"{blue_val:.2f}"],
        textposition='auto',
        name='Intensitas'
    ))
    fig.update_layout(
        title="Komposisi Intensitas RGB Hasil",
        yaxis=dict(range=[0, 1.1]),
        height=400,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

with col_graph2:
    st.markdown("### Detail Nilai")
    st.write(f"**Merah:** {red_val:.3f}")
    st.write(f"**Hijau:** {green_val:.3f}")
    st.write(f"**Biru:** {blue_val:.3f}")
    st.write("---")
    st.write("### Input Lampu")
    st.write(f"R: {r_lamps}, G: {g_lamps}, B: {b_lamps}")
    st.write(f"C: {c_lamps}, M: {m_lamps}, Y: {y_lamps}")

# --- REKAM DATA & DOWNLOAD CSV ---
st.divider()
st.subheader("Eksperimen dan Unduh Data")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("Rekam Percobaan Ini", type="primary"):
        record = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mode": mode,
            "Input_R": r_lamps,
            "Input_G": g_lamps,
            "Input_B": b_lamps,
            "Input_C": c_lamps,
            "Input_M": m_lamps,
            "Input_Y": y_lamps,
            "Output_R": round(red_val, 3),
            "Output_G": round(green_val, 3),
            "Output_B": round(blue_val, 3),
            "Hex_Color": color_hex
        }
        st.session_state.history.append(record)
        st.success("Data percobaan berhasil disimpan ke memori sesi.")

with col_btn2:
    if len(st.session_state.history) > 0:
        df_history = pd.DataFrame(st.session_state.history)
        csv = df_history.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Unduh Data Percobaan (CSV)",
            data=csv,
            file_name=f"simulasi_warna_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    else:
        st.download_button(
            label="Unduh Data Percobaan (CSV)",
            data="",
            file_name="simulasi_warna.csv",
            mime="text/csv",
            disabled=True
        )

if len(st.session_state.history) > 0:
    with st.expander("Lihat Riwayat Percobaan"):
        st.dataframe(df_history, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2024 Felix Marcellino Henrikus, S.Si. - UKSW Salatiga")
