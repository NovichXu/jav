#coding=utf-8
#尼玛原来是windows上执行的python编码默认是ascii的。。。

import urllib
import urllib2
import cookielib
import re
import os

#你懂的目录
av_path = 'E:\\av'

#arzon站url
arzon = 'https://www.arzon.jp/'

#模拟登录
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
login = 'https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=' + urllib.quote_plus(arzon)
urllib2.urlopen(login)

#递归遍历你懂的目录
def ll(rootPath):
	for lists in os.listdir(rootPath):
		path = os.path.join(rootPath, lists)
		if os.path.isdir(path): 
			ll(path)
		else:
			#判断文件大小
			if os.path.getsize(path) > 10000000:
				#正则取番号
				av = re.search(r'(%5b)?([a-zA-Z]{2,5})\-?([0-9]{2,5})(%5d)?', lists)
				if av:
					url = 'https://www.arzon.jp/itemlist.html?t=&m=all&s=&q=' + av.group(2) + av.group(3)
					response = urllib2.urlopen(url)
					html = response.read()
					#正则取图片
					ret = re.search(r'\/\/img.arzon.jp\/image\/([0-9])\/([0-9]*)\/([0-9]*)S\.jpg', html)

					if ret:
						#缩略图换大图
						pic = 'https:' + ret.group(0).replace('S', 'L')
						request = urllib2.Request(pic)
						request.add_header('Referer', arzon)
						content = opener.open(request)
						#生成jpg文件
						with open(av.group(2) + av.group(3) + '.jpg', mode='wb') as f:
							f.write(content.read())
					else:
						print lists

ll(av_path)