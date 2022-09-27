import os

import PyPDF2
import scrapy
import wget
from scrapy.crawler import CrawlerProcess

all_data = []


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()
class wordfence(scrapy.Spider):
    name = 'wordfence'
    def start_requests(self):
        url = 'https://www.wordfence.com/blog/2021/07/episode-125-critical-sql-injection-vulnerability-patched-in-woocommerce/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        episodename = response.css('h1::text').extract_first().replace('<', '').replace('>', '').replace(':', '')\
            .replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        makedirectory(episodename)
        audiolink = response.css('#app-wrapper > section.blog-post-content > div > p:nth-child(6) > a:nth-child(1)::attr(href)').extract_first()
        transcript = ''.join(response.css('#app-wrapper > section.blog-post-content > div > p ::text').extract()[45:])
        try:
            downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        except:
            pass

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ffo.write(transcript)
        ffo.close()
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ff.write(transcript)
        ff.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(wordfence)
process.start()