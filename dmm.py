#coding=utf-8
#尼玛原来是windows上执行的python编码默认是ascii的。。。

import re
import sys
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#登录到ssh
client.connect('', '', username = '', password = '', timeout = 10)
stdin, stdout, stderr = client.exec_command('curl http://www.dmm.co.jp/search/=/searchstr=ezd311')

#<a href="http://www.dmm.co.jp/rental/-/detail/=/cid=118ezd311r/?i3_ref=search&i3_ord=1">

for std in stdout.readlines():
	#正则取cid
	detail = re.search(r'<a href="http:\/\/www.dmm.co.jp\/rental\/-\/detail\/=\/cid=(.*?)\/', std.decode("UTF-8"))
	if detail:
		cid = detail.group(1)

#http://pics.dmm.co.jp/mono/movie/118ezd311r/118ezd311rpl.jpg
		picin, picout, picerr = client.exec_command('curl http://pics.dmm.co.jp/mono/movie/'+cid+'/'+cid+'pl.jpg')
		content = '';
		for pic in picout.readlines():
			content+= pic
#生成jpg文件
with open(cid+'pl.jpg', mode='wb') as f:
	f.write(content)
client.close()