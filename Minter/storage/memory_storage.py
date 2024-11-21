from Minter.types import (
    Wallet,
    ABI,
)
from Minter.types.nft_data import NFTData
from typing import Literal, Union, List, Dict

class MemoryStorage:
    def __init__(self):
        self.db = {
            "wallets": [],
            "abis": [],
            "nft_data": NFTData({})
        }
    
    async def build(self) -> None:
        return
    
    def rm_rf(self) -> None:
        self.db["wallets"] = []
        self.db["abis"] = []
        self.db["nft_data"] = {}

    def exists(
        self,
        key: Literal["wallets", "abis", "nft_data"]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis,nft_data not {key}"
        return self.db.exists(key)
    
    def get(
        self,
        key: Literal["wallets", "abis", "nft_data"]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis.,nft_data not {key}"
        return self.db.get(key, None)
    
    def set(
        self,
        key: Literal["wallets", "abis", "nft_data"],
        data: Union[List[Dict], Dict]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis,nft_data not {key}"
        assert isinstance(data, list) or isinstance(data, dict), "data must be dict or a list of dict's"
        self.db[key] = data
    
    def delete(
        self,
        key: Literal["wallets", "abis", "nft_data"]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis,nft_data not {key}"
        return self.db.pop(key)
    
    def wallets(self) -> List[Wallet]:
        return self.db.get("wallets", [])
    
    def abis(self) -> List[ABI]:
        return self.db.get("abis", [])
    
    def nft_data(self) -> Union[NFTData, None]:
        return self.db.get("nft_data", None)
    
    def insert_data(
        self,
        wallets: List[Wallet] = None,
        abis: List[ABI] = None,
        nft_data: NFTData = None
    ):
        
        if wallets:
            new = self.wallets() + wallets
            self.set("wallets", new)

        if abis:
            new = self.abis() + abis
            self.set("abis", new)

        if nft_data:
            self.set("nft_data", NFTData)