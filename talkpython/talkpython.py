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
        url = 'https://talkpython.fm/episodes/all'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        episodeurl = [v for v in response.css('table.table.table-hover.episodes td a::attr(href)').extract()]
        for url in episodeurl:
            yield scrapy.Request(url='https://talkpython.fm'+url, callback=self.next_parse)

    def next_parse(self, response):
        episode_name = response.css('h1::text').get().replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\','').replace('|', '').replace('?', '').replace('*', '').strip()
        audio_link = 'https://talkpython.fm'+response.css('audio source::attr(src)').get()
        transcript_url = response.css('.action-buttons a[title="View and search the episode transcripts."]::attr(href)').get()
        yield scrapy.Request(url='https://talkpython.fm'+transcript_url, callback=self.last_parse, meta={'epiname': episode_name, 'audio': audio_link})

    def last_parse(self, response):
        episodename = response.meta['epiname']
        audiolink = response.meta['audio']
        transcript = '\n'.join([''.join([u for u in v.css('::text').extract()]).strip() for v in response.css('.large-content-text p')])

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
process.crawl(filterspodcast)
process.start()
