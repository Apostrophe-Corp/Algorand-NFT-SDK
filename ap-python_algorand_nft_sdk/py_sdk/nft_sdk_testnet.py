import hashlib
import json
from promisio import wait_for
import asyncio
from algosdk.v2client import algod, indexer
from algosdk import transaction, account, mnemonic

algod_address_testnet = "https://testnet-api.algonode.cloud"
indexer_address_testnet = "https://testnet-idx.algonode.cloud"
algod_token = ""
indexer_token = ""
admin_address = "W4BERQ52RZILAKXNJJ6X5FNY3ASIAK3OV6KWX7DRTLKHXE7HNNGCO5OVUA"
admin_key = "3d43u0uywHWdackLRDwgZA8cBqpb2FxUJECl36fhcvS3AkjDuo5QsCrtSn1+lbjYJIArbq+Va/xxmtR7k+drTA=="

algod_client = algod.AlgodClient(algod_token, algod_address_testnet)
indexer_client = indexer.IndexerClient(indexer_token, indexer_address_testnet)

def verify_opt_in(address, asset_id):
  account_info = indexer_client.lookup_account_assets(address=address, asset_id=asset_id)
  
  if account_info.get("assets")[0].get("asset-id") == asset_id:
    return True
  else:
    return False

 
def claim_nft(address, asset_id):
  
  if (verify_opt_in(address=address, asset_id=asset_id)) == False:
    print("Asset with Id: {} has not yet been opted into by Wallet: {}. Please opt-in).format(asset_id, address)
    return False
   
  sp = algod_client.suggested_params()
 
  txn = transaction.AssetTransferTxn(
    sender=admin_address,
    sp=sp,
    receiver=address,
    amt=1,
    index=asset_id  
  )
 
  signed_txn = txn.sign(admin_key)

  txid = algod_client.send_transaction(signed_txn)
  print("Successfully sent transaction with txID: {}".format(txid))

  try:
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)

  except Exception as err:
    print(err)
    return False

  print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

  return txid

async def verify_opt_in_before_transfer(address, asset):
    await wait_for(verify_opt_in(address, asset), retries=100, delay=5)
    # call the function to transfer the asset
    claim_nft(address, asset)
 
def create_account():
  private_key, address = account.generate_account()
  print("Please store all account information safely. You can import the mnemonic in a Pera Algo wallet or a MyAlgo wallet")
  print("My address: {}".format(address))
  print("My private key: {}".format(private_key))
  print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
  print("Please fund the wallet from the algo faucet at https://bank.testnet.algorand.network/")
  return address

async def create_nft(name, symbol, metadata_url, address="", reserve="", freeze="", clawback=""):
  """
  returns the id of the created NFT
  """
  if address == "":
    address = create_account()

  metadata_hash = hashlib.new("sha256", metadata_url.encode())
  metadata_bytes = metadata_hash.digest()
  
  print("Your metadata hash: {}".format(metadata_hash.hexdigest()))

  # build unsigned transaction

  sp = algod_client.suggested_params()

  txn = transaction.AssetConfigTxn(
    sender=admin_address,
    sp=sp,
    total=1,
    decimals=0,
    default_frozen=False,
    unit_name=symbol,
    asset_name=name,
    manager=admin_address,
    strict_empty_address_check=False,
    reserve=reserve,
    freeze=freeze,
    clawback=clawback,
    url=metadata_url,
    metadata_hash=metadata_bytes 
  )

  # sign transaction
  signed_txn = txn.sign(admin_key)

  #submit transaction
  txid = algod_client.send_transaction(signed_txn)

  print("Successfully sent transaction with txID: {}".format(txid))

  # wait for confirmation 
  try:
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
  except Exception as err:
    print(err)
    return False

  print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

  print("Asset ID: {}".format(confirmed_txn["asset-index"]))

  print("Please opt-in to asset on your wallet by adding the Asset Id")

  await verify_opt_in_before_transfer(address, confirmed_txn["asset-index"])

  return confirmed_txn["asset-index"]
 
 
def update_nft(asset_id, reserve="", clawback="", freeze=""):
  sp = algod_client.suggested_params()
   
  txn = transaction.AssetConfigTxn(
    sender=admin_address,
    sp=sp,
    default_frozen=False,
    index=asset_id,
    manager=admin_address,
    reserve=reserve,
    freeze=freeze,
    clawback=clawback,    
  )
  
    # sign transaction
  signed_txn = txn.sign(admin_key)

  #submit transaction
  txid = algod_client.send_transaction(signed_txn)

  print("Successfully sent transaction with txID: {}".format(txid))

  # wait for confirmation 
  try:
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
  except Exception as err:
    print(err)
    return False

  print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

  print("Asset ID: {}".format(confirmed_txn["asset-index"]))

  return confirmed_txn["asset-index"]
 
 
 
 
