import scrapy
from scrapy.crawler import CrawlerProcess
import wget
import os


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")

cwd = os.getcwd()



class libertarianism(scrapy.Spider):
    name = 'libertarianism'

    headers = {
        "authority": "www.libertarianism.org",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "if-none-match": "\"1654152553\"",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }
    cookies = {
        'nlbi_1209447': '0oBrLqJfPWwJJId2tDnAHwAAAACJTeXQ+kwJKmorI2IttJGH',
        'visid_incap_1209447': 'SN/0arNjTRmjwQUxK4YzpvOXkGIAAAAAQUIPAAAAAADfuZi6Sxn2JelbGP2nISAv',
        '_ga': 'GA1.2.632381274.1653643253',
        '_fbp': 'fb.1.1653643253300.186327486',
        '_omappvp': 'iIPNRwqveryM53fwirn73YtTi931KQOTVKE8ovC5aEvihjEhGXfMOxLEKgQ0hYDkWGsBELPoomO4li3BsR6edoHvOlDCZBmo',
        'hubspotutk': '2351df3992ccffacb47eec2a50a59f38',
        '__hssrc': '1',
        'incap_ses_776_1209447': 'z6LadNns7HF5EUG+nejECu1fmGIAAAAAbgLTTxzpTCTwEwicK4QytQ==',
        'incap_ses_1558_1209447': 'V7osaML38C55JF0f1iCfFU36mWIAAAAAotz/BTUkkqVC7cnC/gs7sw==',
        '_gid': 'GA1.2.1919606075.1654258255',
        'outbrain_cid_fetch': 'true',
        '__hstc': '150127785.2351df3992ccffacb47eec2a50a59f38.1653643254539.1654153207234.1654258258089.4',
        '__hssc': '150127785.2.1654258258089',
    }

    def start_requests(self):
        i = 0
        while i < 45:
            i = i + 1
            yield scrapy.Request(url=f'https://www.libertarianism.org/podcasts/free-thoughts?page={i}',headers=self.headers,cookies=self.cookies)

    def parse(self, response, **kwargs):
        epi_links = response.css('h5.index-listing__title.font-bold a::attr(href)').extract()
        for i in epi_links:
            yield scrapy.Request(url='https://www.libertarianism.org'+i,headers=self.headers,cookies=self.cookies,callback=self.parse_next)


    def parse_next(self,response):
        episodename = response.css('h1.h2.spacer--small--bottom.spacer--nomargin--last-child::text').get()
        episodename = episodename.replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink = response.css('div.spacer--top div.spacer--tiny--bottom a::attr(href)').get()
        transcript = response.css('div.accordion-item div.accordion-content.p-mb-last-child-0 ::text').extract()

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

process.crawl(libertarianism)
process.start()