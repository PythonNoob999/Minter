from Minter import Minter, ABI
import asyncio

async def main():
    rpc = "your_rpc"
    minter = Minter(rpc)
    abi = ABI(
        "someTokenABI",
        abi={
            "inputs":[
                {
                    "internalType":"address",
                    "name":"owner",
                    "type":"address"
                }
            ],
            "name":"balanceOf",
            "outputs":[
                {
                    "internalType":"uint256",
                    "name":"",
                    "type":"uint256"
                }
            ],
            "stateMutability":"view",
            "type":"function"
        },
        function_name="balanceOf",
    )

    # connect
    await minter.connect()
    tokens = await minter.execute(
        tx_builder_method=minter.tx_builder.execute_read_function,
        contract_address="TOKEN/NFT_address",
        abi=abi,
        args={
            "owner": "0xMyWalletAddress"
        }
    )

    print(f"i have a total of {tokens} NFTs from NFT_Name")

asyncio.run(main())