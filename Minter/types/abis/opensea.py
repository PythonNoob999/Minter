from Minter.types.abis.abi import ABI
import json, pathlib

path = pathlib.Path(__file__).parent.parent.parent
OPENSEA_ABI = json.load(open(path/"data/opensea_abi.json", "r+"))

class OpenseaABI(ABI):
    def __init__(
        self,
        name,
        nft_address: str,
        quantity: int = 1,
    ):
        self.nft_address = nft_address
        super().__init__(
            name=name,
            abi=OPENSEA_ABI,
            function_name="mintPublic",
            default_args={
                "nftContract": nft_address,
                "feeRecipient": "0x0000a26b00c1F0DF003000390027140000fAa719",
                "minterIfNotPayer": "0x0000000000000000000000000000000000000000",
                "quantity": quantity
            }
        )