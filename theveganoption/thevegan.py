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

class theveganpodcast(scrapy.Spider):
    name = 'theveganpodcast'

    def start_requests(self):
        url = 'http://theveganoption.org/vegetarian-history/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        episoseurl = [v for v in response.css('ol#lcp_instance_0 li a:nth-child(1)::attr(href)').extract()]
        for url in episoseurl:
            yield scrapy.Request(url=url, callback=self.next_parse)

    def next_parse(self, response):
        episode_name = response.css('h2::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\','').replace('|', '').replace('?', '').replace('*', '').strip()
        try:
            audio_link = [v for v in response.css('p a') if 'Play or download' in v.css('::text').get()][0].attrib['href']
        except:
            pass

        try:
            trans = [v for v in response.css('p a') if 'read transcript' in v.css('::text').get()][0].attrib['href']
            yield scrapy.Request(url=trans, callback=self.last_parse, meta={'epiname': episode_name, 'audio': audio_link})
        except:
            pass

    def last_parse(self, response):
        episodename = response.meta['epiname']
        audiolink = response.meta['audio']
        transcript = '\n'.join(response.css('div.entry.clearfix p ::text').extract()).strip()

        makedirectory(episodename)
        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ff.write(transcript)
        ff.close()

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w',  encoding='utf-8')
        ffo.write(transcript)
        ffo.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(theveganpodcast)
process.start()
