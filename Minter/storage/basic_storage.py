from Minter.types.wallet import Wallet
from Minter.types.abis.abi import ABI
from Minter.types.nft_data import NFTData, ContractData
from Minter.storage.base_storage import BaseStorage
from typing import Union, List, Dict, Callable
import json

class BasicStorage(BaseStorage):
    async def wallets(
        self,
    ) -> Union[None, List[Wallet]]:
        '''returns a list of Minter.types.Wallet'''
        return [Wallet(**wallet) for wallet in (await self.get("wallets"))]
    
    async def abis(
        self,
    ):
        '''returns a list of Minter.types.ABI'''
        return [ABI(**abi) for abi in (await self.get("abis"))]
    
    async def nft_data(
        self,
    ) -> NFTData:
        '''returns all of the nft_data in the db in Minter.types.NFTData object'''
        return NFTData((await self.get("nft_data")))
    
    async def insert_data(
        self,
        data_file: str = None,
        wallets: List[Wallet] = None,
        abis: List[ABI] = None,
        nft_data: NFTData = None
    ) -> Dict:
        '''used to insert any new wallets,abis,nft_data or a json data file
        returns a dict with the updated numbers'''
        data = {
            "wallets": None,
            "abis": None,
            "nft_data": None
        }

        if data_file:
            data = json.load(open(data_file, "r+"))
            wallets = [Wallet(**c) for c in data["wallets"]]
            abis = [ABI(**c) for c in data["abis"]]
            nft_data = NFTData(data["nft_data"])

        if wallets:
            stored_wallets = await self.wallets()
            stored_wallets = stored_wallets + wallets
            await self.set("wallets", [wallet.json for wallet in stored_wallets])
            data["wallets"] = len(stored_wallets)
        
        if abis:
            stored_abis = await self.abis()
            stored_abis = stored_abis + abis
            await self.set("abis", [abi.json for abi in abis])
            data["abis"] = len(stored_abis)

        if nft_data:
            n = '0x7695Ad12A94B4BA7a3eB073638279250509fBEA7'
            current_data = await self.nft_data()
            current_data.combine(nft_data)
            await self.set("nft_data", current_data.raw_json)
            data["nft_data"] = current_data

        return data
    
    async def export(
        self,
        output_file = "minter_data.json"
    ):
        data = {
            "wallets": await self.get("wallets"),
            "abis": await self.get("abis"),
            "nft_data": await self.get("nft_data")
        }

        with open(output_file, "w+") as f:
            f.write(json.dumps(
                data, indent=4, ensure_ascii=False
            ))
            f.close()
        return output_file