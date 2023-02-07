const { generateAccount } = require("algosdk");
const algosdk = require("algosdk");
const crypto = require("crypto");
const fs = require("fs");
const { createInflate } = require("zlib");

const algodTestnetServer = "https://testnet-api.algonode.cloud";
const indexerTestnetServer = "https://testnet-idx.algonode.cloud"
const algodBetanetServer = "https://betanet-api.algonode.cloud";
const indexerBetanetServer = "https://betanet-idx.algonode.cloud"
const algodMainetServer = "https://mainnet-api.algonode.cloud";
const indexerMainnetServer = "https://mainnet-idx.algonode.cloud"
const algodPort = 443;
const indexerPort = 443;
const algodToken = "";
const indexerToken = ""

adminAddress = "W4BERQ52RZILAKXNJJ6X5FNY3ASIAK3OV6KWX7DRTLKHXE7HNNGCO5OVUA"
adminKey = "3d43u0uywHWdackLRDwgZA8cBqpb2FxUJECl36fhcvS3AkjDuo5QsCrtSn1+lbjYJIArbq+Va/xxmtR7k+drTA=="

const algodClient = new algosdk.Algodv2(algodToken, algodTestnetServer, algodPort)
const indexerClient = new algosdk.Indexer(indexerToken, indexerTestnetServer, indexerPort);

const createAccount = function () {
  try {
    const myaccount = algosdk.generateAccount();
    console.log("Account Address = " + myaccount.addr);
    let account_mnemonic = algosdk.secretKeyToMnemonic(myaccount.sk);
    console.log("Account Mnemonic = " + account_mnemonic);
    console.log("Account created. Please store Mnemonic and address");
    console.log("Add funds to account using the TestNet Dispenser: ");
    console.log(
      "https://dispenser.testnet.aws.algodev.network/?account=" + myaccount.addr
    );

    return myaccount;
  } catch (err) {
    console.log("err", err);
  }
};

// Function used to wait for a tx confirmation
const waitForConfirmation = async function (algodclient, txId) {
 let response = await algodclient.status().do();
 let lastround = response["last-round"];
 while (true) {
  const pendingInfo = await algodclient.pendingTransactionInformation(txId).do();
  if (pendingInfo["confirmed-round"] !== null && pendingInfo["confirmed-round"] > 0) {
   //Got the completed Transaction
   console.log("Transaction " + txId + " confirmed in round " + pendingInfo["confirmed-round"]);
   break;
  }
  lastround++;
  await algodclient.statusAfterBlock(lastround).do();
 }
};

// Function used to print asset holding for account and assetid
const printAssetHolding = async function (algodclient, account, assetid) {
 let accountInfo = await indexerClient.searchAccounts().assetID(assetIndex).do();

 for (idx = 0; idx < accountInfo['assets'].length; idx++) {
  let scrutinizedAsset = ['accounts'][idx][account];
  if (scrutinizedAsset['asset-id'] == assetid) {
   let myassetholding = JSON.stringify(scrutinizedAsset, undefined, 2);
   console.log("assetholdinginfo = " + myassetholding);
   break;
  }
 }
};


async function createNft (name, symbol, address, imageUrl, reserve, clawback, freeze) {

 
 // todo hash url and log it to the console

 if (address === undefined) {
  generateAccount();    
  } 

 const sp = await algodClient.getTransactionParams().do();

 // todo create if statement to check if reserve and if reserve, build metadata hash else empty string 
 const reserveHash = "";

 const txn = algosdk.makeAssetCreateTxnWithSuggestedParamsFromObject({
  // todo may change url p
  assetMetadataHash: imageUrl,
  assetName: name,
  assetURL: imageUrl,
  clawback: clawback ? clawback : "",
  decimals: 0,
  defaultFrozen: false,
  freeze: freeze ? freeze : "",
  from: adminAddress,
  manager: adminAddress,
  reserve: reserveHash,
  suggestedParams: sp,
  total: 1,
  unitName: symbol,
 });

 const rawSignedTxn = txn.signTxn(adminKey);

}