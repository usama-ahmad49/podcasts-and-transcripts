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

class wnycpodcast(scrapy.Spider):
    name = 'wnycpodcast'

    def start_requests(self):
        url = 'https://www.wnycstudios.org/podcasts'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        episode_url = [v for v in response.css('.shows-list h3.show-tease__title a::attr(href)').extract()]
        for url in episode_url:
            for i in range(1, 20):
                yield scrapy.Request(url='https://www.wnycstudios.org' + url + f'/articles/{i}', callback=self.next_parse)

    def next_parse(self, response):
        try:
            if(response.css('section[data-test-selector="episode-list"]')):
                print('section available')
                episodeurl = [v for v in response.css('h1.episode-tease__title a::attr(href)').extract()]
                for url in episodeurl:
                    yield scrapy.Request(url='https://www.wnycstudios.org' + url, callback=self.last_parse)

        except:
            return

    def last_parse(self, response):
        episodename = response.css('h2::text').get() +' '+ response.css('h3.story__title::text').get().replace("\n","").replace('|', '').replace('/', '').replace(':', '').replace('?', '').replace('-', '').strip()
        audiolink = response.css('.story__download-link a::attr(href)').get()
        transcript = '\n'.join(response.css('.transcript p ::text').extract()).strip()

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
process.crawl(wnycpodcast)
process.start()

