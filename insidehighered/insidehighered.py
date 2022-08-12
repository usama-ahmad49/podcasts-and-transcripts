import os
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
import wget
import json


def makedirectory(dirname):
    try:
        path = os.path.join(cwd, dirname)
        mode = 0o666
        os.mkdir(path, mode)
        print("Directory " + dirname + " Created ")
    except:
        print("Directory " + dirname + " already exists")


cwd = os.getcwd()


class insidepodcast(scrapy.Spider):
    name = 'insidepodcast'

    def start_requests(self):
        # url = 'https://www.insidehighered.com/views/ajax'
        headers = {
            "authority": "www.insidehighered.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://www.insidehighered.com",
            "referer": "https://www.insidehighered.com/audio/2021/06/22/ep-50-better-%E2%80%98transcript%E2%80%99-learners-and-employers",
            "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        cookies = {
            "_fbp": "fb.1.1658286352209.947638232",
            "pelcro.unique.id": "ZTMwbHg3c2Fyb3ZsNXQwdm4wYg==",
            "_cb": "Dk0j5UBs921-BC6iz4",
            "_gid": "GA1.2.1380395009.1660205921",
            "_ga": "GA1.2.1021846509.1658286350",
            "__atuvc": "3%7C29%2C0%7C30%2C0%7C31%2C1%7C32",
            "__atuvs": "62f4bb6043cc4e7a000",
            "_chartbeat2": ".1658286353183.1660205922538.0000000000000001.Cty_PQtIYu4BSILJYBgGcWFB9df9E.1",
            "_cb_svref": "null",
            "_ga_F07KT3P0SW": "GS1.1.1660205920.3.1.1660206065.0",
            "_chartbeat5": "622|2424|%2Faudio%2F2021%2F06%2F22%2Fep-50-better-%25E2%2580%2598transcript%25E2%2580%2599-learners-and-employers|https%3A%2F%2Fwww.insidehighered.com%2Faudio%2F2021%2F06%2F22%2Fep-50-better-%25E2%2580%2598transcript%25E2%2580%2599-learners-and-employers%3Fpage%3D1|CMR8glDt9eh-B27GBEaXIjV7w1I0||c|D90JneDSdKyUDTAoxVDINFdgDfmkAW|insidehighered.com|::374|2420|%2Faudio%2F2021%2F06%2F22%2Fep-50-better-%25E2%2580%2598transcript%25E2%2580%2599-learners-and-employers|https%3A%2F%2Fwww.insidehighered.com%2Faudio%2F2021%2F06%2F22%2Fep-50-better-%25E2%2580%2598transcript%25E2%2580%2599-learners-and-employers%3Fpage%3D2|BHFk75HMefSBOFZ777Kp9zd86bX||c|SMj0T1ip8iCCdGHWBKivBEC81kqv|insidehighered.com|"
        }
        for i in range(1, 6):
            body = f'page={i}&view_name=audio&view_display_id=block_17&view_args=365341&view_path=node%2F365341&view_base_path=advice%2Ffeed%2F%25&view_dom_id=aa170aff904c16267c659cb0822ac3ab&pager_element=0&ajax_html_ids%5B%5D=pelcro-sdk&ajax_html_ids%5B%5D=gpt-impl-0.29279315837924536&ajax_html_ids%5B%5D=_goober&ajax_html_ids%5B%5D=skip-link&ajax_html_ids%5B%5D=top-menu&ajax_html_ids%5B%5D=page-wrapper&ajax_html_ids%5B%5D=page&ajax_html_ids%5B%5D=header&ajax_html_ids%5B%5D=captureEmailNewsLetterEnrollemntLink&ajax_html_ids%5B%5D=morejump&ajax_html_ids%5B%5D=search-term&ajax_html_ids%5B%5D=search-option&ajax_html_ids%5B%5D=new-search-submit&ajax_html_ids%5B%5D=new-nav-logo&ajax_html_ids%5B%5D=navigation&ajax_html_ids%5B%5D=nice-menu-0&ajax_html_ids%5B%5D=secondmenu&ajax_html_ids%5B%5D=main-wrapper&ajax_html_ids%5B%5D=main&ajax_html_ids%5B%5D=content&ajax_html_ids%5B%5D=block-dfp-article_superleaderboard&ajax_html_ids%5B%5D=dfp-ad-article_superleaderboard-wrapper&ajax_html_ids%5B%5D=dfp-ad-article_superleaderboard&ajax_html_ids%5B%5D=google_ads_iframe_%2F309842%2Fsite172.tmus%2Farticle_superleader_0__container__&ajax_html_ids%5B%5D=main-content&ajax_html_ids%5B%5D=block-block-146&ajax_html_ids%5B%5D=block-system-main&ajax_html_ids%5B%5D=atstbx2&ajax_html_ids%5B%5D=at-fbb11572-c742-48d2-a6ed-fe840603eb4e&ajax_html_ids%5B%5D=at-svg-facebook-1&ajax_html_ids%5B%5D=at-svg-twitter-2&ajax_html_ids%5B%5D=at-svg-linkedin-3&ajax_html_ids%5B%5D=at-svg-link-4&ajax_html_ids%5B%5D=topics&ajax_html_ids%5B%5D=moreblogs&ajax_html_ids%5B%5D=dfp-ad-webinars-wrapper&ajax_html_ids%5B%5D=dfp-ad-webinars&ajax_html_ids%5B%5D=dfp-ad-article_sidebar_low-wrapper&ajax_html_ids%5B%5D=dfp-ad-article_sidebar_low&ajax_html_ids%5B%5D=backtotop&ajax_html_ids%5B%5D=footer-deep&ajax_html_ids%5B%5D=foot-container&ajax_html_ids%5B%5D=foot-search&ajax_html_ids%5B%5D=foot-term&ajax_html_ids%5B%5D=foot-option&ajax_html_ids%5B%5D=foot-submit&ajax_html_ids%5B%5D=captureEmailNewsLetterEnrollemntLink&ajax_html_ids%5B%5D=site-social-footer&ajax_html_ids%5B%5D=halt&ajax_html_ids%5B%5D=block-block-121&ajax_html_ids%5B%5D=block-block-131&ajax_html_ids%5B%5D=block-block-201&ajax_html_ids%5B%5D=&ajax_html_ids%5B%5D=&ajax_html_ids%5B%5D=&ajax_html_ids%5B%5D=&ajax_html_ids%5B%5D=stickfoot&ajax_html_ids%5B%5D=sticky-inner&ajax_html_ids%5B%5D=registration-header&ajax_html_ids%5B%5D=stickpopper&ajax_html_ids%5B%5D=btn-default&ajax_html_ids%5B%5D=page-message&ajax_html_ids%5B%5D=btn-register&ajax_html_ids%5B%5D=btn-login&ajax_html_ids%5B%5D=state-holder&ajax_html_ids%5B%5D=error-zone&ajax_html_ids%5B%5D=state-welcome&ajax_html_ids%5B%5D=state-login&ajax_html_ids%5B%5D=login&ajax_html_ids%5B%5D=btn-register&ajax_html_ids%5B%5D=btn-reset&ajax_html_ids%5B%5D=state-register&ajax_html_ids%5B%5D=register-form&ajax_html_ids%5B%5D=btn-login&ajax_html_ids%5B%5D=state-reset&ajax_html_ids%5B%5D=reset-password&ajax_html_ids%5B%5D=btn-register&ajax_html_ids%5B%5D=btn-login&ajax_html_ids%5B%5D=state-default&ajax_html_ids%5B%5D=btn-register&ajax_html_ids%5B%5D=btn-login&ajax_html_ids%5B%5D=_atssh&ajax_html_ids%5B%5D=_atssh140&ajax_html_ids%5B%5D=service-icons-0&ajax_html_ids%5B%5D=root&ajax_html_ids%5B%5D=pelcro-app&ajax_html_ids%5B%5D=&ajax_html_ids%5B%5D=&ajax_page_state%5Btheme%5D=ihecustom&ajax_page_state%5Btheme_token%5D=GYtXbyuTzgdAnRNNxv0fpef-J_kjjAcx3oXiEt7ZCZE&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.base.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.menus.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.messages.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.theme.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Faggregator%2Faggregator.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fdate%2Fdate_api%2Fdate.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fdate%2Fdate_popup%2Fthemes%2Fdatepicker.1.7.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fdate%2Fdate_repeat_field%2Fdate_repeat_field.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Ffield%2Ftheme%2Ffield.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fnode%2Fnode.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsearch%2Fsearch.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fuser%2Fuser.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fviews%2Fcss%2Fviews.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fckeditor%2Fcss%2Fckeditor.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fctools%2Fcss%2Fctools.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fpanels%2Fcss%2Fpanels.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fpanels%2Fplugins%2Flayouts%2Fflexible%2Fflexible.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fctools%2Fcss%2Fabc1d07d2267d7d2d90911a30e1dde4e.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fnice_menus%2Fcss%2Fnice_menus.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fnice_menus%2Fcss%2Fnice_menus_default.css%5D=1&ajax_page_state%5Bcss%5D%5Bhttps%3A%2F%2Ffonts.googleapis.com%2Fcss2%3Ffamily%3DOpen%2BSans%3Awght%40300%3B400%3B500%3B600%3B700%26family%3DRoboto%2BSlab%3Awght%40300%3B400%3B500%3B600%3B700%26family%3DRoboto%3Awght%40100%3B3%0A00%3B400%3B500%3B700%26family%3DUbuntu%3Awght%40300%3B400%3B500%3B700%26display%3Dswap%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fhtml-reset.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fwireframes.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Flayout-fixed.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fpage-backgrounds.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Ftabs.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fmessages.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fpages.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fblocks.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fnavigation.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fviews-styles.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fnodes.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fcomments.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fforms.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Ffields.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fcss%2Fprint.css%5D=1&ajax_page_state%5Bjs%5D%5B0%5D=1&ajax_page_state%5Bjs%5D%5B1%5D=1&ajax_page_state%5Bjs%5D%5B2%5D=1&ajax_page_state%5Bjs%5D%5B3%5D=1&ajax_page_state%5Bjs%5D%5B4%5D=1&ajax_page_state%5Bjs%5D%5B5%5D=1&ajax_page_state%5Bjs%5D%5Bhttps%3A%2F%2Fwww.insidehighered.com%2Fsites%2Fdefault%2Fserver_files%2Fgoogle_tag%2Fproduction%2Fgoogle_tag.script.js%5D=1&ajax_page_state%5Bjs%5D%5B%2F%2Fajax.googleapis.com%2Fajax%2Flibs%2Fjquery%2F1.8.3%2Fjquery.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery-extend-3.4.0.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery-html-prefilter-3.5.0-backport.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery.once.js%5D=1&ajax_page_state%5Bjs%5D%5Bhttps%3A%2F%2Fsecurepubads.g.doubleclick.net%2Ftag%2Fjs%2Fgpt.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fdrupal.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fblazy%2Fblazy.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fjquery_update%2Freplace%2Fui%2Fexternal%2Fjquery.cookie.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fjquery_update%2Freplace%2Fmisc%2Fjquery.form.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fnice_menus%2Fjs%2Fjquery.bgiframe.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fnice_menus%2Fjs%2Fjquery.hoverIntent.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fnice_menus%2Fjs%2Fsuperfish.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fnice_menus%2Fjs%2Fnice_menus.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fajax.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fjquery_update%2Fjs%2Fjquery_update.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fcustom_behaviors%2Fcustom_behaviors.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Flazy%2Flazy.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fimage_caption%2Fimage_caption.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fviews%2Fjs%2Fbase.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fprogress.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fviews%2Fjs%2Fajax_view.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fjs%2Fviewswork.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fjs%2Fgeneral.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fjs%2Flogin-flow.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fihecustom%2Fjs%2Fad-refresh.js%5D=1&ajax_page_state%5Bjquery_version%5D=1.8'

            resp = json.loads(
                requests.post(url='https://www.insidehighered.com/views/ajax', headers=headers, cookies=cookies,
                              data=body).text)

            htmldata = resp[2]['data']
            response = scrapy.Selector(text=htmldata)
            for url in response.css('div.views-field.views-field-title a::attr(href)').extract():
                yield scrapy.Request(url='https://www.insidehighered.com' + url, callback=self.next_parse)

    def next_parse(self, response):
        episodename = response.css('.pane-node-title a::text').get().replace('<', '').replace('>', '').replace(':',
                                                                                                               '').replace(
            '"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        makedirectory(episodename)

        iframeid = \
            response.css('iframe[data-name="pb-iframe-player"]::attr(data-src)').get().split('i=')[-1].split('-p')[0]
        resp = requests.get(
            f'https://www.podbean.com/player/{iframeid}-pb?scode=&pfauth=&referrer=https:%2F%2Fwww.insidehighered.com%2F&touchable=false')
        # text = html.unescape(resp.text)
        audio_resp = json.loads(resp.text)

        audiolink = audio_resp['episodes'][0]['downloadLink']
        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(insidepodcast)
process.start()
