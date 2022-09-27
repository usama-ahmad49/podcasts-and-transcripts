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

class copspodcast(scrapy.Spider):
    name = 'copspodcast'

    def start_requests(self):
        url = 'https://cops.usdoj.gov/thebeat'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        namelist = response.css('#two h3::text').extract()
        mp3list = [v for v in response.css('#two > p > a') if '.mp3' in v.css('::attr(href)').extract_first()]
        transcriptlist = [v for v in response.css('#two > p > a') if '.pdf' in v.css('::attr(href)').extract_first()]
        for i, res in enumerate(namelist):
            makedirectory(res)
            audiolink = 'https://cops.usdoj.gov' + mp3list[i].css('::attr(href)').get()
            transcriptlink = 'https://cops.usdoj.gov' + transcriptlist[i].css('::attr(href)').get()
            try:
                downloadaudio = wget.download(audiolink, cwd + '\\' + res + '\\' + res + '.mp3')
            except:
                pass
            try:
                downloadtranscript = wget.download(transcriptlink, cwd + '\\' + res + '\\' + res + '_original.pdf')
            except:
                pass

            try:
                pdfFileObj = open(cwd + '\\' + res + '\\' + res + '_original.pdf', 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                totalPagespdf = pdfReader.getNumPages()
                ff = open(cwd + '\\' + res + '\\' + res + '.txt', 'w', encoding='utf-8')
                for i in range(0, totalPagespdf):
                    pageObj = pdfReader.getPage(i)
                    ff.writelines(pageObj.extractText())
                ff.close()
            except:
                pass

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(copspodcast)
process.start()
