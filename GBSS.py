import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

page_bg_img="""
<style>
[data-testid=""stAppViewContainer]
{
background-color : #fefbd8;
}
</style>
"""

dfgiziburuk = pd.read_csv("giziburuk.csv")
dfgiziburuk.drop(['id','kode_provinsi','nama_provinsi','bps_kode_kabupaten_kota','bps_kode_kecamatan','bps_kode_desa_kelurahan','kemendagri_kode_kecamatan','kemendagri_kode_desa_kelurahan','satuan'],axis=1,inplace=True)
dfgbfilters = dfgiziburuk[dfgiziburuk['bps_nama_kabupaten_kota'] == 'KABUPATEN SUBANG']

dfproduksisususapi = pd.read_csv("produksisususapi.csv")
dfproduksisususapi.drop(['id','kode_provinsi','nama_provinsi','kode_kabupaten_kota'],axis=1,inplace=True)
dfpsfilters = dfproduksisususapi[dfproduksisususapi['nama_kabupaten_kota'] == 'KABUPATEN SUBANG']

st.set_page_config(layout="wide")
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Korelasi Produksi Susu Sapi dengan Gizi Buruk di Kabupaten Subang")
st.write("Nurfitria Khoirunnisa")

option = st.sidebar.selectbox(
     'Silakan pilih:',
    ('Home','Dataframe','Chart')
)

# st.set_page_config(layout="wide")
# st.write("Nurfitria Khoirunnisa")
# st.caption("Dashboard Susu Sapi Gizi Buruk")
# st.write("Gizi buruk atau malnutrisi adalah kondisi serius yang terjadi ketika asupan makanan seseorang tidak sesuai dengan jumlah nutrisi yang dibutuhkan. Nutrisi yang didapat bisa terlalu sedikit atau terlalu banyak. Kondisi ini dapat menyebabkan banyak masalah kesehatan seperti stunting, gangguan mata, diabetes, dan penyakit jantung.")

if option == 'Home' or option == '':
    st.write("""# Halaman Utama""") #menampilkan halaman utama 
    st.header("Latar Belakang")
    st.write("Gizi buruk atau malnutrisi adalah kondisi serius yang terjadi ketika asupan makanan seseorang tidak sesuai dengan jumlah nutrisi yang dibutuhkan. Nutrisi yang didapat bisa terlalu sedikit atau terlalu banyak. Kondisi ini dapat menyebabkan banyak masalah kesehatan seperti ditandai dengan berat badan dan tinggi badan tidak sesuai umur atau dibawah rata-rata (stunting), gangguan mata, diabetes, dan penyakit jantung")
    st.write("Dari berita yang dimuat pada website suara.com tanggal 4 Agustus 2022, 7 juta anak Indonesia alami kekurangan gizi akibat dari adanya pandemi covid-19. Kemenkes mencatat, kasus stunting saat ini masih ada 24,4 persen dari sebelumnya 30,8 persen pada 2018. Sementara target pemerintah pada 2024, angka stunting tersisa 14 persen. ")
    st.write("Salah satu upaya yang dilakukan Kabupaten Subang dalam mengatasi permasalahan gizi adalah dengan program peningkatan konsumsi susu dalam kehidupan sehari-hari. ")
    st.header("Hipotesis")
    st.write("Akibat kondisi pandemi setelah dua tahun ini, menyebabkan peningkatan jumlah bayi kurus dan kurang gizi menjadi 15 persen.")
    st.header("Metode")
    st.write("Proses pengumpulan data dilakukan dengan cara mengambil dan mengekstraksi data dari sebuah website atau dikenal juga dengan Web Scraping")

elif option == 'Dataframe':
    st.write("""## Dataframe""") #menampilkan judul halaman dataframe
    #membuat dataframe dengan pandas yang terdiri dari 2 kolom dan 4 baris data 
    #importing data
    dfgiziburuk = pd.read_csv("giziburuk.csv")
    dfgiziburuk.drop(['id','kode_provinsi','nama_provinsi','bps_kode_kabupaten_kota','bps_kode_kecamatan','bps_kode_desa_kelurahan','kemendagri_kode_kecamatan','kemendagri_kode_desa_kelurahan','satuan'],axis=1,inplace=True)
    # st.write("Data Frame")
    # dfgiziburuk1 = pd.read_csv("giziburuk.csv")
    # dfgbfilters1= dfgiziburuk[dfgiziburuk['bps_nama_kabupaten_kota'] == 'KABUPATEN SUBANG']
    # st.dataframe(dfgbfilters1) #menampilkan dataframe
    
    #filter subang saja
    st.header("Data Frame Gizi Buruk di Subang")
    st.write("Berikut terlampir data kejadian gizi buruk di Kabupaten Subang. Data ini didapatkan dari data set kejadian Gizi Buruk di Provinsi Jawa Barat yang kemudian dilakukan filtering data khusus Kabupaten Subang saja")
    dfgbfilters = dfgiziburuk[dfgiziburuk['bps_nama_kabupaten_kota'] == 'KABUPATEN SUBANG']
    st.dataframe(dfgbfilters) #menampilkan dataframe

    #membuat dataframe dengan pandas yang terdiri dari 2 kolom dan 4 baris data
    dfproduksisususapi = pd.read_csv("produksisususapi.csv")
    dfproduksisususapi.drop(['id','kode_provinsi','nama_provinsi','kode_kabupaten_kota'],axis=1,inplace=True)
    # st.write("Data Frame")
    # st.dataframe(dfproduksisususapi)
    #filter subang saja
    st.header("Data Frame Produksi Susu Sapi di Subang")
    st.write("Berikut terlampir data produksi susu sapi di Kabupaten Subang. Data ini didapatkan dari data set Produksi Susu Sapi di Provinsi Jawa Barat yang kemudian dilakukan filtering data khusus Kabupaten Subang pada tahiun 2019 sampai dengan 2021 saja")
    dfpsfilters = dfproduksisususapi.query ('nama_kabupaten_kota == "KABUPATEN SUBANG"')
    dfpsfilter = dfpsfilters.query ('tahun >= 2019')
    st.dataframe(dfpsfilter) #menampilkan dataframe

elif option =='Chart':
    
    st.write("""### Draw Charts""") #menampilkan judul halaman
    st.write("Plotting Gizi Buruk")
    # Configuring plotting visual and sizes
    sns.set_style('whitegrid')
    sns.set_context('talk')
    params = {'legend.fontsize': 'x-large',
            'figure.figsize': (50, 100),
            'axes.labelsize': 'x-large',
            'axes.titlesize':'x-large',
            'xtick.labelsize':'x-large',
            'ytick.labelsize':'x-large'}
    plt.rcParams.update(params)
    fig,ax = plt.subplots()
    sns.pointplot(data=dfgbfilters[['jumlah_kejadian_balita_gizi_buruk',
                            'bps_nama_desa_kelurahan',
                            'tahun']],
                x='jumlah_kejadian_balita_gizi_buruk',
                y='bps_nama_desa_kelurahan',
                hue='tahun',
                ax=ax)
    ax.set(title="Gizi Buruk")
    st.pyplot(fig,ax)

    st.write("Plotting Produksi Susu Sapi")
    # Configuring plotting visual and sizes
    sns.set_style('whitegrid')
    sns.set_context('talk')
    params = {'legend.fontsize': 'x-large',
            'figure.figsize': (30, 30),
            'axes.labelsize': 'x-large',
            'axes.titlesize':'x-large',
            'xtick.labelsize':'x-large',
            'ytick.labelsize':'x-large'}
    plt.rcParams.update(params)
    fig,ax = plt.subplots()
    sns.pointplot(data=dfpsfilters[['jumlah_produksi',
                            'tahun',
                            'nama_kabupaten_kota']],
                x='jumlah_produksi',
                y='tahun',
                hue='nama_kabupaten_kota',
                ax=ax)
    ax.set(title="Produksi Susu Sapi")
    st.pyplot(fig,ax)


    df = pd.DataFrame(np.random.randn(250, 2) / [50, 50] + [-6.56985, 107.762831],
    columns=['lat', 'lon'])
    st.map(df)

