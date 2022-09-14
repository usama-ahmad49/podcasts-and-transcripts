import json
import os

import scrapy
import wget
from scrapy.crawler import CrawlerProcess

headers = {
    "authority": "www.cfr.org",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "dnt": "1",
    "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjI0NTYxNjAiLCJhcCI6IjM0NTY3NTgwMyIsImlkIjoiNmY2MjI3Y2FiZDQ2NmQ5MyIsInRyIjoiYTUzOWFkNzY5OWRiOGFmZGZjMDg2ZGQyZjIwN2ZlMzAiLCJ0aSI6MTY1MTA0MDEwNDUzNywidGsiOiI2NjY4NiJ9fQ==",
    "origin": "https://www.cfr.org",
    "referer": "https://www.cfr.org/podcasts/why-it-matters",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-a539ad7699db8afdfc086dd2f207fe30-6f6227cabd466d93-01",
    "tracestate": "66686@nr=0-1-2456160-345675803-6f6227cabd466d93----1651040104537",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "x-newrelic-id": "VgICV1dVCBADUFNSBwkCX1M=",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "_cb_ls": "1",
    "cookie-agreed": "2",
    "_cb": "CCDHmPCoKUABDl9D-G",
    "_cb_svref": "null",
    "_ga": "GA1.2.2071489426.1651039658",
    "_gid": "GA1.2.1335359989.1651039658",
    "_hjFirstSeen": "1",
    "_hjSession_1768366": "eyJpZCI6IjA1ZWYxZmNmLTk4ZjYtNDg1Mi04N2E5LTJjMzJmZTkwMWY2NCIsImNyZWF0ZWQiOjE2NTEwMzk2NTgxOTksImluU2FtcGxlIjp0cnVlfQ==",
    "_hjIncludedInPageviewSample": "1",
    "_hjSessionUser_1768366": "eyJpZCI6IjI1ZWM1YWU4LTBkM2YtNThlMC1hMDI2LWY1MTBmOGNlNGZhMCIsImNyZWF0ZWQiOjE2NTEwMzk2NTgxODcsImV4aXN0aW5nIjp0cnVlfQ==",
    "_chartbeat2": ".1651039656611.1651040039321.1.CHm019brqFCQjnSqB4eb2lDFIy3H.8",
    "sailthru_pageviews": "8",
    "sailthru_content": "e2efc6c04551931816e1f91da2f93405e2f4979263ff6a5ea40423d6419385d3d727b82e40a3904552885b4a4ae88453d4aded48c2a0fec2b2d8f6348402b355",
    "sailthru_visitor": "931d5278-4c38-4289-81fb-f8f430dc4af9",
    "amp_2be1ae": "ZkYvY1zJgPvngWZfIyTbMR...1g1kq3mjg.1g1kqgchn.i.0.i"
}


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class cfrpodcast(scrapy.Spider):
    name = 'cfrpodcast'

    def start_requests(self):
        url = 'https://www.cfr.org/views/ajax?_wrapper_format=drupal_ajax'
        for i in range(0, 4):
            body = f'view_name=latest_and_archive_podcast&view_display_id=podcasts_filters_and_cards&view_args=62311&view_path=%2Ftaxonomy%2Fterm%2F62311&view_base_path=&view_dom_id=fd2046896b6dd8f2de11a0b88afbe168831ed0d5828702f3c32a0e206f4e8b65&pager_element=0&topics=All&regions=All&page={i}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=cfr_theme&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=cfr_chartbeat%2Fcfr-chartbeat-body%2Ccfr_chartbeat%2Fcfr-chartbeat-header%2Ccfr_homepage_sections%2Fadvanced_autocomplete%2Ccfr_sailthru%2Fjavascript_api_library%2Ccfr_theme%2Falert%2Ccfr_theme%2Fbg-image-switch%2Ccfr_theme%2Ffacebook-pixel%2Ccfr_theme%2Fglobal-legacy%2Ccfr_theme%2Fheader%2Ccfr_theme%2Fheader-contextual%2Ccfr_theme%2Fkrt-grid%2Ccore%2Fdrupal.autocomplete%2Cdatalayer%2Fbehaviors%2Cdatalayer%2Fhelper%2Cdd_datalayer_tools%2Famplitude%2Cdd_datalayer_tools%2FcustomDimensionUserCategory%2Cdd_datalayer_tools%2FdatalayerItems%2Cdd_datalayer_tools%2FpodcastFinish%2Cdd_datalayer_tools%2FpodcastStart%2Cdd_datalayer_tools%2FvideoFinish%2Cdd_datalayer_tools%2FvideoStart%2Ceu_cookie_compliance%2Feu_cookie_compliance_default%2Clazy%2Flazy%2Csearch_autocomplete%2Ftheme.minimal.css%2Csystem%2Fbase%2Cviews%2Fviews.module%2Cviews_infinite_scroll%2Fviews-infinite-scroll'
            yield scrapy.Request(
                url=url,
                method='POST',
                dont_filter=True,
                cookies=cookies,
                headers=headers,
                body=body,
            )

    def parse(self, response, **kwargs):
        json_data = json.loads(response.text)
        try:
            html = json_data[-1]['data']
        except:
            pass
        html_content = scrapy.Selector(text=html)

        if 'No results found' in html:
            return

        podcasturl = [v for v in html_content.css('html body div.podcast-episode__bottom a::attr(href)').extract()]
        for url in podcasturl:
            yield scrapy.Request(url='https://www.cfr.org' + url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('.episode-header__title::text').get().strip().replace('/', '').replace(':', '').replace('?', '').replace('-', '').replace('&', '').replace('"', '').replace("'", '').strip()
        audiolink = response.css('audio#player-default::attr(src)').get()
        transcripttext = response.css('.podcast-body p ::text').extract()

        makedirectory(episodename)
        i=0
        while True:
            try:
                downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
                break
            except:
                if i == 10:
                    break
                i+=1

        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ff.writelines(transcripttext)
        ff.close()

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ffo.writelines(transcripttext)
        ffo.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(cfrpodcast)
process.start()
