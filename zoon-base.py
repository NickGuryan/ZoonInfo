#!/usr/bin/env python3
# -*-coding:UTF8-*-#
import pandas as pd
from lxml import html
import pandas as pd
import time
import base64
import random
import requests
from fake_useragent import UserAgent

def createProxy():
    '''proxy = {}
    data = pd.read_csv('hidemy_proxy_https.csv')
    ip_list = list(data.IP)
    #port_list = list(data.Port)
    #type_list = list(data.Type)
    for i in range(0, len(ip_list)):
        proxy[i+1] = str(ip_list[i])
    print('Proxy:',len(proxy))
    return proxy'''
    proxy = {}
    data = pd.read_csv('bin/hidemy_proxy_https.csv')
    ip_list = list(data.IP)
    #port_list = list(data.Port)
    for i in range(0, len(ip_list)):
        proxy[i+1] = str(ip_list[i])
    print('Proxy:',len(proxy))
    return proxy

def prePageV2(url, proxy):
    ua = UserAgent()
    rnd = random.randint(1, len(proxy)+1)
    proxies = {
      'http': proxy[rnd]
    }
    headers = {
        'User-Agent':str(ua.random)
    }
    time.sleep(3)
    page = requests.get(url, proxies=proxies, headers=headers)
    tree = html.fromstring(page.content)
    
    return tree

def not_premium(data):
    data = data.copy()
    metro = {}
    tel = {}
    rating = {}
    ratingCount = {}
    reviewCount = {}
    address = {}
    timing = {}
    desc = {}
    sites = {}
    
    proxy = createProxy()
    
    k = 1
    for ID in list(data.ID):
        try:
            page = prePageV2('https://zoon.ru/msk/beauty/'+str(ID), proxy)
        except:
            try:
                page = prePageV2('https://zoon.ru/msk/beauty/'+str(ID), proxy)
            except:
                try:
                    page = prePageV2('https://zoon.ru/msk/beauty/'+str(ID), proxy)
                except:
                    try:
                        page = prePageV2('https://zoon.ru/msk/beauty/'+str(ID), proxy)
                    except:
                        page = prePageV2('https://zoon.ru/msk/beauty/'+str(ID), proxy)
		
        
        try:
            metro[ID] = page.cssselect('div.map-text span a')[0].text_content()
        except:
            metro[ID] = '-'
            
        try:
            tel[ID] = page.cssselect('a.tel-phone.js-phone-number')[0].attrib.get('href')[5:]
        except:
            tel[ID] = '-'
            
        try:
            rating[ID] = page.xpath('//span[@itemprop="ratingValue"]/text()')[0]
        except:
            rating[ID] = 0
            
        try:
            reviewCount[ID] = page.xpath('//span[@itemprop="reviewCount"]/text()')[0]
        except:
            reviewCount[ID] = 0
        
        try:
            ratingCount[ID] = page.xpath('//span[@itemprop="ratingCount"]/text()')[0]
        except:
            ratingCount[ID] = 0
        
        try:
            address[ID] = page.cssselect('address.iblock')[0].text_content()
        except:
            address[ID] = '-'
        
        try:
            s = page.cssselect('dl.fluid.uit-cover dd.simple-text div')[0].text_content()
            timing[ID] = ' '.join(s.split(' ')[2:])
        except:
            timing[ID] = '-'
            
        try:
            s1 =  page.cssselect('dd.simple-text.js-desc.oh.word-break')[0].text_content()
            desc[ID] = s1.replace('...','').replace('показать еще','').replace('\t',' ').replace('\n',' ')
        except:
            desc[ID] = '-'
        
        try:
            sites[ID] = page.cssselect('div.service-website a')[0].text_content()
        except:
            sites[ID] = '-'
            
        #s2 = page.cssselect('div.service-description-block.invisible-links div.params-list')
        #s3 = s2[s2.find('data = "')+8:s2.find('";')]
        #print(s2)
        #print(s3)
        if(sites[ID] == '-') and (desc[ID] == '-') and (address[ID] == '-') and (tel[ID] == '-') and (metro[ID] == '-'):
            print('Not Succces ID:', ID, 'Access denied; Left:', len(list(data.ID))-k)
        else:
            print('Success ID:', ID, 'Left: ',len(list(data.ID))-k)
        k+=1
    
    data['metro'] = data.ID.apply(lambda x: metro[x]).astype(str)
    data['tel'] = data.ID.apply(lambda x: tel[x]).astype(str)
    data['rating'] = data.ID.apply(lambda x: rating[x]).astype(float)
    data['ratingCount'] = data.ID.apply(lambda x: ratingCount[x]).astype(int)
    data['reviewCount'] = data.ID.apply(lambda x: reviewCount[x]).astype(int)
    data['address'] = data.ID.apply(lambda x: address[x]).astype(str)
    data['timing'] = data.ID.apply(lambda x: timing[x]).astype(str)
    data['description'] = data.ID.apply(lambda x: desc[x]).astype(str)
    data['site'] = data.ID.apply(lambda x: sites[x]).astype(str)
    
    #data[''] = data.ID.apply(lambda x: )
    
    #one_photo - parsing from home_listings
    #price_list - separately parser - ?
    #roubrics:tags - trouble JS - parsing from home_listings - OK
    return data

if __name__ == '__main__':
    data = pd.read_csv('bin/ZoonBeaty - all_salon - v1.csv')
    '''data = data[:3].copy()
    log = not_premium(data)
    name = 'tmp/ZoonBeautyTags - test.csv'
    log.to_csv(name, index=False, encoding='utf-8')'''
    old = 8091
    for batch in range(8370, len(list(data.ID)), 279):
        try:
            tac = time.time()
            log = not_premium(data[old:batch])
            name = 'tmp/ZoonBeautyTags - ' +str(old)+'_'+str(batch)+'.csv'
            log.to_csv(name, index=False, encoding='utf-8')
            tic = time.time()
            old = batch
            print(batch, 'OK', len(list(data.ID))-batch, tic-tac)
        except:
            print(batch, 'fail pack')
            old = batch
            continue
        time.sleep(3)
