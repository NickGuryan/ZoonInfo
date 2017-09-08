#!/usr/bin/env python3
#-*-coding:UTF-8-*-#
#import pandas
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import csv
#import pandas as pd
import requests
import os
import http.cookies
import random
import time
#from lxml import html
import cgitb
import cgi
cgitb.enable()

def setCookie():
    '''past = time.time()
    my_file = open("tmp/some.txt")
    my_string = my_file.read()
    #my_string = my_string.split('\n')
    print('<p style="display:none;">{}</p>'.format(my_string))
    #dicti = {}
    #for s in my_string:
        #dicti[s[:s.find(':')-1]] = float(s[s.find(':')+1:])
    #for i in dicti:
        #if(past-dicti[i]>299):
            #file = 'tmp/output-'+str(i)+'.csv'
            #os.remove(file)
            #dicti.pop(i)
    my_file.close()'''


    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    name = cookie.get("name")
    value = random.randint(1,1000000000000)
    if name is None:
        tstart = time.time()
        print("Set-cookie: id={0}; expires={1}".format(str(value), str(time.ctime(tstart+500))))
        #print("Content-type: text/html\n")
        #print("Cookies!!!")
        #with open('cook.txt', 'a') as txt:
            #txt.write('\n'+str(value))
        #my_file = open("tmp/some.txt", 'a')
        #my_file.write('\n'+str(value)+':'+str(tstart)+'\n')
        #my_file.close()
    return value



class LinkPad():
    def __init__(self, link='https://yandex.ru'):
        req = 'http://xml.linkpad.ru/?url=' + str(link)
        page = requests.get(req)
        self.content = page.content
        self.s1 = ''
        self.s2 = ''

    ###Расширить класс Rank&Rating от Ahrefs

    def getDIN(self):
        s1 = str(self.content).split('\\r\\n')
        #s1 = s1[7]
        #s1 = self.content[self.content.find('<din '):self.content.rfind('</din>')]
        #s1 = int(s1[s1.find('>') + 1:])
        self.s1 = str(s1[7])
        self.s1 = self.s1[self.s1.find('<din '):self.s1.rfind('</din>')]
        self.s1 = int(self.s1[self.s1.find('>') + 1:])
        return self.s1

    def getDOUT(self):
        #s2 = int(self.content[self.content.find('<dout>') + 6:self.content.find('</dout>')])
        s2 = str(self.content).split('\\r\\n')
        self.s2 = str(s2[9])
        self.s2 = int(self.s2[self.s2.find('<dout>') + 6:self.s2.find('</dout>')])
        return self.s2

    def ratio(self):
        #s_1 = self.s1[self.s1.find('<din '):self.s1.rfind('</din>')]
        #s_1 = int(s_1[s_1.find('>') + 1:])
        #s_2 = int(self.s2[self.s2.find('<dout>') + 6:self.s2.find('</dout>')])

        if (int(self.s2) != 0):
            return round(int(self.s1) / int(self.s2), 2)
        else:
            return int(self.s1)

'''
def auth():
    USERNAME = 'justp.stats@yandex.ru' # put correct username here
    PASSWORD = 'eLz6JDR2218I' # put correct password here
    
    session_requests = requests.session()
    login_url = "https://ahrefs.com/user/login"
    result = session_requests.get(login_url)

    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]
    #print(authenticity_token)
    
    formdata = {
        'email': USERNAME,
        'password': PASSWORD,
        '_token': authenticity_token
    }
    r = session_requests.post(
        login_url, 
        data = formdata, 
        headers = dict(referer=login_url)
    )
    print('<h1 style="display: none;">YEAH</h1>')
    return session_requests


def AH(session_requests, target):
    try:
        url = 'https://ahrefs.com/ahrefs-top?domain='+str(target)
        res = session_requests.get(
            url, 
            headers = dict(referer = url)
        )
        tree = html.fromstring(res.content)
        rank = tree.xpath("//li[@class=' highlight ']/div[@class='table ']/div[@class='td td-first text-xs-left']/text()")
        
        s = ''.join(rank)
        s = s.replace('\n','')
        s = s.replace('  ','')
        s = int(s.replace(',',''))
    
        return s
    except:
        return 'N/A'
    print('<h3 style="display:none;">good</h3>')
'''     

def ResultCSV(url, cook): #url,cookie
    #s_r = auth()
    
    #result_table = pd.DataFrame()
    #Rank = []
    #Rating = []
    DIN = []
    DOUT = []
    Ratio = []

    print('''<table>
        <tr>
            <th>URL</th>
            <th>LinkPadIn</th>
            <th>LinkPadOut</th>
            <th>In/Out</th>
        </tr>''')

    for i in url:
        #Rank.append(0)
        #Rank.append(AH(s_r, i))
        #Rating.append(0)
        LP = LinkPad(link=i)
        print('''<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td> </tr>'''.format(i,LP.getDIN(),LP.getDOUT(),LP.ratio()))
        DIN.append(LP.getDIN())
        DOUT.append(LP.getDOUT())
        Ratio.append(LP.ratio())
    #k = random.randint(1,10)

    print('</table>')

    name = '../tmp/output-'+ str(cook) +'.csv'
    with open(name, 'w') as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter   = ',',
                            quotechar='|',
                            quoting=csv.QUOTE_NONE,
                            escapechar='\\')
        #spamwriter.writerows(data)
        #spamwriter.writerow(['URL', 'Ahrefs rank', 'Domain Rank', 'LinkPadIn', 'LinkPadOut', 'In/Out'])
        spamwriter.writerow(['URL', 'LinkPadIn', 'LinkPadOut', 'In/Out'])
        for i in range(len(url)):
            spamwriter.writerow([str(url[i]),  str(DIN[i]), str(DOUT[i]), str(Ratio[i])])
    '''result_table['url'] = url
    result_table['Ahrefs rank'] = Rank
    result_table['Domain rank'] = Rating
    result_table['Linkpad In'] = DIN
    result_table['Linkpad Out'] = DOUT
    result_table['In/Out'] = Ratio
    print('<h3 style="display:none;">good_1</h3>')
    #result_table.to_csv('output-1.csv')'''
    #print('<h3 style="display:none;">good_2</h3>')
    #return k

form = cgi.FieldStorage()
text1 = form.getfirst('text')

url = text1.split('\r\n')

cook = setCookie()
print("Content-type: text/html\n")

print("""<!DOCTYPE HTML>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Обработка данных форм</title>
                <link href="https://fonts.googleapis.com/css?family=Merriweather" rel="stylesheet">
                <style>
                body{font-family: 'Merriweather', serif; color: white; background: #1abc9c;}
                #myDiv{height: 100%; width: 650px;margin: 150px auto;border-radius:5px;border:2px solid #ececec;padding:20px}
                /* Center the loader */
                table{margin: 0 auto; font-size:14px;padding-bottom:20px}
                td, th{text-align:center; padding:10px;}
                #loader {
                  position: absolute;
                  left: 50%;
                  top: 50%;
                  z-index: 1;
                  width: 150px;
                  height: 150px;
                  margin: -75px 0 0 -75px;
                  border: 16px solid #f3f3f3;
                  border-radius: 50%;
                  border-top: 16px solid #2c3e50;
                  width: 120px;
                  height: 120px;
                  -webkit-animation: spin 2s linear infinite;
                  animation: spin 2s linear infinite;
                }

                @-webkit-keyframes spin {
                  0% { -webkit-transform: rotate(0deg); }
                  100% { -webkit-transform: rotate(360deg); }
                }

                @keyframes spin {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }

                /* Add animation to "page content" */
                .animate-bottom {
                  position: relative;
                  -webkit-animation-name: animatebottom;
                  -webkit-animation-duration: 1s;
                  animation-name: animatebottom;
                  animation-duration: 1s
                }

                @-webkit-keyframes animatebottom {
                  from { bottom:-100px; opacity:0 }
                  to { bottom:0px; opacity:1 }
                }

                @keyframes animatebottom {
                  from{ bottom:-100px; opacity:0 }
                  to{ bottom:0; opacity:1 }
                }

                #myDiv {
                  display: none;
                  text-align: center;
                }

                button{padding: 15px; width: 40%; background: #1abc9c; color: white; border: 2px solid white; font-weight:bold;border-radius:100px;cursor:pointer}
                button:hover{background:white; color:#1abc9c; transition: all 0.25s ease-in-out}
                </style>
            </head>
            <body onload="myFunction()" style="margin:0;">""")

print('<div id="loader"></div>')
print('<div style="display:none;" id="myDiv" class="animate-bottom">')
print("<h1>Анализ выполнен</h1>")
#j = 1

'''for i in url:
    Rank.append(0)
    Rating.append(0)
    LP = LinkPad(link=i)
    DIN.append(LP.getDIN())
    DOUT.append(LP.getDOUT())
    Ratio.append(LP.ratio())
    #print("<p>Site {0} - {1}</p>".format(j, i))
    #j+=1
#for i in range(len(url)):
    #print("<p>Site {0} - {1}: {2}, {3}, {4}, {5}, {6};</p>".format(i+1, url[i],Rank[i],Rating[i],DIN[i],DOUT[i],Ratio[i]))
print('<h3>URL Count: {}</h3>'.format(len(url)))

with open('output.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['URL', 'Ahrefs rank', 'Domain Rank', 'LinkPadIn', 'LinkPadOut', 'In/Out'])
    for i in range(len(url)):
        spamwriter.writerow([str(url[i]), str(Rank[i]), str(Rating[i]), str(DIN[i]), str(DOUT[i]), str(Ratio[i])])'''

print('<h3>URL Count: {}</h3>'.format(len(url)))

ResultCSV(url, cook)

print('<form method="get" action="../tmp/output-{}.csv">'.format(str(cook)))
print('<button type="submit">Загрузить CSV</button>')
print('</div>')

print("""<script>
            var myVar;

            function myFunction() {
                myVar = setTimeout(showPage, 1000);
            }
            function showPage() {
              document.getElementById("loader").style.display = "none";
              document.getElementById("myDiv").style.display = "block";
            }
            </script>""")
print("""</body>
        </html>""")