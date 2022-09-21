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

class teachingin(scrapy.Spider):
    name = 'teachingin'

    def start_requests(self):
        yield scrapy.Request(url='https://teachinginhighered.com/episodes/')
    def parse(self, response, **kwargs):
        for link in list(set(response.css('div.entry-content a.content-link::attr(href)').extract())):
            yield scrapy.Request(url=link,callback=self.next_parse)

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page!= None:
            yield scrapy.Request(url=next_page,callback=self.parse)
        a=1
    def next_parse(self,response):
        episodename = response.css('h1.entry-title::text').get()
        audiolink = response.css('a[title="Download"]::attr(href)').get()
        transcript = response.css('div#transcriptcontainer p ::text').extract()

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

process.crawl(teachingin)
process.start()