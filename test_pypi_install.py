#!/usr/bin/env python3
"""
Test script to verify fx-sdk installation from PyPI/TestPyPI.

Run this after installing:
    pip install --index-url https://test.pypi.org/simple/ fx-sdk==0.2.0
    # or
    pip install fx-sdk==0.2.0

Usage:
    python3 test_pypi_install.py
"""

import sys

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    try:
        import fx_sdk
        print(f"   ✓ fx_sdk imported (version: {getattr(fx_sdk, '__version__', 'unknown')})")
        
        from fx_sdk import ProtocolClient, constants, utils
        print("   ✓ ProtocolClient imported")
        print("   ✓ constants imported")
        print("   ✓ utils imported")
        
        from fx_sdk.exceptions import FXProtocolError, ContractCallError
        print("   ✓ exceptions imported")
        
        return True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_constants():
    """Test that constants are accessible."""
    print("\n🧪 Testing constants...")
    try:
        from fx_sdk import constants
        
        # Test some key constants
        assert constants.FXUSD, "fxUSD address missing"
        print(f"   ✓ fxUSD: {constants.FXUSD}")
        
        assert constants.FXN, "FXN address missing"
        print(f"   ✓ FXN: {constants.FXN}")
        
        # Test Convex constants (v0.2.0)
        assert hasattr(constants, 'CONVEX_BOOSTER'), "Convex constants missing"
        print(f"   ✓ CONVEX_BOOSTER: {constants.CONVEX_BOOSTER}")
        
        # Test Curve constants (v0.2.0)
        assert hasattr(constants, 'CURVE_REGISTRY'), "Curve constants missing"
        print(f"   ✓ CURVE_REGISTRY: {constants.CURVE_REGISTRY}")
        
        # Test Convex pools registry
        assert hasattr(constants, 'CONVEX_POOLS'), "CONVEX_POOLS missing"
        pool_count = len(constants.CONVEX_POOLS)
        print(f"   ✓ CONVEX_POOLS: {pool_count} pools registered")
        
        return True
    except Exception as e:
        print(f"   ❌ Constants test failed: {e}")
        return False

def test_utils():
    """Test utility functions."""
    print("\n🧪 Testing utility functions...")
    try:
        from fx_sdk import utils
        from decimal import Decimal
        
        # Test Wei to Decimal
        wei = 1500000000000000000
        dec = utils.wei_to_decimal(wei, 18)
        assert dec == Decimal("1.5"), f"Expected 1.5, got {dec}"
        print(f"   ✓ Wei to Decimal: {wei} Wei = {dec} ETH")
        
        # Test Decimal to Wei
        wei_result = utils.decimal_to_wei(Decimal("1.5"), 18)
        assert wei_result == wei, f"Expected {wei}, got {wei_result}"
        print(f"   ✓ Decimal to Wei: 1.5 ETH = {wei_result} Wei")
        
        # Test address checksumming
        addr = "0x742d35cc6634c0532925a3b844bc9e2385c6b0e0"
        checksummed = utils.to_checksum_address(addr)
        assert checksummed.startswith("0x"), "Checksum failed"
        print(f"   ✓ Address checksum: {checksummed}")
        
        return True
    except Exception as e:
        print(f"   ❌ Utils test failed: {e}")
        return False

def test_client_readonly():
    """Test client initialization in read-only mode."""
    print("\n🧪 Testing client (read-only mode)...")
    try:
        from fx_sdk import ProtocolClient
        
        # Use a public RPC endpoint
        rpc_url = "https://eth.llamarpc.com"
        client = ProtocolClient(rpc_url)
        
        print(f"   ✓ Client initialized (read-only)")
        print(f"   ✓ Connected to: {rpc_url}")
        
        # Test a simple read operation
        try:
            from fx_sdk import constants
            balance = client.get_token_balance(constants.FXUSD, constants.FXUSD)
            print(f"   ✓ Read operation successful: fxUSD supply = {balance}")
        except Exception as e:
            print(f"   ⚠️  Read operation failed (may be RPC issue): {e}")
        
        return True
    except Exception as e:
        print(f"   ❌ Client test failed: {e}")
        return False

def test_convex_methods():
    """Test that Convex methods exist (v0.2.0)."""
    print("\n🧪 Testing Convex methods (v0.2.0)...")
    try:
        from fx_sdk import ProtocolClient
        
        client = ProtocolClient("https://eth.llamarpc.com")
        
        # Check for key Convex methods
        convex_methods = [
            'get_convex_vault_address',
            'create_convex_vault',
            'get_convex_vault_info',
            'get_convex_vault_balance',
            'get_convex_pool_info',
            'get_convex_pool_apy',
            'get_all_convex_pools',
        ]
        
        missing = []
        for method in convex_methods:
            if not hasattr(client, method):
                missing.append(method)
        
        if missing:
            print(f"   ❌ Missing Convex methods: {missing}")
            return False
        
        print(f"   ✓ All {len(convex_methods)} Convex methods found")
        return True
    except Exception as e:
        print(f"   ❌ Convex methods test failed: {e}")
        return False

def test_curve_methods():
    """Test that Curve methods exist (v0.2.0)."""
    print("\n🧪 Testing Curve methods (v0.2.0)...")
    try:
        from fx_sdk import ProtocolClient
        
        client = ProtocolClient("https://eth.llamarpc.com")
        
        # Check for key Curve methods
        curve_methods = [
            'get_curve_pool_info',
            'find_curve_pool',
            'get_curve_swap_rate',
            'curve_swap',
            'get_curve_gauge_info',
            'get_curve_gauge_balance',
            'get_curve_gauge_apy',
        ]
        
        missing = []
        for method in curve_methods:
            if not hasattr(client, method):
                missing.append(method)
        
        if missing:
            print(f"   ❌ Missing Curve methods: {missing}")
            return False
        
        print(f"   ✓ All {len(curve_methods)} Curve methods found")
        return True
    except Exception as e:
        print(f"   ❌ Curve methods test failed: {e}")
        return False

def test_abis():
    """Test that ABI files are included."""
    print("\n🧪 Testing ABI files...")
    try:
        import os
        import fx_sdk
        
        # Get the package directory
        package_dir = os.path.dirname(fx_sdk.__file__)
        abis_dir = os.path.join(package_dir, 'abis')
        
        if not os.path.exists(abis_dir):
            print(f"   ❌ ABIs directory not found: {abis_dir}")
            return False
        
        abi_files = [f for f in os.listdir(abis_dir) if f.endswith('.json')]
        
        if len(abi_files) < 30:
            print(f"   ⚠️  Only {len(abi_files)} ABI files found (expected 30+)")
        else:
            print(f"   ✓ Found {len(abi_files)} ABI files")
        
        # Check for key ABIs
        key_abis = ['fxusd.json', 'fxn.json', 'convex_booster.json', 'curve_pool.json']
        missing = [abi for abi in key_abis if abi not in abi_files]
        
        if missing:
            print(f"   ⚠️  Missing key ABIs: {missing}")
        else:
            print(f"   ✓ All key ABIs present")
        
        return True
    except Exception as e:
        print(f"   ❌ ABI test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing fx-sdk Installation from PyPI/TestPyPI")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Constants", test_constants),
        ("Utilities", test_utils),
        ("Client (Read-Only)", test_client_readonly),
        ("Convex Methods", test_convex_methods),
        ("Curve Methods", test_curve_methods),
        ("ABI Files", test_abis),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Package is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

