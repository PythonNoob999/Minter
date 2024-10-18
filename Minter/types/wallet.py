class Wallet:
    def __init__(
        self,
        address: str,
        private_key: str,
    ) -> None:
        '''an abstract Wallet class to store your wallet data
        attrs:
            address: wallet address
            private_key: wallet private key'''

        self.address = address
        self.private_key = private_key
    
    @property
    def json(self):
        return {
            "address": self.address,
            "private_key": self.private_key,
        }
    
    def __str__(self):
        return f'Wallet({self.address}, {self.private_key})'
    
    def __eq__(self, value: object) -> bool:
        return self.address == value if isinstance(value, str) else value.address