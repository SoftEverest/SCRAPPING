import scrapy
import time
import os
import shutil
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import logging

output_timestamp = datetime.today().strftime('%Y-%m-%d-%H%M')
log_output_file = 'scrape-order-images-{}.log'.format(output_timestamp)

class ProductSpider(scrapy.Spider):
    name = "download_image_new"
    start_urls = ['https://shop.turascandinavia.com/sv/inloggningssida']
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
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

        image_urls = []
        image_names = []
        
        try:
            shutil.rmtree('images')
        except Exception as e:
            self.loggger.info(e)
            self.loggger.info('no folder!')
        
        os.mkdir('images')

        with open('tura.csv', 'r') as ins:
            for line in ins:
                if line.split(',')[0] == 'NEW':
                    for i in range(16, 34):
                        if len(line.split(',')[i]) > 10:
                            image_urls.append(line.split(',')[i])
                            image_names.append(line.split(',')[1].replace(' ', '_').replace('Å', 'A').replace('Ä', 'A').replace('Ö', 'O').replace('å', 'a').replace('ä', 'a').replace('ö', 'o').lower() + '_' + str(i-15))

        try:
            os.chdir('./images')
        except Exception as e:
            self.loggger.info(e)
            self.loggger.info('error')

        for j in range(0, len(image_urls)):
            self.loggger.info('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            self.loggger.info(image_urls[j])
            try:
                urllib.request.urlretrieve(image_urls[j], image_names[j] + ".jpg")
            except Exception as e:
                self.loggger.info(e)
                self.loggger.info('download error')
       
        self.driver.close()
