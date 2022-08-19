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

class artspodcast(scrapy.Spider):
    name = 'artspodcast'

    def start_requests(self):
        for i in range(1, 23):
            url = f'https://www.arts.gov/stories/podcast/list?search_api_fulltext=&page={i}'
            yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        episodeurl = [v for v in response.css('h3.teaser__title a::attr(href)').extract()]
        for url in episodeurl:
            yield scrapy.Request(url='https://www.arts.gov' + url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('h1.page-title__title::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink = 'https://www.arts.gov' + response.css('audio source::attr(src)').get()
        transcript = '\n'.join(["".join([u for u in v.css("::text").getall()]) for v in response.css('div.accordion-item__description p')]).strip()

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
process.crawl(artspodcast)
process.start()
