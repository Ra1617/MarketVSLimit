"""
Test script to verify installation and basic functionality
Run this to make sure everything is set up correctly
"""
import sys


def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    required_packages = [
        ('yfinance', 'yfinance'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib.pyplot'),
        ('seaborn', 'seaborn'),
        ('tabulate', 'tabulate'),
    ]
    
    failed = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError as e:
            print(f"  ✗ {package_name} - {e}")
            failed.append(package_name)
    
    return len(failed) == 0, failed


def test_project_modules():
    """Test if project modules can be imported"""
    print("\nTesting project modules...")
    
    modules = [
        'real_time_data',
        'order_executor',
        'visualizer',
        'main'
    ]
    
    failed = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}.py")
        except Exception as e:
            print(f"  ✗ {module}.py - {e}")
            failed.append(module)
    
    return len(failed) == 0, failed


def test_data_fetching():
    """Test basic data fetching functionality"""
    print("\nTesting data fetching...")
    
    try:
        from real_time_data import RealTimeDataFetcher
        
        fetcher = RealTimeDataFetcher('AAPL')
        price = fetcher.get_current_price()
        
        if price and price > 0:
            print(f"  ✓ Successfully fetched AAPL price: ${price:.2f}")
            return True
        else:
            print(f"  ✗ Failed to fetch valid price data")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_order_creation():
    """Test order creation functionality"""
    print("\nTesting order creation...")
    
    try:
        from order_executor import OrderExecutor, OrderSide
        
        executor = OrderExecutor()
        
        # Create market order
        market_order = executor.create_market_order('AAPL', OrderSide.BUY, 10)
        print(f"  ✓ Created market order: {market_order.order_id}")
        
        # Create limit order
        limit_order = executor.create_limit_order('AAPL', OrderSide.SELL, 5, 150.00)
        print(f"  ✓ Created limit order: {limit_order.order_id}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("Order Execution Simulator - Installation Test")
    print("="*60 + "\n")
    
    all_passed = True
    
    # Test 1: Package imports
    passed, failed = test_imports()
    if not passed:
        all_passed = False
        print(f"\n⚠️  Missing packages: {', '.join(failed)}")
        print("   Install with: pip install -r requirements.txt")
    
    # Test 2: Project modules
    passed, failed = test_project_modules()
    if not passed:
        all_passed = False
        print(f"\n⚠️  Missing or broken modules: {', '.join(failed)}")
    
    # Test 3: Data fetching
    if not test_data_fetching():
        all_passed = False
        print("\n⚠️  Note: Data fetching test failed. This might be due to:")
        print("   - No internet connection")
        print("   - Yahoo Finance API issues")
        print("   - Market is closed (try during market hours)")
    
    # Test 4: Order creation
    if not test_order_creation():
        all_passed = False
    
    # Final summary
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed! Installation is complete.")
        print("\nYou can now run:")
        print("  python main.py --demo")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  pip install -r requirements.txt")
        print("  pip install --upgrade yfinance pandas matplotlib")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())






