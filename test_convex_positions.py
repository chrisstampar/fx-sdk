#!/usr/bin/env python3
"""
Test script to check Convex positions for specific wallet addresses.

Usage:
    python3 test_convex_positions.py
"""

import sys
import os
from decimal import Decimal

# Add parent directory to path to use local development code
# Must be first to override installed package
local_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if local_path not in sys.path:
    sys.path.insert(0, local_path)

# Remove fx_sdk from cache if already imported (to force reload from local code)
if 'fx_sdk' in sys.modules:
    del sys.modules['fx_sdk']
if 'fx_sdk.client' in sys.modules:
    del sys.modules['fx_sdk.client']
if 'fx_sdk.constants' in sys.modules:
    del sys.modules['fx_sdk.constants']
if 'fx_sdk.exceptions' in sys.modules:
    del sys.modules['fx_sdk.exceptions']
if 'fx_sdk.utils' in sys.modules:
    del sys.modules['fx_sdk.utils']

from fx_sdk import ProtocolClient, constants, utils

# Configuration
RPC_URL = "https://eth.llamarpc.com"

# Test address
# fxUSD V2 Stability Pool (Earns FXN) - Pool ID 37
VAULT_ADDRESS = "0x1234567890123456789012345678901234567890"

# Pool configuration for fxUSD V2 Stability Pool (Earns FXN)
POOL_ID = 37
POOL_KEY = "fxusd_stability_fxn"  # Key in CONVEX_POOLS registry
POOL_NAME = "fxUSD V2 Stability Pool (Earns FXN)"


def format_decimal(value, decimals=18):
    """Format Decimal value for display."""
    if value is None:
        return "N/A"
    if isinstance(value, Decimal):
        # Format with appropriate precision, removing trailing zeros
        if value >= 1:
            return f"{value:.2f}".rstrip('0').rstrip('.')
        else:
            return f"{value:.6f}".rstrip('0').rstrip('.')
    return str(value)


def check_vault_position(client, vault_address, pool_id, pool_name):
    """Check a specific vault position for fxUSD V2 Stability Pool (Earns FXN)."""
    print(f"\n{'='*70}")
    print(f"fxUSD V2 Stability Pool (Earns FXN) - Pool ID {pool_id}")
    print(f"Vault Address: {vault_address}")
    print(f"{'='*70}")
    
    try:
        # Get vault info
        print("\n📋 Vault Information:")
        vault_info = client.get_convex_vault_info(vault_address)
        # Note: get_convex_vault_info returns 'pid', not 'pool_id'
        vault_pool_id = vault_info.get('pid', vault_info.get('pool_id', 'N/A'))
        
        # Verify this is the correct pool
        if vault_pool_id != pool_id and vault_pool_id != 'N/A':
            print(f"  ⚠️  WARNING: Vault pool ID ({vault_pool_id}) doesn't match expected ({pool_id})")
        
        print(f"  • Pool: {pool_name}")
        print(f"  • Pool ID: {vault_pool_id}")
        print(f"  • Owner: {vault_info.get('owner', 'N/A')}")
        print(f"  • Staking Token: {vault_info.get('staking_token', 'N/A')}")
        print(f"  • Gauge Address: {vault_info.get('gauge_address', 'N/A')}")
        print(f"  • Rewards Contract: {vault_info.get('rewards', vault_info.get('rewards_contract', 'N/A'))}")
        
        # Get pool info from registry
        try:
            pool_info = client.get_convex_pool_info(pool_id=pool_id)
            if pool_info:
                print(f"  • Pool Name: {pool_info.get('name', 'N/A')}")
                print(f"  • Earns: {pool_info.get('earns', 'N/A')}")
                print(f"  • Redeems To: {pool_info.get('redeems_to', 'N/A')}")
        except:
            pass
        
        # Get vault balance
        print("\n💰 Vault Balance (fxBASE LP tokens staked):")
        balance = client.get_convex_vault_balance(vault_address)
        # get_convex_vault_balance already returns a Decimal, not Wei
        print(f"  • Staked Amount: {format_decimal(balance)} fxBASE LP tokens")
        
        # Get vault rewards
        print("\n🎁 Claimable Rewards:")
        try:
            rewards_data = client.get_convex_vault_rewards(vault_address)
            # get_convex_vault_rewards returns a dict with 'amounts' key
            rewards = rewards_data.get('amounts', {}) if isinstance(rewards_data, dict) else rewards_data
            
            if rewards:
                for token_address, amount in rewards.items():
                    # Try to get token symbol
                    try:
                        token_contract = client._get_contract("erc20", token_address)
                        symbol = token_contract.functions.symbol().call()
                        
                        # amount is already a Decimal from get_convex_vault_rewards
                        if isinstance(amount, Decimal):
                            amount_decimal = amount
                        else:
                            # Fallback if it's not a Decimal
                            decimals = token_contract.functions.decimals().call()
                            amount_decimal = utils.wei_to_decimal(amount, decimals)
                        
                        print(f"  • {symbol}: {format_decimal(amount_decimal)}")
                    except Exception as e:
                        # Fallback if we can't get symbol
                        if isinstance(amount, Decimal):
                            amount_decimal = amount
                        else:
                            amount_decimal = utils.wei_to_decimal(amount, 18)
                        print(f"  • {token_address}: {format_decimal(amount_decimal)}")
            else:
                print("  • No claimable rewards")
        except Exception as e:
            print(f"  ⚠️  Error getting rewards: {e}")
            import traceback
            traceback.print_exc()
        
        # APY calculation removed in v0.3.0 - refer to Convex website for official APY values
        
        return {
            'vault_address': vault_address,
            'balance': balance,  # Already a Decimal from get_convex_vault_balance
            'rewards': rewards,
            'info': vault_info
        }
        
    except Exception as e:
        print(f"\n❌ Error checking vault: {e}")
        return None


def main():
    """Main test function."""
    print("="*70)
    print("Convex Positions Test Script")
    print("="*70)
    print(f"\nRPC URL: {RPC_URL}")
    print(f"\nTarget Pool: {POOL_NAME}")
    print(f"Pool ID: {POOL_ID}")
    print(f"Vault Address: {VAULT_ADDRESS}")
    
    try:
        # Initialize client (read-only mode)
        client = ProtocolClient(RPC_URL)
        print("\n✅ Client initialized (read-only mode)")
        
        # Check specific vault for fxUSD V2 Stability Pool (Earns FXN)
        print("\n" + "="*70)
        print(f"CHECKING {POOL_NAME.upper()}")
        print("="*70)
        vault_result = check_vault_position(client, VAULT_ADDRESS, POOL_ID, POOL_NAME)
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"✅ Vault check: {'Success' if vault_result else 'Failed'}")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

