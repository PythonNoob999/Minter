from setuptools import setup, find_packages

setup(
    name="Minter",
    version="1.0.0",
    description="a lib/cli to mint nft's on any EVM chain (as long you fill the correct ABI args)",
    author="SpicyPenguin",
    packages=["Minter", "Minter.types", "Minter.types.abis", "Minter.storage", "Minter.data"],
    include_package_data=True,
    package_data={"": ["*.json"]},
    install_requires=["kvsqlite", "web3"]
)