import scrapy
from scrapy.crawler import CrawlerProcess
import wget
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

class timblog(scrapy.Spider):
    name = 'timblog'
    def start_requests(self):
        yield scrapy.Request(url='https://tim.blog/2018/06/21/the-tim-ferriss-show-transcripts-krista-tippett/')

    def parse(self, response, **kwargs):
        for i in response.css('div.entry-content p a'):
            if i.css(" ::text").get() == 'here':
                audiolink = i.css(" ::attr(href)").get()
        episodename = response.css('h1.entry-title::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()

        transcript = response.css('div.entry-content p ::text').extract()

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

process.crawl(timblog)
process.start()
