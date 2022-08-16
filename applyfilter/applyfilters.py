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

class filterspodcast(scrapy.Spider):
    name = 'filterspodcast'

    def start_requests(self):
        for i in range(1, 10):
            url = f'https://applyfilters.fm/podcast/page/{i}/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for url in response.css('div.post-header a::attr(href)').extract():
            yield scrapy.Request(url=url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('h2::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\','').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink = response.css('audio source::attr(src)').get()

        makedirectory(episodename)
        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        try:
            transcript = '\n'.join(response.css('.arconix-toggle-content ::text')).extract()
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
process.crawl(filterspodcast)
process.start()
