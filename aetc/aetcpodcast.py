import os
import wget
import scrapy
from scrapy.crawler import CrawlerProcess
import requests

def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")

cwd = os.getcwd()

class aetcpodcast(scrapy.Spider):
    name = 'aetcpodcast'

    def start_requests(self):
        url = 'https://www.aetc.af.mil/Podcast/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        episodeurl = [v.split('(')[1][1:-2] for v in response.css('.DVIDSCarouselItem a::attr(href)').extract()]
        for url in episodeurl:
            yield scrapy.Request(url=url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('.DVIDSMediaTitle::text').get().replace('/', '').replace(':', '').replace('?', '').replace('-', '').replace('&', '').replace('"', '').strip()
        audiolink = response.css('#playerDownload a::attr(href)').get()
        try:
            compare = int(response.css('.DVIDSMediaTitle::text').get().replace('/','').replace('.','').split('-')[1].strip()[-2:])
        except:
            compare = int(response.css('.DVIDSMediaTitle::text').get().replace('/', '').replace('.', '').split('–')[1].strip()[-2:])

        for v in response.css('tbody tr td a'):
            if str(compare) == v.css('::text').get().split()[-1]:
                transcripturl = 'https://www.aetc.af.mil' + v.css('::attr(href)').get()
                response = requests.get(transcripturl)

        try:
            makedirectory(episodename)
            downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')

            ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
            ff.writelines(response.text)
            ff.close()

            ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
            ffo.writelines(response.text)
            ffo.close()

        except:
            pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(aetcpodcast)
process.start()
