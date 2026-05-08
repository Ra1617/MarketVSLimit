"""
Example usage of the Order Execution Simulator
This script demonstrates various ways to use the simulator components
"""
from real_time_data import RealTimeDataFetcher, LivePriceMonitor
from order_executor import OrderExecutor, OrderSimulator, OrderSide, OrderType
from visualizer import ExecutionVisualizer


def example_1_basic_price_fetching():
    """Example 1: Basic real-time price fetching"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Price Fetching")
    print("="*60 + "\n")
    
    # Create a data fetcher
    fetcher = RealTimeDataFetcher('AAPL')
    
    # Get current price
    current_price = fetcher.get_current_price()
    print(f"Current AAPL Price: ${current_price:.2f}")
    
    # Get market info
    info = fetcher.get_market_info()
    if info:
        print(f"\nMarket Information:")
        print(f"  Open: ${info.get('open', 0):.2f}")
        print(f"  High: ${info.get('day_high', 0):.2f}")
        print(f"  Low: ${info.get('day_low', 0):.2f}")
        print(f"  Previous Close: ${info.get('previous_close', 0):.2f}")
    
    # Get bid/ask spread
    bid, ask = fetcher.get_bid_ask_spread()
    if bid and ask:
        print(f"\nBid/Ask Spread:")
        print(f"  Bid: ${bid:.2f}")
        print(f"  Ask: ${ask:.2f}")
        print(f"  Spread: ${ask - bid:.2f}")


def example_2_price_monitoring():
    """Example 2: Monitor prices for a short period"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Price Monitoring (30 seconds)")
    print("="*60 + "\n")
    
    monitor = LivePriceMonitor('AAPL')
    
    # Monitor for 30 seconds with 5-second updates
    monitor.start_monitoring(duration=30, interval=5)
    
    # Get statistics
    stats = monitor.get_price_statistics()
    if stats:
        print(f"\nPrice Statistics:")
        print(f"  Observations: {stats['count']}")
        print(f"  High: ${stats['high']:.2f}")
        print(f"  Low: ${stats['low']:.2f}")
        print(f"  Average: ${stats['average']:.2f}")
        print(f"  Volatility: ${stats['volatility']:.4f}")


def example_3_simple_orders():
    """Example 3: Create and execute simple orders"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Simple Order Execution")
    print("="*60 + "\n")
    
    fetcher = RealTimeDataFetcher('AAPL')
    executor = OrderExecutor()
    
    current_price = fetcher.get_current_price()
    print(f"Current Price: ${current_price:.2f}\n")
    
    # Create a market order
    market_order = executor.create_market_order('AAPL', OrderSide.BUY, 10)
    print(f"Created: {market_order}")
    
    # Create a limit order
    limit_price = current_price * 0.99  # 1% below current price
    limit_order = executor.create_limit_order('AAPL', OrderSide.BUY, 10, limit_price)
    print(f"Created: {limit_order} @ ${limit_price:.2f}")
    
    # Execute based on current market data
    print(f"\nProcessing orders at current price...")
    executor.process_market_data('AAPL', current_price)
    
    # Check order status
    print(f"\nOrder Status:")
    print(f"  Market Order: {market_order.status.value}")
    print(f"  Limit Order: {limit_order.status.value}")
    
    if market_order.execution_price:
        print(f"\nMarket Order executed at: ${market_order.execution_price:.2f}")
    
    if limit_order.status.value == 'PENDING':
        print(f"\nLimit Order still pending (waiting for price to reach ${limit_price:.2f})")


def example_4_comparison_simulation():
    """Example 4: Run a comparison simulation"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Market vs Limit Comparison (60 seconds)")
    print("="*60 + "\n")
    
    fetcher = RealTimeDataFetcher('AAPL')
    simulator = OrderSimulator(fetcher)
    
    # Run a 60-second simulation
    simulator.run_live_simulation(
        symbol='AAPL',
        side=OrderSide.BUY,
        quantity=10,
        duration=60,
        update_interval=10,
        limit_offset_pct=0.5
    )


def example_5_multiple_orders():
    """Example 5: Create multiple orders and track them"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Multiple Orders (45 seconds)")
    print("="*60 + "\n")
    
    fetcher = RealTimeDataFetcher('AAPL')
    executor = OrderExecutor()
    visualizer = ExecutionVisualizer()
    monitor = LivePriceMonitor('AAPL')
    
    current_price = fetcher.get_current_price()
    print(f"Current Price: ${current_price:.2f}\n")
    
    # Create various orders
    print("Creating orders...")
    executor.create_market_order('AAPL', OrderSide.BUY, 5)
    executor.create_market_order('AAPL', OrderSide.SELL, 3)
    executor.create_limit_order('AAPL', OrderSide.BUY, 10, current_price * 0.995)
    executor.create_limit_order('AAPL', OrderSide.SELL, 8, current_price * 1.005)
    
    print(f"Created {len(executor.orders)} orders\n")
    
    # Monitor and process
    def process_callback(price_data):
        timestamp = price_data['timestamp'].strftime('%H:%M:%S')
        price = price_data['price']
        print(f"[{timestamp}] Price: ${price:.2f}")
        executor.process_market_data('AAPL', price)
    
    monitor.start_monitoring(callback=process_callback, duration=45, interval=10)
    
    # Display results
    print("\nOrder Summary:")
    summary = executor.get_order_summary()
    print(f"  Total: {summary['total']}")
    print(f"  Executed: {summary['executed']}")
    print(f"  Pending: {summary['pending']}")
    print(f"  Execution Rate: {summary['execution_rate']:.1f}%\n")
    
    # Show order table
    visualizer.print_order_table(executor.orders)


def example_6_custom_callback():
    """Example 6: Custom price monitoring callback"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Custom Price Alert (30 seconds)")
    print("="*60 + "\n")
    
    monitor = LivePriceMonitor('AAPL')
    
    # Get initial price
    initial_price = monitor.fetcher.get_current_price()
    print(f"Initial Price: ${initial_price:.2f}")
    print(f"Alert: Will notify if price changes by more than $0.50\n")
    
    # Custom callback with alert
    def alert_callback(price_data):
        price = price_data['price']
        timestamp = price_data['timestamp'].strftime('%H:%M:%S')
        change = price - initial_price
        
        if abs(change) > 0.50:
            print(f"[{timestamp}] 🔔 ALERT! Price: ${price:.2f} (Change: ${change:+.2f})")
        else:
            print(f"[{timestamp}] Price: ${price:.2f} (Change: ${change:+.2f})")
    
    monitor.start_monitoring(callback=alert_callback, duration=30, interval=5)


def main():
    """Run all examples"""
    print("\n" + "#"*60)
    print("ORDER EXECUTION SIMULATOR - EXAMPLES")
    print("#"*60)
    
    examples = [
        ("Price Fetching", example_1_basic_price_fetching),
        ("Price Monitoring", example_2_price_monitoring),
        ("Simple Orders", example_3_simple_orders),
        ("Comparison Simulation", example_4_comparison_simulation),
        ("Multiple Orders", example_5_multiple_orders),
        ("Custom Callback", example_6_custom_callback),
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRun specific example or all:")
    choice = input("Enter number (1-6) or 'all' to run all examples: ").strip().lower()
    
    try:
        if choice == 'all':
            for name, func in examples:
                print(f"\n\nRunning: {name}")
                func()
                input("\nPress Enter to continue to next example...")
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                examples[idx][1]()
            else:
                print("Invalid choice")
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == '__main__':
    main()






