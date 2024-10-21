<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/PythonNoob999/Minter">
    <img src="images/nft.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Minter</h3>

  <p align="center">
    A tool to mint NFTs
    <br />
    <a href="https://github.com/PythonNoob999/Minter"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/PythonNoob999/Minter/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/PythonNoob999/Minter/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Minter is a python tool/lib to let you mint NFTs (mint = minting nfts from a nft collection, not creating nfts)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Web3.py](https://github.com/ethereum/web3.py)
* [kvsqlite](https://github.com/AYMENJD/Kvsqlite)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

this is how you can get started using Minter

### Prerequisites

* python
* web3
* kvsqlite

### Installation

Here are the instalation steps

1. Clone the repo
   ```sh
   git clone https://github.com/PythonNoob999/Minter.git
   ```
2. Build lib
   ```sh
   pip install . -U
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

here are some using examples


### initilazing your Minter
```python
from Minter import Minter
import asyncio

async def main():
    # the RPC for your wanted evm chain
    BASE_RPC = "https://mainnet.base.org"
    # semaphore for rate limitng, e.g semaphore=30 means max requests can be handeld per time is 30
    minter = Minter(BASE_RPC, semaphore=30)
    await minter.connect()

asyncio.run(main())
```

### Creating Wallets
```python
from Minter import Minter, generate_wallets
import asyncio

async def main():
    minter = Minter(BASE_RPC, semaphore=30)
    await minter.connect()
    # generate 10 new wallets
    wallets = generate_wallets(10)
    # save them
    await minter.storage.insert_data(wallets=wallets)

asyncio.run(main())
```

#### importing Wallets
```python
from Minter import Minter, Wallet
import asyncio

minter = Minter(BASE_RPC, semaphore=30)
await minter.connect()
wallets = [
    Wallet(
        "0x..",
        "ce.."
    ),
    ...
]
await minter.storage.insert_data(wallets=wallets)
```

_For more examples, please refer to the [Documentation](https://github.com/PythonNoob999/Minter)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Todo
- [ ] Add price option to mint_bulk
- [ ] Add custom ABIs
- [ ] Add get_nft_balances Method
- [ ] Add send_nfts Method
- [ ] Add More Storage Options

See the [open issues](https://github.com/PythonNoob999/Minter/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

SpicyPneguin - [telegram](https://t.me/kerolis55463)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
