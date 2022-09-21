import json
import os
import time

import PyPDF2
import requests
import scrapy
import wget
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

if __name__ == '__main__':
    res = requests.get('https://trainingindustry.com/training-industry-podcast/')
    resp = scrapy.Selector(text=res.content.decode('utf-8'))
    for i, epi in enumerate(resp.css('p strong::text').extract()):
        episodename = epi.replace('|', '').replace('/', '').replace(':', '').replace('?', '').replace('-', '').strip()
        link = [v for v in resp.css('p a') if 'Click to listen' in v.css('::text').extract_first()][i].css('::attr(href)').extract_first()
        makedirectory(episodename)
        options = webdriver.ChromeOptions()
        preferences = {'download.default_directory': cwd + '\\' + episodename}
        options.add_experimental_option('prefs', preferences)
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get(link)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_css_selector('div > div:nth-child(1) > p:nth-child(2)'))
        while True:
            try:
                driver.find_element_by_css_selector('.Campaign__canvas > div > button').click()
                break
            except:
                pass
        ps = driver.page_source
        res = scrapy.Selector(text=ps)
        transcript = '\n'.join(res.css('div:nth-child(1) > p ::text')[6:121].extract())

        ff = open(cwd + '\\' + episodename + '\\' + episodename + '_original.txt', 'w', encoding='utf-8')
        ff.writelines(transcript)
        ff.close()

        ffo = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        ffo.writelines(transcript)
        ffo.close()

        frame = driver.find_element_by_css_selector('iframe[data-name="pb-iframe-player"]')
        driver.switch_to.frame(frame)
        try:
            # downloadbtn = driver.find_element_by_css_selector('#app > div > div.main.col.min-w-0.p-0 > div.row.no-gutters.pd-episode-name > div.col-auto.pb-actions.pr-2 > a:nth-child(2)')
            downloadbtn = driver.find_element_by_css_selector('a[title="Download"]')
            downloadbtn.click()
            time.sleep(20)
        except:
            pass
        driver.close()

