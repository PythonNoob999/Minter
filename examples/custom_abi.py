from Minter import ABI
import time

class MyCustomABI(ABI):
    def __init__(
        self, 
        name,
        amount: int = 1
    ):
        super().__init__(
            name=name,
            abi="CustomABI",
            function_name="mintNFT",
            default_args={
                "amount": amount,
                "timestamp": self.timestamp,
                "refferal": "0xSomeAddress",
            }
        )

    def timestamp(self) -> int:
        return time.time()

abi = MyCustomABI("test", amount=10)