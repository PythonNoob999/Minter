from Minter import BasicStorage, Wallet
import asyncio

async def main():
    storage = BasicStorage("my_wallets.db")
    # make sure to init your db if it has not been built before
    await storage.build()

    wallet_data = [
        {
            "address": "0xSomeAddress",
            "private_key": "SomePrivateKey"
        },
        ...
    ]

    await storage.insert_data(
        wallets=[
            Wallet(**wallet) for wallet in wallet_data
        ]
    )

asyncio.run(main())