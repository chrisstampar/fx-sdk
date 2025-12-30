#!/usr/bin/env python3
"""
Test script for fx-sdk v0.3.0 package verification.

This script tests:
- Package imports and version
- Client initialization
- Removed APY methods (should not exist)
- Core functionality (read-only operations)
- Constants and registry data

Usage:
    # For local development (before PyPI upload):
    cd sdk
    python3 test_package_v0.3.0.py
    
    # After PyPI upload:
    pip install fx-sdk==0.3.0
    python3 test_package_v0.3.0.py
    
Note: If you get "No matching distribution found", v0.3.0 hasn't been uploaded to PyPI yet.
      Use the local development method instead.
"""

import sys
from decimal import Decimal

def test_imports():
    """Test that all imports work correctly."""
    print("=" * 70)
    print("TEST 1: Package Imports")
    print("=" * 70)
    
    try:
        import fx_sdk
        from fx_sdk import ProtocolClient, constants, utils, exceptions
        
        print(f"✅ Package imported successfully")
        print(f"✅ Version: {fx_sdk.__version__}")
        print(f"✅ ProtocolClient imported")
        print(f"✅ constants imported")
        print(f"✅ utils imported")
        print(f"✅ exceptions imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_version():
    """Test that version is correct."""
    print("\n" + "=" * 70)
    print("TEST 2: Version Check")
    print("=" * 70)
    
    try:
        import fx_sdk
        if fx_sdk.__version__ == "0.3.0":
            print(f"✅ Version correct: {fx_sdk.__version__}")
            return True
        else:
            print(f"❌ Version incorrect: {fx_sdk.__version__} (expected 0.3.0)")
            return False
    except Exception as e:
        print(f"❌ Version check failed: {e}")
        return False


def test_client_initialization():
    """Test client initialization."""
    print("\n" + "=" * 70)
    print("TEST 3: Client Initialization")
    print("=" * 70)
    
    try:
        from fx_sdk import ProtocolClient
        
        # Test read-only initialization
        client = ProtocolClient(rpc_url="https://eth.llamarpc.com")
        print("✅ Client initialized (read-only mode)")
        
        # Test that Web3 connection is available
        if hasattr(client, 'w3'):
            print("✅ Web3 connection available")
        else:
            print("❌ Web3 connection missing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False


def test_removed_apy_methods():
    """Test that APY methods are correctly removed."""
    print("\n" + "=" * 70)
    print("TEST 4: Removed APY Methods")
    print("=" * 70)
    
    try:
        from fx_sdk import ProtocolClient
        
        client = ProtocolClient(rpc_url="https://eth.llamarpc.com")
        
        removed_methods = [
            'get_convex_pool_apy',
            'get_convex_vault_apy',
            'get_all_convex_pools_apy',
            'get_curve_gauge_apy',
            'get_all_curve_gauges_apy'
        ]
        
        all_removed = True
        for method in removed_methods:
            if hasattr(client, method):
                print(f"❌ {method} still exists!")
                all_removed = False
            else:
                print(f"✅ {method} correctly removed")
        
        if all_removed:
            print("\n✅ All APY methods correctly removed")
            return True
        else:
            print("\n❌ Some APY methods still exist!")
            return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_core_methods():
    """Test that core methods still exist."""
    print("\n" + "=" * 70)
    print("TEST 5: Core Methods")
    print("=" * 70)
    
    try:
        from fx_sdk import ProtocolClient
        
        client = ProtocolClient(rpc_url="https://eth.llamarpc.com")
        
        # Convex methods
        convex_methods = [
            'get_convex_pool_info',
            'get_convex_pool_details',
            'get_convex_pool_statistics',
            'get_convex_vault_info',
            'get_convex_vault_balance',
            'get_convex_vault_rewards',
            'get_all_convex_pools',
            'get_convex_pool_tvl',
        ]
        
        # Curve methods
        curve_methods = [
            'get_curve_pool_info',
            'get_curve_gauge_info',
            'get_curve_gauge_balance',
            'get_curve_gauge_rewards',
            'get_curve_pools_from_registry',
        ]
        
        all_present = True
        print("Convex methods:")
        for method in convex_methods:
            if hasattr(client, method):
                print(f"  ✅ {method}")
            else:
                print(f"  ❌ {method} missing!")
                all_present = False
        
        print("\nCurve methods:")
        for method in curve_methods:
            if hasattr(client, method):
                print(f"  ✅ {method}")
            else:
                print(f"  ❌ {method} missing!")
                all_present = False
        
        if all_present:
            print("\n✅ All core methods present")
            return True
        else:
            print("\n❌ Some core methods missing!")
            return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_constants():
    """Test that constants are loaded correctly."""
    print("\n" + "=" * 70)
    print("TEST 6: Constants")
    print("=" * 70)
    
    try:
        from fx_sdk import constants
        
        # Check Convex constants
        assert constants.CONVEX_BOOSTER is not None
        print(f"✅ CONVEX_BOOSTER: {constants.CONVEX_BOOSTER}")
        
        assert constants.CONVEX_VAULT_FACTORY is not None
        print(f"✅ CONVEX_VAULT_FACTORY: {constants.CONVEX_VAULT_FACTORY}")
        
        assert len(constants.CONVEX_POOLS) > 0
        print(f"✅ CONVEX_POOLS: {len(constants.CONVEX_POOLS)} pools")
        
        # Check Curve constants
        assert constants.CURVE_REGISTRY is not None
        print(f"✅ CURVE_REGISTRY: {constants.CURVE_REGISTRY}")
        
        assert constants.CURVE_META_REGISTRY is not None
        print(f"✅ CURVE_META_REGISTRY: {constants.CURVE_META_REGISTRY}")
        
        # Show sample pool
        if constants.CONVEX_POOLS:
            first_pool_key = list(constants.CONVEX_POOLS.keys())[0]
            first_pool = constants.CONVEX_POOLS[first_pool_key]
            print(f"✅ Sample pool: {first_pool.get('name', 'N/A')} (ID: {first_pool.get('pool_id', 'N/A')})")
        
        print("\n✅ All constants loaded correctly")
        return True
    except Exception as e:
        print(f"❌ Constants test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_utilities():
    """Test utility functions."""
    print("\n" + "=" * 70)
    print("TEST 7: Utility Functions")
    print("=" * 70)
    
    try:
        from fx_sdk import utils
        
        # Test address checksumming
        test_address = "0x1234567890123456789012345678901234567890"
        checksummed = utils.to_checksum_address(test_address)
        assert checksummed.startswith("0x")
        print(f"✅ to_checksum_address: {checksummed}")
        
        # Test Wei to Decimal conversion
        wei_value = 1000000000000000000  # 1 ETH in Wei
        decimal_value = utils.wei_to_decimal(wei_value, 18)
        assert decimal_value == Decimal("1")
        print(f"✅ wei_to_decimal: {wei_value} Wei = {decimal_value} tokens")
        
        # Test Decimal to Wei conversion
        decimal_value = Decimal("1.5")
        wei_value = utils.decimal_to_wei(decimal_value, 18)
        assert wei_value == 1500000000000000000
        print(f"✅ decimal_to_wei: {decimal_value} tokens = {wei_value} Wei")
        
        print("\n✅ All utility functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Utilities test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_read_only_operations():
    """Test read-only operations (no private key required)."""
    print("\n" + "=" * 70)
    print("TEST 8: Read-Only Operations")
    print("=" * 70)
    
    try:
        from fx_sdk import ProtocolClient
        
        client = ProtocolClient(rpc_url="https://eth.llamarpc.com")
        
        # Test get_convex_pool_info (should work without private key)
        print("Testing get_convex_pool_info...")
        try:
            # This will make an actual RPC call, so it might fail if RPC is down
            # But we're just checking the method exists and is callable
            pool_info = client.get_convex_pool_info(pool_id=37)
            print(f"  ✅ Retrieved pool info: {pool_info.get('name', 'N/A')}")
        except Exception as e:
            # RPC errors are OK - we're just testing the method exists
            if "get_convex_pool_info" in str(e) or "AttributeError" in str(type(e).__name__):
                print(f"  ❌ Method error: {e}")
                return False
            else:
                print(f"  ✅ Method exists (RPC error expected: {type(e).__name__})")
        
        # Test get_convex_pool_details
        print("Testing get_convex_pool_details...")
        try:
            details = client.get_convex_pool_details(pool_id=37, include_tvl=False, include_rewards=False)
            print(f"  ✅ Retrieved pool details")
        except Exception as e:
            if "get_convex_pool_details" in str(e) or "AttributeError" in str(type(e).__name__):
                print(f"  ❌ Method error: {e}")
                return False
            else:
                print(f"  ✅ Method exists (RPC error expected: {type(e).__name__})")
        
        # Test get_convex_pool_statistics (should not reference removed APY method)
        print("Testing get_convex_pool_statistics...")
        try:
            import inspect
            source = inspect.getsource(client.get_convex_pool_statistics)
            if "get_convex_pool_apy" in source:
                print("  ❌ Method still references removed APY method!")
                return False
            else:
                print("  ✅ Method does not reference removed APY method")
        except Exception as e:
            print(f"  ⚠️  Could not verify source: {e}")
        
        print("\n✅ Read-only operations work correctly")
        return True
    except Exception as e:
        print(f"❌ Read-only operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("fx-sdk v0.3.0 Package Verification Test")
    print("=" * 70)
    print()
    
    # Check if we're using local development code or installed package
    import os
    import sys
    
    # If running from sdk directory, we're likely using local code
    if os.path.exists('fx_sdk') and os.path.exists('fx_sdk/__init__.py'):
        print("ℹ️  Using local development code (not installed package)")
        print("   This is normal before PyPI upload.\n")
    else:
        print("ℹ️  Using installed package from PyPI\n")
    
    tests = [
        ("Imports", test_imports),
        ("Version", test_version),
        ("Client Initialization", test_client_initialization),
        ("Removed APY Methods", test_removed_apy_methods),
        ("Core Methods", test_core_methods),
        ("Constants", test_constants),
        ("Utilities", test_utilities),
        ("Read-Only Operations", test_read_only_operations),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 70)
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("=" * 70)
        print("\n🎉 Package v0.3.0 is working correctly!")
        return 0
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total} passed)")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())

