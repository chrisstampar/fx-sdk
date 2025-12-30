# Curve Finance Integration

**Last Updated:** December 22, 2025  
**Status:** ✅ Complete - Production Ready

## Overview

The Curve Finance integration allows users to interact with Curve pools for swapping, adding/removing liquidity, and staking LP tokens in gauges to earn CRV rewards. The implementation supports all Curve pools used by the f(x) Protocol.

## Key Concepts

### Curve Pools
- **Decentralized Exchange**: Curve is optimized for stablecoin swaps and low-slippage trading
- **LP Tokens**: Users receive LP tokens when adding liquidity
- **Virtual Price**: LP token price relative to underlying assets
- **Pool Types**: Stable pools (2-4 tokens), Crypto pools (2 tokens), Factory pools

### Curve Gauges
- **Staking Mechanism**: Stake LP tokens to earn CRV rewards
- **Reward Tokens**: Typically CRV, but can include additional tokens
- **Gauge Addresses**: Already documented in `CONVEX_POOLS` registry as `fx_gauge`

### Registry Contracts
- **Main Registry**: `0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5` - Original Curve registry
- **Meta Registry**: `0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC` - Aggregates all pools
- **Address Provider**: `0x0000000022D53366457F9d5E68Ec105046FC4383` - Gets registry addresses

## Implemented Methods

### Pool Information (Read-Only)

#### `get_curve_pool_info(pool_address: str) -> Dict[str, Any]`
Get comprehensive information about a Curve pool.

**Parameters:**
- `pool_address`: Curve pool contract address

**Returns:**
- Dictionary with pool information:
  - `pool_address`: Pool address
  - `coins`: List of coin addresses
  - `balances`: List of coin balances (Wei)
  - `balances_decimal`: List of coin balances (human-readable)
  - `decimals`: List of coin decimals
  - `lp_token`: LP token address
  - `virtual_price`: LP token virtual price (Wei)
  - `virtual_price_decimal`: LP token virtual price (human-readable)
  - `A`: Amplification parameter (if available)
  - `fee`: Pool fee (if available)

**Example:**
```python
from fx_sdk import ProtocolClient

client = ProtocolClient(rpc_url="https://eth.llamarpc.com")

# Get pool info for ETH/FXN pool
pool_info = client.get_curve_pool_info("0xE06A65e09Ae18096B99770A809BA175FA05960e2")

print(f"Coins: {pool_info['coins']}")
print(f"Balances: {pool_info['balances_decimal']}")
print(f"LP Token: {pool_info['lp_token']}")
print(f"Virtual Price: {pool_info['virtual_price_decimal']}")
```

#### `get_curve_pool_balances(pool_address: str) -> List[Decimal]`
Get token balances for a Curve pool.

**Example:**
```python
balances = client.get_curve_pool_balances("0xE06A65e09Ae18096B99770A809BA175FA05960e2")
print(f"Token 0: {balances[0]}, Token 1: {balances[1]}")
```

#### `get_curve_pool_virtual_price(pool_address: str) -> Decimal`
Get virtual price (LP token price) for a Curve pool.

**Example:**
```python
vp = client.get_curve_pool_virtual_price("0xE06A65e09Ae18096B99770A809BA175FA05960e2")
print(f"LP Token Price: {vp}")
```

#### `get_curve_swap_rate(pool_address: str, token_in: str, token_out: str, amount_in: Decimal) -> Decimal`
Calculate the output amount for a swap on Curve.

**Parameters:**
- `pool_address`: Curve pool contract address
- `token_in`: Input token address
- `token_out`: Output token address
- `amount_in`: Input amount

**Example:**
```python
from decimal import Decimal
from fx_sdk import constants

amount_out = client.get_curve_swap_rate(
    pool_address="0xE06A65e09Ae18096B99770A809BA175FA05960e2",
    token_in="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  # ETH
    token_out=constants.FXN,
    amount_in=Decimal("1.0")
)
print(f"1 ETH = {amount_out} FXN")
```

#### `find_curve_pool(token_a: str, token_b: str) -> Optional[str]`
Find a Curve pool for a token pair.

**Example:**
```python
pool = client.find_curve_pool(
    token_a="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  # ETH
    token_b=constants.FXN
)
if pool:
    print(f"Found pool: {pool}")
```

#### `get_curve_pool_from_lp_token(lp_token: str) -> Optional[str]`
Find Curve pool address from LP token address.

**Example:**
```python
pool = client.get_curve_pool_from_lp_token("0xE06A65e09Ae18096B99770A809BA175FA05960e2")
```

### Gauge Information (Read-Only)

#### `get_curve_gauge_info(gauge_address: str) -> Dict[str, Any]`
Get comprehensive information about a Curve gauge.

**Returns:**
- Dictionary with gauge information:
  - `gauge_address`: Gauge address
  - `lp_token`: LP token address
  - `total_supply`: Total staked LP tokens (Wei)
  - `total_supply_decimal`: Total staked LP tokens (human-readable)
  - `reward_count`: Number of reward tokens
  - `reward_tokens`: List of reward token addresses
  - `is_killed`: Whether gauge is killed
  - `reward_data`: List of reward data dictionaries

**Example:**
```python
gauge_info = client.get_curve_gauge_info("0xA5250C540914E012E22e623275E290c4dC993D11")
print(f"LP Token: {gauge_info['lp_token']}")
print(f"Reward Tokens: {gauge_info['reward_tokens']}")
print(f"Total Staked: {gauge_info['total_supply_decimal']}")
```

#### `get_curve_gauge_balance(gauge_address: str, user_address: Optional[str] = None) -> Decimal`
Get staked LP token balance in a Curve gauge.

**Example:**
```python
balance = client.get_curve_gauge_balance(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11",
    user_address="0x..."  # Optional, defaults to connected wallet
)
print(f"Staked: {balance} LP tokens")
```

#### `get_curve_gauge_rewards(gauge_address: str, user_address: Optional[str] = None, reward_token: Optional[str] = None) -> Dict[str, Decimal]`
Get claimable rewards from a Curve gauge.

**Example:**
```python
rewards = client.get_curve_gauge_rewards(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11",
    user_address="0x..."  # Optional, defaults to connected wallet
)
for token, amount in rewards.items():
    print(f"{token}: {amount}")
```

#### `get_curve_gauge_from_pool(pool_address: str) -> Optional[str]`
Find Curve gauge address from pool address.

**Example:**
```python
gauge = client.get_curve_gauge_from_pool("0xE06A65e09Ae18096B99770A809BA175FA05960e2")
```

### Swap Operations (Write - Requires Private Key)

#### `curve_swap(pool_address: str, token_in: str, token_out: str, amount_in: Union[int, float, Decimal, str], min_amount_out: Optional[Union[int, float, Decimal, str]] = None) -> str`
Execute a swap on Curve.

**Parameters:**
- `pool_address`: Curve pool contract address
- `token_in`: Input token address
- `token_out`: Output token address
- `amount_in`: Input amount
- `min_amount_out`: Minimum output amount (optional, defaults to 0.5% slippage tolerance)

**Returns:**
- Transaction hash

**Example:**
```python
from decimal import Decimal

tx_hash = client.curve_swap(
    pool_address="0xE06A65e09Ae18096B99770A809BA175FA05960e2",
    token_in="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  # ETH
    token_out=constants.FXN,
    amount_in=Decimal("1.0"),
    min_amount_out=Decimal("0.95")  # 5% slippage tolerance
)
print(f"Swap transaction: {tx_hash}")
```

### Liquidity Operations (Write - Requires Private Key)

#### `curve_add_liquidity(pool_address: str, amounts: List[Union[int, float, Decimal, str]], min_lp_tokens: Optional[Union[int, float, Decimal, str]] = None) -> str`
Add liquidity to a Curve pool.

**Parameters:**
- `pool_address`: Curve pool contract address
- `amounts`: List of token amounts to deposit (one per coin)
- `min_lp_tokens`: Minimum LP tokens to receive (optional, defaults to 0.5% slippage tolerance)

**Example:**
```python
tx_hash = client.curve_add_liquidity(
    pool_address="0xE06A65e09Ae18096B99770A809BA175FA05960e2",
    amounts=[Decimal("1.0"), Decimal("100.0")],  # 1 ETH, 100 FXN
    min_lp_tokens=Decimal("0.99")  # 1% slippage tolerance
)
```

#### `curve_remove_liquidity(pool_address: str, lp_token_amount: Union[int, float, Decimal, str], min_amounts: Optional[List[Union[int, float, Decimal, str]]] = None) -> str`
Remove liquidity from a Curve pool.

**Parameters:**
- `pool_address`: Curve pool contract address
- `lp_token_amount`: Amount of LP tokens to burn
- `min_amounts`: Minimum token amounts to receive (optional, no slippage protection if None)

**Example:**
```python
tx_hash = client.curve_remove_liquidity(
    pool_address="0xE06A65e09Ae18096B99770A809BA175FA05960e2",
    lp_token_amount=Decimal("10.0"),
    min_amounts=[Decimal("0.9"), Decimal("90.0")]  # 10% slippage tolerance
)
```

### Gauge Operations (Write - Requires Private Key)

#### `curve_stake_lp_tokens(gauge_address: str, lp_token_amount: Union[int, float, Decimal, str], claim_rewards: bool = False) -> str`
Stake LP tokens in a Curve gauge.

**Parameters:**
- `gauge_address`: Curve gauge contract address
- `lp_token_amount`: Amount of LP tokens to stake
- `claim_rewards`: Whether to claim rewards when staking (default: False)

**Example:**
```python
tx_hash = client.curve_stake_lp_tokens(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11",
    lp_token_amount=Decimal("100.0"),
    claim_rewards=True
)
```

#### `curve_unstake_lp_tokens(gauge_address: str, lp_token_amount: Union[int, float, Decimal, str], claim_rewards: bool = False) -> str`
Unstake LP tokens from a Curve gauge.

**Example:**
```python
tx_hash = client.curve_unstake_lp_tokens(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11",
    lp_token_amount=Decimal("50.0"),
    claim_rewards=True
)
```

#### `curve_claim_gauge_rewards(gauge_address: str, receiver: Optional[str] = None) -> str`
Claim rewards from a Curve gauge.

**Example:**
```python
tx_hash = client.curve_claim_gauge_rewards(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11"
)
```

## Complete Workflow Examples

### Example 1: Swap ETH for FXN

```python
from fx_sdk import ProtocolClient
from decimal import Decimal

# Initialize client with private key
client = ProtocolClient(
    rpc_url="https://eth.llamarpc.com",
    private_key="your_private_key_here"
)

# Find the pool
pool = client.find_curve_pool(
    token_a="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  # ETH
    token_b=client.constants.FXN
)

# Check swap rate
amount_out = client.get_curve_swap_rate(
    pool_address=pool,
    token_in="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    token_out=client.constants.FXN,
    amount_in=Decimal("1.0")
)
print(f"1 ETH = {amount_out} FXN")

# Execute swap
tx_hash = client.curve_swap(
    pool_address=pool,
    token_in="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    token_out=client.constants.FXN,
    amount_in=Decimal("1.0"),
    min_amount_out=amount_out * Decimal("0.95")  # 5% slippage
)
print(f"Swap transaction: {tx_hash}")
```

### Example 2: Add Liquidity and Stake in Gauge

```python
# Add liquidity
tx_hash = client.curve_add_liquidity(
    pool_address="0xE06A65e09Ae18096B99770A809BA175FA05960e2",
    amounts=[Decimal("1.0"), Decimal("100.0")],  # 1 ETH, 100 FXN
    min_lp_tokens=Decimal("0.99")
)
print(f"Added liquidity: {tx_hash}")

# Wait for transaction confirmation
receipt = client.w3.eth.wait_for_transaction_receipt(tx_hash)

# Get LP token balance
lp_token = "0xE06A65e09Ae18096B99770A809BA175FA05960e2"
lp_balance = client.get_token_balance(lp_token)
print(f"LP Token Balance: {lp_balance}")

# Find gauge address
gauge = client.get_curve_gauge_from_pool("0xE06A65e09Ae18096B99770A809BA175FA05960e2")

# Stake LP tokens
tx_hash = client.curve_stake_lp_tokens(
    gauge_address=gauge,
    lp_token_amount=lp_balance,
    claim_rewards=False
)
print(f"Staked LP tokens: {tx_hash}")

# Check staked balance
staked = client.get_curve_gauge_balance(gauge_address=gauge)
print(f"Staked Balance: {staked}")

# Check rewards
rewards = client.get_curve_gauge_rewards(gauge_address=gauge)
print(f"Claimable Rewards: {rewards}")
```

### Example 3: Claim Rewards and Unstake

```python
# Check rewards
rewards = client.get_curve_gauge_rewards(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11"
)

# Claim rewards
if any(amount > 0 for amount in rewards.values()):
    tx_hash = client.curve_claim_gauge_rewards(
        gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11"
    )
    print(f"Claimed rewards: {tx_hash}")

# Unstake LP tokens
staked = client.get_curve_gauge_balance(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11"
)

tx_hash = client.curve_unstake_lp_tokens(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11",
    lp_token_amount=staked,
    claim_rewards=True  # Claim rewards when unstaking
)
print(f"Unstaked LP tokens: {tx_hash}")
```

## Error Handling

All methods raise appropriate exceptions:

- `ContractCallError`: Invalid addresses, contract call failures
- `FXProtocolError`: Missing private key for write operations
- `InsufficientBalanceError`: Insufficient token balance (if implemented)

**Example:**
```python
try:
    pool_info = client.get_curve_pool_info("invalid_address")
except ContractCallError as e:
    print(f"Error: {e}")
```

## Read-Only Support

All read methods work without a private key:

```python
# Read-only client (no private key)
client = ProtocolClient(rpc_url="https://eth.llamarpc.com")

# All read methods work
pool_info = client.get_curve_pool_info("0xE06A65e09Ae18096B99770A809BA175FA05960e2")
gauge_info = client.get_curve_gauge_info("0xA5250C540914E012E22e623275E290c4dC993D11")
balance = client.get_curve_gauge_balance(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11",
    user_address="0x..."  # Any address
)
```

## Integration with f(x) Protocol Pools

All f(x) Protocol Curve pools are documented in the `CONVEX_POOLS` registry in `constants.py`. Each pool entry includes:

- `fx_gauge`: f(x) Protocol gauge address (Curve gauge)
- `lp_token`: Curve LP token address
- `pool_type`: "curve_lp" for Curve pools

**Example:**
```python
from fx_sdk import constants

# Get pool info from registry
pool_id = 6  # ETH/FXN Curve Pool
pool_info = constants.CONVEX_POOLS.get(pool_id)

if pool_info and pool_info.get("pool_type") == "curve_lp":
    lp_token = pool_info["lp_token"]
    gauge_address = pool_info["fx_gauge"]
    
    # Get pool address from LP token
    pool_address = client.get_curve_pool_from_lp_token(lp_token)
    
    # Get pool info
    pool_data = client.get_curve_pool_info(pool_address)
    
    # Get gauge info
    gauge_data = client.get_curve_gauge_info(gauge_address)
```

## Notes

1. **Automatic Approvals**: All write methods automatically check and approve token allowances if needed
2. **Slippage Protection**: Default 0.5% slippage tolerance for swaps and liquidity operations
3. **Pool Support**: Currently optimized for 2-coin pools (most f(x) Protocol pools)
4. **Registry Fallbacks**: Methods try Meta Registry first, then fall back to Main Registry
5. **Decimal Precision**: All amounts use `Decimal` for high precision

## Testing

Comprehensive test suite available in `tests/test_curve.py`:

```bash
python3 -m unittest tests.test_curve -v
```

## Helper Methods

### Registry Queries

#### `get_curve_pools_from_registry() -> Dict[str, Dict[str, Any]]`
Get all Curve pools from the SDK's registry.

**Returns:**
- Dictionary mapping pool keys to pool information

**Example:**
```python
pools = client.get_curve_pools_from_registry()
for key, pool in pools.items():
    print(f"{key}: {pool['name']}")
```

#### `get_curve_pool_from_registry(pool_id: Optional[int] = None, pool_key: Optional[str] = None) -> Optional[Dict[str, Any]]`
Get Curve pool information from the SDK's registry.

**Example:**
```python
pool = client.get_curve_pool_from_registry(pool_id=6)  # ETH/FXN pool
if pool:
    print(f"LP Token: {pool['lp_token']}")
    print(f"Gauge: {pool['fx_gauge']}")
```

### Batch Operations

#### `get_curve_gauge_balances_batch(gauge_addresses: List[str], user_address: Optional[str] = None) -> Dict[str, Decimal]`
Get staked balances for multiple Curve gauges in a batch.

**Example:**
```python
gauges = ["0xA5250C540914E012E22e623275E290c4dC993D11", "0x..."]
balances = client.get_curve_gauge_balances_batch(gauges, user_address="0x...")
for gauge, balance in balances.items():
    print(f"{gauge}: {balance}")
```

#### `get_curve_gauge_rewards_batch(gauge_addresses: List[str], user_address: Optional[str] = None) -> Dict[str, Dict[str, Decimal]]`
Get claimable rewards for multiple Curve gauges in a batch.

**Example:**
```python
gauges = ["0xA5250C540914E012E22e623275E290c4dC993D11", "0x..."]
rewards = client.get_curve_gauge_rewards_batch(gauges, user_address="0x...")
for gauge, gauge_rewards in rewards.items():
    print(f"{gauge}: {gauge_rewards}")
```

### Position Summary

#### `get_user_curve_positions_summary(user_address: Optional[str] = None, include_pool_info: bool = True) -> Dict[str, Any]`
Get comprehensive summary of user's Curve positions across all f(x) Protocol pools.

**Returns:**
- Dictionary with:
  - `total_gauges`: Number of gauges with positions
  - `total_staked`: Total LP tokens staked
  - `total_rewards`: Total claimable rewards (by token)
  - `positions`: List of position details

**Example:**
```python
summary = client.get_user_curve_positions_summary(user_address="0x...")
print(f"Total Staked: {summary['total_staked']}")
print(f"Total Rewards: {summary['total_rewards']}")
for position in summary['positions']:
    print(f"{position['pool_name']}: {position['staked']} LP tokens")
```

### APY Calculations

#### `get_curve_gauge_apy(gauge_address: str, reward_token_price: Optional[Decimal] = None, lp_token_price: Optional[Decimal] = None) -> Dict[str, Any]`
Calculate APY (APR) for a Curve gauge based on current reward rate.

**Returns:**
- Dictionary with:
  - `apy`: APY as decimal (e.g., 0.05 for 5%)
  - `apy_percentage`: APY as percentage (e.g., 5.0)
  - `usd_apy`: USD-denominated APY (if prices provided)
  - `reward_rate`: Current reward rate per second
  - `total_staked`: Total LP tokens staked
  - `reward_token`: Reward token address
  - `period_finish`: When current reward period ends

**Example:**
```python
apy_data = client.get_curve_gauge_apy("0xA5250C540914E012E22e623275E290c4dC993D11")
print(f"APY: {apy_data['apy_percentage']}%")

# With prices for USD APY
apy_data = client.get_curve_gauge_apy(
    gauge_address="0xA5250C540914E012E22e623275E290c4dC993D11",
    reward_token_price=Decimal("0.5"),  # CRV price
    lp_token_price=Decimal("1.0")  # LP token price
)
print(f"USD APY: {apy_data['usd_apy_percentage']}%")
```

#### `get_all_curve_gauges_apy(reward_token_prices: Optional[Dict[str, Decimal]] = None, lp_token_prices: Optional[Dict[str, Decimal]] = None) -> Dict[str, Dict[str, Any]]`
Get APY for all Curve gauges in the f(x) Protocol registry.

**Example:**
```python
apy_data = client.get_all_curve_gauges_apy()
for gauge, data in apy_data.items():
    print(f"{data['pool_name']}: {data['apy_percentage']}%")

# With prices for USD APY
apy_data = client.get_all_curve_gauges_apy(
    reward_token_prices={constants.CRV_TOKEN: Decimal("0.5")},
    lp_token_prices={lp_token: Decimal("1.0")}
)
```

## Related Documentation

- [CURVE_INTEGRATION_PLAN.md](./CURVE_INTEGRATION_PLAN.md) - Original integration plan
- [CONVEX_INTEGRATION_COMPLETE.md](./CONVEX_INTEGRATION_COMPLETE.md) - Convex integration (builds on Curve)

