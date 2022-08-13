import os
import wget
import requests
import html
from scrapy.selector import Selector


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
    response = requests.get('https://crimebeat.libsyn.com/rss')
    text = html.unescape(response.text)
    sel = Selector(text=text)

    for j in sel.css('item'):
        episodename = j.css('title:nth-child(1)::text').get().replace('<', '').replace('>', '').replace(':',
                                                                                                        '').replace('"',
                                                                                                                    '').replace(
            '/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink = j.css('enclosure ::attr(url)').get()
        makedirectory(episodename)

        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')


if __name__ == "__main__":
    main()
