from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class EkstrakFeature:
    def __init__(self, link, b, c):
        #setup driver
        opt = webdriver.ChromeOptions()
        #opt.add_argument('headless')
        opt.add_argument('--header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}')
        self.__browser = webdriver.Chrome(executable_path="chromedriver.exe", options=opt)
        #get url
        self.__browser.get(link,)
        time.sleep(2)
        #click button
        try:
            button = self.__browser.find_element(By.XPATH,'//button[@class="Detail_btn-show__fEx09 Button_ui-atomic-button__my_nP Button_ui-atomic-button__size-large__bqtCl Button_ui-atomic-button__theme-default__Y2GTX"]')
            self.__browser.execute_script("arguments[0].click();", button) 
        except:
            skip = ''
        #find elements
        o = self.__browser.find_elements(By.XPATH,'//td[@class="Detail_attribute-table-header__7uTHo"]')
        io = self.__browser.find_elements(By.XPATH,'//td[@class="Detail_attribute-table-description__2AQ2l"]')
        #extract elements
        self.__header = []
        self.__descr = []
        for o_ in o:
            self.__header.append(o_.text)
        for io_ in io:
            self.__descr.append(io_.text)        
        # bs4
        self.__soup = BeautifulSoup(self.__browser.page_source, "html.parser")

        # Tanggal
        tanggal = self.__soup.findAll('div', 'style_ui-molecules-badge__3YCKy style_ui-molecules-badge__theme-light-blue__0dYYn')
        tanggal = tanggal[2].text.split(' : ')[1].split(' ')
        if tanggal[1] == 'JAN':
            tanggal[1] = '01'
        elif tanggal[1] == 'FEB':
            tanggal[1] = '02'
        elif tanggal[1] == 'MAR':
            tanggal[1] = '03'
        elif tanggal[1] == 'APR':
            tanggal[1] = '04'
        elif tanggal[1] == 'MAY':
            tanggal[1] = '05'
        elif tanggal[1] == 'JUN':
            tanggal[1] = '06'
        elif tanggal[1] == 'JUL':
            tanggal[1] = '07'
        elif tanggal[1] == 'AUG':
            tanggal[1] = '08'
        elif tanggal[1] == 'SEP':
            tanggal[1] = '09'
        elif tanggal[1] == 'OCT':
            tanggal[1] = '10'
        elif tanggal[1] == 'NOV':
            tanggal[1] = '11'
        elif tanggal[1] == 'DEC':
            tanggal[1] = '12'
        tanggal = '{}-{}-{}'.format(tanggal[2],tanggal[1],tanggal[0])
        self.__tanggal = datetime.strptime(tanggal,'%Y-%m-%d').date()

        # Harga
        harga = self.__soup.findAll('div','style_ui-molecules-listing-price__price-tag__Rtrg6')
        self.__harga = int(harga[0].text.replace('Rp ', '').replace(',-','').replace('.',''))

        # Luas Bangunan
        luas_bangunan = self.__soup.findAll('div','style_property-detail-attribute--item__Dxx5r')
        self.__luas_bangunan =  int(luas_bangunan[3].text.replace('LB','').split(' ')[0])

        # Luas Tanah
        luas_tanah = self.__soup.findAll('div','style_property-detail-attribute--item__Dxx5r')
        self.__luas_tanah =  int(luas_tanah[2].text.replace('LT','').split(' ')[0])

        # Kamar Tidur
        try:
            kamar_tidur = self.__soup.findAll('div','style_property-detail-attribute--item__Dxx5r')
            kamar_tidur =  kamar_tidur[0].text.replace('LT','').split(' ')[0]
            # Kamar Tidur Pembantu
            if 'Kamar Tidur Pembantu' in self.__header:
                index = self.__header.index('Kamar Tidur Pembantu')
                kamar_tidur_p = self.__descr[index]
            else:
                kamar_tidur_p = 0
            self.__bedroom = int(kamar_tidur) + int(kamar_tidur_p)
        except:
            self.__bedroom = 0

        # Kamar Mandi
        try:
            kamar_mandi = self.__soup.findAll('div','style_property-detail-attribute--item__Dxx5r')
            kamar_mandi =  kamar_mandi[1].text.replace('LT','').split(' ')[0]
            # Kamar Mandi Pembantu
            if 'Kamar Mandi Pembantu' in self.__header:
                index = self.__header.index('Kamar Mandi Pembantu')
                kamar_mandi_p = self.__descr[index]
            else:
                kamar_mandi_p = 0
            self.__bathroom = int(kamar_mandi) + int(kamar_mandi_p)                
        except:
            self.__bathroom = 0

        # Sertifikat
        if 'Sertifikat' in self.__header:
            index = self.__header.index('Sertifikat')
            self.__sertifikat = self.__descr[index]
        else:
            self.__sertifikat = '-'  

        # Lantai
        if 'Jumlah Lantai' in self.__header:
            index = self.__header.index('Jumlah Lantai')
            self.__floor = int(self.__descr[index])
        else:
            self.__floor = 1

        # Garasi
        if 'Garasi' in self.__header:
            index = self.__header.index('Garasi')
            self.__garage = int(self.__descr[index])
        else:
            self.__garage = 0        

        # Carplots
        if 'Carpots' in self.__header:
            index = self.__header.index('Carpots')
            self.__carpots = int(self.__descr[index])
        else:
            self.__carpots = 0   

        # Tipe Properti
        if 'Tipe Properti' in self.__header:
            index = self.__header.index('Tipe Properti')
            self.__tipe = self.__descr[index]
        else:
            self.__tipe = 'Rumah'  

        # Daya Listrik
        if 'Daya Listrik' in self.__header:
            index = self.__header.index('Daya Listrik')
            watt = self.__descr[index]
            try:
                self.__watt = int(watt.replace(' Watt',''))
            except:
                self.__watt = 0
        else:
            self.__watt = 0     

        # Kab
        try:
            alamat = self.__soupfindAll('div', 'Address_wrapper-address__eIXy0')
            alamat = alamat[0].text.split(', ')
            self.__kab = alamat[1]
        except:
            self.__kab = b.lower()

        # Kec
        try:
            alamat = self.__soupfindAll('div', 'Address_wrapper-address__eIXy0')
            alamat = alamat[0].text.split(', ')
            self.__kec = alamat[0]
        except:
            self.__kec = c.replace('-', ' ')

        self.__browser.close()
    
    def ekstrak_date(self):
        return self.__tanggal
    
    def ekstrak_price(self):
        return self.__harga
    
    def ekstrak_lb(self):
        return self.__luas_bangunan
    
    def ekstrak_lt(self):
        return self.__luas_tanah
    
    def ekstrak_bedroom(self):
        return self.__bedroom
    
    def ekstrak_bathroom(self):

        return self.__bathroom
    
    def ekstrak_certifikat(self):
        return self.__sertifikat
    
    def ekstrak_floor(self):
        return self.__floor
    
    def ekstrak_garage(self):
        return self.__garage
    
    def ekstrak_carpots(self):
        return self.__carpots
    
    def ekstrak_type(self):
        return self.__tipe

    def ekstrak_watt(self):       
        return self.__watt
    
    def ekstrak_kab(self):
        return self.__kab
    
    def ekstrak_kec(self):
        return self.__kec

class EkstrakPages:
    def __init__(self, link):
        #setup driver
        opt = webdriver.ChromeOptions()
        #opt.add_argument('headless')
        opt.add_argument('--header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}')
        self.__browser = webdriver.Chrome(executable_path="chromedriver.exe", options=opt)
        #get url
        self.__browser.get(link,)
        time.sleep(2)
        # bs4
        self.__soup = BeautifulSoup(self.__browser.page_source, "html.parser")
        # Ekstrak Link
        self.__link = []
        divs = self.__soup.find_all('div', {'class': 'style_ui-molecules-card-secondary__content-info_wrapper__RjnEZ'})
        for div in divs:
            links = div.find_all('a', {'class': 'style_ui-molecules-card-secondary__content-info_detail__IqXHZ'})
            for i in links:
                self.__link.append(i.get('href'))

        # Alamat Lengkap
        self.__alamat = []
        address = self.__soup.findAll('div', 'style_ui-molecules-card-secondary__content-info_detail--main__GaMJD')
        for i in range(len(address)):
            #data = i.find('span', 'block mb-8 ui-atomic-text ui-atomic-text--style-h6 ui-atomic-text--font-secondary ui-atomic-text--font-weight-normal ui-atomic-text--align-initial').text
            self.__alamat.append(address[i].find('address').text.lower())

        self.__browser.close()

    def ekstrak_link(self):
        return self.__link

    def ekstrak_address(self):
        return self.__alamat