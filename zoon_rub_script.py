#!/usr/bin/env python3
# -*-coding:UTF8-*-#
# import pandas
import sys
from selenium import webdriver
import os
import random
import time
import requests
from lxml import html
import pandas as pd

def createProxy():
    '''headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get('http://www.freeproxylists.net/ru/?c=RU&pt=&pr=HTTP&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0', headers=headers)
    tree = html.fromstring(r.content)
    print(r)
    proxy = {}
    ip_list = tree.xpath('//table[@class="proxy__t"]/tbody/tr/td[1]/text()')
    port_list = tree.xpath('//table[@class="proxy__t"]/tbody/tr/td[2]/text()')
    type_list = tree.xpath('//table[@class="proxy__t"]/tbody/tr/td[5]/text()')
    for i in range(0, len(ip_list)):
        proxy[i+1] = type_list[i].lower()+';'+str(ip_list[i])+':'+str(port_list[i])
    '''
    proxy = {}
    data = pd.read_csv('hidemy_proxy.csv')
    ip_list = list(data.IP)
    port_list = list(data.Port)
    for i in range(0, len(ip_list)):
        proxy[i+1] = str(ip_list[i])+':'+str(port_list[i])
    print('Proxy:',len(proxy))
    return proxy


def webCrowl(url_id, proxy):
    rnd = random.randint(1, len(proxy)+1)
    proxies = ['--proxy=' + str(proxy[rnd]), '--proxy-type=http']
    time.sleep(3)
    browser = webdriver.PhantomJS(service_args=proxies)
    browser = webdriver.PhantomJS()# replace with .Firefox(), or with the browser of your choice
    browser.get('https://zoon.ru/msk/beauty/'+url_id)  # navigate to the page
    try:
        r = browser.find_element_by_xpath('//div[@class="service-description-block invisible-links"]/div').text
    except:
        r = '-'
    browser.close()
    return r

def ResultCSV(url, proxy, R):  # url,cookie
    roub_list = []
    N = 1
    tic = time.time()
    for u in url:
        if(N%10 == 0):
            tac=time.time()
            print(len(url)-N,':', tac-tic)
            tic=time.time()
        try:
            l = webCrowl(u, proxy)
        except:
            l = webCrowl(u, proxy)
        
        if(l != '-'):
            j = l.split('\n')
            for i in range(0, len(j), 2):
                j[i] += ':'
                j[i + 1] += ';'
            roub_list.append(' '.join(j))
        else:
            roub_list.append(l)
        print('success', N)
        N += 1




    name = 'output-zoon-roubricks-' + str(R) + '.csv'

    data = pd.DataFrame()
    data['ID'] = url
    data['Tags'] = roub_list
    
    data.to_csv(name, index=False, encoding='UTF-8')
    '''with open(name, 'wb') as csvfile:
        for i in url:
            csvfile.write(i.encode('cp1251'))
            csvfile.write(b'|')
            csvfile.write(roub_list[i].encode('cp1251'))
            csvfile.write(b'\n')'''

if __name__ == '__main__':
    '''f = open('input_id.txt')
    url = f.readlines()
    f.close()'''

    data = pd.read_csv('ZoonBeaty - all_salon - v1.csv')
    #data = data[data.premium == True].copy()
    proxy = createProxy()
    #ResultCSV(list(data.ID), proxy, 'Premiums')
    old = 558
    for batch in range(837, len(list(data.ID)), 279):
        try:
            ResultCSV(list(data[old:batch].ID), proxy, str(old)+'_'+str(batch))
            old = batch
            print(batch, 'OK', len(list(data.ID))-batch)
        except:
            print(batch, 'fail pack')
            old = batch
            continue
        time.sleep(3)
