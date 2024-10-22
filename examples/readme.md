<!-- https://www.github.com/PythonNoob999/examples -->

## Getting started
**to start using the minter you need an RPC**
[get one here](https://www.alchemy.com/pricing)

### initilazing Minter
```python
from Minter import Minter, BasicStorage
import asyncio

async def main():
    rpc = "your_(alchemy or other provider)_rpc"
    # your database
    storage = BasicStorage("my_wallets.db")
    minter = Minter(rpc, storage=storage)

    # connect
    await minter.connect()

asyncio.run(main())
```

## Contents

### wallets

* [create wallets](https://www.github.com/PythonNoob999/examples/create_wallets.py)
* [import wallets](https://www.github.com/PythonNoob999/examples/import_wallets.py)

### ABIs

* [usage example](https://www.github.com/PythonNoob999/examples/abi.py)
* [custom abi](https://www.github.com/PythonNoob999/examples/custom_abi.py)

### storage

* [export data](https://www.github.com/PythonNoob999/examples/export.py)

### minting

* [minting](https://www.github.com/PythonNoob999/examples/mint.py)