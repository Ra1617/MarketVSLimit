"""
Order Execution Simulator - Main Script
Real-time comparison of market vs limit orders using live market data
"""
import argparse
from datetime import datetime
from real_time_data import RealTimeDataFetcher, LivePriceMonitor
from order_executor import OrderExecutor, OrderSimulator, OrderSide, OrderType
from visualizer import ExecutionVisualizer


def quick_demo(symbol='AAPL', duration=60):
    """
    Quick demonstration of real-time order execution
    
    Args:
        symbol: Stock ticker symbol
        duration: Duration in seconds
    """
    print("\n" + "="*70)
    print("QUICK DEMO: Real-Time Order Execution Simulator".center(70))
    print("="*70 + "\n")
    
    # Initialize components
    fetcher = RealTimeDataFetcher(symbol)
    simulator = OrderSimulator(fetcher)
    
    # Show current market info
    info = fetcher.get_market_info()
    if info:
        print(f"Symbol: {info['symbol']}")
        print(f"Current Price: ${info['current_price']:.2f}")
        print(f"Previous Close: ${info.get('previous_close', 'N/A')}")
        print(f"Day Range: ${info.get('day_low', 0):.2f} - ${info.get('day_high', 0):.2f}")
        print()
    
    # Run simulation
    simulator.run_live_simulation(
        symbol=symbol,
        side=OrderSide.BUY,
        quantity=10,
        duration=duration,
        update_interval=5,
        limit_offset_pct=0.5
    )


def advanced_simulation(symbol='AAPL', duration=180, num_orders=5):
    """
    Advanced simulation with multiple orders and visualization
    
    Args:
        symbol: Stock ticker symbol
        duration: Duration in seconds
        num_orders: Number of order pairs to create
    """
    print("\n" + "="*70)
    print("ADVANCED SIMULATION: Multiple Orders Comparison".center(70))
    print("="*70 + "\n")
    
    # Initialize
    fetcher = RealTimeDataFetcher(symbol)
    executor = OrderExecutor()
    visualizer = ExecutionVisualizer()
    monitor = LivePriceMonitor(symbol)
    
    # Show market info
    info = fetcher.get_market_info()
    if info:
        print(f"Symbol: {symbol}")
        print(f"Current Price: ${info['current_price']:.2f}")
        print(f"Market Status: Monitoring for {duration} seconds")
        print()
    
    # Create multiple order pairs
    current_price = fetcher.get_current_price()
    
    print(f"Creating {num_orders} pairs of orders...\n")
    for i in range(num_orders):
        # Alternate between buy and sell
        side = OrderSide.BUY if i % 2 == 0 else OrderSide.SELL
        quantity = 10 * (i + 1)
        
        # Create market order
        market_order = executor.create_market_order(symbol, side, quantity)
        
        # Create limit order with varying offsets
        offset = 0.5 + (i * 0.3)  # 0.5%, 0.8%, 1.1%, etc.
        if side == OrderSide.BUY:
            limit_price = current_price * (1 - offset / 100)
        else:
            limit_price = current_price * (1 + offset / 100)
        
        limit_order = executor.create_limit_order(symbol, side, quantity, limit_price)
        
        print(f"  Pair {i+1}: {side.value} {quantity} shares")
        print(f"    Market: {market_order.order_id}")
        print(f"    Limit:  {limit_order.order_id} @ ${limit_price:.2f}")
    
    print(f"\n{'='*70}")
    print("Starting live monitoring and order execution...")
    print(f"{'='*70}\n")
    
    # Define callback for price updates
    def process_price_update(price_data):
        timestamp = price_data['timestamp'].strftime('%H:%M:%S')
        price = price_data['price']
        
        # Get bid/ask if available
        bid, ask = fetcher.get_bid_ask_spread()
        
        print(f"[{timestamp}] {symbol}: ${price:.2f}", end="")
        if bid and ask:
            print(f" | Bid: ${bid:.2f} | Ask: ${ask:.2f}", end="")
        print()
        
        # Process orders
        executor.process_market_data(symbol, price, bid, ask)
    
    # Start monitoring
    monitor.start_monitoring(
        callback=process_price_update,
        duration=duration,
        interval=5
    )
    
    # Generate reports and visualizations
    print("\n" + "="*70)
    print("Generating Analysis...")
    print("="*70 + "\n")
    
    # Get statistics
    stats = monitor.get_price_statistics()
    if stats:
        print("PRICE STATISTICS:")
        print(f"  Observations: {stats['count']}")
        print(f"  Current: ${stats['current']:.2f}")
        print(f"  High: ${stats['high']:.2f}")
        print(f"  Low: ${stats['low']:.2f}")
        print(f"  Average: ${stats['average']:.2f}")
        print(f"  Volatility: ${stats['volatility']:.4f}")
        print()
    
    # Order summary
    summary = executor.get_order_summary()
    print("ORDER SUMMARY:")
    print(f"  Total Orders: {summary['total']}")
    print(f"  Executed: {summary['executed']}")
    print(f"  Pending: {summary['pending']}")
    print(f"  Execution Rate: {summary['execution_rate']:.1f}%")
    print()
    
    # Display order tables
    print("\nALL ORDERS:")
    visualizer.print_order_table(executor.orders)
    
    # Separate by type for analysis
    market_orders = [o for o in executor.orders if o.order_type == OrderType.MARKET]
    limit_orders = [o for o in executor.orders if o.order_type == OrderType.LIMIT]
    
    # Generate performance report
    visualizer.generate_performance_report(executor.orders, monitor.price_history)
    
    # Create visualizations
    print("Generating visualizations...\n")
    
    try:
        visualizer.plot_price_with_executions(
            monitor.price_history,
            executor.get_executed_orders(),
            save_path='execution_chart.png'
        )
    except Exception as e:
        print(f"Note: Could not generate price chart: {e}")
    
    try:
        visualizer.plot_execution_comparison(
            market_orders,
            limit_orders,
            save_path='comparison_chart.png'
        )
    except Exception as e:
        print(f"Note: Could not generate comparison chart: {e}")


def interactive_mode():
    """Interactive mode for custom simulations"""
    print("\n" + "="*70)
    print("INTERACTIVE MODE: Order Execution Simulator".center(70))
    print("="*70 + "\n")
    
    # Get user inputs
    symbol = input("Enter stock symbol (default: AAPL): ").strip().upper() or "AAPL"
    
    print("\nOrder Side:")
    print("  1. BUY")
    print("  2. SELL")
    side_choice = input("Select (1 or 2): ").strip()
    side = OrderSide.BUY if side_choice == '1' else OrderSide.SELL
    
    try:
        quantity = int(input("Enter quantity (default: 10): ").strip() or "10")
    except ValueError:
        quantity = 10
    
    try:
        duration = int(input("Simulation duration in seconds (default: 120): ").strip() or "120")
    except ValueError:
        duration = 120
    
    try:
        limit_offset = float(input("Limit price offset % (default: 1.0): ").strip() or "1.0")
    except ValueError:
        limit_offset = 1.0
    
    # Run simulation
    fetcher = RealTimeDataFetcher(symbol)
    simulator = OrderSimulator(fetcher)
    
    simulator.run_live_simulation(
        symbol=symbol,
        side=side,
        quantity=quantity,
        duration=duration,
        update_interval=5,
        limit_offset_pct=limit_offset
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Order Execution Simulator - Compare Market vs Limit Orders',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo                     # Quick 60-second demo
  python main.py --advanced --symbol MSFT   # Advanced simulation with MSFT
  python main.py --interactive              # Interactive mode
  python main.py --symbol TSLA --duration 300  # 5-minute simulation
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run quick demo (60 seconds)')
    parser.add_argument('--advanced', action='store_true',
                       help='Run advanced simulation with multiple orders')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--symbol', type=str, default='AAPL',
                       help='Stock symbol (default: AAPL)')
    parser.add_argument('--duration', type=int, default=120,
                       help='Simulation duration in seconds (default: 120)')
    parser.add_argument('--orders', type=int, default=5,
                       help='Number of order pairs for advanced mode (default: 5)')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            quick_demo(symbol=args.symbol, duration=60)
        elif args.advanced:
            advanced_simulation(
                symbol=args.symbol,
                duration=args.duration,
                num_orders=args.orders
            )
        elif args.interactive:
            interactive_mode()
        else:
            # Default: run quick demo
            print("No mode specified. Running quick demo...")
            print("Use --help to see all available options.\n")
            quick_demo(symbol=args.symbol, duration=args.duration)
    
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()






