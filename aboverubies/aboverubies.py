import scrapy
from scrapy.crawler import CrawlerProcess
import wget
import requests
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

class aboverubies(scrapy.Spider):
    name = 'aboverubies'
    def start_requests(self):
        yield scrapy.Request(url='https://aboverubies.org/index.php/ar-podcasts-transcripts/2948-podcast-transcript-episode-177-celebrate-with-your-family')

    def parse(self, response, **kwargs):
        episodename= response.css('h1.title::text').get().split('|')[-1].replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink ='https://www.buzzsprout.com/183665/9477104-episode-177-celebrate-with-your-family.mp3?client_source=large_player&download=true'
        transcript = response.css('div.content.clearfix p ::text').extract()

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

process.crawl(aboverubies)
process.start()

