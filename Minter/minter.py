from Minter.storage import BasicStorage, MemoryStorage
from Minter.types.wallet import Wallet
from Minter.types.abis.abi import ABI
from Minter.types.nft_data import NFTData
from Minter.transaction_builder import TransactionBuilder
from aiohttp import ClientSession
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.types import TxReceipt
from typing import List, Union, Callable, Any
from time import perf_counter
import asyncio, json, pathlib

path = pathlib.Path(__file__).parent
NFT_ABI: dict = json.load(open(path/"data/nft_abi.json"))

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
    ) -> List[Any]:
        if not wallets:

            if isinstance(self.storage, MemoryStorage):
                wallets = self.storage.wallets()
            else:
                wallets = await self.storage.wallets()

        _tasks = [
            asyncio.create_task(
                self.execute(tx_builder_method, wallet=wallet, **method_kwargs)
            ) for wallet in wallets
        ]
        result = []

        if bulk:
            result = await asyncio.gather(*_tasks)
        else:
            for task in _tasks:
                result.append(await task)
        
        return result
    
    def process_ids(
        self,
        receipt: TxReceipt,
        rng: int
    ) -> List[int]:
        ids = []

        for log in receipt.get("logs"):
            _ids = [
                self.w3.to_int(hexstr=topic.hex()) for topic in log.get("topics") if 0 < self.w3.to_int(hexstr=topic.hex()) <= rng
            ]
            ids += _ids

        return ids
    
    # raw methods
    async def _save_nft_data(
        self,
        nft_contract: str,
        data: List[Union[None, str]],
        task: bool,
        sleep: int = 5
    ):
        if task:
            return await asyncio.create_task(
                self._save_nft_data(
                    nft_contract=nft_contract,
                    data=data,
                    task=False,
                    sleep=sleep
                )
            )
        
        await asyncio.sleep(sleep)
        supply = await self.execute(
            tx_builder_method=self.tx_builder.get_nft_max_supply,
            contract_address=nft_contract
        )
        receipts: List[TxReceipt] =(await asyncio.gather(
            *[
                asyncio.create_task(self.execute(
                    tx_builder_method=self.tx_builder.get_tx,
                    tx=tx
                )) for tx in data if tx is not None
            ]
        ))
        receipts = [rec for rec in receipts if rec is not None]
        filtered_data = {nft_contract: {}}

        for receipt in receipts:
            receipt_owner = receipt.get("from")

            # success
            if receipt.get("status") == 1:
                nft_ids = self.process_ids(receipt, supply)
                filtered_data[nft_contract][receipt_owner] = nft_ids
            # ??
            elif receipt.get("status") is None:
                continue

            # failed tx
            else:
                continue
        
        # save ids
        if isinstance(self.storage, MemoryStorage):
            self.storage.insert_data(nft_data=NFTData(filtered_data))
        else:
            await self.storage.insert_data(nft_data=NFTData(filtered_data))
    
    # abstract methods
    async def get_balances(
        self,
        wallets: List[Wallet] = None,
        human_readable: bool = False,
        return_raw_data: bool = False,
    ) -> Union[List[float], float]:
        if not wallets:
            if isinstance(self.storage, MemoryStorage):
                wallets = self.storage.wallets()
            else:
                wallets = await self.storage.wallets()
        
        result = await self.execute_many(
            tx_builder_method=self.tx_builder.get_balance,
            bulk=True,
            wallets=wallets,
            human_readable=human_readable,
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
        gas: int = 21000,
        tries: int = 3
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
            if isinstance(self.storage, MemoryStorage):
                wallets = self.storage.wallets()
            else:
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
                amount=n,
                gas=gas,
                tries=tries
            )
            await asyncio.sleep(hold)
            total += n
        return total
    
    async def mint_bulk(
        self,
        nft_contract: str,
        abi: ABI,
        wallets: List[Wallet] = None,
        args: dict = {},
        price: float = 0,
        gas: int = 250000,
        return_signed_tx: bool = False,
        save_tx_data: bool = True,
        save_in_background: bool = False
    ) -> List[Union[int, asyncio.Task]]:
        start = perf_counter()
        value = self.w3.to_wei(price, "ether")
        result = await self.execute_many(
            tx_builder_method=self.tx_builder.execute_write_function,
            wallets=wallets,
            bulk=True,
            contract_address=nft_contract,
            value=value,
            abi=abi,
            args=args,
            gas=gas,
            return_signed_tx=return_signed_tx
        )
        end = perf_counter()

        if return_signed_tx:
            return result
        
        # saving data and shit
        if save_tx_data:
            # for custom platform mints
            if hasattr(abi, "nft_address"):
                nft_contract = abi.nft_address
            await self._save_nft_data(nft_contract, result, save_in_background)

        return int(end-start)
    
    async def get_nft_balances(
        self,
        nft_contract: str,
        wallets: List[Wallet] = None
    ):
        abi = NFT_ABI
        result = await self.execute_many(
            tx_builder_method=self.tx_builder.execute_read_function,
            wallets=wallets,
            bulk=True,
            contract_address=self.w3.to_checksum_address(nft_contract),
            abi=ABI(
                name="balanceOf",
                abi=abi,
                function_name="balanceOf",
                default_args={"owner": (lambda abi : getattr(abi, "wallet", Wallet(None, None)).address)}
            ),
        )
        
        return sum([r for r in result if isinstance(r, int)])
    
    async def send_nfts(
        self,
        nft_contract: str,
        to: Union[Wallet, str],
        sleep: int = 3,
        limit: int = float("inf"),
        wallets: List[Wallet] = None
    ):
        if isinstance(self.storage, MemoryStorage):
            nft_data = self.storage.nft_data()
        else:
            nft_data = await self.storage.nft_data()
        
        if not wallets:
            if isinstance(self.storage, MemoryStorage):
                wallets = self.storage.wallets()
            else:
                wallets = await self.storage.wallets()
        
        wallets = wallets
        result = []
        n = 0

        for wallet in wallets:
            token_ids = nft_data.get(nft_contract, wallet.address)

            if not token_ids:
                continue

            for _id in token_ids:
                if n >= limit:
                    break

                has_it = await self.execute(
                    tx_builder_method=self.tx_builder.execute_read_function,
                    contract_address=nft_contract,
                    abi=ABI(
                        "ownerOf",
                        abi=NFT_ABI,
                        function_name="ownerOf",
                        default_args={
                            "tokenId": _id
                        }
                    )
                )

                if not has_it:
                    continue

                tx = await self.execute(
                    tx_builder_method=self.tx_builder.execute_write_function,
                    wallet=wallet,
                    contract_address=nft_contract,
                    abi=ABI(
                        "safeTransferFrom",
                        abi=NFT_ABI,
                        function_name="safeTransferFrom",
                        default_args={
                            "from": wallet.address,
                            "to": (to if isinstance(to, str) else to.address),
                            "tokenId": _id
                        }
                    ),
                )

                if tx:
                    result.append(tx)
                    n += 1
                    await asyncio.sleep(sleep)
        return result