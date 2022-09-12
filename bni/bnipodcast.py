import scrapy

from scrapy.crawler import CrawlerProcess
import wget
import json
import os


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

class bnipodcast(scrapy.Spider):
    name = 'bnipodcast'

    def start_requests(self):
        count = 0
        while count < 161:
            count+=1
            yield scrapy.Request(url=f'https://www.bnipodcast.com/page/{count}/')


    def parse(self, response, **kwargs):
        for i in response.css('main article'):
            episodename = i.css('h2 a::text').get()
            transcription_link = i.css('a.more-link::attr(href)').get()
            iframe_link = i.css('iframe::attr(src)').get()
            if iframe_link is not None:
                yield scrapy.Request(url=iframe_link,callback=self.next_parse,meta={'epi_name':episodename,'transcrip_link':transcription_link})

    def next_parse(self,response):
        audiolink = response.css('div[title="Download"] a::attr(href)').get()

        yield scrapy.Request(url=response.meta['transcrip_link'], callback=self.next_next_parse,meta={'epi_name': response.meta['epi_name'],'audio_link':audiolink})

    def next_next_parse(self,response):
        episodename = response.meta['epi_name'].split(':')[-1].replace('<', '').replace('>', '').replace(':', '') \
        .replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink =response.meta['audio_link']

        name = response.css('div.entry-content h2 ::text').extract()[-1]

        all_data = response.css('div.entry-content ::text').extract()

        transcript = all_data[all_data.index(name)+1:]

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

process.crawl(bnipodcast)
process.start()

