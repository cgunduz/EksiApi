#!/usr/bin/python
# -*- coding: utf-8 -*-

import pycurl
import StringIO
from BeautifulSoup import BeautifulSoup
import json
import sys

class EksiApi :

	def __init__(self) :

		self.url = 'https://eksisozluk.com/'
		self.curl = pycurl.Curl()

		# !!!!!!!
		# DIRTY IDENTIFIERS HERE 

		self.gundem_header_class = 'topic-list partial'

		self.entry_link_identifier_1 = 'a'
		self.entry_link_identifier_2 = 'find'

		self.entry_container_ol_identifier = 'entry-list'

		# END OF IDENTIFIERS
		# !!!!!!!

	def get_channel(self, channel) :

		parsed_html = self.__get_sozluk_response(channel, None)
		headlines_list = parsed_html.find('ul', attrs={'class': self.gundem_header_class}).findAll('a')

		headline_list = []

		if headlines_list != None :

			for headline in headlines_list:

				clean_headline = BeautifulSoup(str(headline))

				# :(
				try :

					expected_length = -1 * (len(clean_headline.find('a').text) - clean_headline.find('a').text.index('&nbsp;'))
					content = headline.text[:expected_length]

				except ValueError :

					expected_length = 0
					content = headline.text

				if clean_headline.find('small') == None :

					popularity = 1

				else :

					popularity = clean_headline.find('small').text

				# :(
				try :

					hyperlink = clean_headline.find('a').attrs[1][1]

				except IndexError :

					hyperlink = clean_headline.find('a').attrs[0][1]

				instance = { 'content': content , 'popularity': popularity, 'hyperlink' : hyperlink}
				headline_list.append(instance)
		
		return json.dumps(headline_list, indent=4, separators=(',',':'))

	def get_entries_by_headline(self, headline, page_amount, today = False, sort_by_like = False) :

		path = self.__get_entry_hyperlink(headline) + '?'

		if (today) :
			
			path = path + 'a=today&'

		elif (sort_by_like) :

			path = path + 'a=nice&'

		entry_list = []

		for page in range(1,page_amount+1) :

			path = path + 'p=' + str(page)
			parsed_html = self.__get_sozluk_response(path, None) 
			enrty_list_10 = self.__get_entries_on_a_single_page(parsed_html)

			if enrty_list_10 != None :
			
				for entry in enrty_list_10 : 

					entry_list.append(entry)

		return json.dumps(entry_list, indent=4, separators=(',',':'))

	def __get_entries_on_a_single_page(self, parsed_html) :

		entries = []
		all_entry_blocks_on_the_page = parsed_html.find('ol', attrs={'id': self.entry_container_ol_identifier}).findAll('li')

		if all_entry_blocks_on_the_page == None :

			return None

		for entry_block in all_entry_blocks_on_the_page :

			author = entry_block.find('a', attrs={'rel': 'author'}).text
			date = entry_block.find('time').text
			content = entry_block.find('div', attrs={'class': 'content'}).text

			entry = { 'author': author , 'date': date, 'content' : content}
			entries.append(entry)

		return entries

	def __get_entry_hyperlink(self, headline) :

		path = '?q=' + headline
		parsed_html = self.__get_sozluk_response(path, None)
		return str(parsed_html.find('form', attrs={'data-filternameparameter': self.entry_link_identifier_1 , 'data-keywordsearchaction' : self.entry_link_identifier_2}).attrs[2][1])

	def test(self) :

		return self.get_entries_by_headline('gundem',1)

	def __get_sozluk_response(self, path, params) :

		self.curl.setopt(pycurl.URL, self.url + path)
		responseString = StringIO.StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, responseString.write)
		self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt(pycurl.MAXREDIRS, 5)
		self.curl.perform()
		return BeautifulSoup(responseString.getvalue())
