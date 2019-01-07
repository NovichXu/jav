#coding=utf-8
#尼玛原来是windows上执行的python编码默认是ascii的。。。

import urllib
import urllib2
import cookielib
import re
import os
import sys

av_path = 'E:\\av'

arzon = 'https://www.arzon.jp/'

cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

login = 'https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=' + urllib.quote_plus(arzon)

urllib2.urlopen(login)

def ll(rootPath):
	for lists in os.listdir(rootPath):
		path = os.path.join(rootPath, lists)
		if os.path.isdir(path): 
			ll(path)
		else:
			if os.path.getsize(path) > 10000000 and '.bt.td' not in path:
				av = re.search(r'(%5b)?([a-zA-Z]{2,5})\-?([0-9]{2,5})(%5d)?', lists)
				if av:
					url = 'https://www.arzon.jp/itemlist.html?t=&m=all&s=&q=' + av.group(2) + av.group(3)
					response = urllib2.urlopen(url)
					html = response.read()

					ret = re.search(r'\/\/img.arzon.jp\/image\/([0-9])\/([0-9]*)\/([0-9]*)S\.jpg', html)

					if ret:
						filepath = 'E:\\new\\' + av.group(2).upper() + '-' + av.group(3).upper()
						print filepath
						isExists = os.path.exists(filepath)

						if isExists:
							print path
							sys.exit()
						else:
							os.makedirs(filepath)

						pic_m = 'https:' + ret.group(0).replace('S', 'M')
						request = urllib2.Request(pic_m)
						request.add_header('Referer', arzon)
						content = opener.open(request)
						with open(filepath + '\\' + av.group(2).upper() + '-' + av.group(3).upper() + 'm.jpg', mode='wb') as f:
							f.write(content.read())
							
						pic_l = 'https:' + ret.group(0).replace('S', 'L')
						request = urllib2.Request(pic_l)
						request.add_header('Referer', arzon)
						try:
							content = opener.open(request)
							with open(filepath + '\\' + av.group(2).upper() + '-' + av.group(3).upper() + 'l.jpg', mode='wb') as f:
								f.write(content.read())
						except urllib2.HTTPError, e:
							print e.code

						os.renames(path, filepath + '\\' + lists)

#						open(filepath + '\\' + lists, "wb").write(open(path, "rb").read())

					else:
						print lists

ll(av_path)