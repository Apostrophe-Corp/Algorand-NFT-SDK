# py-algorand-nft-sdk

## Introduction

This SDK builds upon the py-algo-sdk NFT minting and updating capabilities, making it a lot easier for developers to create and update NFTs on testnet, betanet and mainnet
using the different ARC standards.

The developer simply needs to call the appropriate function to either mint or update an NFT, providing the necessary arguments including the metadata url in accordance with
the ARC standard they intend to use. 

### The ARC standards for NFTs include: 

- **ARC3**
  - <https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md>
  - NFT metadata focused standard.
  - The url field points to the NFT metadata. The metadata supports a schema which can have associated integrity and mimetype fields. 
  - Suitable for immutable NFTs with large metadata files (>1KB size of JSON) and multiple off-chain data references.

- **ARC19**
  - <https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md>
  - NFT metadata focused standard. 
  - Enforces off-chain IPFS metadata by using the url field as a template populated by the reserve address field which holds the IPFS CID. Easy to update since the reserve address value can be replaced with a single transaction, which in turn changes the metadata. The reserve address is only irrelevant (and thus can be used in this way) for pure NFTs (1 of 1).
  - Suitable for mutable NFTs intended to transition into immutable NFTs, with complete metadata (+mediafile) changes. 

- **ARC69**
  - <https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0069.md>
  - NFT mediafile focused standard. 
  - The url field points to the NFT digital asset file. The ASA metadata is stored on-chain and represented by the note field of the latest valid assetconfig transaction. Since the note field is limited to 1KB the metadata JSON is also restricted to this size. This design means fetching the metadata is complex and requires access to an archive node, but also allows metadata to be updated with a single transaction and simple access to the mediafile url.
  - Suitable for mutable NFTs where the mediafile is locked, easily accessed, but the compact metadata associated with it changes over time.

## Getting Started

### Prerequisites

At least Python 3.10

### Install

```sh
#create a virtual environment
python3 -m venv venv

#activate virtual environment
source venv/bin/activate

#update pip
pip install pip upgrade

#install py-algo-nft-sdk
pip install py-algo-nft-sdk

#install py-algo-sdk
pip install py-algorand-sdk

```

## Usage

To use the SDK in your python script you simply need to follow the steps below.

### Step 1

**Import SDK**

```{python}
'''
import the file coresponding to the network that you intend to connect to and alias it.
Testnet: nft_sdk_testnet
Betanet: nft_sdk_betanet
Mainnet: nft_sdk_mainnet
'''
from py_sdk import nft_sdk_testnet as nft_sdk
```

### Step 2

**Call the function to mint an NFT**

create_nft(name, symbol, media_url, reserve=False, freeze="", clawback="")

Descripton: This function mints a new NFT. 

Arguments:

Required :-
- name: This should be passed as a string and denotes the name of the NFT.
- symbol: This should be no more than 8 chararacters and passed as a string. It denotes symbol that would be associated with the NFT.
- media_url: This should be passed as a string and should be a URL pointing to a file where the NFT media such as an image is stored.

Optiopnal :-
- reserve: This argument should be set to true if the user wants the NFT to be mutable it should be ignored. It is of type boolean.
- freeze: This is an argument of type string. It denotes a wallet that can sign a transaction to freeze the asset. It usually does not apply to NFTs.
- clawback: This is an argument of type string. It denotes a wallet that can reclaim an asset.

Example:
In this example, we create an NFT that can be updated (ARC-19 standard), but with no clawback or freeze address.

```{python}
nft_sdk.create_nft("exampleNFT", "EX", "https://bit.ly/3WlA41Y#i", True)
```

### Step 3

The next step 
