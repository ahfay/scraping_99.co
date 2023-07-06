from ekstrak import EkstrakPages
from load import CreateDataframe
import pandas as pd
import os
from time import sleep
import requests
from bs4 import BeautifulSoup
from ekstrak import EkstrakFeature

firt_running_program = True
# Data berisi dafftar Provinsi dan kabupaten kotanya
df = pd.read_csv('wil_ind.csv')
subcity = pd.read_csv('kab_kec.csv')

# Menentukan lokasi penyimpanan hasil scrapping
path_indo = os.path.join('web99', 'Indonesia')
path_prov = os.path.join('web99', 'Prov')
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'
}

tag_divs = 'div'
tag_address = 'div'
tag_addr = 'span'
tag_date = 'div'
tag_price = 'p'
tag_lb = 'div'
tag_lt = 'div'
tag_bedroom = 'div'
tag_bathroom = 'div'
tag_cert = 'div'
tag_floor = 'div'
tag_kab_kec = 'div'
attr_divs = 'style_ui-molecules-card-secondary__content-info_wrapper__RjnEZ'
attr_link = {'class': 'ui-molecules-secondary-card__link'}
attr_address = 'relative ui-molecules-secondary-card__description'
attr_addr = 'block mb-8 ui-atomic-text ui-atomic-text--style-h6 ui-atomic-text--font-secondary ui-atomic-text--font-weight-normal ui-atomic-text--align-initial'
attr_date = 'style_ui-molecules-badge__3YCKy style_ui-molecules-badge__theme-light-blue__0dYYn'
attr_price = 'style_ui-molecules-listing-price__price-tag__Rtrg6'
attr_lb = 'style_property-detail-attribute--item__Dxx5r'
attr_lt = 'style_property-detail-attribute--item__Dxx5r'
attr_bedroom = 'style_property-detail-attribute--item__Dxx5r'
attr_bathroom = 'style_property-detail-attribute--item__Dxx5r'
attr_cert = 'style_wrapper-attribute__YLGFs detail-attribute'
attr_floor = 'style_wrapper-attribute__YLGFs detail-attribute'
attr_kab_kec = 'Address_wrapper-address__eIXy0'

build_df = CreateDataframe() # Objek Untuk Membuat Dataframe

# Membuat Folder Indonesia dan Prov
try:
    os.mkdir(path_indo)
    os.mkdir(path_prov)
except:
    skip = ''

# Load Checkpoint
try:
    checkpoint = pd.read_csv("D:/FAYYYAD/PROGRES MAGANG/test2/Indonesia/CHECKPOINT.csv")
except:
    skip = ''

# List Seluruh Provinsi
list_prov = df['Provinsi'].unique()
# Load Checkpoint Provinsi
try:
    list_prov = list_prov[checkpoint['PROV'][0]:]
except:
    skip = ''

for ai, a in enumerate(list_prov): # Ekstrak List Provinsi Beserta Indeksnya
    checkpoint_kab = 0
    print('====================')
    print('[Start] PROV ', a)
    dir_prov = os.path.join(path_prov, a) 
    try:
        os.mkdir(dir_prov) # Membuat Folder Nama Provinsi di dalam Folder Prov
    except:
        skip = ''
    list_kab = df[df['Provinsi'] == a ]['Kabupaten / Kota'] # Membuat List Seluruh kabupaten di 1 Provinsi
    list_kab = list_kab.unique()

    # LOAD CHECKPOINT KABUPATEN
    try:
        if firt_running_program == True:
            list_kab = list_kab[checkpoint['KAB'][0]:]
    except:
        skip =''

    for bi, b in enumerate(list_kab): # Ekstrak List Kabupaten Beserta Indeksnya
        try:
            if firt_running_program == True:
                checkpoint_kec = checkpoint['KEC'][0]
                checkpoint_kab = checkpoint['KAB'][0]
            else:
                checkpoint_kec = -1
        except:
            skip = ''

        # Variabel Untuk Menyiman Data yang Error
        error = []
        ket_error = []

        dir_kab = os.path.join(dir_prov, b) 
        try:
            os.mkdir(dir_kab) # Membuat Folder Nama Kabupaten di dalam Folder Prov
        except:
            skip = ''
        print('[Start] KAB ', b)

        # Membuat List Seluruh Kecamatan di 1 Kabupaten
        list_kec = None
        try:
            list_kec = subcity[subcity['Kab'] == b]['Kec']
            try:
                if checkpoint_kec + 1 == len(list_kec):
                    list_kec = None
                else:
                    list_kec = list_kec[checkpoint_kec + 1:]
            except:
                print('[ERROR] UNKNOWN KAB ', b)
                error.append(b)
                ket_error.append('UNKNOWN')
        except:
            print('[ERROR] TYPO KAB ', b)
            error.append(b)
            ket_error.append('TYPO')
        if list_kec is None:
            try:
                df_checkpoint = build_df.dataframe_checkpoint(checkpoint=checkpoint, path_indo=path_indo, ai=ai, bi=checkpoint_kab+bi, ci=0)
                print(df_checkpoint)
            except:
                checkpoint = None
                df_checkpoint = build_df.dataframe_checkpoint(checkpoint=checkpoint, path_indo=path_indo, ai=ai, bi=checkpoint_kab+bi, ci=0)
                print(df_checkpoint)
            pass
        elif len(list_kec) == 0:
            print('[ERROR] NOTHING KAB ', b)
            error.append(b)
            ket_error.append('TIDAK ADA')
            # Dataframe Check Point
            try:
                df_checkpoint = build_df.dataframe_checkpoint(checkpoint=checkpoint, path_indo=path_indo, ai=ai, bi=checkpoint_kab+bi, ci=0)
                print(df_checkpoint)
            except:
                checkpoint = None
                df_checkpoint = build_df.dataframe_checkpoint(checkpoint=checkpoint, path_indo=path_indo, ai=ai, bi=checkpoint_kab+bi, ci=0)
                print(df_checkpoint)
            pass
        else:            
            for ci, c in enumerate(list_kec): # Ekstrak List Kecamatan Beserta Indeksnya
            
                print('[Start] KEC ', c)
                data = [[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
                broken_link = []
                c_ = c.lower().replace(' ', '-')
                halaman = 1
                url = "https://www.99.co/id/jual/rumah/{}/{}?hlmn={}".format(b, c_, halaman)
                req = requests.get(url, headers=header)
                soup = BeautifulSoup(req.text, 'html.parser')
                divs = soup.find_all('div', attr_divs)
                try:
                    head_search = soup.findAll('div', 'style_ui-srp-heading__6SDF6')[0].text
                except:
                    head_search = 'KOSONG'
                head_title = "{}, {}".format(c.lower(), b.lower())
                if head_search == []:
                    head_search = 'KOSONG'
                if head_title in head_search.lower():
                    while divs != []:
                        sleep(0.15) # Jeda Waktu
                        
                        url = "https://www.99.co/id/jual/rumah/{}/{}?hlmn={}".format(b, c_, halaman)
                        req = requests.get(url, headers=header)
                        soup = BeautifulSoup(req.text, 'html.parser')
                        divs = soup.find_all('div', attr_divs)

                        if divs != []:
                            ekstrak_ = EkstrakPages(url)
                            link = ekstrak_.ekstrak_link() # Ekstrak Link
                            alamat_lengkap = ekstrak_.ekstrak_address() # Ekstrak Alamat Lengkap
        
                            # Scarpping per Link yang sudah di dapatkan dari setiap halaman
                            for index, url in enumerate(link):
                                
                                print("[PROCESS] Prov ", a, " Kab/Kota", b, " Kec ", c_, ' Halaman ', halaman, ' LINK ', index + 1, '/', len(link))
                                sleep(0.15) # Jeda Waktu
                                status = False
                                batas = 1
                                while status != True:
                                    row = []
                                    
                                    try:
                                        ekstrak = EkstrakFeature(url, b, c)
                                        tanggal = ekstrak.ekstrak_date() # Ekstrak Tanggal Posting
                                        harga = ekstrak.ekstrak_price() # Ekstrak Harga
                                        luas_bangunan = ekstrak.ekstrak_lb() # Ekstrak Luas Bangunan
                                        luas_tanah = ekstrak.ekstrak_lt() # Ekstrak Luas Tanah
                                        kamar_tidur = ekstrak.ekstrak_bedroom() # Ekstrak Jumlah Kamar Tidur
                                        kamar_mandi = ekstrak.ekstrak_bathroom() # Ekstrak Jumlah Kamar Mandi
                                        sertifikat = ekstrak.ekstrak_certifikat() # Ekstrak Sertifikat
                                        jumlah_lantai = ekstrak.ekstrak_floor() # Ekstrak Berapa Lantai
                                        kab = ekstrak.ekstrak_kab() # Ekstrak Kabupaten
                                        kec = ekstrak.ekstrak_kec() # Ekstrak Kecataman
                                        prov = a.lower() # Menambahkan provinsi
                                        garasi = ekstrak.ekstrak_garage() # Menambahkan Garasi
                                        carplot = ekstrak.ekstrak_carpots() # Menambahkan Carplots
                                        watt = ekstrak.ekstrak_watt() # Menambahkan Daya Listrik
                                        type = ekstrak.ekstrak_type() # Menambahkan Tipe Properti
                                        link_id = url

                                        row.append(harga)
                                        row.append(luas_tanah)
                                        row.append(luas_bangunan )
                                        row.append(jumlah_lantai)
                                        row.append(kamar_tidur)
                                        row.append(kamar_mandi)
                                        row.append(garasi)
                                        row.append(carplot)
                                        row.append(watt)
                                        row.append(type)
                                        row.append(sertifikat)
                                        row.append(tanggal)
                                        row.append(kec)
                                        row.append(kab)
                                        row.append(prov)
                                        row.append(alamat_lengkap[index])
                                        row.append(link_id)
                                        data.append(row)
                                        status = True
                                    except:
                                        print('[ERROR] URL', url)
                                        sleep(1)
                                        
                                        if batas == 3:
                                            error.append(b)
                                            ket_error.append(url)
                                            batas += 1
                                            status = True
                                        else:
                                            batas += 1
                                
                            halaman += 1
                    else:
                        print('[End] KEC ', c, halaman - 1, 'Halaman')
                else:
                    print('[End] KEC ', c, halaman - 1, 'Halaman')


                # Dataframe KECAMATAN
                df_kec = build_df.dataframe_kec(data=data, dir_kab=dir_kab, c=c)
                print(df_kec)
            
                # Dataframe Check Point
                try:
                    if checkpoint_kec == -1:
                        df_checkpoint = build_df.dataframe_checkpoint(checkpoint=checkpoint, path_indo=path_indo, ai=ai, bi=checkpoint_kab+bi, ci=checkpoint_kec+1+ci)
                        print(df_checkpoint)
                    else:
                        df_checkpoint = build_df.dataframe_checkpoint(checkpoint=checkpoint, path_indo=path_indo, ai=ai, bi=checkpoint_kab+bi, ci=checkpoint_kec+1+ci)
                        print(df_checkpoint)
                except:
                    checkpoint = zip([ai], [bi], [ci])
                    df_checkpoint = build_df.dataframe_checkpoint(checkpoint=checkpoint, path_indo=path_indo, ai=ai, bi=bi, ci=ci)
                    print(df_checkpoint)

                firt_running_program = False

            # Dataframe KABUPATEN
            df_kab = build_df.dataframe_kab(dir_kab=dir_kab, dir_prov=dir_prov, b=b)
            print(df_kab)

        # Dataframe ERROR
        if error != []:
            build_df.dataframe_error(error=error, ket_error=ket_error, path_indo=path_indo, b=b)

    # Dataframe PROVINSI
    df_prov = build_df.dataframe_prov(dir_prov=dir_prov, path_indo=path_indo, a=a)
    print(df_prov)

# DATAFRAME ALL PROVINSI
build_df.dataframe_allprof(path_indo=path_indo)
