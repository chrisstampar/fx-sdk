# Convex Finance Integration

**Last Updated:** December 22, 2025  
**Status:** ✅ Complete - Production Ready

> **Note:** This is the main documentation for Convex Finance integration. For a quick status summary, see [CONVEX_INTEGRATION_TODO.md](./CONVEX_INTEGRATION_TODO.md).

## Overview

The Convex Finance integration allows users to interact with Convex vaults for all f(x) Protocol pools on Convex. The implementation is **generic** and works with any Convex pool by accepting `pool_id` and `vault_address` parameters. Each user has their own vault address that must be created before depositing.

### Generic Implementation

All Convex functions are designed to work with any pool:
- Functions accept `pool_id` as a parameter (works for any pool)
- Functions accept `vault_address` as a parameter (user-specific, works for any pool)
- The vault contract handles pool-specific details internally
- Pool metadata is stored in the `CONVEX_POOLS` registry

See [CONVEX_POOL_COMPARISON.md](./CONVEX_POOL_COMPARISON.md) for details on how the generic approach works.

## Key Concepts

### Vault Addresses
- **User-Specific**: Each user has their own unique vault address
- **Created via Factory**: Vaults are created using the factory contract
- **Required Parameter**: Users must provide their vault address for all operations
- **Example**: `0x1234567890123456789012345678901234567890`

### Factory Contract
- **Address**: `0xAffe966B27ba3E4Ebb8A0eC124C7b7019CC762f8`
- **Function**: `createVault(uint256 _pid)` - Returns the vault address
- **Event**: `AddUserVault(address user, uint256 poolid)` - Emitted when vault is created

## Implemented Methods

### Vault Management

#### `create_convex_vault(pool_id: int) -> Dict[str, Any]`
Creates a new Convex vault for the user.

**Parameters:**
- `pool_id`: Convex pool ID (37 for fxUSD stability pool)

**Returns:**
- Dictionary with `transaction_hash` and `vault_address` (after confirmation)

**Example:**
```python
result = client.create_convex_vault(37)
print(f"Vault creation tx: {result['transaction_hash']}")
# Query vault address after confirmation
```

#### `get_convex_vault_address(user_address: str, pool_id: int, from_block: int = 0) -> Optional[str]`
Gets a user's vault address by querying events.

**Parameters:**
- `user_address`: User's wallet address
- `pool_id`: Convex pool ID
- `from_block`: Block number to start searching (0 = from genesis)

**Returns:**
- Vault address if found, None if vault doesn't exist

**Example:**
```python
vault_address = client.get_convex_vault_address(
    user_address="0x...",
    pool_id=37
)
```

#### `get_convex_vault_address_or_create(pool_id: int, user_address: Optional[str] = None, auto_create: bool = False) -> Optional[str]`
Helper method that gets vault address, optionally creating it if it doesn't exist.

**Parameters:**
- `pool_id`: Convex pool ID
- `user_address`: User address (defaults to client's address)
- `auto_create`: If True, create vault if it doesn't exist

**Returns:**
- Vault address, or None if not found and auto_create is False

### Vault Information

#### `get_convex_vault_info(vault_address: str) -> Dict[str, Any]`
Gets information about a vault.

**Returns:**
- `owner`: Vault owner address
- `pid`: Pool ID
- `staking_token`: Staking token address
- `gauge_address`: Gauge address
- `rewards`: Rewards contract address

#### `get_convex_vault_balance(vault_address: str, token_address: Optional[str] = None) -> Decimal`
Gets the staked balance in a vault.

**Parameters:**
- `vault_address`: User's vault address (required - user-specific)
- `token_address`: Optional token address to check balance for

**Returns:**
- Staked balance as Decimal

#### `get_convex_vault_rewards(vault_address: str) -> Dict[str, Any]`
Gets claimable rewards for a vault.

**Returns:**
- `token_addresses`: List of reward token addresses
- `amounts`: Dictionary mapping token addresses to claimable amounts (Decimal)

### Vault Operations

#### `deposit_to_convex_vault(vault_address: str, amount: Union[int, float, Decimal, str], manage: bool = False) -> str`
Deposits tokens to a Convex vault.

**Parameters:**
- `vault_address`: User's vault address (required - user-specific)
- `amount`: Amount of LP tokens to deposit
- `manage`: Whether to manage the deposit (auto-stake, etc.)

**Returns:**
- Transaction hash

**Example:**
```python
# User must provide their vault address
vault_address = "0x..."  # User's specific vault address
tx_hash = client.deposit_to_convex_vault(
    vault_address=vault_address,
    amount=100.0,  # 100 LP tokens
    manage=False
)
```

#### `withdraw_from_convex_vault(vault_address: str, amount: Union[int, float, Decimal, str]) -> str`
Withdraws tokens from a Convex vault.

**Parameters:**
- `vault_address`: User's vault address (required - user-specific)
- `amount`: Amount of tokens to withdraw

**Returns:**
- Transaction hash

#### `claim_convex_vault_rewards(vault_address: str, claim: bool = True, token_list: Optional[List[str]] = None) -> str`
Claims rewards from a Convex vault.

**Parameters:**
- `vault_address`: User's vault address (required - user-specific)
- `claim`: Whether to claim rewards
- `token_list`: Optional list of specific tokens to claim (if None, claims all)

**Returns:**
- Transaction hash

## Usage Examples

### Complete Workflow

```python
from fx_sdk import ProtocolClient, constants
from decimal import Decimal

# Initialize client with private key for write operations
client = ProtocolClient(
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    private_key="YOUR_PRIVATE_KEY"  # Or use environment variable
)

# Pool ID for fxUSD stability pool (earns FXN)
POOL_ID = 37

# Step 1: Get or create vault
vault_address = client.get_convex_vault_address(
    user_address=client.address,
    pool_id=POOL_ID
)

if not vault_address:
    # Create vault
    print("Creating new vault...")
    result = client.create_convex_vault(POOL_ID)
    print(f"Vault creation tx: {result['transaction_hash']}")
    
    # Try to get vault address from transaction
    if result['vault_address']:
        vault_address = result['vault_address']
        print(f"Vault created at: {vault_address}")
    else:
        # Wait a moment for confirmation, then query again
        import time
        time.sleep(5)  # Wait for block confirmation
        vault_address = client.get_convex_vault_address(
            user_address=client.address,
            pool_id=POOL_ID
        )
        if not vault_address:
            # If still not found, user can provide it manually
            vault_address = input("Please enter your vault address: ")

# Step 2: Check vault info
vault_info = client.get_convex_vault_info(vault_address)
print(f"Vault owner: {vault_info['owner']}")
print(f"Pool ID: {vault_info['pid']}")
print(f"Staking token: {vault_info['staking_token']}")

# Step 3: Check balance
balance = client.get_convex_vault_balance(vault_address)
print(f"Staked balance: {balance}")

# Step 4: Check rewards
rewards = client.get_convex_vault_rewards(vault_address)
print(f"Claimable rewards:")
for token_addr, amount in rewards['amounts'].items():
    print(f"  {token_addr}: {amount}")

# Step 5: Deposit (if needed)
# The deposit method will automatically check and approve if needed
lp_token = constants.CONVEX_POOLS["fxusd_stability_fxn"]["staked_token"]
tx_hash = client.deposit_to_convex_vault(
    vault_address=vault_address,
    amount=100.0  # Amount in LP tokens
)
print(f"Deposit transaction: {tx_hash}")

# Step 6: Claim rewards
tx_hash = client.claim_convex_vault_rewards(vault_address)
print(f"Reward claim transaction: {tx_hash}")

# Step 7: Withdraw (if needed)
tx_hash = client.withdraw_from_convex_vault(
    vault_address=vault_address,
    amount=50.0  # Amount to withdraw
)
print(f"Withdrawal transaction: {tx_hash}")
```

### Using a Known Vault Address

If you already know your vault address, you can use it directly:

```python
from fx_sdk import ProtocolClient

client = ProtocolClient(
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    private_key="YOUR_PRIVATE_KEY"
)

# Use your known vault address
vault_address = "0x1234567890123456789012345678901234567890"

# Check balance
balance = client.get_convex_vault_balance(vault_address)
print(f"Staked balance: {balance}")

# Check rewards
rewards = client.get_convex_vault_rewards(vault_address)
print(f"Rewards: {rewards}")

# Deposit
tx_hash = client.deposit_to_convex_vault(vault_address, amount=100.0)
```

### Read-Only Operations (No Private Key)

You can query vault information without a private key:

```python
from fx_sdk import ProtocolClient

# Initialize in read-only mode
client = ProtocolClient(rpc_url="https://eth.llamarpc.com")

# Query any user's vault (if you know the address)
vault_address = "0x1234567890123456789012345678901234567890"

# Get vault info
vault_info = client.get_convex_vault_info(vault_address)
print(f"Vault owner: {vault_info['owner']}")
print(f"Pool ID: {vault_info['pid']}")

# Get balance
balance = client.get_convex_vault_balance(vault_address)
print(f"Staked balance: {balance}")

# Get rewards
rewards = client.get_convex_vault_rewards(vault_address)
print(f"Claimable rewards: {rewards}")
```

### cvxFXN Staking

```python
from fx_sdk import ProtocolClient

client = ProtocolClient(
    rpc_url="https://mainnet.infura.io/v3/YOUR_KEY",
    private_key="YOUR_PRIVATE_KEY"
)

# Check cvxFXN balance
cvxfxn_balance = client.get_cvxfxn_balance(client.address)
print(f"cvxFXN balance: {cvxfxn_balance}")

# Check staked balance
staked_balance = client.get_staked_cvxfxn_balance(client.address)
print(f"Staked cvxFXN: {staked_balance}")

# Check rewards
rewards = client.get_cvxfxn_staking_rewards(client.address)
print(f"Claimable rewards: {rewards}")

# Deposit FXN to get cvxFXN (automatically approves if needed)
tx_hash = client.deposit_fxn_to_cvxfxn(amount=100.0)
print(f"Deposit transaction: {tx_hash}")

# Stake cvxFXN (automatically approves if needed)
tx_hash = client.stake_cvxfxn(amount=50.0)
print(f"Stake transaction: {tx_hash}")

# Claim rewards
tx_hash = client.claim_cvxfxn_staking_rewards()
print(f"Reward claim transaction: {tx_hash}")

# Unstake
tx_hash = client.unstake_cvxfxn(amount=25.0)
print(f"Unstake transaction: {tx_hash}")
```

## Important Notes

1. **Vault Address is User-Specific**: 
   - Each user has their own vault address
   - Never hardcode vault addresses in the SDK
   - Users must provide their vault address or query it
   - If automatic extraction fails, users can query their vault address using:
     ```python
     vault_address = client.get_convex_vault_address(user_address, pool_id)
     ```

2. **Vault Creation**:
   - Users must create a vault before depositing
   - Vault creation is a one-time operation per pool
   - The vault address is returned by `createVault()` function
   - If automatic extraction fails, wait a few seconds and query again:
     ```python
     result = client.create_convex_vault(pool_id)
     time.sleep(5)  # Wait for confirmation
     vault_address = client.get_convex_vault_address(user_address, pool_id)
     ```

3. **Pool ID**:
   - fxUSD V2 Stability Pool (Earns FXN): **Pool ID 37**
   - fxUSD V2 Stability Pool (Earns wstETH): **Pool ID 36**
   - See `constants.CONVEX_POOLS` for all available pools

4. **Error Handling**:
   - All methods validate vault addresses
   - Insufficient balance errors are raised before transactions
   - Invalid vault addresses raise `ContractCallError`
   - Methods check for private key before write operations

5. **ABIs**:
   - Factory ABI: `convex_vault_factory.json`
   - Vault ABI: `convex_vault.json`
   - cvxFXN ABIs: `cvxfxn.json`, `cvxfxn_deposit.json`, `cvxfxn_stake.json`
   - All are in `fx_sdk/abis/`

6. **Automatic Approvals**:
   - `deposit_to_convex_vault()` automatically checks and approves tokens if needed
   - `deposit_fxn_to_cvxfxn()` automatically approves FXN if needed
   - `stake_cvxfxn()` automatically approves cvxFXN if needed

## Constants Added

```python
# Convex Finance
CONVEX_BOOSTER = "0xF403C135812408BFbE8713b5A23a04b3D48AAE31"
CONVEX_VAULT_FACTORY = "0xAffe966B27ba3E4Ebb8A0eC124C7b7019CC762f8"
CONVEX_VAULT_REGISTRY = "0xdb95d646012bb87ac2e6cd63eab2c42323c1f5af"

# Convex Pools
CONVEX_POOLS = {
    "fxusd_stability": {
        "pool_id": 37,
        "name": "fxUSD V2 Stability Pool",
        "lp_token": FXUSD_BASE_POOL,  # fxBASE
        "fx_gauge": "0x215D87bd3c7482E2348338815E059DE07Daf798A",
    }
}
```

## Testing Recommendations

1. **Test Vault Creation**:
   - Create a vault on testnet first
   - Verify the vault address is returned correctly
   - Test with a test account

2. **Test Vault Queries**:
   - Query existing vault addresses
   - Test with known vault addresses
   - Verify event parsing works correctly

3. **Test Operations**:
   - Test deposit with small amounts
   - Test withdrawal
   - Test reward claiming
   - Verify balances update correctly

## Future Enhancements

1. **Improve Vault Address Extraction**:
   - Better parsing of transaction receipts
   - Extract vault address from `createVault()` return value
   - Use transaction tracing if available

2. **Add Pool-Specific Methods**:
   - Helper methods for fxUSD pool (Pool ID 37)
   - Pre-configured methods that use the correct pool ID

3. **Add Batch Operations**:
   - Query multiple vaults at once
   - Batch reward claims

## Error Handling

The SDK includes comprehensive error handling:

- **Invalid Vault Address**: Raises `ContractCallError` with descriptive message
- **Insufficient Balance**: Raises `InsufficientBalanceError` before attempting transaction
- **Missing Private Key**: Raises `FXProtocolError` for write operations without authentication
- **Vault Not Found**: Returns `None` for vault address queries, logs warning

## Helper Methods

### `get_all_user_vaults(user_address: Optional[str] = None, from_block: int = 0) -> Dict[int, Optional[str]]`

Get all Convex vault addresses for a user across all known pools.

**Returns:** Dictionary mapping pool_id to vault_address (None if vault doesn't exist)

**Example:**
```python
vaults = client.get_all_user_vaults()
# Returns: {37: "0x...", 36: "0x...", 0: None, ...}

# Check which pools the user has vaults for
for pool_id, vault_address in vaults.items():
    if vault_address:
        print(f"Pool {pool_id}: {vault_address}")
```

### `get_convex_pool_info(pool_id: Optional[int] = None, pool_key: Optional[str] = None) -> Dict[str, Any]`

Get information about a Convex pool from the registry.

**Example:**
```python
# By pool ID
pool_info = client.get_convex_pool_info(pool_id=37)
print(f"Pool: {pool_info['name']}")
print(f"Staked Token: {pool_info['staked_token']}")
print(f"Earns: {pool_info['earns']}")

# By pool key
pool_info = client.get_convex_pool_info(pool_key="fxusd_stability_fxn")
```

### `get_all_convex_pools() -> Dict[str, Dict[str, Any]]`

Get information about all Convex pools in the registry.

**Example:**
```python
all_pools = client.get_all_convex_pools()
for pool_key, pool_info in all_pools.items():
    print(f"{pool_info['name']}: Pool ID {pool_info['pool_id']}")
```

### `get_vault_balances_batch(vault_addresses: List[str]) -> Dict[str, Decimal]`

Get balances for multiple vaults in a single batch query.

**Example:**
```python
vaults = ["0x...", "0x...", "0x..."]
balances = client.get_vault_balances_batch(vaults)
for vault, balance in balances.items():
    print(f"{vault}: {balance} staked")
```

### `get_vault_rewards_batch(vault_addresses: List[str]) -> Dict[str, Dict[str, Any]]`

Get rewards for multiple vaults in a single batch query.

**Example:**
```python
vaults = ["0x...", "0x..."]
rewards = client.get_vault_rewards_batch(vaults)
for vault, vault_rewards in rewards.items():
    total = sum(vault_rewards['amounts'].values())
    print(f"{vault}: {total} in rewards")
```

### `get_user_vaults_summary(user_address: Optional[str] = None, from_block: int = 0) -> Dict[str, Any]`

Get a comprehensive summary of all user's Convex vaults including balances and rewards.

**Example:**
```python
summary = client.get_user_vaults_summary()
print(f"User has {summary['total_vaults']} vaults")

for pool_id, vault_data in summary['vaults'].items():
    if vault_data['vault_address']:
        pool_name = vault_data['pool_info']['name']
        balance = vault_data['balance']
        rewards = sum(vault_data['rewards']['amounts'].values())
        print(f"Pool {pool_id} ({pool_name}):")
        print(f"  Balance: {balance}")
        print(f"  Rewards: {rewards}")
```

## APY Calculation Methods

### `get_convex_pool_apy(pool_id: int, reward_token_price: Optional[Decimal] = None, staking_token_price: Optional[Decimal] = None) -> Dict[str, Any]`

Calculate APY for a Convex pool based on current reward rate and total staked amount.

**Returns:**
- `apy`: APY as percentage (e.g., 15.5 for 15.5%)
- `reward_rate`: Reward rate per second
- `total_staked`: Total staked amount
- `reward_token`: Reward token address
- `staking_token`: Staking token address
- `usd_apy`: USD-denominated APY (if prices provided)
- `period_finish`: When current reward period ends
- `is_active`: Whether rewards are currently active
- `pool_id`: Pool ID
- `pool_name`: Pool name (if available)
- `pool_key`: Pool key (if available)

**Example:**
```python
# Basic APY calculation
apy_data = client.get_convex_pool_apy(pool_id=37)
print(f"Pool 37 APY: {apy_data['apy']}%")
print(f"Reward Rate: {apy_data['reward_rate']} tokens/second")
print(f"Total Staked: {apy_data['total_staked']} tokens")
print(f"Active: {apy_data['is_active']}")

# With USD prices for USD-denominated APY
apy_data = client.get_convex_pool_apy(
    pool_id=37,
    reward_token_price=Decimal("0.5"),  # FXN price in USD
    staking_token_price=Decimal("1.0")   # LP token price in USD
)
print(f"USD APY: {apy_data['usd_apy']}%")
```

### `get_convex_vault_apy(vault_address: str, reward_token_price: Optional[Decimal] = None, staking_token_price: Optional[Decimal] = None) -> Dict[str, Any]`

Calculate APY for a specific Convex vault using the vault's rewards contract.

**Example:**
```python
vault_address = "0x1234567890123456789012345678901234567890"
apy_data = client.get_convex_vault_apy(vault_address)
print(f"Vault APY: {apy_data['apy']}%")
print(f"Pool: {apy_data['pool_name']}")
print(f"Active: {apy_data['is_active']}")
```

### `get_all_convex_pools_apy(reward_token_prices: Optional[Dict[str, Decimal]] = None, staking_token_prices: Optional[Dict[str, Decimal]] = None) -> Dict[int, Dict[str, Any]]`

Get APY for all Convex pools in the registry.

**Example:**
```python
# Get APY for all pools
all_apys = client.get_all_convex_pools_apy()

# Sort by APY
sorted_pools = sorted(
    all_apys.items(),
    key=lambda x: x[1].get('apy', 0),
    reverse=True
)

print("Top 5 pools by APY:")
for pool_id, apy_data in sorted_pools[:5]:
    if 'error' not in apy_data:
        print(f"Pool {pool_id} ({apy_data.get('pool_name', 'Unknown')}): {apy_data['apy']}% APY")
```

**Note on APY Calculation:**
- The calculation uses simple APR (Annual Percentage Rate) formula: `(reward_rate * seconds_per_year) / total_staked * 100`
- This is based on current reward rate and does not account for compounding
- Actual APY may vary based on:
  - Reward claiming frequency (compounding effect)
  - Token price changes
  - Reward period expiration
  - Changes in total staked amount
- The `is_active` field indicates whether rewards are currently being distributed

## Pool Information Queries

### `get_convex_pool_details(pool_id: int, include_tvl: bool = True, include_rewards: bool = True) -> Dict[str, Any]`

Get comprehensive details about a Convex pool including live on-chain data.

**Returns:**
- Registry data: `pool_id`, `name`, `staked_token`, `base_token`, `redeems_to`, `earns`, etc.
- Live data: `tvl`, `reward_tokens`, `gauge_address`, `base_reward_pool` address
- Contract addresses: `lptoken`, `token`, `stash`, `shutdown` status
- Reward information: `reward_rate`, `reward_period_finish`, `rewards_active`

**Example:**
```python
details = client.get_convex_pool_details(pool_id=37)
print(f"Pool: {details['name']}")
print(f"TVL: {details['tvl']} tokens")
print(f"Reward Tokens: {details['reward_tokens']}")
print(f"Gauge: {details['gauge_address']}")
print(f"Rewards Active: {details['rewards_active']}")
print(f"Shutdown: {details['shutdown']}")
```

### `get_convex_pool_tvl(pool_id: int) -> Optional[Decimal]`

Get Total Value Locked (TVL) for a Convex pool.

**Example:**
```python
tvl = client.get_convex_pool_tvl(pool_id=37)
if tvl:
    print(f"Pool 37 TVL: {tvl} tokens")
```

### `get_convex_pool_reward_tokens(pool_id: int) -> List[str]`

Get list of reward token addresses for a Convex pool.

**Note:** This currently returns the primary reward token. Additional reward tokens may be available through extra reward contracts (stash).

**Example:**
```python
reward_tokens = client.get_convex_pool_reward_tokens(pool_id=37)
print(f"Reward Tokens: {reward_tokens}")
```

### `get_convex_pool_gauge_address(pool_id: int) -> Optional[str]`

Get the gauge address for a Convex pool.

**Example:**
```python
gauge = client.get_convex_pool_gauge_address(pool_id=37)
if gauge:
    print(f"Pool 37 Gauge: {gauge}")
```

### `get_all_convex_pools_tvl() -> Dict[int, Optional[Decimal]]`

Get TVL for all Convex pools in the registry.

**Example:**
```python
all_tvls = client.get_all_convex_pools_tvl()

# Sort by TVL
sorted_pools = sorted(
    [(pid, tvl) for pid, tvl in all_tvls.items() if tvl],
    key=lambda x: x[1],
    reverse=True
)

print("Top 5 pools by TVL:")
for pool_id, tvl in sorted_pools[:5]:
    print(f"Pool {pool_id}: {tvl} TVL")
```

### `get_convex_pool_statistics(pool_id: int) -> Dict[str, Any]`

Get comprehensive statistics for a Convex pool, combining pool details, TVL, APY, and other metrics.

**Example:**
```python
stats = client.get_convex_pool_statistics(pool_id=37)
print(f"Pool: {stats['name']}")
print(f"TVL: {stats['tvl']} tokens")
print(f"APY: {stats['apy']}%")
print(f"Rewards Active: {stats['rewards_active']}")
print(f"Total Staked: {stats['apy_total_staked']} tokens")
print(f"Reward Rate: {stats['reward_rate']} tokens/second")
```

## Testing

Comprehensive tests are available in `tests/test_convex.py`:

```bash
cd sdk
python -m pytest tests/test_convex.py -v
```

Tests cover:
- Vault creation and address lookup
- Vault information queries
- Deposits and withdrawals with validation
- Reward claiming
- Error handling (invalid addresses, insufficient balance, etc.)
- cvxFXN staking operations
- Helper methods (pool info, batch queries, user vaults summary)

---

**Status**: ✅ Implementation complete with comprehensive error handling, testing, and helper methods.

