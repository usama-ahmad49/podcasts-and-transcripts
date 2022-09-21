import os
import json
import wget
import scrapy
import requests
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

class tradepodcast(scrapy.Spider):
    name = 'tradepodcast'
    def start_requests(self):
        url = 'https://www.trade.gov/export-nation'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('.horizontal-list__item'):
            link = res.css('.static-cards__bottom a::attr(href)').extract_first()
            yield scrapy.Request(url=link, callback=self.parse_data)
    def parse_data(self, response):
        try:
            link = 'https:'+[v for v in response.css('iframe::attr(src)').extract() if 'html5-player' in v][0]
        except:
            pass
        transcripttext = '\n'.join(response.css('.layout__region.layout__region--content p[align="left"] ::text').extract())
        res = requests.get(link)
        resp = scrapy.Selector(text=res.text)
        jsondata = [v for v in resp.css('script::text').extract() if 'var debug = false;' in v][0].split('var playlistItem =')[1].split(';')[0]
        data = json.loads(jsondata)
        episodename = data['item_title'].replace(':','')
        makedirectory(episodename)
        audiolink = data['download_link']
        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt','w', encoding='utf-8')
        ffo.write(transcripttext)
        ffo.close()
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '.txt','w', encoding='utf-8')
        ff.write(transcripttext)
        ff.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(tradepodcast)
process.start()