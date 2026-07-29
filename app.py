import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import streamlit as st
import io
import datetime
import re

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="SmartBis UMKM",
    layout="wide",
)

# --- GLOBAL CSS UNTUK NAIKIN TATA LETAK ---
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. SESSION STATE FOR FAKE LOGIN & CHAT ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        {"role": "assistant", "content": "Halo! Ada yang bisa SMARTBis bantu untuk analisis usahamu hari ini? (Coba tanya: 'Berapa omzetku?', 'Apa produk terlaris?', atau 'Cek stok')"}
    ]

# --- 3. LOGIN SCREEN ---
if not st.session_state['logged_in']:
    st.markdown(
        """
        <style>
            .stApp { background-color: #F8FAFC; }
            .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6, label { color: #15803d !important; }
            div[data-baseweb="input"] {
                border: 2px solid #15803d;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
            div[data-baseweb="input"] input { color: #15803d !important; }
            .stButton>button {
                background-color: #16a34a;
                color: white !important;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                border: 2px solid #15803d;
                width: 100%;
                font-weight: bold;
                margin-top: 10px;
            }
            .stButton>button:hover {
                background-color: #15803d;
                border: 2px solid #14532d;
            }
            .center-text {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        try:
            st.image("LOGO.png", use_container_width=True)
        except:
            st.markdown("<h1 class='center-text' style='font-size: 3rem;'>SMARTBis UMKM</h1>", unsafe_allow_html=True)
            
        with st.form("login_form"):
            email = st.text_input("Alamat Email")
            password = st.text_input("Kata Sandi", type="password")
            submit_button = st.form_submit_button("[ Masuk ]")
            
            if submit_button:
                st.session_state['logged_in'] = True
                st.rerun()
                
        st.markdown(
            """
            <p style='text-align: center; margin-top: 15px; font-size: 14px; color: #475569;'>
                Belum punya akun? <a href='#' style='color: #f59e0b; text-decoration: none; font-weight: bold;'>Daftar di sini</a>
            </p>
            """, 
            unsafe_allow_html=True
        )

# --- 4. MAIN DASHBOARD SCREEN ---
else:
    # --- CSS DASHBOARD ---
    st.markdown(
        """
        <style>
            .stApp { background-color: #F8FAFC; } 
            
            [data-testid="stSidebar"] {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E2E8F0;
            }
            
            [data-testid="stSidebar"] * {
                color: #0F172A !important;
            }
            
            .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6, label, .stChatMessage {
                color: #0F172A !important; 
            }
            
            div[data-baseweb="select"], div[data-baseweb="input"] {
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
            
            .stButton>button {
                background-color: #16a34a; 
                color: white !important;
                border-radius: 6px;
                border: none;
                font-weight: 600;
                transition: all 0.2s;
            }
            .stButton>button:hover {
                background-color: #15803d;
            }
            
            .metric-card {
                background-color: #FFFFFF;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                border: 1px solid #E2E8F0; 
                border-left: 6px solid #16a34a; 
                margin-bottom: 20px;
            }
            .metric-card h4 {
                color: #64748B !important; 
                font-size: 14px;
                margin-bottom: 8px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .metric-card h2 {
                color: #0F172A !important;
                font-size: 28px;
                font-weight: 800;
            }
            
            [data-testid="stVegaLiteChart"], [data-testid="stDataFrame"] {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E2E8F0; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                padding: 0 !important;
                overflow: hidden;
            }
            
            .info-box {
                background-color: #f0fdf4; 
                padding: 18px;
                border-radius: 10px;
                border: 1px solid #bbf7d0;
                border-left: 6px solid #22c55e;
                margin-bottom: 20px;
                color: #166534;
            }
            
            .ai-card {
                background-color: #FFFFFF;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #f59e0b; 
                margin-bottom: 20px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .ai-card h4 {
                margin-top: 0;
                font-size: 1.1rem;
                color: #0F172A !important;
            }
            .ai-card p {
                margin-bottom: 0;
                color: #475569 !important;
                font-size: 0.95rem;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # --- SIDEBAR: LOGO, NAVIGATION & HYBRID DATA UPLOAD ---
    try:
        st.sidebar.image("LOGO.png", use_container_width=True)
    except:
        st.sidebar.title("SmartBis UMKM")
        
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "📍 Menu Utama",
        [
            "🏠 Beranda", 
            "📈 Penjualan", 
            "👥 Pelanggan", 
            "💰 Keuangan", 
            "📦 Persediaan", 
            "💡 Saran SMARTBis", 
            "🤖 Tanya SMARTBis"
        ]
    )
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("📂 Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload Data Transaksi", type=["csv", "xlsx"])

    # --- EKSTRAK NAMA BRAND DARI NAMA FILE ---
    brand_name = "Bisnismu" # Default kalau filenya ngga di-upload
    
    if uploaded_file is not None:
        # Ambil nama asli tanpa ekstensi
        raw_name = uploaded_file.name.rsplit('.', 1)[0]
        # Hapus kata-kata generic biar sisa nama brand-nya doang
        clean_name = re.sub(r'(?i)(data|rekap|penjualan|transaksi|laporan)', '', raw_name)
        # Ganti underscore/strip jadi spasi
        clean_name = clean_name.replace('_', ' ').replace('-', ' ').strip()
        
        # Kalo habis di-clean ternyata namanya ngga kosong, kita pake!
        if clean_name:
            brand_name = clean_name.title()
            
    # --- DATA PROCESSING (HYBRID) ---
    is_real_data = False
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        
        rename_map = {
            "Kategori_Produk": "Product_Category",
            "Nama_Produk": "Product_Name",
            "Tanggal": "Date",
            "Qty": "Quantity",
            "ID_Pelanggan": "Customer_ID"
        }
        data.rename(columns=rename_map, inplace=True)
        
        if "Date" in data.columns:
            data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
        
        if "Harga_Jual" in data.columns and "HPP_Modal" in data.columns and "Quantity" in data.columns:
            data["Sales_Amount"] = data["Quantity"] * data["Harga_Jual"]
            data["Cost"] = data["Quantity"] * data["HPP_Modal"]
            data["Profit"] = data["Sales_Amount"] - data["Cost"]
            
        is_real_data = True
            
    else:
        # Dummy data
        np.random.seed(42)
        dates = pd.date_range(start="2026-06-25", periods=100, freq="12h") 
        products_info = {
            "Dimsum Mentai": {"Kategori": "Premium", "Harga": 25000, "Modal": 15000, "Stok": 45},
            "Dimsum Mozzarella": {"Kategori": "Premium", "Harga": 25000, "Modal": 15000, "Stok": 15},
            "Hakau Udang": {"Kategori": "Kukus", "Harga": 20000, "Modal": 12000, "Stok": 4},
            "Siomay Ayam": {"Kategori": "Kukus", "Harga": 15000, "Modal": 8000, "Stok": 120},
            "Lumpia Kulit Tahu": {"Kategori": "Goreng", "Harga": 18000, "Modal": 10000, "Stok": 0}
        }
        chosen_products = np.random.choice(list(products_info.keys()), size=100)
        
        data = pd.DataFrame({
            "Date": dates,
            "Customer_ID": np.random.randint(101, 150, size=100),
            "Product_Name": chosen_products,
            "Quantity": np.random.randint(1, 5, size=100),
        })
        data["Product_Category"] = data["Product_Name"].map(lambda x: products_info[x]["Kategori"])
        data["Harga_Jual"] = data["Product_Name"].map(lambda x: products_info[x]["Harga"])
        data["HPP_Modal"] = data["Product_Name"].map(lambda x: products_info[x]["Modal"])
        data["Stok_Gudang"] = data["Product_Name"].map(lambda x: products_info[x]["Stok"])
        
        data["Sales_Amount"] = data["Quantity"] * data["Harga_Jual"]
        data["Cost"] = data["Quantity"] * data["HPP_Modal"]
        data["Profit"] = data["Sales_Amount"] - data["Cost"]
        is_real_data = True

    # --- ROUTING MENU ---
    
    if menu == "🏠 Beranda":
        st.title(f"🏠 Hari Ini di {brand_name}")
        st.markdown("Ringkasan operasional bisnismu hari ini.")
        
        if "Product_Category" in data.columns:
            top_cat = data["Product_Category"].value_counts().idxmax()
            st.markdown(
                f"""<div class="info-box">
                    <b>💡 SMARTBis Insight:</b> Kategori <b>{top_cat}</b> mendominasi penjualan. Sebaiknya tingkatkan stok dan buat paket <i>bundling</i> untuk mendongkrak margin.
                </div>""", unsafe_allow_html=True
            )

        total_omzet = data["Sales_Amount"].sum() if "Sales_Amount" in data.columns else 0
        total_profit = data["Profit"].sum() if "Profit" in data.columns else 0
        total_transaksi = len(data)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="metric-card"><h4>Total Omzet</h4><h2>Rp {total_omzet:,.0f}</h2></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-card"><h4>Total Profit</h4><h2>Rp {total_profit:,.0f}</h2></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="metric-card"><h4>Jumlah Transaksi</h4><h2>{total_transaksi} trx</h2></div>""", unsafe_allow_html=True)

    elif menu == "📈 Penjualan":
        st.title("📈 Performa Penjualan")
        
        avg_trx = int(data["Quantity"].mean()) if "Quantity" in data.columns else 45
        
        st.subheader("1. Pertumbuhan Penjualan")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total Transaksi Tercatat", f"{len(data)} Transaksi")
        with col_m2:
            st.metric("Rata-rata Qty per Transaksi", f"{avg_trx} Item")
            
        st.markdown("---")
        
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.subheader("2. Tren Penjualan")
            if "Date" in data.columns and "Sales_Amount" in data.columns:
                chart_data = data.groupby(data['Date'].dt.date)["Sales_Amount"].sum()
                st.line_chart(chart_data, color="#16a34a")
            else:
                st.info("Pastikan kolom 'Tanggal' dan 'Harga_Jual' tersedia di data CSV Anda.")
                
        with col_right:
            st.subheader("3. Prediksi Penjualan")
            if "Date" in data.columns and "Sales_Amount" in data.columns:
                daily_sales = data.groupby(data['Date'].dt.date)["Sales_Amount"].sum()
                if len(daily_sales) > 7:
                    last_7_days = daily_sales.iloc[-7:].sum()
                    prev_7_days = daily_sales.iloc[-14:-7].sum()
                    if prev_7_days > 0:
                        growth = ((last_7_days - prev_7_days) / prev_7_days) * 100
                        trend = "naik" if growth > 0 else "turun"
                        pred_text = f"Berdasarkan performa 14 hari terakhir, sistem mendeteksi tren <b>{trend} {abs(growth):.1f}%</b>. Diprediksi minggu depan penjualan akan bergerak di kisaran angka tersebut."
                    else:
                        pred_text = "Data historis sedang dikumpulkan untuk membuat prediksi akurat minggu depan."
                else:
                    pred_text = "Belum cukup data hari untuk melakukan prediksi AI. Terus input data penjualan harianmu!"
            else:
                pred_text = "Upload data dengan format kolom Tanggal dan Nominal untuk mengaktifkan AI Prediksi."
                
            st.markdown(
                f"""
                <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border: 1px dashed #cbd5e1;">
                    <p style="font-size: 0.9rem; color: #475569;">{pred_text}</p>
                </div>
                """, unsafe_allow_html=True
            )

        st.markdown("---")
        
        col_cat, col_prod = st.columns(2)
        with col_cat:
            st.subheader("4. Kategori Terlaris")
            if "Product_Category" in data.columns and "Sales_Amount" in data.columns:
                cat_data = data.groupby("Product_Category")["Sales_Amount"].sum()
                st.bar_chart(cat_data, color="#f59e0b")
            else:
                st.info("Kolom 'Kategori_Produk' tidak tersedia.")
            
        with col_prod:
            st.subheader("5. Produk Terlaris")
            if "Product_Name" in data.columns and "Quantity" in data.columns:
                prod_data = data.groupby("Product_Name")["Quantity"].sum().sort_values(ascending=False).head(5)
                st.bar_chart(prod_data, color="#1d4ed8")
            else:
                st.info("Kolom 'Nama_Produk' tidak tersedia di dataset.")

    elif menu == "👥 Pelanggan":
        st.title("👥 Kenali Pelanggan Anda")
        st.markdown("Segmentasi pelanggan berbasis transaksi menggunakan kecerdasan buatan (Machine Learning).")
        
        if len(data) > 5 and "Quantity" in data.columns and "Sales_Amount" in data.columns:
            X = data[["Quantity", "Sales_Amount"]]
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            data["Cluster"] = kmeans.fit_predict(X)

            cluster_map = {0: "😴 Pelanggan yang Belum Kembali", 1: "😊 Pelanggan Aktif", 2: "❤️ Pelanggan Setia"}
            data["Segment"] = data["Cluster"].map(cluster_map)

            st.scatter_chart(
                data, x="Quantity", y="Sales_Amount", color="Segment", size="Sales_Amount"
            )
            
            if "Customer_ID" in data.columns:
                st.dataframe(data[["Customer_ID", "Quantity", "Sales_Amount", "Segment"]].head(15), use_container_width=True)
            else:
                st.dataframe(data[["Quantity", "Sales_Amount", "Segment"]].head(15), use_container_width=True)
        else:
            st.warning("Data tidak cukup atau format kolom tidak sesuai untuk segmentasi AI.")

    elif menu == "💰 Keuangan":
        st.title("💰 Kesehatan Keuangan Usaha")
        st.markdown("Ringkasan performa finansial berdasarkan data transaksi.")
        
        total_revenue = data["Sales_Amount"].sum() if "Sales_Amount" in data.columns else 0
        total_cost = data["Cost"].sum() if "Cost" in data.columns else 0
        net_margin = (data["Profit"].sum() / total_revenue * 100) if total_revenue > 0 and "Profit" in data.columns else 0
        
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.metric(label="Pendapatan (Revenue)", value=f"Rp {total_revenue:,.0f}")
        with col2: 
            st.metric(label="Total Pengeluaran (HPP)", value=f"Rp {total_cost:,.0f}")
        with col3: 
            st.metric(label="Estimasi Margin Profit", value=f"{net_margin:.1f}%")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Tren Arus Kas (Berdasarkan Waktu)")
        
        if "Date" in data.columns and "Sales_Amount" in data.columns and "Cost" in data.columns:
            cf_data = data.groupby(data["Date"].dt.date)[["Sales_Amount", "Cost"]].sum()
            st.line_chart(cf_data)
        else:
            st.info("Pastikan data CSV memiliki kolom 'Tanggal', 'Harga_Jual', dan 'HPP_Modal' untuk melihat tren arus kas.")

    elif menu == "📦 Persediaan":
        st.title("📦 Kelola Persediaan")
        st.markdown("Pantau ketersediaan barang di gudang agar tidak kehabisan (Out of Stock).")
        
        with st.expander("ℹ️ Keterangan Status Stok", expanded=True):
            st.markdown("""
            | Status | Keterangan |
            |---|---|
            | 🟢 **Aman** | Stok masih mencukupi dan tidak perlu tindakan. |
            | 🔵 **Cukup** | Stok masih tersedia, namun mulai perlu dipantau. |
            | 🟡 **Menipis** | Stok mulai berkurang, sebaiknya siapkan restok. |
            | 🟠 **Hampir Habis** | Segera lakukan pembelian agar penjualan tidak terganggu. |
            | 🔴 **Habis** | Produk tidak tersedia dan perlu segera diisi kembali. |
            """)
        
        if is_real_data and "Product_Name" in data.columns and "Stok_Gudang" in data.columns:
            stock_df = data.groupby(["Product_Name"])["Stok_Gudang"].max().reset_index()
            if "Product_Category" in data.columns:
                cat_df = data.groupby("Product_Name")["Product_Category"].first().reset_index()
                stock_df = pd.merge(stock_df, cat_df, on="Product_Name")
                stock_df = stock_df[["Product_Name", "Product_Category", "Stok_Gudang"]]
                stock_df.rename(columns={"Product_Name": "SKU / Nama Barang", "Product_Category": "Kategori", "Stok_Gudang": "Stok Gudang (Unit)"}, inplace=True)
            else:
                stock_df.rename(columns={"Product_Name": "SKU / Nama Barang", "Stok_Gudang": "Stok Gudang (Unit)"}, inplace=True)
        else:
            stock_df = pd.DataFrame({
                "SKU / Nama Barang": ["Snack Taro", "Kopi Susu", "Kerajinan", "Kaos", "Keripik"],
                "Stok Gudang (Unit)": [35, 20, 12, 4, 0]
            })
            
        def assign_status(stok):
            if stok >= 30: return "🟢 Aman"
            elif stok >= 15: return "🔵 Cukup"
            elif stok >= 5: return "🟡 Menipis"
            elif stok > 0: return "🟠 Hampir Habis"
            else: return "🔴 Habis"
                
        stock_df["Status Stok"] = stock_df["Stok Gudang (Unit)"].apply(assign_status)
        st.dataframe(stock_df, use_container_width=True)

    elif menu == "💡 Saran SMARTBis":
        st.title("💡 Rekomendasi SMARTBis")
        st.markdown(f"Sistem AI kami menganalisis data transaksi **{brand_name}** dan merekomendasikan langkah-langkah berikut:")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. Penjualan
        if "Product_Name" in data.columns and "Quantity" in data.columns:
            top_prod = data.groupby("Product_Name")["Quantity"].sum().idxmax()
            rekomendasi_jual = f"Produk <b>{top_prod}</b> adalah pahlawan omzetmu bulan ini. Pastikan display/promosi difokuskan ke produk ini."
        else:
            rekomendasi_jual = "Pastikan kolom Nama Produk ada untuk mendapatkan insight penjualan."
            
        # 2. Keuntungan
        if "Product_Name" in data.columns and "Profit" in data.columns:
            top_profit = data.groupby("Product_Name")["Profit"].sum().idxmax()
            rekomendasi_untung = f"Produk <b>{top_profit}</b> menyumbang margin paling sehat. Coba tawarkan sebagai add-on/bundling untuk menaikkan Net Profit."
        else:
            rekomendasi_untung = "Jaga margin keuntungan Anda dengan memastikan HPP tetap stabil."

        # 3. Pelanggan
        if "Customer_ID" in data.columns:
            top_cust = data["Customer_ID"].value_counts().idxmax()
            rekomendasi_pelanggan = f"Pelanggan dengan ID <b>{top_cust}</b> terpantau sebagai pembeli paling aktif. Berikan reward khusus atau voucher loyalti agar dia makin sering jajan di <b>{brand_name}</b>!"
        else:
            rekomendasi_pelanggan = "Sebanyak 18% pelanggan belum melakukan pembelian ulang dalam periode terakhir. Jalankan kampanye retensi dengan voucher diskon."

        # 4. Persediaan
        if "Stok_Gudang" in data.columns and "Product_Name" in data.columns:
            stock_df = data.groupby("Product_Name")["Stok_Gudang"].max()
            low_stock = stock_df[stock_df < 10]
            if not low_stock.empty:
                items_low = ", ".join(low_stock.index.tolist())
                rekomendasi_stok = f"⚠️ WARNING: Stok <b>{items_low}</b> menipis atau habis! Segera hubungi supplier hari ini agar tidak hilang potensi omzet."
            else:
                rekomendasi_stok = "Gudang aman! Semua produk andalanmu masih tersedia di atas ambang batas."
        else:
            rekomendasi_stok = "Tambahkan kolom 'Stok_Gudang' untuk dipantau AI."
            
        # 5. Pemasaran
        if "Product_Category" in data.columns:
            cats = data["Product_Category"].value_counts()
            if len(cats) >= 2:
                top1 = cats.index[0]
                top2 = cats.index[1]
                rekomendasi_marketing = f"Kategori <b>{top1}</b> dan <b>{top2}</b> lagi naik daun. Buat paket *Bundling* dari dua kategori ini untuk menaikkan rata-rata nilai transaksi (AOV) dari setiap *customer*."
            else:
                rekomendasi_marketing = "Fokuskan pemasaran digital Anda pada platform dengan engagement tertinggi minggu ini."
        else:
            rekomendasi_marketing = "Paket bundling diprediksi dapat meningkatkan nilai transaksi rata-rata."
        
        st.markdown(
            f"""
            <div class="ai-card">
                <h4>📈 Rekomendasi Penjualan</h4>
                <p>{rekomendasi_jual}</p>
            </div>
            
            <div class="ai-card">
                <h4>💰 Rekomendasi Keuntungan</h4>
                <p>{rekomendasi_untung}</p>
            </div>
            
            <div class="ai-card">
                <h4>👥 Rekomendasi Pelanggan</h4>
                <p>{rekomendasi_pelanggan}</p>
            </div>
            
            <div class="ai-card">
                <h4>📦 Peringatan Persediaan</h4>
                <p>{rekomendasi_stok}</p>
            </div>
            
            <div class="ai-card">
                <h4>📣 Rekomendasi Pemasaran</h4>
                <p>{rekomendasi_marketing}</p>
            </div>
            """, unsafe_allow_html=True
        )

    elif menu == "🤖 Tanya SMARTBis":
        st.title("💬 Diskusi dengan SMARTBis")
        st.markdown(f"SmartBot ini membaca data transaksi **{brand_name}** secara real-time!")
        
        for message in st.session_state['chat_history']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ketik di sini... (Contoh: omzet, produk laris, stok habis)"):
            st.session_state['chat_history'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            p_lower = prompt.lower()
            reply = "Maaf, SMARTBis belum mengerti. Coba tanyakan spesifik tentang kata kunci 'omzet', 'profit', 'laris', atau 'stok'."
            
            if "omzet" in p_lower or "pendapatan" in p_lower:
                tot_omzet = data['Sales_Amount'].sum() if 'Sales_Amount' in data.columns else 0
                reply = f"Total omzet yang tercatat di sistem saat ini adalah **Rp {tot_omzet:,.0f}**. Pertahankan performamu!"
            elif "profit" in p_lower or "untung" in p_lower:
                tot_profit = data['Profit'].sum() if 'Profit' in data.columns else 0
                reply = f"Total bersih margin/profit yang kamu kantongi adalah **Rp {tot_profit:,.0f}**."
            elif "laris" in p_lower or "laku" in p_lower or "banyak" in p_lower:
                if "Product_Name" in data.columns:
                    top_item = data.groupby("Product_Name")["Quantity"].sum().idxmax()
                    reply = f"Produk jagoanmu saat ini adalah **{top_item}**. Coba push promo lebih banyak untuk produk ini!"
            elif "stok" in p_lower or "habis" in p_lower:
                if "Stok_Gudang" in data.columns:
                    stock_min = data.groupby("Product_Name")["Stok_Gudang"].max().idxmin()
                    val_min = data.groupby("Product_Name")["Stok_Gudang"].max().min()
                    reply = f"Cek gudang sekarang! Produk **{stock_min}** sisa stoknya tinggal {val_min}. Jangan sampai kehabisan."

            st.session_state['chat_history'].append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)