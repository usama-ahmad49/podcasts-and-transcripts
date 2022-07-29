import os
import wget
import time
from selenium import webdriver
import PyPDF2
from selenium.webdriver.common.action_chains import ActionChains


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://icslawyer.com/podcasts/')
    time.sleep(2)
    transcript = [v.get_attribute('href') for v in driver.find_elements_by_css_selector('a') if
                  'Download Transcript' in v.text]
    episodes = []
    frames = driver.find_elements_by_xpath("//iframe[contains(@src,'/direction/backward')]")
    for frame in frames:
        driver.switch_to.default_content()
        driver.execute_script("arguments[0].scrollIntoView();", frame)
        driver.switch_to.frame(frame)
        try:
            episodename = driver.find_element_by_css_selector(
                "div.col-lg-12.col-xs-12.episode-title.nopadding").text.replace('<', '').replace('>', '').replace(':',
                                                                                                                  '').replace(
                '"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        except:
            pass
        episodes.append(episodename)
    driver.close()

    for i, episode in enumerate(episodes):
        options = webdriver.ChromeOptions()
        preferences = {'download.default_directory': cwd + '\\' + episode}
        options.add_experimental_option('prefs', preferences)
        driver1 = webdriver.Chrome(options=options)
        driver1.maximize_window()
        driver1.get("https://icslawyer.com/podcasts/")
        time.sleep(2)
        try:
            driver1.find_element_by_css_selector('a#cookie_action_close_header').click()
            time.sleep(0.05)
        except:
            pass
        makedirectory(episode)

        switch_frame = driver1.find_elements_by_xpath("//iframe[contains(@src,'/direction/backward')]")[i]
        driver1.switch_to.frame(switch_frame)
        actions = ActionChains(driver1)
        scroll_to_frame = driver1.find_element_by_css_selector('a#download-player')
        actions.move_to_element(scroll_to_frame).perform()
        time.sleep(2)

        driver1.find_element_by_css_selector('a#download-player').click()
        time.sleep(15)

        driver1.switch_to.default_content()

        transcripdownload = wget.download(transcript[i], cwd + '\\' + episode + '\\' + episode + '_original.pdf')
        pdfFileObj = open(cwd + '\\' + episode + '\\' + episode + '_original.pdf', 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        totalPagespdf = pdfReader.getNumPages()
        ff = open(cwd + '\\' + episode + '\\' + episode + '.txt', 'w', encoding='utf-8')
        for i in range(0, totalPagespdf):
            pageObj = pdfReader.getPage(i)
            ff.writelines(pageObj.extractText())
        ff.close()

        driver1.quit()


if __name__ == "__main__":
    main()
