import os
import time

import scrapy
from selenium import webdriver
from scrapy.crawler import CrawlerProcess


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class justicepodcast(scrapy.Spider):
    name = 'justicepodcast'

    def start_requests(self):
        url = 'https://www.justice.gov/ovw/podcast'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('.views-row'):
            link = 'https://www.justice.gov' + res.css('.views-field.views-field-title span a::attr(href)').extract_first()
            episodename = res.css('.views-field.views-field-title span a::text').extract_first().replace(':', '').strip()
            makedirectory(episodename)
            options = webdriver.ChromeOptions()
            preferences = {'download.default_directory': cwd + '\\' + episodename}
            options.add_experimental_option('prefs', preferences)
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            driver.get(link)
            transcriptbtn = driver.find_element_by_css_selector('.fieldset-title')
            transcriptbtn.click()
            ps = driver.page_source
            iframe = driver.find_element_by_css_selector('.field__item.even iframe')
            time.sleep(2)
            driver.execute_script("arguments[0].scrollIntoView();", iframe)
            driver.switch_to.frame(iframe)
            sharebtn = driver.find_element_by_css_selector('div.episode-container > div.footer > div > div.more > a.controls-button.controls-button--last.icon-share')
            try:
                sharebtn.click()
            except:
                pass
            downloadbtn = driver.find_element_by_css_selector('.window__share-group .icon-download')
            try:
                downloadbtn.click()
            except:
                pass
            time.sleep(10)
            driver.close()
            res = scrapy.Selector(text=ps)
            transcripttext = '\n'.join(res.css('.collapse-text-text p ::text').extract())
            ffo = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
            ffo.write(transcripttext)
            ffo.close()
            ff = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
            ff.write(transcripttext)
            ff.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(justicepodcast)
process.start()
