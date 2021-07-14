# coding=utf-8
from prettytable import PrettyTable
import grequests
import requests
import json
import os
import re
from apscheduler.schedulers.blocking import BlockingScheduler
class Fund(object):

	fund_code_map = {};
	base_url = "http://fundgz.1234567.com.cn/js/"
	
	# 读取text基金编号和对应资金
	def read_fund_code(self):
		f = open("fundCode.txt","r")
		fund_map = json.load(f)
		self.fund_code_map = fund_map
		f.close()

	def request_fund_data(self):
		x = PrettyTable(["code", "name", "估算净值","盈利"])
		x.align["code"] = "|"
		x.padding_width = 0 
		req_list = []
		for code in self.fund_code_map.keys():
			request_url = self.base_url + code + ".js"
			req_list.append(grequests.get(request_url))
		res_list = grequests.map(req_list)
		print("start")
		for res in res_list:
			list = re.findall(r'[(](.*?)[)]', res.text)
			code = json.loads(list[0])['fundcode']
			name = json.loads(list[0])['name']
			gszzl = float(json.loads(list[0])['gszzl'])
			yl = gszzl*float(self.fund_code_map[code])/100.00
			x.add_row([code,name,gszzl,float('%.2f' % yl)])	
		os.system('clear')
		print(x)

	def start(self):
		self.read_fund_code()
		scheduler = BlockingScheduler()
		scheduler.add_job(self.request_fund_data, 'interval', seconds=3)
		scheduler.start()
			

if __name__ == '__main__':
	fund = Fund()
	fund.start()





