import base64
import json
from algosdk.v2client import algod
from algosdk import transaction, account, mnemonic
from config import algod_token, algod_address, admin_address, admin_key

client = algod.AlgodClient(algod_token, algod_address)

def create_nft(name, symbol, metadata_url, manager="", reserve="", freeze="", clawback=""):
 """
 returns the id of the created NFT
 """
 
 metadata_bytes = json.dumps(metadata_url).encode()
 metadata_base_64 = base64.b64encode(metadata_bytes).decode()
 
 # build unsigned transaction
 
 current_round = client.status.get("lastRound")
 sp = client.suggested_params(current_round, "").get("lastRound")
 
 txn = transaction.AssetConfigTxn(
		sender=admin_address,
  sp=sp,
  total=1,
  decimals=0,
  default_frozen=False,
  unit_name=symbol,
  asset_name=name,
  manager=manager,
  strict_empty_address_check=False,
  reserve=reserve,
  freeze=freeze,
  clawback=clawback,
  url=url,
  metadata_hash=metadata_bytes  
	)
 
 # sign transaction
 signed_txn = txn.sign(admin_key)
 
 #submit transaction
 txid = client.send_transaction(signed_txn)
 
 print("Successfully sent transaction with txID: {}".format(txid))

	# wait for confirmation 
	try:
					confirmed_txn = transaction.wait_for_confirmation(client, txid, 4)  
	except Exception as err:
					print(err)
					return

	print("Transaction information: {}".format(
					json.dumps(confirmed_txn, indent=4)))
 
 print("Asset ID: {}".format(confirmed_txn["asset-index"]))

	# write the asset index to an environment file
	f = open('asset.index', 'w+')
	f.write(f'{confirmed_txn["asset-index"]}')
	f.close()
 
def claim_nft(address, asset_id):
 sp = client.suggested_params()
 
 txn = transaction.AssetTransferTxn(
		sender=admin_address,
  sp=sp,
  receiver=address,
  amt=1,
  index=asset_id  
	)
 
 signed_txn = txn.sign(admin_key)
 
 txid = client.send_transaction(signed_txn)
 print("Successfully sent transaction with txID: {}".format(txid))
 
 try:
  confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
  
 except Exception as err:
  print(err)
  return
 
 print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
 
def create_account():
 private_key, address = account.generate_account()
	print("My address: {}".format(address))
	print("My private key: {}".format(private_key))
	print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
 
def update_nft(asset_id, manager, reserve, freeze, clawback):
 current_round = client.status.get("lastRound")
 sp = client.suggested_params(current_round, "").get("lastRound")
 
 txn = transaction.AssetConfigTxn(
		sender=admin_address,
  sp=sp,
  default_frozen=False,
  index=asset_id,
  manager=manager,
  strict_empty_address_check=False,
  reserve=reserve,
  freeze=freeze,
  clawback=clawback,  
	)
 
 
 
 
