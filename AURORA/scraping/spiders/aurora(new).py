import scrapy
import time
import os.path
import sys
import codecs
koden=sys.stdin.encoding
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

from datetime import datetime
import logging

output_timestamp = datetime.today().strftime('%Y-%m-%d-%H%M')
log_output_file = 'scrape-order-images-{}.log'.format(output_timestamp)

class ProductSpider(scrapy.Spider):
    name = "aurora_new"
    allowed_domains = ['www.auroragroup.se']
    start_urls = ['http://www.auroragroup.se/']

    def __init__(self):
        # self.driver = webdriver.Chrome("./chromedriver.exe")
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)

    def parse(self, response):
        fh = logging.FileHandler(log_output_file)
        fh.setLevel(logging.INFO)

        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        logging.getLogger('selenium.webdriver.remote.remote_connection').addHandler(fh)
        logging.getLogger('urllib3.connectionpool').addHandler(fh)
        logging.getLogger().addHandler(fh)
        self.loggger = logging.getLogger()
        self.loggger.info('Start')


        self.driver.get(response.url)
        list1 = []
        list2 = []
     
        csv_name = ''
        csv_stock = ''
        csv_margin = ''
        csv_price = ''
        csv_price_recommended = ''
        # csv_desciption = ''
        csv_category = ''
        csv_image_url = []
        csv_artno = ''
        old_product_url = []
        csv_ean = ''
        csv_weight = ''
        csv_summary = ''

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'qmhlbl')))
        login_btn = self.driver.find_element_by_id('qmhlbl')
        login_btn.click()
        time.sleep(3)
        username = self.driver.find_element_by_id('Username')
        time.sleep(1)
        username.send_keys("raatish")
        username = self.driver.find_element_by_id('Password')
        time.sleep(1)
        username.send_keys("rshabnam7878")
        login = self.driver.find_element_by_id('loginbut')
        time.sleep(1)
        login.click()
        time.sleep(5)

        list1.append('http://www.auroragroup.se/sv/#ac=m_W3S&ns=ns2&vs=v3')
        list1.append('http://www.auroragroup.se/sv/#ac=m_W3C&ns=ns2&vs=v3')
        list1.append('http://www.auroragroup.se/sv/#ac=m_W3M&ns=ns2&vs=v3')
        list1.append('http://www.auroragroup.se/sv/#ac=m_W3P&ns=ns2&vs=v3')
        list1.append('http://www.auroragroup.se/sv/#ac=m_W3W&ns=ns2&vs=v3')
        list1.append('http://www.auroragroup.se/sv/#ac=m_W3H&ns=ns2&vs=v3')
        list1.append('http://www.auroragroup.se/sv/#ac=m_W3U&ns=ns2&vs=v3')


        #Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open("aurora.csv") as old_file:
                for line in old_file:
                    new_file.write(line.replace('NEW', 'old'))
        #Remove original file
        remove("aurora.csv")
        #Move new file
        move(abs_path, "aurora.csv")

        with open('aurora.csv', 'r') as ins:
            for line in ins:
                old_product_url.append(line.split(',')[-1])
        
        file = open("aurora.csv", "a")
        # file.write('O/N' + ',' + 'Category' + ',' + 'Name' + ',' + 'Rec.Price' + ',' + 'Price' + ',' + 'EAN' + ',' + 'Supplier ID' + ',' + 'Article No' + ',' + 'Weight' + ',' + 'Stock' + ',' + 'Description_html' + ',' + 'image_1' + ',' + 'image_2' + ',' + 'image_3' + ',' + 'image_4' + ',' + 'image_5' + ',' + 'image_6' + ',' + 'image_7' + ',' + 'image_8' + ',' + 'image_9' + ',' + 'image_10' + ',' + 'image_11' + ',' + 'image_12' + ',' + 'image_13' + ',' + 'image_14' + ',' + 'image_15' + ',' + 'PageUrl' + '\n')

        for i in range(0, len(list1)):
            self.loggger.info(str(len(list1)) + '**********' + str(i) + '***********')
            self.loggger.info('**********' + list1[i] + '***********')
            self.driver.get(list1[i])
            time.sleep(5)
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID,'results')))
                results = self.driver.find_element_by_id('results')
                result_val = int(results.text.split(' ')[0])
                products = self.driver.find_elements_by_class_name('pic222px')
                while result_val > len(products):
                    if result_val == len(products):
                        break
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        more_btn = self.driver.find_element_by_id('lml')
                        more_btn.click()
                        time.sleep(3)
                        pass
                    except:
                        self.log('error')
                    products = self.driver.find_elements_by_class_name('pic222px')
            except:
                self.loggger.info('page loading error!')

            try:
                for item_id in self.driver.find_elements_by_class_name('itemid'):
                    list2.append(list1[i][:-5] + 'pi=p' + item_id.text.split(' ')[1] + '&vs=v3')
            except:
                self.loggger.info('item getting error!')


        for j in range(0, len(list2)):
            try:
                self.loggger.info(str(len(list2)) + '**********' + str(j) + '***********')
                self.loggger.info('**********' + str(list2[j]) + '***********')
                if list2[j] not in old_product_url:
                    self.driver.get(list2[j])
                    time.sleep(5)

                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "productinfotitle")))
                    try:
                        name = self.driver.find_element_by_id('productinfotitle')
                        csv_name = name.text.split('\n')[-1].replace(',', ' ')
                    except:
                        self.loggger.info('name non-exist')
                        csv_name = ''

                    if list2[j].split('&')[0][-1:] == 'S':
                        csv_category = 'SOUND & PICTURE'
                    if list2[j].split('&')[0][-1:] == 'C':
                        csv_category = 'COMPUTER & GAMES'
                    if list2[j].split('&')[0][-1:] == 'M':
                        csv_category = 'MOBILE & TELECOM'
                    if list2[j].split('&')[0][-1:] == 'P':
                        csv_category = 'SPORTS'
                    if list2[j].split('&')[0][-1:] == 'W':
                        csv_category = 'APPLIANCE'
                    if list2[j].split('&')[0][-1:] == 'H':
                        csv_category = 'ELECTRICITY & LIGHTING'
                    if list2[j].split('&')[0][-1:] == 'U':
                        csv_category = 'AURORA PROFESSIONAL'

                    try:
                        infoprice = self.driver.find_element_by_id('infoprice')
                        csv_price = infoprice.text.split(' ')[-1].replace('.', '').replace(',', '.')
                    except:
                        self.loggger.info('price non-exist')
                        csv_price = ''

                    try:
                        infobasket = self.driver.find_element_by_id('infobasket')
                        for info in infobasket.find_elements_by_xpath('.//tr'):
                            if 'SRP' in info.text:
                                csv_price_recommended = info.text.split(' ')[-1].replace('.', '').replace(',', '.')
                            if 'EAN' in info.text:
                                csv_ean = info.text.split(' ')[-1]
                            if 'Leverantörens' in info.text:
                                csv_supplierid = info.text.split(' ')[-1]
                            if 'Artikel' in info.text:
                                csv_artno = info.text.split(' ')[-1]
                            if 'Vikt' in info.text:
                                csv_weight = info.text.split(' ')[-1].replace(',', '.')
                            if 'Förväntad' in info.text:
                                csv_stock = '0'
                            if 'Bidragsmarginal' in info.text:
                                csv_margin = info.text.split(' ')[-1].replace(',', '.')
                            if 'lager' in info.text:
                                csv_stock = info.text.split(' ')[-2].replace(',', '.')
                    except:
                        self.loggger.info('info basket non-exist')
                        csv_price_recommended = ''
                        csv_ean = ''
                        csv_supplierid = ''
                        csv_artno = ''
                        csv_weight = ''
                        csv_stock = ''
                        csv_margin = ''
                        csv_stock = ''

                    try:
                        summary = self.driver.find_element_by_id('tab2_content')
                        csv_summary = summary.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip()
                    except:
                        self.loggger.info('summary non-exist')
                        csv_summary = ''

                    try:
                        overlayicon = self.driver.find_element_by_id('overlayicons')
                        overlayicon.click()
                    except:
                        self.loggger.info('overlay icon click error!')

                    csv_image_url = []
                    try:
                        pimages = self.driver.find_elements_by_class_name('igthumb')
                        for count in range(1, len(pimages) + 1):
                            if count < 10:
                                csv_image_url.append('http://www.auroragroup.se/actions/aGetImage.aspx?n=' + csv_artno + '_0' + str(count) + '.jpg&s=800x800&f=png')
                            else:
                                csv_image_url.append('http://www.auroragroup.se/actions/aGetImage.aspx?n=' + csv_artno + '_' + str(count) + '.jpg&s=800x800&f=png')
                    except:
                        self.loggger.info('image non-exist')
                        csv_image_url = []
                    
                    try:
                        if len(csv_image_url) == 1:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 2:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 3:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 4:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 5:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 6:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 7:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 8:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 9:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 10:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 11:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 12:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 13:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 14:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 15:
                            file.write('NEW' + ',' + csv_category + ',' + csv_name + ',' + csv_price + ',' + csv_price_recommended + ',' + csv_ean + ',' + csv_supplierid + ',' + csv_artno + ',' + csv_margin + ',' + csv_weight + ',' + csv_stock + ',' + csv_summary + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + list2[j] + '\n')
                    except:
                        self.loggger.info('file write error!')
            except:
                self.log('error')
          
        file.close()
        self.driver.close()
