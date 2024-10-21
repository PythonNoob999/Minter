from web3 import Account
from Minter.types.wallet import Wallet
from typing import List

def generate_wallets(n: int) -> List[Wallet]:
    res = []

    for _ in range(n):
        account = Account.create()
        res.append(Wallet(
            address=account.address,
            private_key=account._private_key.hex()
        ))
    
    return res