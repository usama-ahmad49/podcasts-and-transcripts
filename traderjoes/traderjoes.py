import os
import wget
import requests
import html
from scrapy.selector import Selector
import PyPDF2


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
    resp = requests.get('https://insidetjs.libsynpro.com/rss')
    text = html.unescape(resp.text)
    response = Selector(text=text)

    for episode in response.css('item'):
        episodename = episode.css('title:nth-child(1)::text').get().replace('<', '').replace('>', '').replace(':',
                                                                                                              '').replace(
            '"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').strip()
        audiolink = episode.css('enclosure::attr(url)').get()
        transcript = episode.css('description p a::attr(href)').get()

        makedirectory(episodename)
        downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
        transcripdownload = wget.download(transcript, cwd + '\\' + episodename + '\\' + episodename + '_original.pdf')
        pdfFileObj = open(cwd + '\\' + episodename + '\\' + episodename + '_original.pdf', 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        totalPagespdf = pdfReader.getNumPages()
        ff = open(cwd + '\\' + episodename + '\\' + episodename + '.txt', 'w', encoding='utf-8')
        for i in range(0, totalPagespdf):
            pageObj = pdfReader.getPage(i)
            ff.writelines(pageObj.extractText())
        ff.close()


if __name__ == "__main__":
    main()
