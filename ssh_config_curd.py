#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
~/.ssh/config配置文件操作
"""

import os
import sys
import json
import argparse
import pickle

path = '/Users/wenjie/.ssh/config'
bak_path = "/Users/wenjie/.ssh/config_bak"
config_db = '/Users/wenjie/.ssh/config_db'

DEFAULT_CONFIG = {
	"*": {
		"ControlPersist": "yes",
		"ControlMaster": "auto",
		"ControlPath": "~/.ssh/master-%r@%h:%p",
		"Compression": "yes",
		"IdentityFile": "~/.ssh/id_rsa",
		"IdentitiesOnly": "yes"
	}
} 

def init():
	"""
	初始化数据库
	"""
	if not os.path.exists(config_db):
		with open(config_db, 'w') as f:
			f.write(pickle.dumps(DEFAULT_CONFIG))


def usage():
	"""
	使用方法
	"""
	parser = argparse.ArgumentParser(description='~/.ssh/config curd')
	parser.add_argument('-a', '--Host', type=str)
	parser.add_argument('-H', '--HostName', type=str)
	parser.add_argument('-p', '--Port', type=int)
	parser.add_argument('-u', '--User', type=str)
	parser.add_argument('-A', '--action', type=str, help="add|del|update|get|default")
	parser.add_argument('-m', '--comment', type=str)
	args = parser.parse_args()
	data = args.__dict__
	if not args.action:
		parser.print_help()
		sys.exit()
	if not args.Port:
		args.Port = 22
	if not args.User:
		args.User = "develop"
	return data


def read():
	"""
	读取ssh配置文件
	"""
	with open(path, 'r') as f:
		return f.reads()


def write():
	"""
	写入ssh配置文件中
	"""
	cmd = "cp -f {0} {1}".format(path, bak_path)
	cmd_fp = os.popen(cmd)
	res = read_config_db()
	with open(path, 'w') as fw:
		content = format(res)
		print content
		fw.write(content)


def read_config_db():
	"""
	从库中读取存储数据
	"""
	init()
	with open(config_db, 'r') as f:
		return pickle.load(f)


def write_config_db(data):
	"""
	写数据到库中
	"""
	with open(config_db, 'w') as f:
		f.write(pickle.dumps(data))


def add_config(data):
	"""
	添加数据
	"""
	res = read_config_db()
	new_res = dict(res, **data)
	write_config_db(new_res)


def del_config(data):
	"""
	删除配置文件
	"""
	res = read_config_db()
	for k in data.keys():
		if k in res:
			del res[k]
	write_config_db(res)


def update_config(data):
	"""
	更新配置文件
	"""
	res = read_config_db()
	for k, v in data.items():
		if k in res:
			res[k] = v
	write_config_db(res)


def read_config():
	"""
	读取配置文件
	"""
	res = read_config_db()
	print json.dumps(res, indent=4)


def format(data):
	"""
	格式化字典
	"""
	content = ''
	for k, v in data.items():
		content += "Host " + k + "\r\n"
		for attr, attr_v in v.items():
			if attr == 'comment':
				attr = "#"
			content += " "*4 + attr + " " + str(attr_v) + "\r\n"
		content += "\r\n"
		content += "#"*45 + "\r\n"*2
	return content


def main():
	db = {}
	data = usage()
	action = data['action']
	alias = data['Host']
	del data['action']
	del data['Host']
	db[alias] = data
	if action == "add":
		add_config(db)
		write()
	elif action == "del":
		del_config(db)
		write()
	elif action == "update":
		update_config(db)
		write()
	elif action == "get":
		read_config()
	elif action == 'default':
		update_config(DEFAULT_CONFIG)
		write()


if __name__ == '__main__':
	main()

