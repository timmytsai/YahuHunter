# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import  codecs

PAGE_NUM_START = 3
PAGE_NUM_END = 8

	
for page in range(PAGE_NUM_START, PAGE_NUM_END + 1):
	# get links
	r = requests.get('https://tw.mall.yahoo.com/recent_store?searchby=sname&&apg=' + str(page))
	if r.status_code == requests.codes.ok:
		soup = BeautifulSoup(r.text, 'html.parser')
		divs = soup.find_all('div', 'block first')
		stores = []
		for d in divs:
			link = d.find('a')
			stores.append(link.get('href'))

		divs = soup.find_all('div', 'block')
		for d in divs:
			link = d.find('a')
			stores.append(link.get('href'))

	print stores
	print len(stores)

	# get company info
	for link in stores:
		r = requests.get(link + '/stIntroMgt')
		if r.status_code == requests.codes.ok:
			soup = BeautifulSoup(r.text, 'html.parser')
			divs = soup.find_all('div', id='ypsinfo')
			for d in divs:
				infos = d.find_all('li')

			customer_info = []
			for info in infos:
				customer_info.append(info.get_text('li').encode('utf-8').split('：')[1])

		print link
		for i in customer_info:
			print i

		print "-------------------"

		with open('output.csv', 'ab') as csvfile:
			csvfile.write(codecs.BOM_UTF8)
			writer = csv.writer(csvfile)
			writer.writerow([customer_info[0], customer_info[1], customer_info[2], customer_info[4]])