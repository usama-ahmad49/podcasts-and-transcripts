import json
import os

import requests
import scrapy
import wget
from scrapy.crawler import CrawlerProcess

cwd = os.getcwd()


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created")
    except:
        print("Directory " + dirname + " already exists")


cookies = {
    'bcomID': '6217772502337844163',
    'SessionAuth': 'O4fGvP9vHRHLy5jb7MKmu0KGDWqTB00OYGtet5RMbQvMNyOhvP8wxptbF1XAVUDY',
    '_gid': 'GA1.2.473004143.1657055921',
    'BCSessionID': 'e708ba63-f7c1-4b7e-a933-9b71b9027174',
    'eb_control_group': 'control',
    'referer': 'https%3A%2F%2Fwww.britannica.com%2Fpodcasts%2Fon-this-day%2FOn-this-Day-podcast-May-1',
    'sessionId': 'F1EB8D99-25D2-4EEE-B7E1-347F8D493ED9',
    'subreturn': 'https%3A%2F%2Fwww.britannica.com%2Fpodcasts%2Fon-this-day',
    'webstats': '"referer_page=https%3A%2F%2Fwww.britannica.com%2Fpodcasts%2Fon-this-day"',
    '__mendel': '%7B%27pagesViewed%27%3A3%2C%27surveyShown%27%3Atrue%2C%27topicInitialSequence%27%3A0%7D',
    '_ga_TE6YF92Y0D': 'GS1.1.1657055921.1.1.1657055958.0',
    'last_visit_bc': '1657055958044',
    'CAMLoginRedirectUrl': 'https://www.britannica.com/podcasts/on-this-day',
    '_ga': 'GA1.2.1259829607.1657055921',
    '_gali': '__paginatedBrowseLoadMore',
}

headers = {
    'authority': 'www.britannica.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'bcomID=6217772502337844163; SessionAuth=O4fGvP9vHRHLy5jb7MKmu0KGDWqTB00OYGtet5RMbQvMNyOhvP8wxptbF1XAVUDY; _gid=GA1.2.473004143.1657055921; BCSessionID=e708ba63-f7c1-4b7e-a933-9b71b9027174; eb_control_group=control; referer=https%3A%2F%2Fwww.britannica.com%2Fpodcasts%2Fon-this-day%2FOn-this-Day-podcast-May-1; sessionId=F1EB8D99-25D2-4EEE-B7E1-347F8D493ED9; subreturn=https%3A%2F%2Fwww.britannica.com%2Fpodcasts%2Fon-this-day; webstats="referer_page=https%3A%2F%2Fwww.britannica.com%2Fpodcasts%2Fon-this-day"; __mendel=%7B%27pagesViewed%27%3A3%2C%27surveyShown%27%3Atrue%2C%27topicInitialSequence%27%3A0%7D; _ga_TE6YF92Y0D=GS1.1.1657055921.1.1.1657055958.0; last_visit_bc=1657055958044; CAMLoginRedirectUrl=https://www.britannica.com/podcasts/on-this-day; _ga=GA1.2.1259829607.1657055921; _gali=__paginatedBrowseLoadMore',
    'dnt': '1',
    'referer': 'https://www.britannica.com/podcasts/on-this-day',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

params = {
    'p': '3',
    'n': '10',
}


class APR(scrapy.Spider):
    name = 'APR'

    def start_requests(self):
        for i in range(1, 20):
            url = f'https://www.britannica.com/ajax/podcasts/8669?p={i}&n=10'
            yield scrapy.Request(url=url, cookies=cookies, headers=headers)

    def parse(self, response, **kwargs):
        for res in response.css('.card.mb-20'):
            episodename = res.css('.label.mb-10::Text').extract_first().replace('<', '').replace('>', '').replace(':',
                                                                                                                  '').replace(
                '"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
            audiolink = res.css('.shadow.art19player.micro::attr(src)').extract_first()
            transcriptlink = 'https://www.britannica.com' + res.css(
                '.grid.align-items-center a::attr(href)').extract_first()
            yield scrapy.Request(url=audiolink, callback=self.parse_data,
                                 meta={"episodename": episodename, "tr": transcriptlink})

    def parse_data(self, response):
        makedirectory(response.meta['episodename'])
        audiojson = json.loads(
            response.css('script[data-art19-webplayer-preload="data-art19-webplayer-preload"] ::Text').extract_first())
        audiolink = audiojson['content']['media']['mp3']['url']

        wget.download(audiolink,
                      cwd + '\\' + response.meta['episodename'] + '\\' + response.meta['episodename'] + '.mp3')
        Tres = requests.get(response.meta['tr'])
        Tresss = scrapy.Selector(text=Tres.text)
        transcript = '\n'.join(Tresss.css('.js-transcript.font-serif.font-20.lh-lg.mb-30 ::text').extract())
        ff = open(cwd + '\\' + response.meta['episodename'] + '\\' + response.meta['episodename'] + '_original.txt',
                  'w', encoding='utf-8')
        ff.write(transcript)
        ff.close()

        ffo = open(cwd + '\\' + response.meta['episodename'] + '\\' + response.meta['episodename'] + '.txt', 'w',
                   encoding='utf-8')
        ffo.write(transcript)
        ffo.close()


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(APR)
    process.start()
