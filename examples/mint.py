from Minter import (
    Minter,
    BasicStorage,
    OpenseaABI
)
import asyncio

async def main():
    rpc = "your_rpc"
    storage = BasicStorage("my_wallets.db")
    minter = Minter(rpc, storage=storage)

    # connect
    await minter.connect()

    # minting vars, for this example i will use OpenseaABI
    opensea_contract_base_chain = "0x00005ea00ac477b1030ce78506496e8c2de24bf5"
    my_nft_contract = "0xSomeAddress"
    abi = OpenseaABI(
        name="opensea",
        nft_address=my_nft_contract,
        quantity=3
    )
    wallets = await minter.storage.wallets()
    gas = 200_000 # amount of gas to be used (in wei)

    # minting
    time_to_mint = await minter.mint_bulk(
        nft_contract=my_nft_contract,
        abi=abi,
        # mint only using first 5 wallets
        wallets=wallets[:5],
        gas=gas
    )
    print(f"Finished minting nfts in {time_to_mint} seconds!")


asyncio.run(main())