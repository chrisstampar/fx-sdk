# Pendle Finance Integration Plan

**Created:** December 22, 2025  
**Status:** 📋 Planning Phase

## Overview

This document outlines the integration plan for Pendle Finance with the fxSAVE pool. Pendle is a DeFi protocol that allows users to tokenize and trade future yield. Users can deposit yield-bearing assets (like fxSAVE) and split them into Principal Tokens (PT) and Yield Tokens (YT), enabling advanced yield strategies.

## Current State

### Existing fxSAVE Support
- **fxSAVE Contract**: `0x7743e50F534a7f9F1791DdE7dCD89F7783Eefc39`
- **Current Methods**:
  - `get_fxsave_balance()` - Get fxSAVE balance
  - `get_savings_apr()` - Get current APR
  - `deposit_fxsave()` - Deposit fxUSD into fxSAVE
  - `redeem_fxsave()` - Redeem fxUSD from fxSAVE

### Pendle Integration Goals
- Deposit fxSAVE into Pendle
- Split fxSAVE into PT (Principal Token) and YT (Yield Token)
- Stake PT/YT tokens in Pendle markets
- Claim yield from YT tokens
- Query PT/YT balances and yields
- Swap between PT and YT tokens

## Required Components

### 1. Core Pendle Contracts

#### Main Pendle Contracts (Ethereum Mainnet)
```python
# Core Pendle Contracts (addresses to be confirmed)
PENDLE_ROUTER = "0x..."  # Pendle Router for swaps and operations
PENDLE_MARKET_FACTORY = "0x..."  # Factory for creating markets
PENDLE_ROUTER_V2 = "0x..."  # V2 Router (if applicable)

# fxSAVE Pendle Market (addresses to be confirmed)
PENDLE_FXSAVE_MARKET = "0x..."  # Pendle market for fxSAVE
PENDLE_FXSAVE_PT = "0x..."  # Principal Token for fxSAVE
PENDLE_FXSAVE_YT = "0x..."  # Yield Token for fxSAVE
```

### 2. Required ABIs

#### Essential ABIs to Create/Fetch

1. **pendle_router.json** - Pendle Router ABI
   - Functions: `swapExactTokenForPt()`, `swapExactTokenForYt()`, `addLiquidity()`, `removeLiquidity()`
   - Address: `PENDLE_ROUTER` or `PENDLE_ROUTER_V2`

2. **pendle_market.json** - Pendle Market ABI
   - Functions: `readTokens()`, `readState()`, `getRewardTokens()`, `claimRewards()`
   - Address: Market-specific (fxSAVE market)

3. **pendle_pt_token.json** - Principal Token ABI
   - Functions: Standard ERC20 + Pendle-specific functions
   - Address: `PENDLE_FXSAVE_PT`

4. **pendle_yt_token.json** - Yield Token ABI
   - Functions: Standard ERC20 + `claimRewards()`, `getUnclaimedRewards()`
   - Address: `PENDLE_FXSAVE_YT`

5. **pendle_router_v2.json** - Pendle Router V2 ABI (if using V2)
   - Functions: Similar to V1 but with updated interface

### 3. Core Functionality to Implement

#### Read Methods (No Private Key Required)

**Market Information:**
- `get_pendle_market_info(market_address)` - Get market details (PT, YT, expiry, etc.)
- `get_pendle_market_state(market_address)` - Get current market state (reserves, rates)
- `get_pendle_pt_balance(pt_address, user_address)` - Get PT token balance
- `get_pendle_yt_balance(yt_address, user_address)` - Get YT token balance
- `get_pendle_yt_rewards(yt_address, user_address)` - Get claimable yield from YT
- `get_pendle_swap_rate(market_address, token_in, token_out, amount_in)` - Calculate swap rate

**Market Discovery:**
- `find_pendle_fxsave_markets()` - Discover all active fxSAVE markets from Pendle registry
- `get_active_pendle_fxsave_market()` - Get the most recent active fxSAVE market
- `get_pendle_fxsave_market_by_expiry(expiry_date)` - Get market by expiry date
- `get_all_pendle_fxsave_markets()` - Get all known fxSAVE markets from registry

**fxSAVE Specific:**
- `get_pendle_fxsave_market_info(market_address=None)` - Get fxSAVE Pendle market information (auto-discovers if None)
- `get_pendle_fxsave_pt_balance(user_address, market_address=None)` - Get fxSAVE PT balance
- `get_pendle_fxsave_yt_balance(user_address, market_address=None)` - Get fxSAVE YT balance
- `get_pendle_fxsave_yt_rewards(user_address, market_address=None)` - Get claimable yield from fxSAVE YT

#### Write Methods (Requires Private Key)

**Swapping:**
- `pendle_swap_fxsave_for_pt(amount_fxsave, min_pt_out)` - Swap fxSAVE for PT
- `pendle_swap_fxsave_for_yt(amount_fxsave, min_yt_out)` - Swap fxSAVE for YT
- `pendle_swap_pt_for_fxsave(amount_pt, min_fxsave_out)` - Swap PT for fxSAVE
- `pendle_swap_yt_for_fxsave(amount_yt, min_fxsave_out)` - Swap YT for fxSAVE

**Liquidity:**
- `pendle_add_liquidity(market_address, amount_pt, amount_yt, min_lp_out)` - Add liquidity to Pendle market
- `pendle_remove_liquidity(market_address, lp_amount, min_pt_out, min_yt_out)` - Remove liquidity

**Yield Claiming:**
- `pendle_claim_yt_rewards(yt_address, receiver)` - Claim yield from YT token
- `pendle_claim_market_rewards(market_address, receiver)` - Claim rewards from market

**fxSAVE Specific:**
- `pendle_swap_fxsave_for_pt(amount_fxsave, min_pt_out, market_address=None)` - Swap fxSAVE for PT (auto-discovers market)
- `pendle_claim_fxsave_yt_rewards(receiver, market_address=None)` - Claim yield from fxSAVE YT (auto-discovers market)

**Note**: All fxSAVE-specific methods accept optional `market_address` parameter. If not provided, they automatically discover the active market.

### 4. Helper Methods

- `get_pendle_fxsave_position_summary(user_address)` - Get comprehensive summary of user's Pendle fxSAVE position
- `get_pendle_apy(market_address, reward_token_price)` - Calculate APY for Pendle market
- `get_pendle_fxsave_apy(reward_token_price)` - Calculate APY for fxSAVE Pendle market

## Implementation Phases

### Phase 1: Core Infrastructure & Market Discovery
1. Add Pendle contract addresses to `constants.py`
2. Create `PENDLE_FXSAVE_MARKETS` registry in `constants.py` with expiry tracking
3. Create/fetch required ABIs (including Pendle Registry if available)
4. Implement market discovery methods
5. Implement basic read methods (market info, balances, rewards)
6. Add tests for read methods and market discovery

### Phase 2: Swap Operations
1. Implement swap methods (fxSAVE ↔ PT, fxSAVE ↔ YT)
2. Add slippage protection
3. Implement automatic approvals
4. Add tests for swap operations

### Phase 3: Liquidity & Rewards
1. Implement liquidity methods (add/remove)
2. Implement reward claiming methods
3. Add tests for liquidity and rewards

### Phase 4: Helper Methods
1. Implement position summary methods
2. Implement APY calculation methods
3. Add batch query methods
4. Add tests for helper methods

### Phase 5: Documentation
1. Create comprehensive usage guide
2. Update `features.md`
3. Add examples and workflows

## Key Differences from Convex/Curve

1. **Token Splitting**: Pendle splits yield-bearing tokens into PT and YT
2. **Market-Based**: Operations are market-specific (fxSAVE market)
3. **Expiry Dates**: PT tokens have expiry dates (when they mature) ⚠️ **CRITICAL**
4. **Yield Tokens**: YT tokens represent future yield and can be claimed
5. **Liquidity Pools**: Pendle markets have their own liquidity pools
6. **Market Expiration**: Markets expire and new ones are created - requires dynamic discovery

## ⚠️ Critical Challenge: Market Expiration

Pendle markets have expiry dates. When a market expires:
- The market becomes inactive
- New markets are created for the same underlying asset (fxSAVE)
- Users need to migrate to new markets
- Old market addresses become invalid

### Solution Approaches

#### Option 1: Registry with Active Market Tracking (Recommended)
- Maintain a registry in `constants.py` that tracks active fxSAVE markets
- Include expiry dates in registry entries
- Provide helper methods to find active markets
- Allow manual updates when new markets are created

**Pros:**
- Simple to implement
- Fast lookups
- Can include metadata (expiry, APY, etc.)

**Cons:**
- Requires manual updates when markets expire
- Need to track expiry dates

#### Option 2: Dynamic Discovery via Pendle Registry
- Query Pendle's registry/factory contracts to find active markets
- Filter by underlying asset (fxSAVE)
- Filter by expiry date (only active markets)
- Cache results for performance

**Pros:**
- Always up-to-date
- No manual maintenance
- Handles new markets automatically

**Cons:**
- More complex implementation
- Requires Pendle registry ABI
- Slower (on-chain queries)
- May need caching strategy

#### Option 3: Hybrid Approach (Best of Both)
- Maintain a registry in `constants.py` for known markets
- Provide discovery methods to find new markets
- Helper methods prioritize registry, fall back to discovery
- Allow users to specify market addresses directly

**Pros:**
- Fast for known markets (registry)
- Flexible for new markets (discovery)
- User can override with specific address
- Best user experience

**Cons:**
- More complex implementation
- Need both registry and discovery logic

### Recommended Implementation: Hybrid Approach

```python
# In constants.py
PENDLE_FXSAVE_MARKETS = {
    "2025-12-31": {  # Expiry date as key
        "market": "0x...",
        "pt": "0x...",
        "yt": "0x...",
        "expiry": 1735689600,  # Unix timestamp
        "active": True
    },
    # ... more markets
}

# Helper methods
def get_active_pendle_fxsave_market() -> Optional[str]:
    """Get the most recent active fxSAVE market."""
    # Check registry first, then discovery
    
def find_pendle_fxsave_markets() -> List[Dict[str, Any]]:
    """Discover all active fxSAVE markets from Pendle registry."""
    # Query Pendle registry for fxSAVE markets
    
def get_pendle_fxsave_market_by_expiry(expiry_date: str) -> Optional[str]:
    """Get market by expiry date."""
    # Lookup in registry
```

### User-Facing API Design

**Option A: Auto-Discovery (Easiest for Users)**
```python
# Automatically finds active market
client.pendle_swap_fxsave_for_pt(amount_fxsave=Decimal("100.0"))
```

**Option B: Explicit Market (Most Control)**
```python
# User specifies market address
client.pendle_swap_fxsave_for_pt(
    amount_fxsave=Decimal("100.0"),
    market_address="0x..."  # Optional, auto-discovers if not provided
)
```

**Option C: Expiry-Based (Clear Intent)**
```python
# User specifies expiry date
client.pendle_swap_fxsave_for_pt(
    amount_fxsave=Decimal("100.0"),
    expiry_date="2025-12-31"  # Optional, uses latest if not provided
)
```

### Migration Strategy

When a market expires:
1. **Documentation**: Update docs with new market addresses
2. **Registry Update**: Add new market to `PENDLE_FXSAVE_MARKETS`
3. **Deprecation Warning**: Mark old market as inactive
4. **Helper Methods**: `get_active_pendle_fxsave_market()` automatically returns new market
5. **User Notification**: Users can check expiry dates before operations

## Questions to Resolve

1. **Contract Addresses**: Need confirmed addresses for:
   - Pendle Router (V1 or V2?)
   - Pendle Registry/Factory (for market discovery)
   - Current fxSAVE Pendle Market(s)
   - Current fxSAVE PT Token(s)
   - Current fxSAVE YT Token(s)

2. **ABIs**: Do we have access to Pendle ABIs, or do we need to fetch from Etherscan?

3. **Market Expiry**: What is the expiry date for the current fxSAVE Pendle market?

4. **Yield Source**: What yield does fxSAVE YT token claim from? (fxSAVE APR?)

5. **Router Version**: Are we using Pendle Router V1 or V2?

6. **Market Discovery**: Does Pendle have a registry contract we can query for active markets?

7. **Multiple Markets**: Are there typically multiple active fxSAVE markets at once, or just one?

## Next Steps

1. **Gather Information**: Get contract addresses and ABIs from user
2. **Verify Contracts**: Confirm addresses on Etherscan
3. **Create ABIs**: Fetch or create ABIs for Pendle contracts
4. **Implement Phase 1**: Start with core infrastructure and read methods
5. **Test & Iterate**: Test each phase before moving to the next

## References

- Pendle Finance Documentation: https://docs.pendle.finance/
- Pendle Contracts: https://github.com/pendle-finance/pendle-core-v2-public
- Pendle Etherscan: https://etherscan.io/address/[PENDLE_ROUTER]

