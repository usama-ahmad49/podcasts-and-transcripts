import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")

cwd = os.getcwd()

class lavien(scrapy.Spider):
    name = 'lavien'

    def start_requests(self):
        yield scrapy.Request(url='https://www.lavieencode.net/podcast/')

    def parse(self, response, **kwargs):
        all_data = []
        for link in response.css('h3.elementor-post__title a'):
            item =dict()
            item['episodename'] = link.css(' ::text').get().strip()
            item['page_link'] = link.css(" ::attr(href)").get()
            all_data.append(item)

        for i in all_data:
            episodename = i['episodename'].replace('<', '').replace('>', '').replace(':', '') \
        .replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
            makedirectory(episodename)
            options = Options()
            preferences = {'download.default_directory': cwd + '\\' + episodename}
            options.add_experimental_option('prefs', preferences)
            options.add_argument('--no-sandbox')
            # options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--headless')
            options.add_argument("--incognito")
            options.add_argument('--disable-blink-features=AutomationControlled')
            # options.add_experimental_option('useAutomationExtension', False)
            # options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_argument("disable-infobars")

            driver = webdriver.Chrome(options=options)
            driver.maximize_window()

            driver.get(i['page_link'])
            time.sleep(2)

            element = driver.find_element_by_css_selector("div.spp-main-view")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

            driver.find_element_by_css_selector('div.spp-stpd-download-share-controls a').click()
            transcript = "\n ".join([v.text for v in driver.find_elements_by_css_selector('div.fbxt-content--inner p')])
            if transcript == "":
                transcript = "\n ".join([v.text for v in driver.find_elements_by_css_selector('div.elementor-element.elementor-element-db2d06a.elementor-widget.elementor-widget-theme-post-content div p')])


            ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
            ff.writelines(transcript)
            ff.close()

            ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
            ffo.writelines(transcript)
            ffo.close()
            time.sleep(20)



            driver.quit()









process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(lavien)
process.start()
