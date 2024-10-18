from Minter.storage import BasicStorage
from Minter.types.wallet import Wallet
from Minter.types.abi import ABI
from Minter.transaction_builder import TransactionBuilder
from aiohttp import ClientSession
from web3 import AsyncWeb3, AsyncHTTPProvider
from typing import List, Union, Callable
import asyncio

class Minter:
    def __init__(
        self,
        rpc: str,
        storage: BasicStorage = None,
        semaphore_lock: int = 999999,
    ) -> None:
        self.w3 = AsyncWeb3(AsyncHTTPProvider(rpc))
        self.tx_builder = TransactionBuilder(w3=self.w3)
        self.storage = storage or BasicStorage()
        # for rate limiting purposes
        self.lock = asyncio.Semaphore(semaphore_lock)

    async def connect(self) -> None:
        await self.w3.provider.cache_async_session(ClientSession())
        await self.storage.build()
    
    async def execute(
        self,
        tx_builder_method: Callable,
        *method_args,
        **method_kwargs
    ):
        async with self.lock:
            return await tx_builder_method(
                *method_args,
                **method_kwargs
            )
        
    async def execute_many(
        self,
        tx_builder_method: Callable,
        wallets: List[Wallet] = None,
        bulk: bool = False,
        **method_kwargs
    ):
        if not wallets:
            wallets = await self.storage.wallets()

        _tasks = [
            asyncio.create_task(
                self.execute(tx_builder_method, wallet, **method_kwargs)
            ) for wallet in wallets
        ]
        result = []

        if bulk:
            result = await asyncio.gather(*_tasks)
        else:
            for task in _tasks:
                result.append(await task)
        
        return result
    
    # abstract methods
    async def get_balances(
        self,
        wallets: List[Wallet] = None,
        human_readable: bool = False,
        return_raw_data: bool = False
    ) -> Union[List[float], float]:
        if not wallets:
            wallets = await self.storage.wallets()
        
        result = await self.execute_many(
            tx_builder_method=self.tx_builder.get_balance,
            wallets=wallets,
            human_readable=human_readable
        )
        
        if return_raw_data:
            return result
        return sum(result)

    async def bulk_fees(
        self,
        fees_wallet: Wallet,
        amount: float,
        hold: int = 3,
        subtract: bool = False,
        wallets: List[Wallet] = None,
    ) -> float:
        '''this method is used to distribute fees from fees_wallet to wallets
        Args:
            fees_wallet: Wallet, the wallet that will provide fees
            amount: float, amount of fees every wallet will get IN ETH
            hold: int, sleeps between every fee transfer to keep up with the nonce
            subtract: bool=False,subtract the ETH on every wallet from the amount. aka (keep the wallet at the same amount)
            wallets: List[Wallet]=None, the wallets to distribute fees to, Minter.storage.get_wallets by default
        Returns:
            float, the total amount of ETH sent by the fees_wallet'''
        total = 0
        if not wallets:
            wallets = await self.storage.wallets()
        
        for wallet in wallets:
            n = amount
            fees_wallet_balance, wallet_balance = await self.get_balances([fees_wallet, wallet], True, True)

            if subtract:
                # e.g amount = 0.001, wallet_balance = 0.002, skips
                n = n - wallet_balance

                if n < 0:
                    continue
            
            if fees_wallet_balance <= n:
                break

            await self.execute(
                tx_builder_method=self.tx_builder.send_eth,
                from_wallet=fees_wallet,
                to=wallet,
                amount=n
            )
            await asyncio.sleep(hold)
            total += n
        return total