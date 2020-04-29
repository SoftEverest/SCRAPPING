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

class ProductSpider(scrapy.Spider):
    name = "deltaco_all"
    allowed_domains = ['www.deltaco.se']
    start_urls = ['https://www.deltaco.se/Sidor/Login.aspx?ReturnUrl=%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252F&Source=%2F']

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)

    def parse(self, response):
        self.driver.get(response.url)
        
        product_list = []
        menu_list = []

        csv_heading = ''
        csv_stock = ''
        csv_price = ''
        csv_desc = ''
        csv_brand = ''
        csv_gtin = ''
        csv_specification = ''
        csv_b = ''
        csv_weight = ''
        csv_article_number = ''
        csv_partno = ''
        csv_image_url = []
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,'xloginid')))
        username = self.driver.find_element_by_id('xloginid')
        username.send_keys("12141")
        username = self.driver.find_element_by_id('xloginpassword')
        username.send_keys("58cnk3im")
        login = self.driver.find_element_by_class_name('msax-CommandLogin')
        time.sleep(1)
        login.click()
        time.sleep(5)

        file = open("deltaco.csv", "w")
        file.write('O/N' + ',' + 'Category1' + ',' + 'Category2' + ',' + 'Category3' + ',' + 'Name' + ',' + 'Article Number' + ',' + 'Brand' + ',' + 'ManufacturerPartNo' + ',' + 'EAN' + ',' + 'Weight' + ',' + 'Stock' + ',' + 'B' + ',' + 'Price' + ',' + 'Description_html' + ',' + 'Specification_html' + ',' + 'image_1' + ',' + 'image_2' + ',' + 'image_3' + ',' + 'image_4' + ',' + 'image_5' + ',' + 'image_6' + ',' + 'image_7' + ',' + 'image_8' + ',' + 'image_9' + ',' + 'image_10' + ',' + 'PageUrl' + '\n')
        
        self.driver.get('https://www.deltaco.se/produkter/')

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,'zz12_RootAspMenu')))
        root_menu = self.driver.find_element_by_id('zz12_RootAspMenu')

        for wrapper1 in root_menu.find_elements_by_xpath('./li[1]/ul/li'):
            product1 = wrapper1.find_element_by_xpath('./a')
            menu_list.append(product1.get_attribute('href'))
        
        for wrapper2 in root_menu.find_elements_by_xpath('./li[2]/ul/li'):
            product2 = wrapper2.find_element_by_xpath('./a')
            menu_list.append(product2.get_attribute('href'))

        # for m in range(0, 1):    IF YOU WANT TO DOWNLOAD ABOUT 20 PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(menu_list)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for i in range(0, len(menu_list)):
            page = 1
            while True:
                try:
                    self.driver.get(menu_list[i] + '#k=#s=' + str(page))
                    self.driver.refresh()
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'msax-productGaleryItem')))
                    for product in self.driver.find_elements_by_class_name('msax-productGaleryItem'):
                        product_desc = product.find_element_by_class_name('msax-itemGalleryDescription')
                        product_url = product_desc.find_element_by_xpath('.//a')
                        if product_url.get_attribute('href') not in product_list:
                            product_list.append(product_url.get_attribute('href'))
                    # break    IF YOU WANT TO DOWNLOAD ABOUT 20 PRODUCTS, YOU CAN WRITE LIKE THIS.
                    #           IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
                    page = page + 21
                except:
                    break
        # for m in range(0, 20):    IF YOU WANT TO DOWNLOAD CERTAIN PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(product_list)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for j in range(0, len(product_list)):
            try:
                self.log('***************j  ' + str(len(product_list)) + '    ' + str(j) + '  j***************')
                self.driver.get(product_list[j])
                time.sleep(5)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'msax-thumbnailWrapper')))
                csv_image_url = []
                for image in self.driver.find_elements_by_class_name('msax-thumbnailWrapper'):
                    try:
                        image_url = image.find_element_by_xpath('.//img')
                        csv_image_url.append(image_url.get_attribute('src').split('?')[0])
                    except:
                        csv_image_url.append("")

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
                if len(csv_image_url) == 2:
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                if len(csv_image_url) == 3:
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                if len(csv_image_url) == 4:
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                if len(csv_image_url) == 5:
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                if len(csv_image_url) == 6:
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                if len(csv_image_url) == 7:
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                if len(csv_image_url) == 8:
                    csv_image_url.append(' ')
                    csv_image_url.append(' ')
                if len(csv_image_url) == 9:
                    csv_image_url.append(' ')

                try:
                    article_number = self.driver.find_element_by_class_name('msax-title')
                    csv_article_number = article_number.text
                except:
                    self.log('empty')

                try:
                    brand = self.driver.find_element_by_class_name('msax-Brand')
                    csv_brand = brand.text.split(': ')[1]
                except:
                    self.log('empty')

                try:
                    partno = self.driver.find_element_by_class_name('msax-ManufacturerPartNumber')
                    csv_partno = partno.text.split(': ')[1]
                except:
                    self.log('empty')

                try:
                    gtin = self.driver.find_element_by_class_name('msax-itemPerPackage')
                    csv_gtin = gtin.text.split(': ')[1]
                except:
                    self.log('empty')

                try:
                    weight = self.driver.find_element_by_class_name('msax-itemDetailsWeight')
                    csv_weight = weight.text.split(':')[1]
                except:
                    self.log('empty')

                price = self.driver.find_element_by_class_name('msax-adjustedPrice')
                csv_price = price.text.splitlines()[0].split(' SEK')[0].replace(',', '.')
                if 'B' in price.text:
                    csv_b = 'B'
                csv_stock = price.text.splitlines()[1].split(' I')[0].replace(',', ' ')
                
                desc = self.driver.find_element_by_class_name('msax-longDescription')
                csv_heading = desc.text.splitlines()[0].replace(',', '.')
                csv_desc = desc.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip().lstrip()

                try:
                    specification = self.driver.find_element_by_class_name('msax-Specifications')
                    csv_specification = specification.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip().lstrip()
                except:
                    self.log('error')

                file.write('NEW' + ',' + product_list[j].split('//')[1].split('/')[1] + ',' + product_list[j].split('//')[1].split('/')[2].replace('%C3%B6', 'ö').replace('%EF%BC%82', '"').replace('%C3%A5', 'å').replace('%C3%A4', 'ä') + ',' + product_list[j].split('//')[1].split('/')[3].replace('%C3%B6', 'ö').replace('%EF%BC%82', '"').replace('%C3%A5', 'å').replace('%C3%A4', 'ä') + ',' + csv_heading + ',' + csv_article_number + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_weight + ',' + csv_stock + ',' + csv_b + ',' + csv_price + ',' + csv_desc + ',' + csv_specification + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + product_list[j].replace('%C3%B6', 'ö').replace('%EF%BC%82', '"').replace('%C3%A5', 'å').replace('%C3%A4', 'ä') + '\n')
            except:
                self.logger.info('error')

        file.close()
        self.driver.close()
