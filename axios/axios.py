import os
import wget
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
import json


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class axiospodcast(scrapy.Spider):
    name = 'axiospodcast'

    def start_requests(self):
        for i in range(1, 11):
            url = f'https://www.axios.com/podcasts/today?page={i}'
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for url in response.css('h2 a::attr(href)').extract():
            yield scrapy.Request(url='https://www.axios.com' + url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('h1::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"',
                                                                                                                '').replace(
            '/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        transcript = '\n'.join(
            [v.xpath("following-sibling::p") for v in response.css("h5") if "Transcript" == v.css("::text").get()][
                0].css("::text").extract()).strip()
        iframeid = response.css('iframe[scrolling="no"]::attr(src)').get().split('=')[-1]
        resp = json.loads(requests.get(f'https://player.megaphone.fm/playlist/episode/{iframeid}').text)
        audiolink = resp['episodes'][0]['audioUrl']

        makedirectory(episodename)

        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ff.writelines(transcript)
        ff.close()

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ffo.writelines(transcript)
        ffo.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(axiospodcast)
process.start()
