import os
import time

import requests
import scrapy
from selenium import webdriver

cwd = os.getcwd()


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


if __name__ == '__main__':
    for url in ['https://www.academyofdiplomacy.org/program/podcasts/general-ambassador-conversation/',
                'https://www.academyofdiplomacy.org/program/podcasts/american-diplomat-stories-behind-news/']:
        driver = webdriver.Chrome()
        driver.get(url)
        episodelinks = [v.get_attribute('src') for v in driver.find_elements_by_css_selector('iframe') if 'html5' in v.get_attribute('src')]
        driver.close()
        for link in episodelinks:
            ress = requests.get(link)
            response = scrapy.Selector(text=ress.text)
            try:
                episodename = response.css('.episode-title::text').extract_first().replace('/', '').replace(':', '').replace('?', '').replace('-', '').strip()
            except:
                pass
            makedirectory(episodename)
            options = webdriver.ChromeOptions()
            preferences = {'download.default_directory': cwd + '\\' + episodename}
            options.add_experimental_option('prefs', preferences)
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(link)
            downbtn = driver.find_element_by_id('download')
            downbtn.click()
            time.sleep(10)
            driver.close()
