import json
import os

import scrapy
import wget
from scrapy.crawler import CrawlerProcess

# url = 'https://www.usgs.gov/views/ajax?_wrapper_format=drupal_ajax'
#
headers = {
    "authority": "www.usgs.gov",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "dnt": "1",
    "origin": "https://www.usgs.gov",
    "referer": "https://www.usgs.gov/products/multimedia-gallery/audio",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

cookies = {
    "_ga": "GA1.2.932203535.1652354099",
    "_hjSessionUser_606685": "eyJpZCI6ImZhZjU2YjE3LWU5YzUtNTgwYy04MzI4LTYxZGFlMTBjMjg5MSIsImNyZWF0ZWQiOjE2NTIzNTQwOTk3MDksImV4aXN0aW5nIjp0cnVlfQ==",
    "_gid": "GA1.2.6550451.1652942081",
    "_hjIncludedInSessionSample": "0",
    "_hjSession_606685": "eyJpZCI6IjhhM2EyNjkzLWU5NjQtNGVmMi05NzYyLWE2NDIyNDRiZGI4MiIsImNyZWF0ZWQiOjE2NTI5NDIwODEyMjAsImluU2FtcGxlIjpmYWxzZX0=",
    "GUIDCookie": "45f58597-7489-4612-bf6a-7dcd3df642ac",
    "CFIWebMonPersistent-57": "%7B%22LastAccept%22%3Anull%2C%22LastDecline%22%3A1652942085329%7D",
    "CFIWebMonSession": "%7B%22GUID%22%3A%2243979e2d-7f8b-b168-04ac-652354099468%22%2C%22EmailPhone%22%3A%22%22%2C%22HttpReferer%22%3A%22https%3A//www.usgs.gov/products/multimedia-gallery/audio%22%2C%22PageViews%22%3A4%2C%22CurrentRuleId%22%3A%2257%22%2C%22CurrentPType%22%3A%220%22%2C%22Activity%22%3A%22Browse%22%2C%22SessionStart%22%3A1652354099466%2C%22UnloadDate%22%3Anull%2C%22WindowCount%22%3A2%2C%22LastPageStayTime%22%3A122341%2C%22AcceptOrDecline%22%3A%7B%2257%22%3A%22D%22%7D%2C%22FirstBrowsePage%22%3A%22https%3A//www.usgs.gov/media/audio/eyes-earth-episode-73-global-water-use%22%2C%22FirstBrowseTime%22%3A1652942493997%2C%22FinallyLeaveTime%22%3A1652942493997%2C%22FinallyBrowsePage%22%3A%22https%3A//www.usgs.gov/media/audio/eyes-earth-episode-73-global-water-use%22%2C%22SiteReferrer%22%3A%22https%3A//www.usgs.gov/products/multimedia-gallery/audio%22%2C%22LastPopUpPage%22%3A%22https%3A//www.usgs.gov/products/multimedia-gallery/audio%22%2C%22TimeSpentonSite%22%3A0%2C%22GoogleAnalyticsValue%22%3A%2245f58597-7489-4612-bf6a-7dcd3df642ac%22%2C%22Dimension%22%3A%22%22%2C%22CookiePath%22%3A%22/%3B%20domain%3Dusgs.gov%22%2C%22AdditionalAttributes%22%3A%7B%7D%2C%22ClickTracker%22%3A%22%22%2C%22PageIndex%22%3A0%2C%22AllCookies%22%3A%22%22%2C%22AllCustomVariables%22%3A%22%22%7D",
    "_gat_GSA_ENOR0": "1",
    "_gat_GSA_ENOR1": "1",
    "_gat_GSA_ENOR2": "1",
    "AWSALB": "gT0MsN3lvVPyGGOPXRH6Rq+rsKc3wbsb9EQ4bjMs/Xf/yB6YWzCf7XuxSUv2WfV2W+oL3ItUuK8v7OljvhtVwPjNRTBtxyXJOiGvy/lsx2EnigzOBI6rma187BK9",
    "AWSALBCORS": "gT0MsN3lvVPyGGOPXRH6Rq+rsKc3wbsb9EQ4bjMs/Xf/yB6YWzCf7XuxSUv2WfV2W+oL3ItUuK8v7OljvhtVwPjNRTBtxyXJOiGvy/lsx2EnigzOBI6rma187BK9"
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


class usgspodcast(scrapy.Spider):
    name = 'usgspodcast'

    def start_requests(self):
        for i in range(0, 26):
            body = f'view_name=hq_media&view_display_id=media_bundle_audio&view_args=482342%2Fmedia_bundle_audio&view_path=%2Fnode%2F229185&view_base_path=&view_dom_id=d95a8384c89fd405585c6d999ab690b6bd44a0362bacfb9a6163ef0cf8a7e997&pager_element=0&view_html_id=views-exposed-form-hq-media-media-bundle-audio--LLT8Tb_bjwA&media_audio_type=All&sort_bef_combine=media_release_date_1_DESC&sort_by=media_release_date_1&sort_order=DESC&page={i}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=usgs_tantalum&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=addtoany%2Faddtoany%2Cbetter_exposed_filters%2Fauto_submit%2Cbetter_exposed_filters%2Fgeneral%2Ccore%2Fdrupal.collapse%2Ccore%2Fdrupal.form%2Cextlink%2Fdrupal.extlink%2Cimproved_multi_select%2Fims%2Cmasonry%2Fmasonry.layout%2Cmathjax%2Fconfig%2Cmathjax%2Fsetup%2Cmathjax%2Fsource%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Cresponsive_table_filter%2Fresponsive-table%2Csystem%2Fbase%2Cusgs_tantalum%2Fassets%2Cusgs_tantalum%2Fdotdotdot%2Cusgs_tantalum%2Ffontawesome%2Cusgs_tantalum%2Fslick%2Cusgs_tantalum%2Fusgs.backtotop%2Cusgs_tantalum%2Fusgs.carousel%2Cusgs_tantalum%2Fusgs.group_topic_view%2Cusgs_tantalum%2Fusgs.masonry%2Cusgs_tantalum%2Fusgs.mobile-navigation%2Cusgs_tantalum%2Fusgs.tables%2Cusgs_tantalum%2Fusgs.tabs%2Cusgs_tantalum%2Fusgs.tantalum%2Cusgs_tantalum%2Fusgs.transcript%2Cusgs_tantalum%2Fusgs.truncate%2Cuswds_base%2Fframework%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module'
            url = 'https://www.usgs.gov/views/ajax?_wrapper_format=drupal_ajax'
            yield scrapy.Request(url=url, method='POST', dont_filter=True, cookies=cookies, headers=headers, body=body)

    def parse(self, response, **kwargs):
        Jdata = json.loads(response.text)
        resp = scrapy.Selector(text=Jdata[-1]['data'])
        for res in resp.css('.media--masonry.media--type--audio.media--view-mode--masonry'):
            episodename = res.css('img::attr(alt)').extract_first().replace('<', '').replace('>', '').replace(':', '') \
                .replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
            makedirectory(episodename)
            link = 'https://www.usgs.gov' + res.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=link, callback=self.parsedata, meta={'name': episodename})

    def parsedata(self, response):
        episodename = response.meta['name']
        audiolink = response.css('audio source::attr(src)').extract_first()
        audiodownload = wget.download(audiolink,cwd + '\\' + episodename + '\\' + episodename + '.mp3')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(usgspodcast)
process.start()
