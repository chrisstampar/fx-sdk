# f(x) Protocol Python SDK

Welcome to the f(x) Protocol Python SDK documentation!

## Quick Links

- [Complete Documentation](Documentation.md) - Full API reference and usage guide
- [GitHub Repository](https://github.com/chrisstampar/fx-sdk) - Source code and issues
- [PyPI Package](https://pypi.org/project/fx-sdk/) - Install via pip

## Installation

```bash
pip install fx-sdk
```

## Quick Start

```python
from fx_sdk.client import ProtocolClient

# Initialize in read-only mode
client = ProtocolClient(
    rpc_url="https://mainnet.infura.io/v3/YOUR_API_KEY"
)

# Read balance
balance = client.get_fxusd_balance("0x...")
print(f"fxUSD Balance: {balance}")
```

For complete documentation, see [Documentation.md](Documentation.md).

