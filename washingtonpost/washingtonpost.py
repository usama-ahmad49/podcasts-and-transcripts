import os
import time

import PyPDF2
import wget
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from selenium import webdriver
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

if __name__ == '__main__':
    i=1
    while True:
        url = f'https://audio-api.washpost.arcpublishing.com/api/v1/audio/findBySeries/5bda0d64e4b02752889d6aaf?page={i}&size=20&sort=false'
        res = requests.get(url)
        Jdata = json.loads(res.text)
        if Jdata == []:
            break
        for data in Jdata:
            episodename = data['title'].replace('|', '').replace('/', '').replace(':', '').replace('?', '').replace('-', '').strip()
            makedirectory(episodename)
            audiolink = data['audio']['url']
            try:
                transcriptlink = data['files'][0]['transcript']['vitac']['textUrl']
            except:
                pass

            try:
                downloadaudio = wget.download(audiolink, cwd + '\\' + episodename + '\\' + episodename + '.mp3')
            except:
                pass
            try:
                downloadtranscript = wget.download(transcriptlink, cwd + '\\' + episodename + '\\' + episodename + '_original.txt')
            except:
                pass

            try:
                downloadtranscript = wget.download(transcriptlink, cwd + '\\' + episodename + '\\' + episodename + '.txt')
            except:
                pass

        i+=1


