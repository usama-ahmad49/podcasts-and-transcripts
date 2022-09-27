import os
import time

import wget
import urllib.request
import urllib
import scrapy
from striprtf.striprtf import rtf_to_text
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
class arsdotusda(scrapy.Spider):
    name = 'arsdotusda'

    def start_requests(self):
        url = 'https://www.ars.usda.gov/oc/podcasts/index/'
        yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        for res in response.css('#main-content div table tbody tr')[1:]:
            try:
                link = 'https://www.ars.usda.gov'+res.css('td:nth-child(2) a:nth-child(1)::attr(href)').extract_first()
                name = res.css('td:nth-child(2) a:nth-child(1)::text').extract_first().replace(':','')
                yield scrapy.Request(url = link, callback=self.parse_data, meta={'name':name})
            except:
                pass
    def parse_data(self, response):
        episodeName = ' '.join(response.meta['name'].split()[:6])
        makedirectory(dirname=episodeName)
        try:
            audioFileUrl = [v for v in response.css('a::attr(href)').extract() if '.mp3' in v][0]
        except:
            try:
                videoFileUrl = [v for v in response.css('a::attr(href)').extract() if '.mp4' in v][0]
            except:
                pass
        # if audioFileUrl == None:
        #     audioFileUrl = response.css('#main-content > div.usa-width-three-fourths.usa-layout-docs-main_content > div > p > span > a:nth-child(5)::attr(href)').extract_first()
        #     if audioFileUrl == None:
        #         audioFileUrl = response.css('#main-content > div.usa-width-three-fourths.usa-layout-docs-main_content > table > tbody > tr > td:nth-child(2) > p:nth-child(4) > a:nth-child(1)::attr(href)').extract_first()

        transcriptUrl = [v for v in response.css('a::attr(href)').extract() if '.rtf' in v][0]
        # if transcriptUrl == None:
        #     transcriptUrl = response.css('#main-content > div.usa-width-three-fourths.usa-layout-docs-main_content > div > p > span > a:nth-child(7)::attr(href)').extract_first()
        #     if transcriptUrl == None:
        #         transcriptUrl = response.css('#main-content > div.usa-width-three-fourths.usa-layout-docs-main_content > table > tbody > tr > td:nth-child(2) > p:nth-child(4) > a:nth-child(2)::attr(href)').extract_first()
        try:
            downloadaudio = wget.download('https://www.ars.usda.gov'+audioFileUrl, cwd+'\\'+episodeName+'\\'+episodeName+'.mp3')
        except:
            try:
                downloadaudio = wget.download('https://www.ars.usda.gov'+videoFileUrl, cwd+'\\'+episodeName+'\\'+episodeName+'.mp4')
            except:
                pass
        try:
            downloadtranscript = wget.download('https://www.ars.usda.gov' + transcriptUrl, cwd + '\\' + episodeName + '\\' + episodeName + '_original.rtf')
        except:
            pass
        time.sleep(1)
        with open(cwd + '\\' + episodeName + '\\' + episodeName + '_original.rtf', 'r') as file:
            text = file.read()
        fileopen = open(cwd + '\\' + episodeName + '\\' + episodeName + '.txt','w')
        fileopen.write(rtf_to_text(text))


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(arsdotusda)
process.start()
