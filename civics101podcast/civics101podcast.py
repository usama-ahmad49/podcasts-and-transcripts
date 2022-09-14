import json
import os

import scrapy
import wget
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


class civics101podcast(scrapy.Spider):
    name = 'civics101podcast'

    def start_requests(self):
        url = 'https://www.civics101podcast.org/episodes'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('.archive-item-link'):
            url = 'https://www.civics101podcast.org' + res.css('::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self, response):
        transcript = '\n'.join(response.css('.sqs-block.html-block.sqs-block-html')[1].css('.sqs-block-content p ::text').extract())
        name = response.css('h1.entry-title.p-name a::text').extract_first().replace('/', '').replace(':', '').replace('?', '').replace('-', '').replace('&', '').replace('"', '').strip()
        id = response.css('.sonix--embeddable.sonix-embed::attr(data-sonix-id)').extract_first()
        url = f'https://sonix.ai/embed/{id}/file.json'
        yield scrapy.Request(url=url, meta={'transcript': transcript, 'name': name, 'id': id}, callback=self.parse_data_ind)

    def parse_data_ind(self, response):
        data = json.loads(response.text)
        episodename = response.meta['name']
        transcript = response.meta['transcript']
        audiolink = data['mp3Url']
        makedirectory(episodename)
        i = 0
        while True:
            try:
                downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
                break
            except:
                if i == 10:
                    break
                i += 1
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ff.writelines(transcript)
        ff.close()

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ffo.writelines(transcript)
        ffo.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(civics101podcast)
process.start()
