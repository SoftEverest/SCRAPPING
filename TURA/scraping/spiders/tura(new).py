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
    name = "tura_new"
    allowed_domains = ['www.turascandinavia.com']
    start_urls = ['https://shop.turascandinavia.com/sv/inloggningssida']

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)

    def parse(self, response):
        # Quiet down all the unnecessary logging. 
        fh = logging.FileHandler(log_output_file)
        fh.setLevel(logging.INFO)
        
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

        logging.getLogger('selenium.webdriver.remote.remote_connection').addHandler(fh)
        logging.getLogger('urllib3.connectionpool').addHandler(fh)
        logging.getLogger().addHandler(fh)
        self.loggger = logging.getLogger()

        self.driver.get(response.url)
        list1 = []
        list2 = []
        list3 = []
        
        csv_categories = []
        csv_heading = ''
        csv_stock = ''
        csv_price = ''
        csv_desc = ''
        csv_brand = ''
        csv_gtin = ''
        csv_rec_price = ''
        csv_weight = ''
        csv_article_number = ''
        csv_supplier = ''
        csv_length = ''
        csv_image_url = []
        old_product_url = []
      
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,'LoginFormModel_UserName')))
        username = self.driver.find_element_by_id('LoginFormModel_UserName')
        username.send_keys("info@themobilestore.se")
        username = self.driver.find_element_by_id('LoginFormModel_Password')
        username.send_keys("x6yvzW2LUG")
        login = self.driver.find_element_by_class_name('submit')
        time.sleep(1)
        login.click()

        #Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open("tura.csv") as old_file:
                for line in old_file:
                    new_file.write(line.replace('NEW', 'old'))
        #Remove original file
        remove("tura.csv")
        #Move new file
        move(abs_path, "tura.csv")

        with open('tura.csv', 'r') as ins:
            for line in ins:
                old_product_url.append(line.split(',')[-1])

        file = open("tura.csv", "a", errors ='replace')
        # file.write('O/N' + ',' + 'Name' + ',' + 'Category1' + ',' + 'Category2' + ',' + 'Category3' + ',' + 'Category4' + ',' + 'Price' + ',' + 'Article Number' + ',' + 'EAN' + ',' + 'Stock' + ',' + 'Description_html' + ',' + 'image_1' + ',' + 'image_2' + ',' + 'image_3' + ',' + 'image_4' + ',' + 'image_5' + ',' + 'image_6' + ',' + 'image_7' + ',' + 'image_8' + ',' + 'image_9' + ',' + 'image_10' + ',' + 'image_11' + ',' + 'image_12' + ',' + 'image_13' + ',' + 'image_14' + ',' + 'image_15' + ',' + 'image_16' + ',' + 'image_17' + ',' + 'image_18' + ',' + 'PageUrl' + '\n')
        self.driver.get('https://shop.turascandinavia.com/sv/produkter')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'side-nav')))
        wrapper1 = self.driver.find_element_by_class_name('side-nav')
        for child_wrapper1 in wrapper1.find_elements_by_class_name('has-children'):
            category_url = child_wrapper1.find_element_by_xpath('.//a')
            if category_url.get_attribute('href') != 'https://shop.turascandinavia.com/sv/produkter':
                list1.append(category_url.get_attribute('href'))

        for i in range(0, len(list1)):
            self.loggger.info('***************i  ' + str(len(list1)) + '    ' + str(i) + '  i***************')
            self.driver.get(list1[i])
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'pagination')))
                pagenation = self.driver.find_element_by_class_name('pagination')
                pages = pagenation.find_elements_by_xpath('.//a')
                for j in range(1, int(pages[len(pages)-2].text) + 1):
                    list2.append(list1[i] + '?page=' + str(j))
            except:
                list2.append(list1[i] + '?page=' + str(1))


        # for m in range(0, 5):    IF YOU WANT TO DOWNLOAD CERTAIN PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(list2)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for k in range(0, len(list2)):
            self.loggger.info('***************k  ' + str(len(list2)) + '    ' + str(k) + '  k***************')
            self.driver.get(list2[k])
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'product-list')))
            wrapper2 = self.driver.find_element_by_class_name('product-list')
            for child_wrapper2 in wrapper2.find_elements_by_class_name('product-image'):
                try:
                    product_url = child_wrapper2.find_element_by_xpath('.//a')
                    list3.append(product_url.get_attribute('href'))
                except:
                    self.loggger.info('error')

        # for m in range(0, 20):    IF YOU WANT TO DOWNLOAD CERTAIN PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(list3)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for m in range(0, len(list3)):
            try:
                self.loggger.info('***************m  ' + str(len(list3)) + '    ' + str(m) + '  m***************')
                self.loggger.info('**********' + str(list3[m]) + '***********')
                self.driver.get(list3[m])
                if list3[m] not in old_product_url:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'breadcrumbs')))
                    try:
                        breadcrumbs = self.driver.find_element_by_class_name('breadcrumbs')
                        csv_categories = []
                        for category in breadcrumbs.find_elements_by_xpath('.//a'):
                            csv_categories.append(category.text)
                    except:
                        self.loggger.info('category non-exist')
                        csv_categories = []

                    if len(csv_categories) == 3:
                        csv_categories.append(' ')
                        csv_categories.append(' ')
                        csv_categories.append(' ')
                    if len(csv_categories) == 4:
                        csv_categories.append(' ')
                        csv_categories.append(' ')
                    if len(csv_categories) == 5:
                        csv_categories.append(' ')
                    csv_heading = csv_categories[5]
                    
                    try:
                        image = self.driver.find_element_by_class_name('carousel')
                        pimages = image.find_elements_by_xpath('.//img')
                        csv_image_url = []
                        for pimage in pimages:
                            image_url = pimage.get_attribute('src')
                            csv_image_url.append(image_url)
                        if len(csv_image_url) == 1:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 2:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 3:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 4:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 5:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 6:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 7:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 8:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 9:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 10:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 11:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 12:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 13:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 14:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 15:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 16:
                            csv_image_url.append(' ')
                            csv_image_url.append(' ')
                        elif len(csv_image_url) == 17:
                            csv_image_url.append(' ')
                    except:
                        csv_image_url = []

                    try:
                        product_info = self.driver.find_element_by_class_name('product-info')
                        brand = product_info.find_element_by_xpath('.//h2')
                        csv_brand = brand.text
                    except:
                        self.loggger.info('brand non-exist')
                        csv_brand = ''

                    try:
                        article_number = self.driver.find_element_by_class_name('product-id')
                        csv_article_number = article_number.text.split(' ')[-1]
                    except:
                        self.loggger.info('artno non-exist')
                        csv_article_number = ''

                    try:
                        desc = self.driver.find_element_by_class_name('description')
                        desc_html = desc.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip().lstrip()
                        csv_desc = desc_html
                    except:
                        self.loggger.info('desc non-exist')
                        csv_desc = ''

                    try:
                        rec_price = self.driver.find_element_by_class_name('column-value')
                        csv_rec_price = rec_price.text.replace(',', '.')
                    except:
                        self.loggger.info('rec price non-exist')
                        csv_rec_price = ' '
                    
                    time.sleep(1)
                    try:
                        price = self.driver.find_element_by_class_name('price')
                        csv_price = price.text.split('kr')[0].replace(',', '.').replace(' ', '')
                    except:
                        self.loggger.info('price non-exist')
                        csv_price = ''

                    try:
                        stock = self.driver.find_element_by_class_name('stock-status')
                        if stock.text.split(' ')[-1] == 'SLUT':
                            csv_stock = '0'
                        else:
                            csv_stock = stock.text.split(' ')[-1]
                    except:
                        self.loggger.info('stock non-exist')
                        csv_stock = '0'

                    try:
                        tabs = self.driver.find_element_by_class_name('tabs')
                        for tab_title in tabs.find_elements_by_class_name('tab-title'):
                            if tab_title.text == 'PRODUKTSPECIFIKATION':
                                tab_title.click()

                        time.sleep(1)
                        wrapper3 = self.driver.find_element_by_id('product-specification')
                        for child_wrapper3 in wrapper3.find_elements_by_xpath('.//p'):
                            if child_wrapper3.text.split('\n')[0] == 'EAN-kod':
                                csv_gtin = child_wrapper3.text.split('\n')[-1]
                            if child_wrapper3.text.split('\n')[0] == 'Nettovikt (g)':
                                csv_weight = child_wrapper3.text.split('\n')[-1]
                            if child_wrapper3.text.split('\n')[0] == 'Leverantörens artikelnummer':
                                csv_supplier = child_wrapper3.text.split('\n')[-1]
                            if child_wrapper3.text.split('\n')[0] == 'Längd (m)':
                                csv_length = child_wrapper3.text.split('\n')[-1]
                    except:
                        self.loggger.info('specification non-exist')
                        csv_gtin = ''
                        csv_weight = ''
                        csv_supplier = ''
                        csv_length = ''

                    try:
                        file.write('NEW' + ',' + csv_heading + ',' + csv_categories[1] + ',' + csv_categories[2] + ',' + csv_categories[3] + ',' + csv_categories[4] + ',' + csv_brand + ',' + csv_rec_price + ',' + csv_price + ',' + csv_article_number + ',' + csv_gtin + ',' + csv_weight + ',' + csv_supplier + ',' + csv_length + ',' + csv_stock + ',' + csv_desc + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + csv_image_url[15] + ',' + csv_image_url[16] + ',' + csv_image_url[17] + ',' + list3[m] + '\n')
                    except:
                        self.loggger.info('file write error!')
            except:
                self.loggger.info('error!')
       

        file.close()
        self.driver.close()
