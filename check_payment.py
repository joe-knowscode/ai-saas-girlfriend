import web3

saas_wallet_address = "0xfba9a270Ac51bAEf134fE4F9D2DbDd539B9fd261"

def check_payment(DB, tx_hash: str):
    # Connect to the Binance Smart Chain network
    # Ideally want this to be Ethereum
    bsc = web3.Web3(web3.HTTPProvider("https://bsc-dataseed1.binance.org"))

    # Get tx details
    tx = bsc.eth.get_transaction(tx_hash)
    from_address = tx["from"]
    user_address_existence = DB.find_one({"_id": from_address})
    if user_address_existence:
        return False # someone already paid with this wallet address

    to = tx["to"]
    value = tx["value"]

    return True # for testing purposes


    if to == saas_wallet_address and value > 0: # they have sent BNB to the wallet
        PAYMENTS.insert_one({"_id": from_address})
        return True
    return False

