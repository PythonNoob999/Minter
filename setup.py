from setuptools import setup, find_packages

setup(
    name="Minter",
    version="1.0.2",
    description="a lib to mint nft's on any EVM chain",
    long_description=open("readme.md", "r", encoding="utf-8").read(),
    author="SpicyPenguin",
    packages=["Minter", "Minter.types", "Minter.types.abis", "Minter.storage", "Minter.data"],
    include_package_data=True,
    package_data={"": ["*.json"]},
    install_requires=["kvsqlite", "web3"]
)