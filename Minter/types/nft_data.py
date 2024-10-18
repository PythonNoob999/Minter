from dataclasses import dataclass
from typing import Dict, Union, List
import json

@dataclass
class ContractData:
    '''contract data
    
    Args:
        nft_contract: str, the nft contract address
        minters: Dict[str, str], the dict of address-to-txs that minted the nft'''
    nft_contract: str
    minters: Dict[str, List[str]]

    def get_minter(self, address: str) -> Union[None, List[str]]:
        return self.minters.get(address, None)
    
    def __add__(self, other_contract: "ContractData") -> "ContractData":
        res = ContractData(self.nft_contract, {})
        for address in other_contract.minters:
            if self.minters.get(address, None):
                res.minters[address] = self.minters[address] + other_contract.minters[address]
            else:
                res.minters[address] =  other_contract.minters[address]
        return res

    def __eq__(self, other_contract: Union[str, "ContractData"]) -> bool:
        if isinstance(other_contract, ContractData):
            return self.nft_contract.lower() == other_contract.nft_contract.lower()
        elif isinstance(other_contract, str):
            return self.nft_contract.lower() == other_contract.lower()
        return False

class NFTData:
    def __init__(
        self,
        json_data: dict,
    ):
        self.jd = json_data
        self.nfts = {
            nft_contract: ContractData(nft_contract, minters) for nft_contract,minters in json_data.items()
        }

    def get(
        self,
        nft_contract: str,
        address: str
    ) -> Union[None, List[str]]:
        nft_data = self.nfts.get(nft_contract, None)

        if not nft_data:
            raise ValueError(f"{nft_contract} does not exist in nft data")
        
        return nft_data.get_minter(address)
    
    def combine(
        self,
        data: Union[Dict, "NFTData"]
    ) -> None:
        if isinstance(data, dict):
            data = NFTData(data)

        for nft_contract in data.nfts:
            if self.nfts.get(nft_contract, None):
                cur = self.nfts[nft_contract]
                self.nfts[nft_contract] = cur + data.nfts[nft_contract]
            else:
                self.nfts[nft_contract] = data.nfts[nft_contract]
    
    @property
    def json(self):
        return json.dumps(self.jd, indent=4, ensure_ascii=False)