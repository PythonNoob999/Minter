from Minter import Minter, BasicStorage
import asyncio

async def main():
    storage = BasicStorage("my_wallets.db")
    await storage.export(
        output_file="output.json"
    )

asyncio.run(main())