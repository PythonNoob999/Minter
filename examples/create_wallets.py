from Minter import BasicStorage, generate_wallets
import asyncio

async def main():
    # init your storage
    storage = BasicStorage("my_wallets.db")
    await storage.build()

    print(f"my_wallets.db has {len((await storage.wallets()))}")

    # create wallets
    wallets = generate_wallets(10)

    # save wallets to db
    await storage.insert_data(
        wallets=wallets
    )

    print(f"my_wallets.db has {len((await storage.wallets()))}")

asyncio.run(main())