import os
import wget
import scrapy
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


class ilsrpodcast(scrapy.Spider):
    name = 'ilsrpodcast'

    def start_requests(self):

        url = 'https://ilsr.org/local-energy-rules-podcast-homepage/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for url in response.css('table[style="height: 8305px; width: 81.8904%;"] tr td a::attr(href)').extract():
            yield scrapy.Request(url=url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('h1.entry-title::text').get().replace('<', '').replace('>', '').replace(':',
                                                                                                           '').replace(
            '"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink = response.css('a[title="Download"]::attr(href)').get()
        makedirectory(episodename)

        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        try:
            transcript = '\n'.join(response.css('div.panel-body.postclass table tr ::text').extract()).strip()
            if transcript != "":
                ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
                ff.writelines(transcript)
                ff.close()

                ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
                ffo.writelines(transcript)
                ffo.close()
        except:
            pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(ilsrpodcast)
process.start()
