import os
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
import json
from selenium import webdriver
import time


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class ucsusapodcast(scrapy.Spider):
    name = 'ucsusapodcast'

    def start_requests(self):
        headers = {
            "authority": "www.ucsusa.org",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://www.ucsusa.org",
            "referer": "https://www.ucsusa.org/resources/podcasts",
            "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        cookies = {
            "optimizelyEndUserId": "oeu1659350743997r0.49587507849187507",
            "_gcl_au": "1.1.544064639.1659350745",
            "_gid": "GA1.2.1913751117.1659350745",
            "_gat": "1",
            "_gat_UA-6648639-1": "1",
            "_fbp": "fb.1.1659350744855.1722942032",
            "__qca": "P0-351417515-1659350745461",
            "__ucsactionviewed": "1",
            "_ga": "GA1.2.1533024729.1659350745",
            "_ga_VB9DKE4V36": "GS1.1.1659350744.1.1.1659350776.0"
        }
        for i in range(1, 11):
            body = 'view_name=resource_indices&view_display_id=block_3&view_args=&view_path=%2Fnode%2F13225&view_base_path=resources%2Fall&view_dom_id=355752c9f289b7dc4f64eea005f0eb51d9fd1d559f22e115364d6229cf769fa5&pager_element=0&page=' + str(
                i) + '&_drupal_ajax=1&ajax_page_state%5Btheme%5D=ucstheme&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=classy%2Fbase%2Cclassy%2Fmessages%2Ccore%2Fnormalize%2Csystem%2Fbase%2Cucstheme%2Fglobals%2Cucstheme%2Fjs-header%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module'
            resp = json.loads(
                requests.post('https://www.ucsusa.org/views/ajax?_wrapper_format=drupal_ajax', headers=headers,
                              cookies=cookies, data=body).text)
            htmldata = resp[2]['data']
            response = scrapy.Selector(text=htmldata)

            for url in response.css('div.views-row h3 a::attr(href)').extract():
                yield scrapy.Request(url='https://www.ucsusa.org' + url, callback=self.parse)

    def parse(self, response):
        episodename = response.css('h1.page-title ::text').get().replace('<', '').replace('>', '').replace(':',
                                                                                                           '').replace(
            '"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        transcript = '\n'.join(response.css('div.clearfix.text-formatted.field.field--name-field-text')[-1].css(
            'p ::text').extract()).strip()
        makedirectory(episodename)

        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ff.writelines(transcript)
        ff.close()

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ffo.writelines(transcript)
        ffo.close()

        options = webdriver.ChromeOptions()
        preferences = {'download.default_directory': cwd + '\\' + episodename}
        options.add_experimental_option('prefs', preferences)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get(response.url)
        time.sleep(2)

        try:
            driver.find_element_by_css_selector('button.interrupter-close').click()
            time.sleep(1)
        except:
            pass
        driver.switch_to.frame(driver.find_element_by_css_selector('#main-content iframe'))
        time.sleep(2)
        try:
            driver.find_element_by_css_selector('a.sc-button.sc-button-download').click()
            time.sleep(200)
        except:
            pass

        driver.switch_to.default_content()
        driver.quit()


process = CrawlerProcess({

    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(ucsusapodcast)
process.start()
