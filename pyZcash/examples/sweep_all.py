import os.path
import sys
import time

from rpc.ZDaemon import *
from settings import *

#Sweeps all unspent transparent txs, cleaning them through a temporary zaddr.
def clean_and_collect_all(taddress=TEST_TADDR, fee=DEFAULT_FEE):
	zd = ZDaemon()

	print "Checking balance..."
	tx_unspents = zd.getUnspentTxs()
	if not len(tx_unspents):
		print "No spendable txs available - visit a faucet or mine!"
		exit()

	print "Generating temporary zaddress for tx..."
	# rewrite this
	zaddr = zd.z_getnewaddress()

	print "Generated zaddress: " + zaddr

	print "Gathering and transmitting unspent txs..."
	print "Please wait..."
	# rewrite this
	shielded_txs =  zd.sweepAllUnspentTxs(zaddress)

	print "Sending unspent txs to shieleded address..."
	print "This may take a few minutes..."

	# rewrite this
	while zd.receiveTx(zsecret, encnote1).get('exists') is not True:
		print zd.receiveTx(zsecret,encnote1)
		time.sleep(5)

	print "Sent! Check " + taddress + " shortly."


if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print "Usage: python sweep_all.py <transparent address>"
		print "Ex: python sweep_all.py tm9yooiTA5bTheUD6VgQg2ya8j49XDhrtNW"
		exit()

	taddr = sys.argv[1]
	if len(taddr) != len('tm9yooiTA5bTheUD6VgQg2ya8j49XDhrtNW'):
		print "That doesn't look like a transparent address.. Maybe you are trying to use a zaddress?"
		exit()

	print "Address looks good!"
	clean_and_collect_all(taddr)
