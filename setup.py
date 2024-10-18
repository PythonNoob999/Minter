from setuptools import setup, find_packages

setup(
    name="Minter",
    version="1.0.0",
    description="a lib/cli to mint nft's on any EVM chain (as long you fill the correct ABI args)",
    author="SpicyPenguin",
    packages=["Minter"],
    entry_points={
        "console_scripts": [
            "minter=Minter.cli:main"
        ]
    },
    install_requires=["kvsqlite", "web3"]
)