#coding=utf-8
#尼玛原来是windows上执行的python编码默认是ascii的。。。

import urllib
import urllib2
import cookielib
import re

javs = ['0908-mdyd945.avi', 'EZD311.avi', 'RBD-352.rmvb', 'ADN-009C.AVI', 'big-cup.tv-AVOP007.avi', '206.108.51.3-dep001.avi', '206.108.51.3-FSET520_C.avi', 'javset.com-SDMT-973.mp4', '206.108.51.3-MIST028_C.avi', 'SDDE295R.avi'];

arzon = 'https://www.arzon.jp/'

cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

login = 'https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=' + urllib.quote_plus(arzon)

urllib2.urlopen(login)

for jav in javs:
	av = re.search(r'(%5b)?([a-zA-Z]{2,5})\-?([0-9]{2,5})(%5d)?', jav)
	if av:
		url = 'https://www.arzon.jp/itemlist.html?t=&m=all&s=&q=' + av.group(2) + av.group(3)
		response = urllib2.urlopen(url)
		html = response.read()

		ret = re.search(r'\/\/img.arzon.jp\/image\/([0-9])\/([0-9]*)\/([0-9]*)S\.jpg', html)

		if ret:
			pic = 'https:' + ret.group(0).replace('S', 'L')
			request = urllib2.Request(pic)
			request.add_header('Referer', arzon)
			content = opener.open(request)

			with open(av.group(2) + av.group(3) + '.jpg', mode='wb') as f:
				f.write(content.read())
		else:
			print ret