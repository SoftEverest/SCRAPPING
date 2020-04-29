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
    name = "brightstar_new"
    allowed_domains = ['webshop.brightstar-2020.se']
    start_urls = ['https://webshop.brightstar-2020.se/']

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
        csv_price = ''
        # csv_price_recommended = ''
        csv_desciption = ''
        csv_category1 = ''
        csv_category2 = ''
        csv_family = ''
        old_product_url = []
        csv_manufacturer = ''
        csv_image_url = []
        csv_artno = ''
        csv_ean = ''
        # csv_weight = ''
        # csv_summary = ''
        # csv_code = ''

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'username')))
        
        username = self.driver.find_element_by_id('username')
        username.send_keys("rashid@themobilestore.se")
        username = self.driver.find_element_by_id('password')
        username.send_keys("rshabnam7878")
        login = self.driver.find_element_by_id('btn-login')
        time.sleep(1)
        login.click()
        time.sleep(5)

        #Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open("brightstar.csv") as old_file:
                for line in old_file:
                    new_file.write(line.replace('NEW', 'old'))
        #Remove original file
        remove("brightstar.csv")
        #Move new file
        move(abs_path, "brightstar.csv")

        with open('brightstar.csv', 'r') as ins:
            for line in ins:
                old_product_url.append(line.split(',')[-1])

        file = open("brightstar.csv", "a")
        # file.write('O/N' + ',' + 'Category1' + ',' + 'Category2' + ',' + 'Name' + ',' + 'Family' + ',' + 'Manufacturer' + ',' + 'Article No' + ',' + 'EAN' + ',' + 'Price' + ',' + 'Stock' + ',' + 'Description_html' + ',' + 'image_1' + ',' + 'image_2' + ',' + 'image_3' + ',' + 'image_4' + ',' + 'image_5' + ',' + 'image_6' + ',' + 'image_7' + ',' + 'image_8' + ',' + 'image_9' + ',' + 'image_10' + ',' + 'PageUrl' + '\n')

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'catalog')))
        catalog = self.driver.find_element_by_id('catalog')
        for category1 in catalog.find_elements_by_class_name('sub-menu'):
            for category2 in category1.find_elements_by_xpath('.//a'):
                list1.append(category2.get_attribute('href'))
                # file.write(category2.get_attribute('href') + '\n')
        

        for i in range(0, len(list1)):
            self.loggger.info(str(len(list1)) + '**********' + str(i) + '***********')
            self.loggger.info('**********' + list1[i] + '***********')
            self.driver.get(list1[i])
            time.sleep(5)

            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,'item-details')))
            for item in self.driver.find_elements_by_class_name('item-details'):
                item_url = item.find_element_by_xpath('.//a')
                list2.append(item_url.get_attribute('href'))
                # file.write(item_url.get_attribute('href') + '\n')

        for j in range(0, len(list2)):
            # try:
            self.loggger.info(str(len(list2)) + '**********' + str(j) + '***********')
            self.loggger.info('**********' + str(list2[j]) + '***********')
            if list2[j] not in old_product_url:
                try:
                    self.driver.get(list2[j])
                    time.sleep(5)
                except:
                    self.driver.refresh()
                    time.sleep(5)

                try:
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'breadcrumbs')))
                except:
                    self.driver.refresh()
                    time.sleep(5)
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'username')))
            
                    username = self.driver.find_element_by_id('username')
                    username.send_keys("rashid@themobilestore.se")
                    username = self.driver.find_element_by_id('password')
                    username.send_keys("rshabnam7878")
                    login = self.driver.find_element_by_id('btn-login')
                    time.sleep(1)
                    login.click()
                    time.sleep(5)
                    continue
                
                try:
                    breadcrumbs = self.driver.find_element_by_id('breadcrumbs')
                    csv_category1 = breadcrumbs.text.split(' » ')[1]
                    csv_category2 = breadcrumbs.text.split(' » ')[2]
                except:
                    self.loggger.info('category non-exist')
                    csv_category1 = ''
                    csv_category2 = ''
                
                try:
                    product_detail = self.driver.find_element_by_id('product-details')
                    name = product_detail.find_element_by_tag_name('h1')
                    csv_name = name.text
                except:
                    self.loggger.info('name non-exist')
                    csv_name = ''

                try:
                    paragraph = product_detail.find_element_by_xpath('./p')
                    csv_family = paragraph.text.split(' | ')[0].split(': ')[-1].replace(',', '-')
                    csv_manufacturer = paragraph.text.split(' | ')[1].split(': ')[-1]
                except:
                    self.loggger.info('family and manufacturer non-exist')
                    csv_family = ''
                    csv_manufacturer = ''

                try:
                    product_info = self.driver.find_element_by_id('prod-info-cnt')
                    for info in product_info.find_elements_by_xpath('.//tr'):
                        if 'Art' in info.text:
                            csv_artno = info.text.split(' ')[-1]
                        if 'EAN' in info.text:
                            csv_ean = info.text.split(' ')[-1]
                except:
                    self.loggger.info('artno non-exist')
                    self.loggger.info('ean non-exist')
                    csv_artno = ''
                    csv_ean = ''
            
                try:
                    stock = product_info.find_element_by_class_name('prod-stock')
                    csv_stock = stock.text.split('\n')[-1].split(': ')[-1]
                except:
                    self.loggger.info('stock non-exist')
                    csv_stock = ''

                try:
                    price = self.driver.find_element_by_class_name('prod-current-price')
                    csv_price = price.text.replace('.', '').replace(',', '.')
                except:
                    self.loggger.info('price non-exist')
                    csv_price = ''

                csv_image_url = []
                try:
                    thumbnails = self.driver.find_element_by_class_name('thumbnails')
                    for img in thumbnails.find_elements_by_xpath('.//img'):
                        csv_image_url.append(img.get_attribute('src'))
                except:
                    self.loggger.info('image non-exist')
                    csv_image_url = []
                
                try:
                    desc = self.driver.find_element_by_id('product-information')
                    desc_temp = desc.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').replace('\t', '').strip()
                    csv_desciption = ' '.join(desc_temp.split())
                except:
                    self.loggger.info('description non-exist')
                    csv_desciption = ' '
                
                try:
                    if len(csv_image_url) == 1:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 2:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 3:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 4:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 5:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 6:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 7:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + ' ' + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 8:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + ' ' + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 9:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + ' ' + list2[j] + '\n')
                    if len(csv_image_url) == 10:
                        file.write('NEW' + ',' + csv_category1 + ',' + csv_category2 + ',' + csv_name + ',' + csv_family + ',' + csv_manufacturer + ',' + csv_artno + ',' + csv_ean + ',' + csv_price + ',' + csv_stock + ',' + csv_desciption + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + list2[j] + '\n')
                except:
                    self.loggger.info('file write error!')
            # except:
            #     self.log('error')
            
          
        file.close()
        self.driver.close()
