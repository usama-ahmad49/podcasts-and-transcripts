import os
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
import time


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class capitalismpodcast(scrapy.Spider):
    name = 'capitalismpodcast'

    def start_requests(self):

        url = 'https://www.thisiscapitalism.com/category/podcasts/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        episodeurls = response.css('div.article.col-sm-3.article-small.fadein  a.center-icon::attr(href)').extract()
        for url in episodeurls:
            if 'guide' not in url:
                yield scrapy.Request(url=url, callback=self.next_parse)
            else:
                pass

    def next_parse(self, response):
        episodename = response.css('h1::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"',
                                                                                                                '').replace(
            '/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        transcript = '\n'.join(response.css('div.podcast-transcript p ::text').extract()).strip()

        makedirectory(episodename)
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ff.writelines(transcript)
        ff.close()

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ffo.writelines(transcript)
        ffo.close()

        options = webdriver.ChromeOptions()
        preferences = {'download.default_directory': cwd + '\\' + episodename}
        options.add_experimental_option('prefs', preferences)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get(response.url)
        time.sleep(2)

        element = driver.find_element_by_css_selector('img.alignnone.size-medium')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)

        driver.switch_to.frame(driver.find_element_by_css_selector('iframe[loading="lazy"]'))
        driver.find_element_by_id('download-player').click()
        time.sleep(8)

        driver.switch_to.default_content()
        driver.quit()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(capitalismpodcast)
process.start()
