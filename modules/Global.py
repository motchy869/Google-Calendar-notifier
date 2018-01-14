"""
グローバル変数
"""

import logging

#logging の設定
logger = logging.getLogger(__name__); logger.setLevel(logging.DEBUG)	#output DEBUG or higher level messages
fmt = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s: %(message)s')
log_sh = logging.StreamHandler();\
	log_sh.setLevel(logging.DEBUG);\
	log_sh.setFormatter(fmt)
#log_fh = logging.FileHandler('debug.log');\
#	log_fh.setLevel(logging.DEBUG);\
#	log_fh.setFormatter(fmt)
#log_efh = logging.FileHandler('error.log');\
#	log_efh.setLevel(logging.ERROR);\
#	log_efh.setFormatter(fmt)
logger.addHandler(log_sh)#; logger.addHandler(log_fh); logger.addHandler(log_efh)

APPLICATION_NAME = 'Google-Calendar-notifier'

def add_item_to_list(array, item):
	"""
	Add an item to a list.
	If there is an empty entry in the list, will place the item at there.
	Otherwise, append the item at the end of the list.
	"""
	assert isinstance(array, list)
	for i in array:
		if i is None:
			array[i] = item
			return
	list.append(item)
