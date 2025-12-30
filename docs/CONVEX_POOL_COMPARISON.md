# Convex Pool Comparison Analysis

**Created:** December 22, 2025

## Pool Comparison

### fxUSD V2 Stability Pool (Pool ID 37)
- **F(x) Gauge**: `0x215D87bd3c7482E2348338815E059DE07Daf798A`
- **Staked Token**: fxBASE (`0x65C9A641afCEB9C0E6034e558A319488FA0FA3be`)
- **Base Token**: fxUSD (`0x085780639cc2cacd35e474e71f4d000e2405d8f6`)
- **Convex Pool ID**: 37
- **Vault Example**: `0x1234567890123456789012345678901234567890`

### fETH Stability Pool (Pool ID 1)
- **F(x) Stability Pool**: `0xB87A8332dFb1C76Bb22477dCfEdDeB69865cA9f9`
- **Staked Token**: fETH (`0x53805A76E1f5ebbFE7115F16f9c87C2f7e633726`)
- **Base Token**: stETH (`0xae7ab96520de3a18e5e111b5eaab095312d7fe84`)
- **Convex Pool ID**: 1
- **Vault Example**: `0x83bddc646956C31a081b8B67cb035046fC5f24Bb`

## Analysis

### ✅ Common Elements (Generic)

1. **Same Factory Contract**: Both use `0xAffe966B27ba3E4Ebb8A0eC124C7b7019CC762f8`
2. **Same Vault Structure**: Both create user-specific vaults with the same ABI
3. **Same Creation Process**: Both use `createVault(uint256 _pid)` with pool ID
4. **Same Operations**: Deposit, withdraw, claim rewards work the same way

### 🔄 Pool-Specific Elements

1. **Pool ID**: Different (37 vs 1)
2. **Tokens**: Different staked/base tokens
3. **Gauge/Stability Pool**: Different addresses (but vault handles this internally)

## Conclusion

**✅ The functions are already generic!**

All current functions accept:
- `pool_id` as a parameter (works for any pool)
- `vault_address` as a parameter (user-specific, works for any pool)

The vault contract itself handles pool-specific details internally (it knows its pool ID and tokens).

### What We Need

1. **Update CONVEX_POOLS registry** - Add all pools with their metadata
2. **Keep functions generic** - They already work for any pool
3. **Optional: Add pool-specific helpers** - Convenience methods that use the registry

### Recommendation

**Keep the generic approach** - no need for separate functions per pool. The current implementation is correct:
- `create_convex_vault(pool_id)` - Works for any pool
- `deposit_to_convex_vault(vault_address, amount)` - Works for any vault
- `get_convex_vault_address(user_address, pool_id)` - Works for any pool

The only pool-specific data needed is:
- Pool ID (passed as parameter)
- Token addresses (retrieved from vault via `stakingToken()`)
- Gauge/Stability pool addresses (stored in registry for reference)

---

**Status**: Functions are generic and work for all pools! ✅

