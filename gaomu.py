#!/usr/bin/env python
# coding=utf-8

import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
import js2xml
import base64
import os,stat
import urllib.request

file_path="D:/其他/comic/123/"

list_url = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
	'Host': 'www.manhuafen.com'}

def download(image, count, fpath):

	if not os.path.exists(file_path+str(count)):
		os.mkdir(file_path+str(count))
		print("ok")
	else:
		print("no")
	for img in range(1, len(image)+1):
		#url = (fpath+image[img-1]).replace("\n", '')
		url = image[img-1].replace("\n", '')
		print(url)
		opener = urllib.request.build_opener()
		opener.addheaders = [headers]

		urllib.request.install_opener(opener)
		#urllib.request.urlretrieve(url, file_path+str(count)+"/"+str(img)+".jpg")


def decrypt(text):
	text = base64.b64decode(text)
	key = '123456781234567G'.encode('utf-8')
	iv = 'ABCDEF1G34123412'.encode('utf-8')
	mode = AES.MODE_CBC
	cryptos = AES.new(key, mode, iv)
	plain_text = cryptos.decrypt(text)
	#text_decrypted = cipher.decrypt(encodebytes)
	#plain_text = cryptos.decrypt(a2b_hex(text))
	#print(bytes.decode(plain_text).rstrip('\0'))
	print(plain_text)
	return (eval(plain_text.decode('utf-8').split("]")[0]+"]"))


def getlink(url):
	wb_data = requests.get(url, headers=headers)
	soup = BeautifulSoup(wb_data.text, 'lxml')
	each_url = soup.select('#chapter-list-1 > li > a')
	for each_link in each_url:
		href = each_link.get("href")
		list_url.append("https://www.manhuafen.com" + str(href))

def getpagelink(url):
	header = headers
	header.update({"Referer": url})
	wb_data = requests.get(url, headers=header)
	soup = BeautifulSoup(wb_data.text, 'lxml')
	each_url = soup.select('script')[2].string
	src_text = js2xml.parse(each_url, encoding='utf-8', debug=False)
	src_tree = js2xml.pretty_print(src_text)
	#print(src_tree)
	src_tree = BeautifulSoup(src_tree, 'lxml')
	print(str(src_tree.select("var")[0].text))
	image = decrypt(src_tree.select("var")[0].text)
	fpath = src_tree.select("var")[1].text
	#print(fpath)
	count = soup.select(".head_title > h2")[0].getText()
	print(count)
	#print(image, len(image))
	download(image, count, str(fpath))

if __name__ == '__main__':
	url = "https://www.manhuafen.com/comic/2265/"
	getlink(url)
	for page_url in list_url[:1]:
		getpagelink(page_url)
