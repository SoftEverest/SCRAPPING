import scrapy
import time
import os.path
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
    name = "tekniknet_new"
    allowed_domains = ['www.tekniknet.se']
    start_urls = ['https://www.tekniknet.se/#']

    def __init__(self):
        # self.driver = webdriver.Chrome("./chromedriver.exe")
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
        list4 = []
        list5 = []
        list3_categories = []
        list4_categories = []
        csv_categories1 = ''
        csv_heading = ''
        csv_stock = ''
        csv_price_new = ''
        csv_price_old = ''
        csv_desc = ''
        csv_article_number = ''
        # article_number_list = []
        csv_image_url = []
        # file_exist = False
        old_product_url = []
        
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID,'email')))
        username = self.driver.find_element_by_id('email')
        username.send_keys("info@themobilestore.se")
        username = self.driver.find_element_by_id('password')
        username.send_keys("order88")
        login = self.driver.find_element_by_class_name('button-confirm')
        login.click()
        time.sleep(5)

        #Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open("tekniknet.csv") as old_file:
                for line in old_file:
                    new_file.write(line.replace('NEW', 'old'))
        #Remove original file
        remove("tekniknet.csv")
        #Move new file
        move(abs_path, "tekniknet.csv")

        with open('tekniknet.csv', 'r') as ins:
            for line in ins:
                old_product_url.append(line.split(',')[-1])

        file = open("tekniknet.csv", "a", errors ='replace')
        # file.write('OLD/NEW' + ',' + 'article number' + ',' + 'category1' + ',' + 'category2' + ',' + 'category3' + ',' + 'heading' + ',' + 'description' + ',' + 'current price' + ',' + 'previous price' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'image link' + ',' + 'EAN code' + ',' + 'stock' + ',' + 'product url' + '\n')
        for wrapper1 in self.driver.find_elements_by_class_name('level-0'):
            child_wrapper1 = wrapper1.find_element_by_xpath('./a')
            link1 = child_wrapper1.get_attribute('href')
            list1.append(link1)
            self.loggger.info('*************************************************')
            self.loggger.info(link1)

        for i in range(0, len(list1)-4):
            self.driver.get(list1[i])
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'inner')))
                for wrapper2 in self.driver.find_elements_by_class_name('inner'):
                    try:
                        sub2 = wrapper2.find_element_by_class_name('subLinks')
                        child_wrapper2 = sub2.find_elements_by_xpath('.//a')
                        for child2 in child_wrapper2:
                            link2 = child2.get_attribute('href')
                            list2.append(link2)
                            self.loggger.info('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                            self.loggger.info(link2)
                    
                    except Exception as e:
                        self.loggger.info(e)
                        self.loggger.info('error')
            except:
                try:
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID,'categorySubCategories')))
                    subcategory = self.driver.find_element_by_id('categorySubCategories')
                    wrapper2_1 = subcategory.find_elements_by_xpath('.//a')
                    for child3 in wrapper2_1:
                        link2_1 = child3.get_attribute('href')
                        list5.append(link2_1)
                    for n in range(0, len(list5)):
                        self.driver.get(list5[n])
                        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID,'categorySubCategories')))
                        subcategory = self.driver.find_element_by_id('categorySubCategories')
                        wrapper2_1_1 = subcategory.find_elements_by_xpath('.//a')
                        for child3_1 in wrapper2_1_1:
                            if child3_1.text != 'Visa alla':
                                link2_1_1 = child3_1.get_attribute('href')
                                list2.append(link2_1_1)
                except:
                    try:
                        breadcrumbs2 = self.driver.find_element_by_id('breadcrumbs')
                        categories2 = breadcrumbs2.find_elements_by_xpath('.//li')
                        csv_categories2 = ''
                        for category2 in categories2:
                            csv_categories2 = csv_categories2 + category2.text + '/'
                    
                        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'listProduct')))
                        for wrapper2_2 in self.driver.find_elements_by_class_name('listProduct'):
                            wrapper2_3 = wrapper2_2.find_element_by_xpath(".//a")
                            link2_2 = wrapper2_3.get_attribute('href')
                            list4.append(link2_2)
                            list4_categories.append(csv_categories2)
                            self.loggger.info('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                            self.loggger.info(link2_2)
                            self.loggger.info('error')
                    except Exception as e:
                        self.loggger.info(e)
                        self.loggger.info('error')

        # for m in range(0, 5):    IF YOU WANT TO DOWNLOAD CERTAIN PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(list2)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for j in range(0, len(list2)):
            try:
                self.loggger.info('**********--------------      ' + str(j) + '      ******************************')
                self.driver.get(list2[j])
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'breadcrumbs')))

                breadcrumbs1 = self.driver.find_element_by_id('breadcrumbs')
                categories1 = breadcrumbs1.find_elements_by_xpath('.//li')
                csv_categories1 = ''
                for category1 in categories1:
                    csv_categories1 = csv_categories1 + category1.text + '/'

                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'listProduct')))
                for wrapper3 in self.driver.find_elements_by_class_name('listProduct'):
                    child_wrapper3 = wrapper3.find_element_by_xpath(".//a")
                    link3 = child_wrapper3.get_attribute('href')
                    list3.append(link3)
                    list3_categories.append(csv_categories1)
                    self.loggger.info('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                    self.loggger.info(link3)
            except Exception as e:
                self.loggger.info(e)
                self.loggger.info('error')
        
        for k in range(0, len(list3)):
            try:
                if list3[k] not in old_product_url:
                    self.loggger.info('-----------------------      ' + str(k) + '      ******************************')
                    self.driver.get(list3[k])
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'breadcrumbs')))

                    # breadcrumbs = self.driver.find_element_by_id('breadcrumbs')
                    # categories = breadcrumbs.find_elements_by_xpath('.//a')
                    # for category in categories:
                    #     csv_categories.append(category.text)

                    offer = self.driver.find_element_by_id('productPageUpper')
                    try:
                        heading = offer.find_element_by_class_name('pHeader')
                        csv_heading = heading.text.replace(',', '.')
                    except:
                        self.loggger.info('heading3 non-exist')
                        csv_heading = ''

                    try:
                        stock = offer.find_element_by_class_name('instock')
                        csv_stock = stock.text
                    except:
                        csv_stock = 'Out of stock'
                        self.loggger.info('stock3 non-exist')
                        csv_stock = ''

                    try:
                        price_new = offer.find_element_by_class_name('priceRegular')
                        csv_price_new = price_new.text.split(' ')[0]
                    except:
                        try:
                            price_new = offer.find_element_by_class_name('priceNew')
                            csv_price_new = price_new.text.split(' ')[0]
                            
                            price_old = offer.find_element_by_class_name('priceOld')
                            csv_price_old = price_old.text.split(' ')[0]
                        except:
                            self.loggger.info('price3 non-exist')
                            csv_price_old = ''
                            csv_price_new = ''

                    try:
                        desc = offer.find_element_by_id('pDesc')
                        csv_desc = desc.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip().lstrip()
                    except:
                        self.loggger.info('description3 non-exist')
                        csv_desc = ''

                    try:
                        article_number = offer.find_element_by_id('pManufacturer')
                        csv_article_number = article_number.text.split(' ')[-1].replace(',', '.')
                    except:
                        self.loggger.info('article number3 non-exist')
                        csv_article_number = ''
                    
                    try:
                        pimages = offer.find_elements_by_xpath('.//img')
                        csv_image_url = []
                        for pimage in pimages:
                            image_url = pimage.get_attribute('src')
                            if image_url not in csv_image_url:
                                csv_image_url.append(image_url)
                    except:
                        self.loggger.info('image3 non-exist')

                    #########################################       CSV File Writing        #########################################
                    # if csv_article_number not in article_number_list:
                    if len(csv_image_url) == 1:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 2:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 3:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 4:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 5:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 6:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 7:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 8:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 9:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 10:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 11:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 12:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 13:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 14:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 15:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 16:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + csv_image_url[15] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) == 17:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + csv_image_url[15] + ',' + csv_image_url[16] + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    elif len(csv_image_url) >= 18:
                        file.write('NEW' + ',' + csv_article_number + ',' + list3_categories[k].split('/')[1] + ',' + list3_categories[k].split('/')[2] + ',' + list3_categories[k].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + csv_image_url[15] + ',' + csv_image_url[16] + ',' + csv_image_url[17] + ',' + ' ' + ',' + csv_stock + ',' + list3[k] + '\n')
                    # article_number_list.append(csv_article_number)
            except Exception as e:
                self.loggger.info(e)
                self.loggger.info('error3')

        # for m in range(0, 20):    IF YOU WANT TO DOWNLOAD CERTAIN PRODUCTS, YOU CAN WRITE LIKE THIS.
        # for m in range(0, len(list4)):    IF YOU WANT TO DOWNLOAD ALL PRODUCTS, YOU CAN WRITE LIKE THIS.
        for m in range(0, len(list4)):
            try:
                if list4[m] not in old_product_url:
                    self.loggger.info('**********************      ' + str(k) + '      ******************************')
                    self.driver.get(list4[m])
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,'breadcrumbs')))

                    # breadcrumbs = self.driver.find_element_by_id('breadcrumbs')
                    # categories = breadcrumbs.find_elements_by_xpath('.//a')
                    # for category in categories:
                    #     csv_categories.append(category.text)

                    offer = self.driver.find_element_by_id('productPageUpper')
                    try:
                        heading = offer.find_element_by_class_name('pHeader')
                        csv_heading = heading.text.replace(',', '.')
                    except:
                        self.loggger.info('heading4 non-exist')
                        csv_heading = ''

                    try:
                        stock = offer.find_element_by_class_name('instock')
                        csv_stock = stock.text
                    except:
                        csv_stock = 'Out of stock'
                        self.loggger.info('stock4 non-exist')

                    try:
                        price_new = offer.find_element_by_class_name('priceRegular')
                        csv_price_new = price_new.text.split(' ')[0]
                    except:
                        try:
                            price_new = offer.find_element_by_class_name('priceNew')
                            csv_price_new = price_new.text.split(' ')[0]
                            
                            price_old = offer.find_element_by_class_name('priceOld')
                            csv_price_old = price_old.text.split(' ')[0]
                        except:
                            self.loggger.info('price4 non-exist')
                            csv_price_new = ''
                            csv_price_old = ''

                    try:
                        desc = offer.find_element_by_id('pDesc')
                        csv_desc = desc.get_attribute('innerHTML').replace(',', '-').replace('\n', ' ').replace('\r', '').rstrip().lstrip()
                    except:
                        self.loggger.info('description4 non-exist')
                        csv_desc = ''

                    try:
                        article_number = offer.find_element_by_id('pManufacturer')
                        csv_article_number = article_number.text.split(' ')[-1].replace(',', '.')
                    except:
                        self.loggger.info('article number4 non-exist')
                        csv_article_number = ''
                    
                    try:
                        pimages = offer.find_elements_by_xpath('.//img')
                        csv_image_url = []
                        for pimage in pimages:
                            image_url = pimage.get_attribute('src')
                            if image_url not in csv_image_url:
                                csv_image_url.append(image_url)
                    except:
                        self.loggger.info('image4 non-exist')

                    #########################################       CSV File Writing        #########################################
                    # if csv_article_number not in article_number_list:
                    if len(csv_image_url) == 1:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 2:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 3:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 4:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 5:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 6:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 7:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 8:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 9:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 10:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 11:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 12:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 13:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 14:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 15:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 16:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + csv_image_url[15] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) == 17:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + csv_image_url[15] + ',' + csv_image_url[16] + ',' + ' ' + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                    elif len(csv_image_url) >= 18:
                        file.write('NEW' + ',' + csv_article_number + ',' + list4_categories[m].split('/')[1] + ',' + list4_categories[m].split('/')[2] + ',' + list4_categories[m].split('/')[3] + ',' + csv_heading + ',' + csv_desc + ',' + csv_price_new + ',' + csv_price_old + ',' + csv_image_url[0] + ',' + csv_image_url[1] + ',' + csv_image_url[2] + ',' + csv_image_url[3] + ',' + csv_image_url[4] + ',' + csv_image_url[5] + ',' + csv_image_url[6] + ',' + csv_image_url[7] + ',' + csv_image_url[8] + ',' + csv_image_url[9] + ',' + csv_image_url[10] + ',' + csv_image_url[11] + ',' + csv_image_url[12] + ',' + csv_image_url[13] + ',' + csv_image_url[14] + ',' + csv_image_url[15] + ',' + csv_image_url[16] + ',' + csv_image_url[17] + ',' + ' ' + ',' + csv_stock + ',' + list4[m] + '\n')
                        # article_number_list.append(csv_article_number)
            except Exception as e:
                self.loggger.info(e)
                self.loggger.info('error4')
                
        file.close()
        self.driver.close()
