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
    name = "order_new"
    allowed_domains = ['www.order.se']
    start_urls = ['https://www.order.se']

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
        csv_price_recommended = ''
        csv_breadcrumbs = ''
        csv_desciption = ''
        csv_image_url = []
        csv_artno = ''
        csv_ean = ''
        csv_weight = ''
        old_product_url = []
        # csv_article_number = ''
        # file_exist = False
        
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login-popup")))
        self.driver.find_element_by_css_selector('.show-for-large a[href="#login-popup"].login').click()
        # self.driver.find_element_by_css_selector('.show-for-large a[href="#login-popup"].login').click() # get login button and click
        # login.click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="login"]/input[2]').send_keys('5568877384')  # get username field and type username
        self.driver.find_element_by_xpath('//*[@id="login"]/input[3]').send_keys('9hJdD')       # get password field and type password

        self.driver.find_element_by_xpath('//*[@id="login"]/button').click()
        time.sleep(3)
        entire_category = self.driver.find_element_by_class_name('all-products')
        entire_category.click()
        time.sleep(3)


        #Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open("order.csv") as old_file:
                for line in old_file:
                    new_file.write(line.replace('NEW', 'old'))
        #Remove original file
        remove("order.csv")
        #Move new file
        move(abs_path, "order.csv")

        with open('order.csv', 'r') as ins:
            for line in ins:
                old_product_url.append(line.split(',')[-1])


        file = open("order.csv", "a")
        # file.write('O/N' + ',' + 'Category1' + ',' + 'Category2' + ',' + 'Name' + ',' + 'Rec.Price' + ',' + 'Price' + ',' + 'Art.No' + ',' + 'EAN' + ',' + 'Gross Weight' + ',' + 'Stock' + ',' + 'Description_html' + ',' + 'image_1' + ',' + 'image_2' + ',' + 'image_3' + ',' + 'image_4' + ',' + 'image_5' + ',' + 'image_6' + ',' + 'image_7' + ',' + 'image_8' + ',' + 'image_9' + ',' + 'image_10' + ',' + 'PageUrl' + '\n')
        for wrapper1 in self.driver.find_elements_by_class_name('menu-level-0'):
            # if wrapper1.text != 'Genvägar':
            for child_wrapper1 in wrapper1.find_elements_by_xpath('./li'):
                child_wrapper2 = child_wrapper1.find_element_by_xpath('./a')
                list1.append(child_wrapper2.get_attribute('href'))
                self.log('*************************************************')
                self.log(child_wrapper2.get_attribute('href'))
                # file.write(child_wrapper2.get_attribute('href') + '\n')
        for i in range(3, len(list1)):	# here you can change category1 count for scrapping.	for all products, you have to write like this "range(0, len(list1))" instead of "range(0, 50)".
            try:
                self.driver.get(list1[i])
                time.sleep(3)
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'results')))
                result = self.driver.find_element_by_class_name('results')
                # file.write(result.text.split(' ')[0] + '\n')
                if int(result.text.split(' ')[0])%20 == 0:
                    page = str(int(result.text.split(' ')[0])//20)
                else:
                    page = str(int(result.text.split(' ')[0])//20 + 1)
                    
                self.driver.get(self.driver.current_url + '?page=' + page + '&restore_auto_pagination=true')
                time.sleep(int(page))

                listview = self.driver.find_element_by_class_name('listview')
                for product in listview.find_elements_by_class_name('product-list'):
                    product_image = product.find_element_by_class_name('image')
                    product_url = product_image.find_element_by_xpath('./a')
                    list2.append(product_url.get_attribute('href'))
            except:
                self.log('error')

        for j in range(0, len(list2)):
            if list2[j] not in old_product_url:
                try:
                    self.driver.get(list2[j])
                    self.log('********************' + str(j) + '********************')
                    time.sleep(3)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'product-title')))
                    
                    try:
                        product_name = self.driver.find_element_by_class_name('product-title')
                        csv_name = product_name.text.replace(',', ' ')
                    except:
                        self.loggger.info('product name non-exist')
                    
                    try:
                        breadcrumbs = self.driver.find_element_by_class_name('breadcrumbs')
                        csv_breadcrumbs = breadcrumbs.text
                    except:
                        self.loggger.info('breadcrumbs non-exist')
                        csv_breadcrumbs = ''
                    
                    csv_image_url = []
                    try:
                        images = self.driver.find_element_by_id('product-images-tabs')
                        pimages = images.find_elements_by_xpath('.//img')
                        for pimage in pimages:
                            image_url = pimage.get_attribute('src')
                            if image_url not in csv_image_url:
                                csv_image_url.append(image_url)
                    except:
                        big_image = self.driver.find_element_by_class_name('big-pic')
                        pimage = big_image.find_element_by_xpath('.//img')
                        image_url = pimage.get_attribute('src').replace('1280', '120')
                        csv_image_url.append(image_url)

                    try:
                        price_recommended = self.driver.find_element_by_class_name('price-recommended')
                        csv_price_recommended = price_recommended.text.replace(',', '.').split(' ')[1]
                    except:
                        self.loggger.info('rec_price non-exist')
                        csv_price_recommended = ''

                    try:
                        price = self.driver.find_element_by_class_name('price')
                        csv_price = price.text.replace(',', '.').split(' ')[0]
                    except:
                        self.loggger.info('price non-exist')
                        csv_price = ''
                    
                    try:
                        stock = self.driver.find_element_by_class_name('stock')
                        if 'st' in stock.text:
                            csv_stock = stock.text.split(' ')[-2]
                        else:
                            csv_stock = '0'
                    except:
                        self.loggger.info('stock non-exist')
                        csv_stock = ''

                    try:
                        extra_info = self.driver.find_element_by_class_name('description-info')
                        csv_desciption = extra_info.text
                    except:
                        csv_desciption = ''

                    try:
                        paragraph = self.driver.find_element_by_class_name('tabs-content-description')
                        para_html = paragraph.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip().replace('≤', ' ')
                        csv_paragraph = (''.join(para_html)).encode('utf-8').decode('utf-8')
                    except:
                        self.loggger.info('paragraph non-exist')
                        csv_paragraph = ''
                    
                    try:
                        for desc in csv_desciption.split('\n'):
                            if 'Art. nr' in desc:
                                csv_artno = desc.split(': ')[1]
                            if 'EAN-kod' in desc:
                                csv_ean = desc.split(': ')[1]
                            if 'Bruttovikt' in desc:
                                csv_weight = desc.split(': ')[1]
                    except:
                        self.loggger.info('desc non-exist')
                        csv_artno = ''
                        csv_ean = ''
                        csv_weight = ''
                    
                    if '&' in csv_breadcrumbs:
                        if len(csv_image_url) == 1:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ' ' + csv_breadcrumbs.split(' ')[1] + ' ' + csv_breadcrumbs.split(' ')[2] + ',' + csv_breadcrumbs.split(' ')[3] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 2:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ' ' + csv_breadcrumbs.split(' ')[1] + ' ' + csv_breadcrumbs.split(' ')[2] + ',' + csv_breadcrumbs.split(' ')[3] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 3:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ' ' + csv_breadcrumbs.split(' ')[1] + ' ' + csv_breadcrumbs.split(' ')[2] + ',' + csv_breadcrumbs.split(' ')[3] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 4:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ' ' + csv_breadcrumbs.split(' ')[1] + ' ' + csv_breadcrumbs.split(' ')[2] + ',' + csv_breadcrumbs.split(' ')[3] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 5:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ' ' + csv_breadcrumbs.split(' ')[1] + ' ' + csv_breadcrumbs.split(' ')[2] + ',' + csv_breadcrumbs.split(' ')[3] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 6:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ' ' + csv_breadcrumbs.split(' ')[1] + ' ' + csv_breadcrumbs.split(' ')[2] + ',' + csv_breadcrumbs.split(' ')[3] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + list2[j] + '\n')
                    else:
                        if len(csv_image_url) == 1:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ',' + csv_breadcrumbs.split(' ')[1] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 2:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ',' + csv_breadcrumbs.split(' ')[1] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 3:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ',' + csv_breadcrumbs.split(' ')[1] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 4:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ',' + csv_breadcrumbs.split(' ')[1] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + ' ' + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 5:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ',' + csv_breadcrumbs.split(' ')[1] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + ' ' + ',' + list2[j] + '\n')
                        if len(csv_image_url) == 6:
                            file.write('NEW' + ',' + csv_breadcrumbs.split(' ')[0] + ',' + csv_breadcrumbs.split(' ')[1] + ',' +  csv_name + ',' + csv_price_recommended + ',' + csv_price + ',' + csv_artno + ',' + csv_ean + ',' + csv_weight + ',' + csv_stock + ',' + csv_paragraph + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + list2[j] + '\n')
                except:
                    self.loggger.info('This is error')

        file.close()
        self.driver.close()
