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
        self.function = None
        self.args = default_args

        for func in abi:
            if func["name"] == function_name:
                self.function = func
                break
    
    @property
    def json(self) -> Dict:
        return {
            "name": self.name,
            "abi": json.dumps(self.abi),
            "function": self.function,
            "args": self.args
        }