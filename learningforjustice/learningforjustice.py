import scrapy

from scrapy.crawler import CrawlerProcess
from selenium.webdriver.common.action_chains import ActionChains

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

class learningforjustice(scrapy.Spider):
    name = 'learningforjustice'

    def start_requests(self):
        yield scrapy.Request(url='https://www.learningforjustice.org/podcasts/teaching-hard-history')

    def parse(self, response, **kwargs):
        all_episodes =[]

        for k in response.css('h2 a'):
            item =dict()
            item['episodename'] = k.css(' ::text').get()
            item['pagelink'] = k.css(' ::attr(href)').get()
            all_episodes.append(item)

        for i in all_episodes:
            episode_name = i['episodename'].replace('<', '').replace('>', '').replace(':', '') \
        .replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
            makedirectory(episode_name)
            options = Options()
            preferences = {'download.default_directory': cwd + '\\' + episode_name}
            options.add_experimental_option('prefs', preferences)
            options.add_argument('--no-sandbox')
            # options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--headless')
            options.add_argument("--incognito")
            options.add_argument('--disable-blink-features=AutomationControlled')
            # options.add_experimental_option('useAutomationExtension', False)
            # options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_argument("disable-infobars")

            driver = webdriver.Chrome(options=options)
            driver.maximize_window()

            driver.get(f'https://www.learningforjustice.org{i["pagelink"]}')

            time.sleep(3)
            try:
                driver.find_element_by_css_selector('a.button.close').click()
            except:
                pass

            driver.switch_to.frame(driver.find_element_by_css_selector('div.page-content iframe'))

            element = driver.find_element_by_css_selector("div#download")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            time.sleep(1)

            driver.find_element_by_css_selector('div#download').click()

            driver.switch_to.parent_frame()

            transcript = driver.find_element_by_css_selector('div.page-content').text

            ff = open(cwd + '\\' + episode_name + '\\' + episode_name + '_original.txt', 'w', encoding='utf-8')
            ff.writelines(transcript)
            ff.close()

            ffo = open(cwd + '\\' + episode_name + '\\' + episode_name + '.txt', 'w', encoding='utf-8')
            ffo.writelines(transcript)
            ffo.close()


            time.sleep(20)
            driver.quit()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(learningforjustice)
process.start()

