import requests
import json

from pyZcash.settings import *

class ZDaemon(object):

	id_count = 0

	def __init__(self, url=ZURL, user=RPCUSER, password=RPCPASSWORD, timeout=TIMEOUT):
		#TODO: check utf safety
		self.url = url
		self.user = user.encode('utf8')
		self.password = password.encode('utf8')
		self.timeout = timeout

	def _call(self,  method, *args):
		jsondata = json.dumps({	'version': '2',
				'method': method,
				'params': args,
				'id': self.id_count})

		r = requests.post(self.url, auth=(self.user,self.password), data=jsondata, timeout=self.timeout)

		self.id_count += 1
		resp = json.loads(r.text)

		#TODO: deal with errors better.
		error = resp['error']
		if error:
			print error

		return resp['result']

	#Block Info
	def getBlockHash(self, blockheight):
		return self._call('getblockhash', blockheight)

	def getBlockByHash(self, blockhash):
		return self._call('getblock', blockhash)

	def getBlockByHeight(self, blockheight):
		return self.getBlockByHash(self.getBlockHash(blockheight))

	#Network Info
	def getNetworkHeight(self):
		return self._call('getblockcount')

	def getNetworkDifficulty(self):
		return self._call('getdifficulty')

	def getVersion(self):
		info = self._call('getnetworkinfo')
		client = info['subversion']
		version = client.strip('/').split(':')[1]
		return version

	def getConnectionCount(self):
		return self._call('getconnectioncount')

	#Wallet Info (transparent)
	def getTotalBalance(self, account=""):
		if account:
			return self._call('getbalance', account)
		else:
			return self._call('getbalance')

	def getUnspentTxs(self, minconf=1):
		return self._call('listunspent', minconf)

	#Raw Txs
	def getTxInfo(self, txid):
		return self._call('gettransaction', txid)

	# taddr methods
	def getNewAddress(self, account=""):
		if account:
			return self._call('getnewaddress', account)
		else:
			return self._call('getnewaddress')

	def sendTransparent(self, taddress, amount):
		return self._call('sendtoaddress', taddress, amount)

	# zaddr methods
	def z_getnewaddress(self):
		return self._call('z_getnewaddress')

	def z_listaddresses(self):
		return self._call('z_listaddresses')

	def z_listreceivedbyaddress(self, zaddr):
		return self._call('z_listreceivedbyaddress', zaddr)
