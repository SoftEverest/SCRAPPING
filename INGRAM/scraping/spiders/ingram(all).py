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
    name = "ingram_all"
    allowed_domains = ['www.ingrammicroebusiness.com']
    start_urls = ['https://login.ingrammicroebusiness.com/']

    def __init__(self):
        # self.driver = webdriver.Chrome("./chromedriver.exe")
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)

    def parse(self, response):
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
        csv_partno = ''
        csv_image_url = []
        
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID,'username')))
        username = self.driver.find_element_by_id('username')
        username.send_keys("raatish")
        username = self.driver.find_element_by_id('password')
        username.send_keys("Danira7878????")
        login = self.driver.find_element_by_class_name('btn-primary')
        time.sleep(3)
        login.click()
        time.sleep(5)


        file = open("ingram.csv", "w")
        file.write('O/N' + ',' + 'Category1' + ',' + 'Category2' + ',' + 'Name' + ',' + 'Price' + ',' + 'Sku' + ',' + 'Brand' + ',' + 'ManufacturerPartNo' + ',' + 'GTIN' + ',' + 'QtyAvailable' + ',' + 'Description_html' + ',' + 'image_1' + ',' + 'image_2' + ',' + 'image_3' + ',' + 'image_4' + ',' + 'image_5' + ',' + 'image_6' + ',' + 'image_7' + ',' + 'image_8' + ',' + 'image_9' + ',' + 'image_10' + ',' + 'PageUrl' + '\n')
        for wrapper1 in self.driver.find_elements_by_class_name('topLvl'):
            if wrapper1.text != 'Genvägar':
                for child_wrapper1 in wrapper1.find_elements_by_xpath('.//li'):
                    child_wrapper2 = child_wrapper1.find_element_by_xpath('./a')
                    list1.append(child_wrapper2.get_attribute('href'))
                    self.log('*************************************************')
                    self.log(child_wrapper2.get_attribute('href'))
        for i in range(0, len(list1)):	# here you can change category1 count for scrapping.	for all products, you have to write like this "range(0, len(list1))" instead of "range(0, 50)".
            self.driver.get(list1[i])
            # self.driver.refresh()
            time.sleep(10)
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'pagination')))
                pagenation = self.driver.find_element_by_class_name('pagination') 
                page = pagenation.find_elements_by_class_name('ng-binding')
                if page[-1].text.isdigit() == True:
                    for j in range(1, int(page[-1].text) + 1):
                        list2.append(list1[i] + '?page=' + str(j))
                else:
                    list2.append(list1[i] + '?page=' + '1')
            except:
                self.log('one page')

        # for m in range(0, 5):    IF YOU WANT TO DOWNLOAD CERTAIN PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(list2)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for k in range(0, len(list2)):	# here you can change category2 count for scrapping.	for all products, you have to write like this "range(0, len(list2))" instead of "range(0, 50)".
            self.log('***********************' + str(k) + '***********************')
            try:
                self.driver.get(list2[k])
                time.sleep(3)
                self.driver.refresh()
                time.sleep(10)
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'product-list')))
                    product_list = self.driver.find_element_by_class_name('product-list')
                    for products in product_list.find_elements_by_class_name('product'):
                        product = products.find_element_by_xpath('.//a')
                        list3.append(product.get_attribute('href'))
                except:
                    self.log('non exist')
            except:
                self.log('site error')
        
        # for m in range(0, 20):    IF YOU WANT TO DOWNLOAD CERTAIN PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(list3)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for m in range(0, len(list3)):	# here you can change products count for scrapping.	for all products, you have to write like this "range(0, len(list3))" instead of "range(0, 50)".
            self.log('***********************' + str(m) + '***********************')
            try:
                self.driver.get(list3[m])
                time.sleep(10)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'breadcrumbs-module')))
                breadcrumbs = self.driver.find_element_by_class_name('breadcrumbs-module')
                categories = breadcrumbs.find_elements_by_xpath('.//li')
                for category in categories:
                    csv_categories.append(category.text)

                offer = self.driver.find_element_by_class_name('product-detail')
                try:
                    pimages = offer.find_elements_by_xpath('.//img')
                    csv_image_url = []
                    for pimage in pimages:
                        image_url = pimage.get_attribute('src')[:113]
                        if image_url not in csv_image_url:
                            csv_image_url.append(image_url)
                except:
                    self.log('image non-exist')

                try:
                    heading = offer.find_element_by_class_name('product-detail-title')
                    csv_heading = heading.text.replace(',', '.')
                except:
                    self.log('heading non-exist')
                
                try:
                    desc = offer.find_element_by_class_name('product-text')
                    desc_html = desc.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip()
                    csv_desc = (''.join(desc_html)).encode('utf-8').decode('utf-8')
                except:
                    self.log('description non-exist')

                try:
                    price = offer.find_element_by_class_name('product-price')
                    csv_price = price.text.split(' ')[0].replace('.', ' ').replace(',', '.')
                except:
                    self.log('price non-exist')
                
                side = self.driver.find_element_by_class_name('product-detail-sidebar')
                side_title = side.find_elements_by_xpath('.//li')
                try:
                    csv_sku = side_title[1].text
                    csv_brand = side_title[3].text
                    csv_gtin = side_title[7].text
                    csv_partno = side_title[11].text
                except:
                    self.log('error1')
                
                try:
                    stock = side.find_element_by_class_name('stock-module')
                    csv_stock = stock.text
                except:
                    self.log('error2')
                try:
                    if "b'" not in str(csv_desc):
                        if len(csv_image_url) == 1:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 2:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 3:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 4:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 5:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 6:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 7:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 8:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + ' ' + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 9:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + ' ' + ',' + list3[m] + '\n')
                        if len(csv_image_url) == 10:
                            file.write('NEW' + ',' + csv_categories[2] + ',' + csv_categories[0] + ',' + csv_heading + ',' + csv_price + ',' + csv_sku + ',' + csv_brand + ',' + csv_partno + ',' + csv_gtin + ',' + csv_stock + ',' + str(csv_desc) + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + list3[m] + '\n')
                except:
                    self.log('error3')
            except:
                self.log('error4')

        file.close()
        self.driver.close()
