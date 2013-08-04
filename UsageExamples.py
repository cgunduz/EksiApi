#!/usr/bin/python
# -*- coding: utf-8 -*-

from EksiApi import EksiApi
import json

api = EksiApi()

# GET_CHANNEL

gundem_channel = api.get_channel('gundem')

print gundem_channel 

# Output :

# [
#     {
#         "content":"3 a\u011fustos 2013 porto galatasaray ma\u00e7\u0131",
#         "popularity":"263",
#         "hyperlink":"/3-agustos-2013-porto-galatasaray-maci--3833077?a=popular"
#     },
#     {
#         "content":"i\u00e7ki i\u00e7tikleri i\u00e7in g\u00f6zalt\u0131na al\u0131nan amcalar",
#         "popularity":"245",
#         "hyperlink":"/icki-ictikleri-icin-gozaltina-alinan-amcalar--3956094"
#     },
# ...

print json.loads(gundem_channel)[0]['content']

# Output :

# 3 ağustos 2013 porto galatasaray maçı

# Known Channels
print api.get_channel('spor')
print api.get_channel('iliskiler')
print api.get_channel('siyaset')
print api.get_channel('tv')
print api.get_channel('anket')
print api.get_channel('meta')

# All similar outputs as gundem

# GET_ENTRY

tayyip_entry = api.get_entries_by_headline('tayyip', 1) 
print tayyip_entry

# Output : 

# [
#     {
#         "date":"10.05.2002 14:53",
#         "content":"arapca kelimesidir,iyi kalpli adama denir",
#         "author":"dr legend"
#     },
# ...

print json.loads(tayyip_entry)[0]['content']

# Output :

# arapca kelimesidir,iyi kalpli adama denir

## Have fun !