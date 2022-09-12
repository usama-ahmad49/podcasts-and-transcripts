import os
import PyPDF2
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

class cbopodcast(scrapy.Spider):
    name = 'cbopodcast'

    def start_requests(self):
        url = 'https://www.cbo.gov/podcasts'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('.listing.DirectorsBlog li h3'):
            link = 'https://www.cbo.gov'+res.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=link,callback=self.parse_data)
    def parse_data(self, response):
        episodename = ''.join(response.css('h1.title ::text').extract()).replace('|', '').replace('/', '').replace(':', '').replace('?', '').replace('-', '').strip()
        makedirectory(episodename)
        audiolink = 'https://www.cbo.gov'+response.css('.downloadpodcast a::attr(href)').extract_first()
        transcriptlink = response.css('.downloadtranscript a::attr(href)').extract_first()
        try:
            downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        except:
            pass
        try:
            downloadtranscript = wget.download(transcriptlink, cwd + '\\' + episodename + '\\' + episodename + '_original.pdf')
        except:
            pass
        try:
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
process.crawl(cbopodcast)
process.start()