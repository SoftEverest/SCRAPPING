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

class ProductSpider(scrapy.Spider):
    name = "download_image_work"
    start_urls = ['https://www.deltaco.se/Sidor/Login.aspx?ReturnUrl=%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252F&Source=%2F']
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=options)

    def parse(self, response):
        image_urls = []
        image_names = []
        
        try:
            shutil.rmtree('images')
        except:
            self.log('no folder!')
        
        os.mkdir('images')

        with open('deltaco.csv', 'r') as ins:
            for line in ins:
                if line.split(';')[0] == 'NEW':
                    for i in range(15, 25):
                        if len(line.split(';')[i]) > 10:
                            image_urls.append(line.split(';')[i])
                            image_names.append(line.split(';')[4].replace(' ', '_').replace('Å', 'A').replace('Ä', 'A').replace('Ö', 'O').replace('å', 'a').replace('ä', 'a').replace('ö', 'o').lower() + '_' + str(i-14))

        try:
            os.chdir('./images')
        except:
            self.log('error')

        for j in range(0, len(image_urls)):
            self.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            self.log(image_urls[j])
            try:
                urllib.request.urlretrieve(image_urls[j], image_names[j] + ".jpg")
            except:
                self.log('download error')
       
        self.driver.close()
