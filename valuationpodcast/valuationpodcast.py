import os
import time

import wget
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver

def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory" + dirname + " Created ")
    except:
        print("Directory" + dirname + " already exists")

cwd = os.getcwd()

class valuationpodcast(scrapy.Spider):
    name = 'valuationpodcast'

    def start_requests(self):
        url = 'https://www.valuationpodcast.com/episodes'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('article.hentry'):
            link = 'https://www.valuationpodcast.com'+res.css('h1.blog-title a::attr(href)').extract_first()
            yield scrapy.Request(url=link,callback=self.next_parse)
        try:
            url = 'https://www.valuationpodcast.com'+response.css('.blog-list-pagination .older a::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse)
        except:
            pass

    def next_parse(self, response):
        episodename = response.css('h1.entry-title.entry-title--large.p-name::text').extract_first().replace(':','').replace('?','').strip()
        audiolink = response.css('.sqs-audio-embed::attr(data-url)').extract_first()
        transcripttext = '\n'.join(response.css('.blog-item-content-wrapper .sqs-block.html-block.sqs-block-html')[0].css('p ::text').extract())
        makedirectory(episodename)
        options = webdriver.ChromeOptions()
        preferences = {'download.default_directory': cwd + '\\' + episodename}
        options.add_experimental_option('prefs', preferences)
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        # driver.maximize_window()
        driver.get(audiolink)
        time.sleep(10)
        driver.close()
        # downloadaudio = wget.download(audiolink.split('?')[0], cwd + '\\' + episodename + '\\' + episodename + '.mp3') #
        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ffo.write(transcripttext)
        ffo.close()
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ff.write(transcripttext)
        ff.close()

process = CrawlerProcess({
'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(valuationpodcast)
process.start()
