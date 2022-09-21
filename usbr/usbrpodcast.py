import json
import os
import PyPDF2
import scrapy
import wget
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


class usbrpodcast(scrapy.Spider):
    name = 'usbrpodcast'
    start_urls = [
        'https://www.usbr.gov/gp/podcast/index.html',
    ]

    def parse(self, response, **kwargs):
        urls = [v for v in response.css('#Main > div > div.Main-content.container > div.Main-well > p a') if '.mp3' in v.css('::attr(href)').extract_first()]
        TranscriptUrls = [v for v in response.css('#Main > div > div.Main-content.container > div.Main-well > p a') if 'Text Transcript' in v.css('::text').extract_first()]
        for i, res in enumerate(urls):
            episodename = res.css(' ::text').extract_first().replace('/', '').replace(':', '').replace('?', '').replace('-', '').replace('&', '').replace('"', '').replace("'", '').strip()
            makedirectory(episodename)
            audiolink = 'https://www.usbr.gov/gp/podcast/'+res.css('::attr(href)').extract_first()
            transcirpturl = 'https://www.usbr.gov/gp/podcast/'+TranscriptUrls[i].css('a::attr(href)').extract_first()
            i = 0
            while True:
                try:
                    downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
                    break
                except:
                    if i == 10:
                        break
                    i += 1
            wget.download(transcirpturl, cwd + '\\' + episodename + '\\' + episodename + '_original.pdf')
            pdfFileObj = open(cwd + '\\' + episodename + '\\' + episodename + '_original.pdf', 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            totalPagespdf = pdfReader.getNumPages()
            ff = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
            for i in range(0, totalPagespdf):
                pageObj = pdfReader.getPage(i)
                ff.writelines(pageObj.extractText())
            ff.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(usbrpodcast)
process.start()