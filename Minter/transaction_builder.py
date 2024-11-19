from web3 import AsyncWeb3, Account
from web3.types import TxReceipt
from web3.exceptions import TransactionNotFound
from web3.contract import AsyncContract
from web3.contract.async_contract import AsyncContractFunction
from Minter.types.wallet import Wallet
from Minter.types.abis.abi import ABI
from typing import Union, List
import asyncio, json

class TransactionBuilder:
    
    def __init__(
        self,
        w3: AsyncWeb3
    ) -> None:
        self.w3 = w3

    def get_contract(
        self,
        address: str,
        abi: ABI
    ) -> AsyncContract:
        return self.w3.eth.contract(
            self.w3.to_checksum_address(address),
            abi=abi.abi
        )

    @classmethod
    def sign_tx(
        cls,
        tx,
        wallet: Union[Wallet, str]
    ):
        return Account.sign_transaction(tx, wallet if isinstance(wallet, str) else wallet.private_key)
    
    async def get_tx(
        self,
        tx: str
    ):
        try:
            return await self.w3.eth.get_transaction_receipt(tx)
        except:
            return None
    
    async def execute(
        self,
        tx: dict,
        sign: bool = True,
        signer: Union[Wallet, str] = None,
        broadcast: bool = True,
        tries: int = 3,
    ):
        if sign and signer:
            signed = self.sign_tx(tx, signer)

            if broadcast:
                while tries != 0:
                    try:
                        tx = await self.broadcast(signed)
                        return tx.hex()
                    except:
                        tries -= 1
            return signed
    
    # shortcuts
    async def nonce(
        self,
        address: Union[Wallet, str]
    ):
        return await self.w3.eth.get_transaction_count(address if isinstance(address, str) else address.address)
    
    async def broadcast(
        self,
        tx
    ):
        return await self.w3.eth.send_raw_transaction(tx.raw_transaction)
    
    @property
    async def gas(
        self,
    ):
        return await self.w3.eth.gas_price
    
    @property
    async def _id(
        self,
    ):
        return await self.w3.eth.chain_id

    async def get_balance(
        self,
        wallet: Union[Wallet, str],
        human_readable: bool = False
    ):
        balance = await self.w3.eth.get_balance(wallet if isinstance(wallet, str) else wallet.address)
        
        if human_readable:
            balance = self.w3.from_wei(balance, "ether")
        return float(balance)
    
    async def send_eth(
        self,
        from_wallet: Wallet,
        to: Union[Wallet, str],
        amount: float,
        return_signed_tx: bool = False
    ):
        '''used to send ETH (or the main chain token e.g BSCMainToken=BNB) from "from_wallet" to "to"
        args:
            from_wallet: Minter.Wallet
            to: Union[Minter.Wallet, str]
            amount: float, the amount to be send in ETH*
            return_signed_tx: bool = False, weither to return the signed_tx or broadcast it and return tx_hash'''

        amount = self.w3.to_wei(amount, "ether")
        if isinstance(to, str):
            assert self.w3.is_address(to), "'to' argument must be a Minter.Wallet or a vaild evm address"
            to = Wallet(to, "")
        
        gas = await self.gas
        data = {
            "from": self.w3.to_checksum_address(from_wallet.address),
            "to": self.w3.to_checksum_address(to.address),
            "value": amount,
            "nonce": (await self.nonce(from_wallet)),
            "gas": 21000,
            "maxFeePerGas": gas,
            "maxPriorityFeePerGas": gas,
            "chainId": await self._id
        }
        return (await self.execute(
            tx=data,
            signer=from_wallet,
            broadcast=not return_signed_tx,
        ))
    
    async def execute_write_function(
        self,
        wallet: Wallet,
        contract_address: str,
        abi: ABI,
        value: int = 0,
        gas: int = 250000,
        args: dict = {},
        return_signed_tx: bool = False
    ):
        if not abi.function:
            raise ValueError(f"ABI {abi.name} doesn't have a function")
        abi = abi.copy()
        abi.set_wallet(wallet)

        contract = self.get_contract(contract_address, abi)
        args = abi.get_args(args)
        func: AsyncContractFunction = getattr(contract.functions, abi.function["name"])

        tx = await func(**args).build_transaction({
            "from": self.w3.to_checksum_address(wallet.address),
            "value": value,
            "gas": gas,
            "gasPrice": await self.gas,
            "nonce": await self.nonce(wallet)
        })
        result = await self.execute(
            tx,
            sign=True,
            signer=wallet,
            broadcast=not return_signed_tx
        )
        return result
    
    async def execute_read_function(
        self,
        contract_address: str,
        abi: ABI,
        wallet: Wallet = None,
        args: dict = {}
    ):
        if not abi.function:
            raise ValueError(f"ABI {abi.name} doesn't have a function")
        abi = abi.copy()
        abi.set_wallet(wallet=wallet)

        contract = self.get_contract(contract_address, abi)
        func: AsyncContractFunction = getattr(contract.functions, abi.function["name"])
        result = await func(**abi.get_args(args)).call()
        return result
    
    async def get_nft_max_supply(
        self,
        contract_address: str,
    ) -> int:
        try:
            supply = await self.execute_read_function(
                contract_address=self.w3.to_checksum_address(contract_address),
                abi=ABI(
                    "get_max_supply",
                    abi=json.load(open("Minter/data/nft_abi.json", "r")),
                    function_name="maxSupply"
                )
            )
        except:
            # yeah, ik this sucks :'(
            supply = 200_000

        return supply