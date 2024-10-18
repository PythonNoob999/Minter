from kvsqlite import Client
from typing import Literal, Union, List, Dict, Callable
from Minter.types.wallet import Wallet
from Minter.types.abi import ABI
from Minter.types.nft_data import NFTData
import json

class BaseStorage:
    def __init__(
        self,
        db_name: str = "minter.db",
        table_name: str = "minter",
        *args,
        **kwargs
    ) -> None:
        self.db = Client(db_name, table_name, *args, **kwargs)

    async def build(self):
        keys = ["wallets", "abis", "nft_data"]

        for key in keys:
            if not await self.exists(key):
                await self.set(key, ( {} if key == "nft_data" else []))

    async def rm_rf(self, format_only: bool = True):
        keys = ["wallets", "abis", "nft_data"]

        for key in keys:
            await self.delete(key)        
        if format_only:
            await self.build()

    async def exists(
        self,
        key: Literal["wallets", "abis", "nft_data"]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis,nft_data not {key}"
        return await self.db.exists(key)
    
    async def get(
        self,
        key: Literal["wallets", "abis", "nft_data"]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis.,nft_data not {key}"
        return await self.db.get(key)
    
    async def set(
        self,
        key: Literal["wallets", "abis", "nft_data"],
        data: Union[List[Dict], Dict]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis,nft_data not {key}"
        assert isinstance(data, list) or isinstance(data, dict), "data must be dict or a list of dict's"
        return await self.db.set(key, data)
    
    async def delete(
        self,
        key: Literal["wallets", "abis", "nft_data"]
    ):
        assert key in ["wallets", "abis", "nft_data"], f"key must be one of wallets,abis,nft_data not {key}"
        return await self.db.delete(key)

class BasicStorage(BaseStorage):
    async def get_wallets(
        self,
        filter_by: callable = None
    ) -> Union[None, List[Wallet]]:
        '''returns a list of Minter.Wallet objects or an empty list
        "wallets": [
            {
                "address": "0x..",
                "private_key": "0x.."
            }
        ]'''
        wallets = [Wallet(**wallet) for wallet in (await self.get("wallets"))]

        if isinstance(filter_by, Callable):
            wallets = [wallet for wallet in wallets if filter_by(wallet)]
        
        return wallets
    
    async def get_abis(
        self,
    ):
        '''returns a list of Minter.ABI or an empty list
        "abis": [
            "name": "{abi_name}",
            "abi": {abi_json}
        ]'''
        return [ABI(**abi) for abi in (await self.get("abis"))]
    
    async def get_nft_data(
        self,
    ) -> NFTData:
        '''returns all of the nft_data in the db in Minter.types.NFTData object
        nft_data_object = {
            "{nft_contract}": {
                "{address}": [{tx}, {tx}, {tx}],
                ...
            }
        }'''
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
            wallets = [Wallet(*c) for c in data["wallets"]]
            abis = [ABI(*c) for c in data["abis"]]
            nft_data = NFTData(data["nft_data"])

        if wallets:
            stored_wallets = await self.get_wallets()
            stored_wallets = stored_wallets + wallets
            await self.set("wallets", [wallet.json for wallet in stored_wallets])
            data["wallets"] = len(stored_wallets)
        
        if abis:
            stored_abis = await self.get_abis()
            stored_abis = stored_abis + abis
            await self.set("abis", [abi.json for abi in abis])
            data["abis"] = len(stored_abis)

        if nft_data:
            current_data = await self.get_nft_data()
            current_data.combine(nft_data)
            await self.set("nft_data", current_data)
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