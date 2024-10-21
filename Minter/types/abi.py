from Minter.types.wallet import Wallet
from typing import Union, Dict, Any
import json

class ABI:
    def __init__(
        self,
        name: str,
        abi: Union[Dict, str],
        function_name: str,
        default_args: Dict[str, Any]
    ) -> None:
        if isinstance(abi, str):
            abi = json.loads(abi)

        self.name = name
        self.abi = abi
        self.function: Dict = None
        self.args = default_args

        for func in abi:
            if func.get("name", None) == function_name and func.get("type", None) == "function":
                self.function = func
                break
    
    def get_args(
        self,
        data: Dict
    ):
        '''used to get ABI.func args
        
        Args:
            data: dict, any data to overwrite default args'''
        default = self.args
        args = {}

        for arg in default.keys():
            if arg in data.keys():
                target = data[arg]
            else:
                target = default[arg]

            if callable(target):
                target = target()

            args[arg] = target

        return args

    def __str__(self):
        return json.dumps(self.json, indent=4, ensure_ascii=False)
    
    @property
    def json(self) -> Dict:
        return {
            "name": self.name,
            "abi": json.dumps(self.abi),
            "function": self.function,
            "args": self.args
        }