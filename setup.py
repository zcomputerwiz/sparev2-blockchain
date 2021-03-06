from setuptools import setup

dependencies = [
    "multidict==5.1.0",  # Avoid 5.2.0 due to Avast
    "blspy==1.0.7",  # Signature library
    "chiavdf==1.0.3",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.6",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.15",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.4",  # Colorizes terminal output
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "fasteners==0.16.3",  # For interprocess file locking
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the spare processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspythonchia==2.2.0",  # Query DNS seeds
    "watchdog==2.1.6",  # Filesystem event watching - watches keyring.yaml
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "types-setuptools",
]

kwargs = dict(
    name="spare-blockchain",
    author="Mariano Sorgente",
    author_email="mariano@sparecoin.org",
    description="Spare blockchain full node, farmer, timelord, and wallet.",
    url="https://sparecoin.org/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="spare blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "spare",
        "spare.cmds",
        "spare.clvm",
        "spare.consensus",
        "spare.daemon",
        "spare.full_node",
        "spare.timelord",
        "spare.farmer",
        "spare.harvester",
        "spare.introducer",
        "spare.plotters",
        "spare.plotting",
        "spare.pools",
        "spare.protocols",
        "spare.rpc",
        "spare.server",
        "spare.simulator",
        "spare.types.blockchain_format",
        "spare.types",
        "spare.util",
        "spare.wallet",
        "spare.wallet.puzzles",
        "spare.wallet.rl_wallet",
        "spare.wallet.cc_wallet",
        "spare.wallet.did_wallet",
        "spare.wallet.settings",
        "spare.wallet.trading",
        "spare.wallet.util",
        "spare.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "spare = spare.cmds.spare:main",
            "spare_wallet = spare.server.start_wallet:main",
            "spare_full_node = spare.server.start_full_node:main",
            "spare_harvester = spare.server.start_harvester:main",
            "spare_farmer = spare.server.start_farmer:main",
            "spare_introducer = spare.server.start_introducer:main",
            "spare_timelord = spare.server.start_timelord:main",
            "spare_timelord_launcher = spare.timelord.timelord_launcher:main",
            "spare_full_node_simulator = spare.simulator.start_simulator:main",
        ]
    },
    package_data={
        "spare": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "spare.util": ["initial-*.yaml", "english.txt"],
        "spare.ssl": ["spare_ca.crt", "spare_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    #use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    version="1.0.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)  # type: ignore
