import os
import time
import urllib.request

import PyPDF2
import scrapy

from selenium import webdriver
from scrapy.crawler import CrawlerProcess


def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class childwelfarepodcast(scrapy.Spider):
    name = 'childwelfarepodcast'

    def start_requests(self):
        url = 'https://capacity.childwelfare.gov/states/topics/foster-care-permanency/family-focused-system/podcast'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('.block.custom-block__resource-card'):
            link = 'https://capacity.childwelfare.gov' + res.css('.usa-card__footer a::attr(href)').extract_first()
            episodename = res.css('h2::text').extract_first().replace(':', '')
            makedirectory(dirname=episodename)
            options = webdriver.ChromeOptions()
            preferences = {'download.default_directory': cwd + '\\' + episodename}
            options.add_experimental_option('prefs', preferences)
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            try:
                driver.get(link)
            except:
                pass
            time.sleep(2)
            ps = driver.page_source
            iframe = driver.find_element_by_css_selector('.resource-podcast__podcast iframe')
            driver.execute_script("arguments[0].scrollIntoView();", iframe)
            driver.switch_to.frame(iframe)
            try:
                download = driver.find_element_by_css_selector('#widget > div.singleSound.g-box-full > div > div > div.sound__content.g-transition-opacity > div.sound__header > div > div.soundHeader__rightRow > div.soundHeader__actions.g-transition-opacity > div > a')
                download.click()
            except:
                pass
            time.sleep(10)
            # action = ActionChains(driver)
            driver.close()
            res = scrapy.Selector(text=ps)
            try:
                transcripturl = 'https://capacity.childwelfare.gov' + res.css('.resource-podcast__transcript a::attr(href)').extract_first()
                download_file(transcripturl, cwd + '\\' + episodename + '\\' + episodename + '_original')
                pdfFileObj = open(cwd + '\\' + episodename + '\\' + episodename + '_original.pdf', 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                totalPagespdf = pdfReader.getNumPages()
                ff = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
                for i in range(0, totalPagespdf):
                    pageObj = pdfReader.getPage(i)
                    ff.writelines(pageObj.extractText())
                ff.close()
            except:
                pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(childwelfarepodcast)
process.start()
