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

class cdcpodcast(scrapy.Spider):
    name = 'cdcpodcast'

    def start_requests(self):
        for i in range(1, 79):
            url = f'https://tools.cdc.gov/api/v2/resources/media?enctype=audio,transcript&fields=id,name,url,mediaType,thumbnailUrl,alternateImages,description,isTopSyndicated,language,enclosures&jsonpCallbackParam=cb&language=english&max=12&mediatype=Podcast&pagenum={i}&showchildlevel=0&sort=-datemodified&callback=angular.callbacks._9'
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        json_data = json.loads(response.text.split('angular.callbacks._9(')[1][:-1])
        for res in json_data['results']:
            episodename = res['name'].replace('|', '').replace('/', '').replace(':', '').replace('?', '').replace('-', '').strip()
            makedirectory(episodename)
            transcripturl = res['enclosures'][0]['resourceUrl']
            audiolink = res['enclosures'][1]['resourceUrl']

            downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')

            transcripdownload = wget.download(transcripturl,
                                          cwd + '\\' + episodename + '\\' + episodename + '_original.pdf')

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
process.crawl(cdcpodcast)
process.start()