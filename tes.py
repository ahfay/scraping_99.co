from ekstrak import EkstrakFeature
import pandas as pd

ekstrak = EkstrakFeature('https://www.99.co/id/properti/rumah-siap-huni-semi-furnish-di-jundul-1001027122','Limapuluh', 'Pekanbaru')
row = []
data = [[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
coloumn = ['harga','luas_tanah','luas_bangunan', 'lantai', 'kamar_tidur','kamar_mandi','garasi','carpots','daya_listrik','type','sertifikat','tanggal','kec','kab/kota','prov','link']
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
prov = 'Prov' # Menambahkan provinsi
garasi = ekstrak.ekstrak_garage() # Menambahkan Garasi
carplot = ekstrak.ekstrak_carpots() # Menambahkan Carplots
watt = ekstrak.ekstrak_watt() # Menambahkan Daya Listrik
type = ekstrak.ekstrak_type() # Menambahkan Tipe Properti
link_id = 'https://www.99.co/id/properti/rumah-cantik-di-dekat-bandara-ssk-simpang-tiga-21967709334'

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
row.append(link_id)
data.append(row)

df = pd.DataFrame(data=data[1:], columns=coloumn)
df.to_csv('D:/FAYYYAD/PROGRES MAGANG/test2/Indonesia/test.csv', index=False)