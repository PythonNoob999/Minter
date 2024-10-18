from kvsqlite import Client
from typing import Literal, Union, List, Dict

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