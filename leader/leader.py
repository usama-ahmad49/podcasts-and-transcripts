import os
import time
import requests
import wget
import scrapy
from scrapy.crawler import CrawlerProcess
from seleniumwire import webdriver


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class leaderpodcast(scrapy.Spider):
    name = 'leaderpodcast'

    def start_requests(self):
        new_cookies = dict()
        url = f'https://leader.pubs.asha.org/topic/leader_DO_tag/leader_podcast?target=do-topic&sortBy=do-DateField&startPage=0&pageSize=20'
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)
        headers = dict([v for v in driver.requests if url in v.url][0].headers)
        for v in driver.get_cookies():
            new_cookies[v['name']] = v['value']
        driver.quit()

        for i in range(0, 5):
            url = f'https://leader.pubs.asha.org/topic/leader_DO_tag/leader_podcast?target=do-topic&sortBy=do-DateField&startPage={i}&pageSize=20'
            yield scrapy.Request(url=url, headers=headers, cookies=new_cookies)

    def parse(self, response, **kwargs):
        for url in response.css('h4.do-search-item__title a::attr(href)').extract():
            y = 8
            yield scrapy.Request(url='https://leader.pubs.asha.org' + url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('h1 a::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"',
                                                                                                                  '').replace(
            '/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        makedirectory(episodename)
        audiourl = response.css('iframe[scrolling="no"]').get().split('src="')[-1].split('#')[0]
        resp = requests.get(audiourl)
        audioresp = scrapy.Selector(text=resp.text)
        audiolink = audioresp.css('script').get().split('media_url = "')[-1].split('"')[0].replace('\\', '')
        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')

        try:
            for trans in response.css('div.podcast_content-wrapper a'):
                try:
                    if ('episode.' in trans.css('em ::text').get()) or ('transcript.' in trans.css('em ::text').get()):
                        transurl = 'https://leader.pubs.asha.org' + trans.css(' ::attr(href)').get()
                        transresp = requests.get(transurl)
                        resp_trans = scrapy.Selector(text=transresp.text)
                        transcript = '\n'.join(resp_trans.css('p ::text').extract()[10:]).strip()
                        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w',
                                  encoding='utf-8')
                        ff.write(transcript)
                        ff.close()

                        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
                        ffo.write(transcript)
                        ffo.close()
                except:
                    pass
        except:
            pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(leaderpodcast)
process.start()
