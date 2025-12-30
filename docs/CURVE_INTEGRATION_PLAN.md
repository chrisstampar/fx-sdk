# Curve Finance Integration Plan

**Created:** December 22, 2025  
**Status:** 📋 Planning Phase

## Overview

This document outlines what would be required to add Curve Finance integration to the fx-sdk. Curve Finance is a decentralized exchange optimized for stablecoin swaps and is the foundation that Convex Finance builds upon. The f(x) Protocol has many pools on Curve, and users may want to interact with Curve pools directly (swapping, adding/removing liquidity, staking in gauges).

## Current State

### Existing Curve References

The SDK already has extensive Curve pool information in `CONVEX_POOLS`:
- **20+ Curve LP pools** already documented with:
  - Curve LP token addresses
  - f(x) Protocol gauge addresses
  - Pool metadata (names, pairs, etc.)

### Key Curve Pools in f(x) Protocol

Examples from `constants.py`:
- ETH/FXN Curve Pool
- FXN/cvxFXN Curve Pool
- crvUSD/fxUSD Curve Pool
- pyUSD/fxUSD Curve Pool
- DOLA/fxUSD Curve Pool
- GRAI/fxUSD Curve Pool
- FRAX/fxUSD Curve Pool
- GHO/fxUSD Curve Pool
- And many more...

## Required Components

### 1. Core Curve Contracts & Constants

#### Main Curve Contracts (Ethereum Mainnet)

```python
# Core Curve Contracts
CURVE_REGISTRY = "0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5"  # Main Registry
CURVE_META_REGISTRY = "0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC"  # Meta Registry (newer)
CURVE_ADDRESS_PROVIDER = "0x0000000022D53366457F9d5E68Ec105046FC4383"  # Address Provider
CURVE_FACTORY_REGISTRY = "0x8F942C20D02bEfc377D41489daa13e357D4C4a9e"  # Factory Registry

# Curve Tokens
CRV_TOKEN = "0xD533a949740bb3306d119CC777fa900bA034cd52"  # CRV governance token

# Curve Gauges (pool-specific, but we can query from registry)
# Gauge addresses are already in CONVEX_POOLS as "fx_gauge"
```

#### Curve Pool Types

Curve has different pool types:
- **Stable Pools**: 2-4 tokens, optimized for stablecoins
- **Crypto Pools**: 2 tokens, optimized for volatile assets
- **Tricrypto Pools**: 3 tokens (usually BTC/ETH/USD)
- **Factory Pools**: Created via factory contracts

### 2. Required ABIs

#### Essential ABIs to Create/Fetch

1. **curve_pool.json** - Standard Curve pool ABI
   - Functions: `exchange()`, `add_liquidity()`, `remove_liquidity()`, `get_virtual_price()`, `balances()`, `coins()`
   - Address: Pool-specific (from registry or constants)

2. **curve_gauge.json** - Curve gauge ABI (for staking LP tokens)
   - Functions: `deposit()`, `withdraw()`, `claim_rewards()`, `balanceOf()`, `earned()`
   - Address: Gauge-specific (already in CONVEX_POOLS as "fx_gauge")

3. **curve_registry.json** - Curve registry ABI
   - Functions: `get_pool_from_lp_token()`, `get_lp_token()`, `get_coins()`, `get_balances()`
   - Address: `CURVE_REGISTRY` or `CURVE_META_REGISTRY`

4. **curve_address_provider.json** - Address provider ABI
   - Functions: `get_registry()`, `get_address()`
   - Address: `CURVE_ADDRESS_PROVIDER`

5. **curve_factory_registry.json** - Factory registry ABI
   - Functions: `get_pool_from_lp_token()`, `get_coins()`
   - Address: `CURVE_FACTORY_REGISTRY`

### 3. Core Functionality to Implement

#### Read Methods (No Private Key Required)

**Pool Information:**
- `get_curve_pool_info(pool_address)` - Get pool details (coins, balances, virtual price)
- `get_curve_pool_balances(pool_address)` - Get token balances in pool
- `get_curve_pool_virtual_price(pool_address)` - Get LP token virtual price
- `get_curve_pool_coins(pool_address)` - Get list of coins in pool
- `get_curve_pool_from_lp_token(lp_token)` - Find pool address from LP token
- `get_curve_swap_rate(pool_address, token_in, token_out, amount_in)` - Calculate swap rate

**Gauge Information:**
- `get_curve_gauge_info(gauge_address)` - Get gauge details
- `get_curve_gauge_balance(gauge_address, user_address)` - Get staked LP balance
- `get_curve_gauge_rewards(gauge_address, user_address)` - Get claimable rewards
- `get_curve_gauge_reward_tokens(gauge_address)` - Get reward token addresses

**Registry Queries:**
- `get_curve_pools_by_lp_token(lp_token)` - Find pools using LP token
- `get_all_curve_pools()` - List all pools (from registry)

#### Write Methods (Private Key Required)

**Swapping:**
- `swap_on_curve(pool_address, token_in, token_out, amount_in, min_amount_out)` - Swap tokens
- `swap_underlying_on_curve(pool_address, token_in, token_out, amount_in, min_amount_out)` - Swap underlying tokens

**Liquidity:**
- `add_liquidity_to_curve(pool_address, amounts, min_lp_tokens)` - Add liquidity to pool
- `remove_liquidity_from_curve(pool_address, lp_amount, min_amounts)` - Remove liquidity
- `remove_liquidity_one_coin(pool_address, lp_amount, coin_index, min_amount)` - Remove liquidity as single token

**Gauge Staking:**
- `stake_in_curve_gauge(gauge_address, lp_amount)` - Stake LP tokens in gauge
- `unstake_from_curve_gauge(gauge_address, lp_amount)` - Unstake LP tokens
- `claim_curve_gauge_rewards(gauge_address)` - Claim gauge rewards

### 4. Helper Methods

**Pool Discovery:**
- `find_curve_pool(token_a, token_b)` - Find Curve pool for token pair
- `get_curve_pools_for_token(token_address)` - Get all pools containing a token
- `get_curve_pool_apy(pool_address)` - Calculate APY for a pool (from gauge rewards)

**Batch Operations:**
- `get_curve_pool_balances_batch(pool_addresses)` - Get balances for multiple pools
- `get_curve_gauge_balances_batch(gauge_addresses, user_address)` - Get staked balances for multiple gauges

**Integration Helpers:**
- `get_curve_pool_for_fx_pool(pool_key)` - Get Curve pool address from CONVEX_POOLS registry
- `get_curve_gauge_for_fx_pool(pool_key)` - Get Curve gauge address from CONVEX_POOLS registry

### 5. Constants to Add

```python
# In constants.py

# Curve Core Contracts
CURVE_REGISTRY = "0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5"
CURVE_META_REGISTRY = "0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC"
CURVE_ADDRESS_PROVIDER = "0x0000000022D53366457F9d5E68Ec105046FC4383"
CURVE_FACTORY_REGISTRY = "0x8F942C20D02bEfc377D41489daa13e357D4C4a9e"

# Curve Tokens
CRV_TOKEN = "0xD533a949740bb3306d119CC777fa900bA034cd52"

# Curve Pool Registry (for f(x) Protocol pools)
# Can be derived from CONVEX_POOLS entries with "curve_pool" field
CURVE_POOLS = {
    # Map pool_key to Curve pool address
    # Example: "eth_fxn_curve": "0xE06A65e09Ae18096B99770A809BA175FA05960e2"
}
```

### 6. Implementation Structure

Similar to Convex integration, create methods in `client.py`:

```python
# --- Curve Finance Methods ---

# Pool Information
def get_curve_pool_info(self, pool_address: str) -> Dict[str, Any]
def get_curve_pool_balances(self, pool_address: str) -> List[Decimal]
def get_curve_pool_virtual_price(self, pool_address: str) -> Decimal
def get_curve_swap_rate(self, pool_address: str, token_in: str, token_out: str, amount_in: Decimal) -> Decimal

# Swapping
def swap_on_curve(self, pool_address: str, token_in: str, token_out: str, amount_in: Decimal, min_amount_out: Decimal) -> str

# Liquidity
def add_liquidity_to_curve(self, pool_address: str, amounts: List[Decimal], min_lp_tokens: Decimal) -> str
def remove_liquidity_from_curve(self, pool_address: str, lp_amount: Decimal, min_amounts: List[Decimal]) -> str

# Gauge Operations
def stake_in_curve_gauge(self, gauge_address: str, lp_amount: Decimal) -> str
def unstake_from_curve_gauge(self, gauge_address: str, lp_amount: Decimal) -> str
def claim_curve_gauge_rewards(self, gauge_address: str) -> str
def get_curve_gauge_balance(self, gauge_address: str, user_address: Optional[str] = None) -> Decimal
def get_curve_gauge_rewards(self, gauge_address: str, user_address: Optional[str] = None) -> Dict[str, Decimal]
```

## Implementation Steps

### Phase 1: Core Infrastructure
1. ✅ Add Curve contract addresses to `constants.py`
2. ✅ Fetch/create ABIs for core contracts (pool, gauge, registry)
3. ✅ Create `CURVE_POOLS` registry mapping pool keys to Curve pool addresses
4. ✅ Implement basic read methods (pool info, balances, virtual price)

### Phase 2: Read Operations
1. ✅ Implement pool information queries
2. ✅ Implement gauge information queries
3. ✅ Implement swap rate calculations
4. ✅ Implement registry queries

### Phase 3: Write Operations
1. ✅ Implement token swapping
2. ✅ Implement liquidity operations (add/remove)
3. ✅ Implement gauge staking/unstaking
4. ✅ Implement reward claiming

### Phase 4: Helper Methods
1. ✅ Implement pool discovery methods
2. ✅ Implement batch operations
3. ✅ Implement APY calculations
4. ✅ Implement integration with existing CONVEX_POOLS registry

### Phase 5: Testing & Documentation
1. ✅ Create comprehensive test suite
2. ✅ Update documentation
3. ✅ Add usage examples
4. ✅ Integration testing with f(x) Protocol pools

## Key Differences from Convex Integration

### 1. No User-Specific Vaults
- Curve pools are **shared** (not user-specific)
- Gauges are **shared** (not user-specific)
- Simpler: no vault creation needed

### 2. Direct Pool Interaction
- Users interact directly with pool contracts
- No factory pattern for pools (pools are pre-deployed)
- Gauges are separate contracts (one per pool)

### 3. Multiple Pool Types
- Different pool types have slightly different ABIs
- Need to handle: Stable pools, Crypto pools, Tricrypto pools, Factory pools
- Registry helps identify pool type

### 4. Swap Calculations
- Need to calculate swap rates (slippage)
- Different functions for different pool types
- `exchange()` vs `exchange_underlying()` vs `exchange_multiple()`

## Estimated Complexity

**Similar to Convex Integration:**
- **ABIs**: ~5-6 ABIs needed (similar complexity)
- **Read Methods**: ~15-20 methods (similar to Convex)
- **Write Methods**: ~8-10 methods (similar to Convex)
- **Helper Methods**: ~5-8 methods (similar to Convex)
- **Tests**: ~25-30 tests (similar to Convex)
- **Total Methods**: ~30-40 methods

**Key Advantages:**
- No vault creation logic needed (simpler)
- Pool addresses already in constants (less discovery needed)
- Can leverage existing CONVEX_POOLS registry

## Dependencies

- **Web3.py**: Already in use
- **ABIs**: Need to fetch from Etherscan or Curve docs
- **No new external dependencies**: Uses existing infrastructure

## Next Steps

1. **Research**: Review Curve Finance documentation for exact contract addresses and ABIs
2. **ABI Collection**: Fetch ABIs for core contracts from Etherscan
3. **Constants**: Add Curve contract addresses to `constants.py`
4. **Implementation**: Start with read methods, then write methods
5. **Testing**: Create test suite similar to Convex integration
6. **Documentation**: Create comprehensive usage guide

## References

- [Curve Finance Documentation](https://docs.curve.finance/)
- [Curve Integration Guide](https://docs.curve.finance/integration/overview/)
- [Curve Contract Addresses](https://curve.readthedocs.io/ref-addresses.html)
- [Curve ABIs](https://github.com/curvefi/curve-contract/tree/master/contracts)

---

**Status**: Ready to begin implementation when approved. The structure is similar to Convex integration, making it a natural next step.

