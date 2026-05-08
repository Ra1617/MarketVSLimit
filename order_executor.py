"""
Order Executor for simulating market and limit orders in real-time
"""
from datetime import datetime
from enum import Enum
import time


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Order:
    """Represents a trading order"""
    
    def __init__(self, order_id, symbol, order_type, side, quantity, limit_price=None):
        self.order_id = order_id
        self.symbol = symbol
        self.order_type = order_type
        self.side = side
        self.quantity = quantity
        self.limit_price = limit_price
        self.status = OrderStatus.PENDING
        self.execution_price = None
        self.submission_time = datetime.now()
        self.execution_time = None
        
    def execute(self, price):
        """Execute the order at given price"""
        self.execution_price = price
        self.execution_time = datetime.now()
        self.status = OrderStatus.EXECUTED
        
    def cancel(self):
        """Cancel the order"""
        self.status = OrderStatus.CANCELLED
        
    def expire(self):
        """Mark order as expired"""
        self.status = OrderStatus.EXPIRED
        
    def get_execution_delay(self):
        """Get time between submission and execution"""
        if self.execution_time:
            return (self.execution_time - self.submission_time).total_seconds()
        return None
    
    def get_slippage(self, reference_price):
        """
        Calculate slippage
        
        For BUY orders: positive slippage means paid more than reference
        For SELL orders: positive slippage means received less than reference
        """
        if self.execution_price is None:
            return None
        
        if self.side == OrderSide.BUY:
            return self.execution_price - reference_price
        else:  # SELL
            return reference_price - self.execution_price
    
    def __repr__(self):
        return (f"Order({self.order_id}, {self.symbol}, {self.order_type.value}, "
                f"{self.side.value}, qty={self.quantity}, status={self.status.value})")


class OrderExecutor:
    """Executes orders based on real-time market data"""
    
    def __init__(self):
        self.orders = []
        self.executed_orders = []
        self.next_order_id = 1
        
    def create_market_order(self, symbol, side, quantity):
        """
        Create a market order (executes immediately at current price)
        
        Args:
            symbol: Stock symbol
            side: OrderSide.BUY or OrderSide.SELL
            quantity: Number of shares
        """
        order = Order(
            order_id=f"MKT{self.next_order_id:04d}",
            symbol=symbol,
            order_type=OrderType.MARKET,
            side=side,
            quantity=quantity
        )
        self.next_order_id += 1
        self.orders.append(order)
        return order
    
    def create_limit_order(self, symbol, side, quantity, limit_price):
        """
        Create a limit order (executes only when price condition is met)
        
        Args:
            symbol: Stock symbol
            side: OrderSide.BUY or OrderSide.SELL
            quantity: Number of shares
            limit_price: Price limit for execution
        """
        order = Order(
            order_id=f"LMT{self.next_order_id:04d}",
            symbol=symbol,
            order_type=OrderType.LIMIT,
            side=side,
            quantity=quantity,
            limit_price=limit_price
        )
        self.next_order_id += 1
        self.orders.append(order)
        return order
    
    def process_market_data(self, symbol, current_price, bid=None, ask=None):
        """
        Process incoming market data and execute eligible orders
        
        Args:
            symbol: Stock symbol
            current_price: Current market price
            bid: Current bid price (optional)
            ask: Current ask price (optional)
        """
        pending_orders = [o for o in self.orders if o.status == OrderStatus.PENDING and o.symbol == symbol]
        
        for order in pending_orders:
            if order.order_type == OrderType.MARKET:
                # Market orders execute immediately at current price
                # Use bid/ask spread if available for more realistic simulation
                if order.side == OrderSide.BUY and ask:
                    execution_price = ask  # Buy at ask price
                elif order.side == OrderSide.SELL and bid:
                    execution_price = bid  # Sell at bid price
                else:
                    execution_price = current_price
                
                order.execute(execution_price)
                self.executed_orders.append(order)
                print(f"✓ EXECUTED: {order.order_type.value} {order.side.value} {order.quantity} {symbol} @ ${execution_price:.2f}")
                
            elif order.order_type == OrderType.LIMIT:
                # Limit orders execute only when price condition is met
                should_execute = False
                
                if order.side == OrderSide.BUY:
                    # Buy limit: execute when market price <= limit price
                    check_price = ask if ask else current_price
                    if check_price <= order.limit_price:
                        should_execute = True
                        execution_price = min(check_price, order.limit_price)
                        
                else:  # SELL
                    # Sell limit: execute when market price >= limit price
                    check_price = bid if bid else current_price
                    if check_price >= order.limit_price:
                        should_execute = True
                        execution_price = max(check_price, order.limit_price)
                
                if should_execute:
                    order.execute(execution_price)
                    self.executed_orders.append(order)
                    print(f"✓ EXECUTED: {order.order_type.value} {order.side.value} {order.quantity} {symbol} @ ${execution_price:.2f} (Limit: ${order.limit_price:.2f})")
    
    def cancel_order(self, order_id):
        """Cancel a pending order"""
        for order in self.orders:
            if order.order_id == order_id and order.status == OrderStatus.PENDING:
                order.cancel()
                return True
        return False
    
    def get_pending_orders(self):
        """Get all pending orders"""
        return [o for o in self.orders if o.status == OrderStatus.PENDING]
    
    def get_executed_orders(self):
        """Get all executed orders"""
        return [o for o in self.orders if o.status == OrderStatus.EXECUTED]
    
    def get_order_summary(self):
        """Get summary statistics of all orders"""
        total = len(self.orders)
        executed = len([o for o in self.orders if o.status == OrderStatus.EXECUTED])
        pending = len([o for o in self.orders if o.status == OrderStatus.PENDING])
        cancelled = len([o for o in self.orders if o.status == OrderStatus.CANCELLED])
        
        return {
            'total': total,
            'executed': executed,
            'pending': pending,
            'cancelled': cancelled,
            'execution_rate': (executed / total * 100) if total > 0 else 0
        }


class OrderSimulator:
    """Simulate and compare market vs limit order execution"""
    
    def __init__(self, data_fetcher):
        self.data_fetcher = data_fetcher
        self.executor = OrderExecutor()
        self.price_at_submission = None
        
    def submit_comparison_orders(self, symbol, side, quantity, limit_offset_pct=1.0):
        """
        Submit both market and limit orders for comparison
        
        Args:
            symbol: Stock symbol
            side: OrderSide.BUY or OrderSide.SELL
            quantity: Number of shares
            limit_offset_pct: Percentage offset for limit price (default 1%)
        
        Returns:
            tuple: (market_order, limit_order)
        """
        current_price = self.data_fetcher.get_current_price()
        self.price_at_submission = current_price
        
        print(f"\n{'='*60}")
        print(f"Submitting comparison orders for {symbol}")
        print(f"Current Market Price: ${current_price:.2f}")
        print(f"{'='*60}")
        
        # Create market order
        market_order = self.executor.create_market_order(symbol, side, quantity)
        print(f"→ Created MARKET {side.value} order: {market_order.order_id}")
        
        # Create limit order with offset
        if side == OrderSide.BUY:
            # Buy limit: set below current price (more conservative)
            limit_price = current_price * (1 - limit_offset_pct / 100)
        else:  # SELL
            # Sell limit: set above current price (more aggressive)
            limit_price = current_price * (1 + limit_offset_pct / 100)
        
        limit_order = self.executor.create_limit_order(symbol, side, quantity, limit_price)
        print(f"→ Created LIMIT {side.value} order: {limit_order.order_id} @ ${limit_price:.2f}")
        print()
        
        return market_order, limit_order
    
    def run_live_simulation(self, symbol, side, quantity, duration=300, 
                           update_interval=5, limit_offset_pct=1.0):
        """
        Run a live simulation comparing market and limit orders
        
        Args:
            symbol: Stock symbol
            side: OrderSide.BUY or OrderSide.SELL
            quantity: Number of shares
            duration: Simulation duration in seconds
            update_interval: Price update interval in seconds
            limit_offset_pct: Limit price offset percentage
        """
        print(f"\n{'#'*60}")
        print(f"LIVE ORDER EXECUTION SIMULATION")
        print(f"Symbol: {symbol} | Side: {side.value} | Quantity: {quantity}")
        print(f"Duration: {duration}s | Updates: every {update_interval}s")
        print(f"{'#'*60}\n")
        
        # Submit orders
        market_order, limit_order = self.submit_comparison_orders(
            symbol, side, quantity, limit_offset_pct
        )
        
        # Monitor and execute
        print(f"{'='*60}")
        print("Monitoring market for order execution...")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            current_price = self.data_fetcher.get_current_price()
            bid, ask = self.data_fetcher.get_bid_ask_spread()
            
            if current_price:
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] Price: ${current_price:.2f}", end="")
                if bid and ask:
                    print(f" | Bid: ${bid:.2f} | Ask: ${ask:.2f}", end="")
                print()
                
                # Process orders
                self.executor.process_market_data(symbol, current_price, bid, ask)
                
                # Check if both orders are executed
                if (market_order.status == OrderStatus.EXECUTED and 
                    limit_order.status == OrderStatus.EXECUTED):
                    print("\n✓ Both orders executed!")
                    break
            
            time.sleep(update_interval)
        
        # Final summary
        self._print_comparison_summary(market_order, limit_order)
    
    def _print_comparison_summary(self, market_order, limit_order):
        """Print detailed comparison between market and limit orders"""
        print(f"\n{'='*60}")
        print("EXECUTION COMPARISON SUMMARY")
        print(f"{'='*60}\n")
        
        print(f"Submission Price: ${self.price_at_submission:.2f}\n")
        
        # Market Order Summary
        print("MARKET ORDER:")
        print(f"  Order ID: {market_order.order_id}")
        print(f"  Status: {market_order.status.value}")
        if market_order.execution_price:
            print(f"  Execution Price: ${market_order.execution_price:.2f}")
            delay = market_order.get_execution_delay()
            print(f"  Execution Delay: {delay:.2f}s")
            slippage = market_order.get_slippage(self.price_at_submission)
            print(f"  Slippage: ${slippage:.2f} ({slippage/self.price_at_submission*100:.2f}%)")
            total_cost = market_order.execution_price * market_order.quantity
            print(f"  Total Cost: ${total_cost:.2f}")
        print()
        
        # Limit Order Summary
        print("LIMIT ORDER:")
        print(f"  Order ID: {limit_order.order_id}")
        print(f"  Limit Price: ${limit_order.limit_price:.2f}")
        print(f"  Status: {limit_order.status.value}")
        if limit_order.execution_price:
            print(f"  Execution Price: ${limit_order.execution_price:.2f}")
            delay = limit_order.get_execution_delay()
            print(f"  Execution Delay: {delay:.2f}s")
            slippage = limit_order.get_slippage(self.price_at_submission)
            print(f"  Slippage: ${slippage:.2f} ({slippage/self.price_at_submission*100:.2f}%)")
            total_cost = limit_order.execution_price * limit_order.quantity
            print(f"  Total Cost: ${total_cost:.2f}")
        print()
        
        # Comparison
        if (market_order.execution_price and limit_order.execution_price):
            print("COMPARISON:")
            price_diff = market_order.execution_price - limit_order.execution_price
            if market_order.side == OrderSide.BUY:
                savings = -price_diff * market_order.quantity
                print(f"  Price Difference: ${price_diff:.2f}")
                print(f"  {'Savings' if savings > 0 else 'Extra Cost'} with Limit Order: ${abs(savings):.2f}")
            else:  # SELL
                extra_revenue = price_diff * market_order.quantity
                print(f"  Price Difference: ${price_diff:.2f}")
                print(f"  {'Extra Revenue' if extra_revenue > 0 else 'Lost Revenue'} with Limit Order: ${abs(extra_revenue):.2f}")
        
        print(f"\n{'='*60}\n")






