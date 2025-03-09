import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(style='dark')

st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda")

df = pd.read_csv("main_data.csv")

def create_weather_df(df):
    return df.groupby("weathersit")["cnt"].mean().reset_index()

def create_temp_df(df):
    return df.groupby("temp_category")["cnt"].mean().reset_index()

def create_hourly_df(df):
    return df.groupby(["hr", "day_type"]).agg(total_rentals=('cnt', 'sum')).reset_index()

weather_df = create_weather_df(df)
temp_df = create_temp_df(df)
hourly_df = create_hourly_df(df)

filtered_weather = ["Hujan Ringan", "Cerah", "Mendung"]
df = df[df["weathersit"].isin(filtered_weather)]

temp_order = ["Very Cold", "Cold", "Mild", "Warm", "Hot"]
df["temp_category"] = pd.cut(df["temp"], 
                             bins=[-np.inf, 0.2, 0.4, 0.6, 0.8, np.inf], 
                             labels=temp_order)

tab1, tab2 = st.tabs(["📊 Pengaruh Cuaca & Suhu", "⏳ Distribusi Penyewaan per Jam"])

with tab1:
    st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=df, x="weathersit", y="cnt", estimator=np.mean, 
                hue="weathersit", palette="coolwarm", ax=ax, legend=False)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    st.subheader("Pengaruh Suhu terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=df, x="temp_category", y="cnt", estimator=np.mean, 
                hue="temp_category", palette="viridis", ax=ax, legend=False)
    ax.set_xlabel("Kategori Suhu")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Pengaruh Suhu terhadap Penyewaan Sepeda")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    st.markdown("""
    **📌 Kesimpulan**:
    - Kondisi cuaca yang lebih cerah memiliki jumlah penyewaan lebih tinggi dibandingkan cuaca buruk.
    - Jumlah penyewaan sepeda meningkat saat kondisi suhu udara hangat.
    """)

with tab2:
    st.subheader("Distribusi Penyewaan Sepeda per Jam dalam Sehari")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_df, x="hr", y="total_rentals", hue="day_type", marker="o", palette=["blue", "orange"], ax=ax)
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Penyewaan Sepeda Berdasarkan Waktu (Weekday vs Weekend)")
    ax.legend(title="Tipe Hari")
    ax.set_xticks(range(0, 24))  # Menyesuaikan sumbu x dari 0 hingga 23
    st.pyplot(fig)

    st.markdown("""
    **📌 Kesimpulan**:
    - Weekday: Penyewaan meningkat pada pagi (07:00-09:00) & sore (17:00-19:00), menunjukkan penggunaan untuk perjalanan kerja/sekolah.
    - Weekend: Pola lebih merata, puncak terjadi siang hingga sore (11:00-17:00), menandakan penggunaan untuk rekreasi/santai.
    """)

st.sidebar.markdown(
    """
    <style>
        .sidebar-img img {
            border-radius: 100%;
            display: block;
            margin: auto;
            width: 150px; /* Sesuaikan ukuran */
            height: 150px; /* Sesuaikan ukuran */
            object-fit: cover; /* Memastikan gambar tetap proporsional */
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-img"><img src="https://img.khan.co.kr/news/2021/12/23/l_2021122401003030400267441.jpg"></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown("""
---                    
## 👤 **My Profile**
👋 **Nama** : Ismi Nilam Anggraini  
📧 **Email**: [isminilamng@gmail.com](mailto:isminilamng@gmail.com)  
🏅 **ID Dicoding**: isminilam  

---

## 🚲 **Tentang Website Ini**
📊 **Dashboard Analisis Penyewaan Sepeda** adalah platform interaktif yang menyediakan **analisis tren penyewaan sepeda** berdasarkan berbagai faktor seperti **cuaca, suhu, dan waktu dalam sehari**.

🔍 **Fitur Utama**:
- **Analisis Penyewaan Sepeda Berdasarkan Cuaca & Suhu** 🌦️🌡️
- **Distribusi Penyewaan Sepeda Berdasarkan Waktu (Weekday vs Weekend)** ⏳📅

📌 **Tujuan**:
Membantu memahami pola peminjaman sepeda sehingga dapat digunakan untuk **pengambilan keputusan yang lebih baik** dalam pengelolaan sistem penyewaan sepeda.  
  
""")

st.sidebar.markdown("---")
st.sidebar.markdown(" **Terima kasih sudah mengunjungi dashboard ini!** 🙌")

st.caption('isminilam (c) 2025')
