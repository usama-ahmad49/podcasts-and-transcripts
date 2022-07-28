import os
import time

import requests
import wget
import scrapy
from selenium import webdriver
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

class aarppodcast(scrapy.Spider):
    name = 'aarppodcast'
    def start_requests(self):
        links = ['https://www.aarp.org/podcasts/the-perfect-scam/','https://www.aarp.org/podcasts/take-on-today/','https://www.aarp.org/podcasts/closing-the-savings-gap/']
        for link in links:
            yield scrapy.Request(link)
    def parse(self, response, **kwargs):
        episodelinks = response.css('h2 a::attr(href)').extract()
        episodename = response.css('h2 a::text').extract()
        for res in response.css('.accordionv2item.parbase ul li a::attr(href)').extract():
            episodelinks.append(res)
        for nam in response.css('.accordionv2item.parbase ul li a::text').extract():
            episodename.append(nam)

        for i, link in enumerate(episodelinks):
            try:
                en = episodename[i].replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
                makedirectory(en)
                options = webdriver.ChromeOptions()
                preferences = {'download.default_directory': cwd + '\\' + en}
                options.add_experimental_option('prefs', preferences)
                # options.add_argument('--headless')
                driver = webdriver.Chrome(options=options)
                driver.maximize_window()
                driver.get('https://www.aarp.org'+link)
                driver.find_elements_by_css_selector('.aarp-hpto-banner .expanded.collapser')[-1].click()
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_css_selector('#aarp-begin-content > div.aarpe-all-article-content > div.aarpe-main-content-wrap.container > div > div.col-lg-11.col-lg-offset-1.col-md-11.col-md-offset-1.col-sm-11.col-sm-offset-1.col-xs-12 > div.aarpe-article-two-col-content > div.col-lg-8.aarpe-article-left-content > div.everywhere-article-content.parsys > div:nth-child(1)'))
                ps = driver.page_source
                resp = scrapy.Selector(text=ps)
                transcript = '\n'.join(resp.css('.panel-body ::text').extract())
                ff = open(cwd + '\\' + en + '\\' + en + '_original.txt', 'w', encoding='utf-8')
                ff.writelines(transcript)
                ff.close()

                ffo = open(cwd + '\\' + en + '\\' + en + '.txt', 'w', encoding='utf-8')
                ffo.writelines(transcript)
                ffo.close()
                time.sleep(3)

                frame = driver.find_element_by_css_selector('.iFrameLink.section iframe')
                driver.switch_to.frame(frame)

                try:
                    # downloadbtn = driver.find_element_by_css_selector('#app > div > div.main.col.min-w-0.p-0 > div.row.no-gutters.pd-episode-name > div.col-auto.pb-actions.pr-2 > a:nth-child(2)')
                    downloadbtn = driver.find_element_by_css_selector('a#download-player')
                    downloadbtn.click()
                    time.sleep(20)
                except:
                    pass
                driver.close()
            except:
                pass




if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(aarppodcast)
    process.start()

    # res = requests.get('https://www.aarp.org/podcasts/')
    # resp = scrapy.Selector(text=res.content.decode('utf-8'))
    # links= []
    # for res in resp.css('li[role="menuitem"]'):
    #     link = 'https://www.aarp.org'+res.css('a::attr(href)').extract_first()
    #     links.append(link)
    #
    # for link in links:
    #     res = requests.get(link)
    #     resp = scrapy.Selector(text=res.content.decode('utf-8'))
    #     print('this')
    #
    #
    # print('this')