#seting up virtual environment

echo "setting up a virtual environment"
python3 -m venv venv

source venv/bin/activate

#install py-algorand-sdk
echo "installing Python Algorand SDK"
pip3 install py-algorand-sdk

echo "SDK installed"
echo "check usage for testnet in example-testnet.py"
