# f(x) Protocol SDK Features

**Creator:** Christopher Stampar (@cstampar)  
**Date:** December 20, 2025  
**Last Updated:** December 22, 2025  
**Current Version:** 0.3.0

This document tracks the unique features and capabilities of the f(x) Protocol Python SDK.

## Core SDK Features

- **Class-Based Architecture**: Centralized `ProtocolClient` manages Web3 connections, account signing, and contract orchestration.
- **Secure Multi-Source Authentication**: Production-ready credential management with automatic discovery from multiple secure sources:
  - **Environment Variables**: `FX_PROTOCOL_PRIVATE_KEY` for production deployments
  - **`.env` Files**: Automatic loading for local development (with `.gitignore` protection)
  - **Google Colab Secrets**: Native integration with Colab's `userdata` API
  - **Browser Wallet Support**: Connect to MetaMask and other browser extensions via `use_browser_wallet=True`
  - **Read-Only Mode**: Full protocol querying capabilities without any credentials
  - **Priority-Based Discovery**: Automatically checks sources in security-optimal order
- **High-Precision Data Normalization**: 
  - Automatic `Wei-to-Decimal` and `Decimal-to-Wei` conversion for all inputs and outputs.
  - Uses Python's `Decimal` type to prevent floating-point precision errors in financial calculations.
- **Integrated Logging**: Production-grade logging via the standard `logging` library for transparent operation tracking and debugging.
- **Robust Error Handling**: Custom exception hierarchy (`FXProtocolError`, `TransactionFailedError`, `InsufficientBalanceError`, etc.) for clear, actionable error reporting.
- **Graceful ABI Loading**: Advanced contract loader that handles missing or empty ABI files, allowing the client to operate in "partial" mode while the `/abis` directory is being populated.
- **Modular Design**: Clear separation between "Read" (call) and "Write" (send) operations.

## Protocol Coverage

### V2 Core & Extensions
- **fxUSD Ecosystem**:
  - Full support for `fxUSD` balance and total supply tracking.
  - Integration with the `fxUSD_BasePool` for asset and supply metrics.
- **xPOSITION Ecosystem**:
  - Direct management of leveraged positions via the Pool Manager (`operate`, `rebalance`, `liquidate`).
  - Native support for primary collateral: `stETH`, `wstETH`, `frxETH`, `sfrxETH`.
  - Advanced position and peg discovery via `get_position_info` and `get_peg_keeper_info`.
- **Savings & Stability**:
  - `fxSAVE` (Saving fxUSD): Balance tracking, APR fetching, and deposit/redeem logic.
  - `fxSP` (Stability Pool): Staking and withdrawal management for the fxUSD stability layer.

### V1 Legacy Support
- **Full Asset Portability**:
  - Native support for legacy tokens: `fETH`, `rUSD`, `btcUSD`, `cvxUSD`, and `arUSD`.
  - Complete xToken coverage: `xETH`, `xCVX`, `xWBTC`, `xeETH`, `xezETH`, `xstETH`, `xfrxETH`.
- **Market Insights**: NAV (Net Asset Value) and Collateral Ratio metrics for V1 markets.
- **Rebalance Pool Management**: Dynamic discovery of V1 rebalance pools via the `RebalancePoolRegistry`, with full support for staking (`deposit`), unlocking, and reward claiming.

### Governance & Utility
- **veFXN Staking**: Logic for locking FXN into veFXN to gain voting power, including expiration tracking.
- **Gauge Ecosystem**: 
  - Fetching gauge weights from the `GaugeController`.
  - Voting for gauge weight allocations.
  - Claimable reward tracking and global reward claiming from any `LiquidityGauge`.
- **Vesting Claims**: Specialized methods for claiming vested `FXN`, `fETH`, and `fxUSD`.

## Infrastructure & Analytics
- **V2 Pool Manager**: Comprehensive control over V2 positions, including `operate`, `rebalance`, and `liquidate` methods.
- **Reserve Pool & Treasury**: Interface with protocol reserves and V1 stETH Treasury for NAV tracking and bonus requests.
- **Oracle Integration**: Direct price fetching from the `stETH_PriceOracle`.
- **Advanced Routing**: Support for complex token swaps using the `MultiPathConverter`.
- **Gateway Interactions**: Streamlined ETH/stETH deposits via the `stETH_Gateway` using `mint_f_token_via_gateway` and `mint_x_token_via_gateway`.
- **Flash Loan Support**: Native ERC-3156 flash loan integration via the Pool Manager.

## Convex Finance Integration

### Vault Management
- **User-Specific Vault Creation**: Create Convex vaults for any pool using `create_convex_vault(pool_id)`
- **Automatic Vault Address Extraction**: Attempts to extract vault address from transaction receipts after creation
- **Vault Address Discovery**: Query user vault addresses by wallet address and pool ID via `get_convex_vault_address()`
- **Transaction-Based Lookup**: Extract vault addresses from transaction hashes using `get_convex_vault_address_from_tx()`
- **Helper Methods**: `get_convex_vault_address_or_create()` for automatic vault creation workflow

### Vault Operations
- **Deposit Management**: `deposit_to_convex_vault()` with automatic token approval checking and execution
- **Withdrawal Support**: `withdraw_from_convex_vault()` with balance validation before transaction
- **Reward Claiming**: `claim_convex_vault_rewards()` with support for selective token claiming
- **Balance Queries**: `get_convex_vault_balance()` for staked token balances (read-only, no private key needed)
- **Reward Tracking**: `get_convex_vault_rewards()` returns claimable rewards with proper decimal conversion
- **Vault Information**: `get_convex_vault_info()` provides complete vault metadata (owner, pool ID, staking token, gauge, rewards contract)

### Convex Pool Registry
- **Comprehensive Pool Database**: `CONVEX_POOLS` registry with 30+ f(x) Protocol related pools
- **Pool Types Supported**:
  - Stability Pools (fxUSD, fETH, rUSD, btcUSD, cvxUSD) with multiple redemption options
  - Curve LP Pools (ETH/FXN, FXN/cvxFXN, FXN/sdFXN, and 20+ fxUSD pairs)
- **Pool Metadata**: Each pool includes pool ID, name, staked token, base token, redemption asset, gauge address, and Convex URL
- **Pool Differentiation**: Clear naming with redemption asset indicators (e.g., "fETH Stability Pool (Redeems to xETH)")

### cvxFXN Staking
- **FXN to cvxFXN Conversion**: `deposit_fxn_to_cvxfxn()` with automatic FXN approval
- **cvxFXN Staking**: `stake_cvxfxn()` to stake cvxFXN tokens for additional rewards
- **Unstaking**: `unstake_cvxfxn()` to withdraw staked cvxFXN
- **Reward Management**: `claim_cvxfxn_staking_rewards()` to claim staking rewards
- **Balance Queries**: 
  - `get_cvxfxn_balance()` for cvxFXN token balance
  - `get_staked_cvxfxn_balance()` for staked cvxFXN balance
  - `get_cvxfxn_staking_rewards()` for claimable rewards
- **Staking Information**: `get_cvxfxn_staking_info()` provides reward rate, period finish, and other staking parameters

### Error Handling & Validation
- **Address Validation**: All methods validate vault and token addresses before operations
- **Balance Validation**: Automatic balance checks before deposits and withdrawals to prevent failed transactions
- **Vault Existence Checks**: Verifies vault addresses exist and are valid before operations
- **Automatic Approvals**: Deposit methods automatically check and approve tokens if needed
- **Clear Error Messages**: Descriptive exceptions (`ContractCallError`, `InsufficientBalanceError`, `FXProtocolError`) for actionable debugging
- **Private Key Validation**: Write operations validate authentication before attempting transactions

### Read-Only Support
- **No Private Key Required**: All query methods (`get_convex_vault_info`, `get_convex_vault_balance`, `get_convex_vault_rewards`) work without authentication
- **Public Data Access**: Query any user's vault information, balances, and rewards
- **Event-Based Queries**: Vault address discovery via blockchain event queries

### Helper Methods & Batch Operations
- **Multi-Vault Queries**: `get_all_user_vaults()` discovers all vault addresses for a user across all 37+ pools
- **Pool Information**: `get_convex_pool_info()` retrieves pool metadata by ID or key, `get_all_convex_pools()` lists all pools
- **Batch Balance Queries**: `get_vault_balances_batch()` queries multiple vault balances efficiently
- **Batch Reward Queries**: `get_vault_rewards_batch()` queries multiple vault rewards efficiently
- **Comprehensive Summaries**: `get_user_vaults_summary()` provides complete overview of all user vaults with balances and rewards

### APY Calculation (Removed in v0.3.0)
- **Removed Methods**: All APY calculation methods have been removed in v0.3.0:
  - `get_convex_pool_apy()` - Removed
  - `get_convex_vault_apy()` - Removed
  - `get_all_convex_pools_apy()` - Removed
- **Reason**: Convex APY calculations require historical data and multiple sources that are difficult to accurately replicate on-chain. The calculated values often differed from Convex's displayed APY due to different calculation methods, multiple reward sources, and off-chain data.
- **Alternative**: Users should refer to Convex Finance website (https://fx.convexfinance.com/) for official APY values, which include all reward sources and historical data.
- **Impact**: `get_convex_pool_statistics()` no longer includes APY data, but all other functionality remains intact.

### Pool Information Queries
- **Comprehensive Details**: `get_convex_pool_details()` combines registry data with live on-chain information
- **TVL Queries**: `get_convex_pool_tvl()` and `get_all_convex_pools_tvl()` for Total Value Locked data
- **Reward Tokens**: `get_convex_pool_reward_tokens()` retrieves reward token addresses
- **Gauge Addresses**: `get_convex_pool_gauge_address()` gets gauge contract addresses
- **Pool Statistics**: `get_convex_pool_statistics()` provides comprehensive stats combining details and TVL
- **Live Data**: All queries fetch real-time data from Convex Booster and BaseRewardPool contracts
- **Contract Addresses**: Access to all relevant contract addresses (lptoken, token, gauge, crvRewards, stash)

## Curve Finance Integration

The SDK provides comprehensive integration with Curve Finance, enabling direct interaction with Curve pools for swapping, liquidity management, and gauge staking.

### Pool Information & Discovery
- **Pool Information**: `get_curve_pool_info()` retrieves comprehensive pool data (coins, balances, virtual price, LP token)
- **Pool Discovery**: `find_curve_pool()` finds pools by token pair, `get_curve_pool_from_lp_token()` finds pools from LP tokens
- **Balance Queries**: `get_curve_pool_balances()` and `get_curve_pool_virtual_price()` for real-time pool metrics
- **Swap Rate Calculation**: `get_curve_swap_rate()` calculates output amounts before executing swaps
- **Registry Support**: Automatic fallback between Meta Registry and Main Registry for maximum pool coverage

### Swap Operations
- **Token Swaps**: `curve_swap()` executes swaps with automatic token approvals and slippage protection (default 0.5%)
- **Slippage Control**: Optional `min_amount_out` parameter for custom slippage tolerance
- **Multi-Token Support**: Works with any token pair in supported Curve pools

### Liquidity Management
- **Add Liquidity**: `curve_add_liquidity()` deposits tokens and receives LP tokens with automatic approvals
- **Remove Liquidity**: `curve_remove_liquidity()` burns LP tokens and receives underlying tokens
- **Slippage Protection**: Default 0.5% tolerance with optional custom minimums
- **Multi-Token Pools**: Supports 2-coin pools (most f(x) Protocol pools)

### Gauge Staking & Rewards
- **Gauge Information**: `get_curve_gauge_info()` provides gauge details (LP token, rewards, total staked)
- **Stake LP Tokens**: `curve_stake_lp_tokens()` stakes LP tokens in gauges to earn CRV rewards
- **Unstake LP Tokens**: `curve_unstake_lp_tokens()` unstakes LP tokens with optional reward claiming
- **Reward Tracking**: `get_curve_gauge_rewards()` returns claimable rewards for all reward tokens
- **Claim Rewards**: `curve_claim_gauge_rewards()` claims CRV and other reward tokens
- **Balance Queries**: `get_curve_gauge_balance()` for staked LP token balances (read-only)
- **Gauge Discovery**: `get_curve_gauge_from_pool()` finds gauge addresses from pool addresses

### Read-Only Support
- **No Private Key Required**: All query methods work without authentication
- **Public Data Access**: Query any pool or gauge information for any address
- **Balance Tracking**: Monitor staked balances and rewards for any wallet address

### Integration with f(x) Protocol
- **Pool Registry**: All f(x) Protocol Curve pools documented in `CONVEX_POOLS` registry
- **Gauge Addresses**: f(x) Protocol gauge addresses stored as `fx_gauge` in pool metadata
- **LP Token Tracking**: LP token addresses available for all Curve pools
- **Pool Types**: Automatic identification of Curve LP pools via `pool_type: "curve_lp"`

### Helper Methods
- **Registry Queries**: `get_curve_pools_from_registry()` and `get_curve_pool_from_registry()` for accessing pool metadata
- **Batch Operations**: `get_curve_gauge_balances_batch()` and `get_curve_gauge_rewards_batch()` for efficient multi-gauge queries
- **Position Summary**: `get_user_curve_positions_summary()` provides comprehensive overview of all user Curve positions

### APY Calculation (Removed in v0.3.0)
- **Removed Methods**: All APY calculation methods have been removed in v0.3.0:
  - `get_curve_gauge_apy()` - Removed
  - `get_all_curve_gauges_apy()` - Removed
- **Reason**: Curve APY calculations require historical data and multiple sources that are difficult to accurately replicate on-chain.
- **Alternative**: Users should refer to Curve Finance website for official APY values, which include all reward sources and historical data.

## Developer Tools

- **Address Registry**: Centralized `constants.py` with verified addresses for all protocol contracts (V1 and V2) plus Convex Finance and Curve Finance contracts
- **Comprehensive Balance Aggregator**: `get_all_balances()` and `get_all_gauge_balances()` methods to fetch human-readable snapshots of all protocol-related assets in a single call. Supports 13+ protocol tokens including all x tokens (xETH, xCVX, xWBTC, xeETH, xezETH, xstETH, xfrxETH).
- **Production-Grade Testing**: Fully mocked unit tests in `tests.py`, `test_convex.py`, and `test_curve.py` covering infrastructure, tuple parsing, complex transaction flows, Convex integration, and Curve integration
- **Package Verification**: `test_package_v0.3.0.py` - Comprehensive test script to verify package installation and functionality after PyPI upload
- **Pythonic Interface**: Type hinting (Python 3.9+) and Google-style docstrings for superior IDE support and autocompletion
- **Security-First Design**: Built-in `.gitignore` templates and authentication best practices to prevent accidental credential exposure in version control
- **Comprehensive Test Coverage**: Unit tests for Convex vault operations, cvxFXN staking, Curve operations, error handling, and edge cases
- **Release Documentation**: Complete release process documentation including `RELEASE_CHECKLIST.md`, `UPLOAD_INSTRUCTIONS.md`, `PYPI_AUTH_GUIDE.md`, and `VERIFY_UPLOAD.md`

## Version History

### v0.3.0 (December 22, 2025)
- **Removed**: All APY calculation methods (5 methods total) due to complexity and accuracy issues
- **Changed**: `get_convex_pool_statistics()` no longer includes APY data
- **Reason**: APY calculations require historical data and multiple sources that are difficult to accurately replicate on-chain. Users should refer to Convex/Curve websites for official APY values.
- **Status**: Successfully released to PyPI

### v0.2.0 (December 22, 2025)
- **Added**: Complete Convex Finance integration (22 methods)
- **Added**: Complete Curve Finance integration (22 methods)
- **Added**: 37 Convex pools in registry
- **Added**: cvxFXN staking functionality
- **Added**: Batch operations and helper methods
- **Added**: Comprehensive test suites (52 new tests)

### v0.1.0 (December 20, 2025)
- **Initial Release**: Core f(x) Protocol V1 and V2 support
- **Added**: Secure multi-source authentication
- **Added**: High-precision Decimal handling
- **Added**: Comprehensive test suite
