"""
Visualization tools for order execution analysis
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
import numpy as np
from tabulate import tabulate


class ExecutionVisualizer:
    """Visualize order execution results"""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        
    def plot_price_with_executions(self, price_history, orders, save_path=None):
        """
        Plot price history with order execution points
        
        Args:
            price_history: List of dicts with 'price' and 'timestamp'
            orders: List of Order objects
            save_path: Optional path to save the figure
        """
        if not price_history:
            print("No price history to plot")
            return
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot price history
        timestamps = [p['timestamp'] for p in price_history]
        prices = [p['price'] for p in price_history]
        
        ax.plot(timestamps, prices, label='Market Price', linewidth=2, color='#2E86AB')
        
        # Plot order executions
        for order in orders:
            if order.execution_price and order.execution_time:
                color = 'green' if order.side.value == 'BUY' else 'red'
                marker = 'o' if order.order_type.value == 'MARKET' else '^'
                size = 200 if order.order_type.value == 'MARKET' else 150
                
                ax.scatter(order.execution_time, order.execution_price, 
                          color=color, s=size, marker=marker, 
                          alpha=0.7, edgecolors='black', linewidth=2,
                          label=f"{order.order_type.value} {order.side.value}",
                          zorder=5)
                
                # Add annotation
                offset = 5 if order.side.value == 'BUY' else -5
                ax.annotate(f"{order.order_id}\n${order.execution_price:.2f}",
                           xy=(order.execution_time, order.execution_price),
                           xytext=(0, offset), textcoords='offset points',
                           ha='center', fontsize=9, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor=color, alpha=0.3))
        
        # Format plot
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
        ax.set_title('Real-Time Price Chart with Order Executions', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Format x-axis for time
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)
        
        # Remove duplicate labels
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='best', fontsize=10)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        
        plt.show()
    
    def plot_execution_comparison(self, market_orders, limit_orders, save_path=None):
        """
        Create comparison charts between market and limit orders
        
        Args:
            market_orders: List of market Order objects
            limit_orders: List of limit Order objects
            save_path: Optional path to save the figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Market vs Limit Orders: Execution Comparison', 
                    fontsize=16, fontweight='bold')
        
        # 1. Execution Rate
        ax1 = axes[0, 0]
        market_exec_rate = len([o for o in market_orders if o.status.value == 'EXECUTED']) / len(market_orders) * 100 if market_orders else 0
        limit_exec_rate = len([o for o in limit_orders if o.status.value == 'EXECUTED']) / len(limit_orders) * 100 if limit_orders else 0
        
        bars = ax1.bar(['Market Orders', 'Limit Orders'], 
                      [market_exec_rate, limit_exec_rate],
                      color=['#2E86AB', '#A23B72'])
        ax1.set_ylabel('Execution Rate (%)', fontweight='bold')
        ax1.set_title('Execution Rate Comparison', fontweight='bold')
        ax1.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 2. Average Execution Time
        ax2 = axes[0, 1]
        market_times = [o.get_execution_delay() for o in market_orders if o.get_execution_delay()]
        limit_times = [o.get_execution_delay() for o in limit_orders if o.get_execution_delay()]
        
        avg_market_time = np.mean(market_times) if market_times else 0
        avg_limit_time = np.mean(limit_times) if limit_times else 0
        
        bars = ax2.bar(['Market Orders', 'Limit Orders'], 
                      [avg_market_time, avg_limit_time],
                      color=['#2E86AB', '#A23B72'])
        ax2.set_ylabel('Average Time (seconds)', fontweight='bold')
        ax2.set_title('Average Execution Delay', fontweight='bold')
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}s', ha='center', va='bottom', fontweight='bold')
        
        # 3. Price Distribution
        ax3 = axes[1, 0]
        market_prices = [o.execution_price for o in market_orders if o.execution_price]
        limit_prices = [o.execution_price for o in limit_orders if o.execution_price]
        
        if market_prices or limit_prices:
            if market_prices:
                ax3.hist(market_prices, alpha=0.6, label='Market', bins=10, color='#2E86AB')
            if limit_prices:
                ax3.hist(limit_prices, alpha=0.6, label='Limit', bins=10, color='#A23B72')
            ax3.set_xlabel('Execution Price ($)', fontweight='bold')
            ax3.set_ylabel('Frequency', fontweight='bold')
            ax3.set_title('Execution Price Distribution', fontweight='bold')
            ax3.legend()
        
        # 4. Summary Statistics Table
        ax4 = axes[1, 1]
        ax4.axis('tight')
        ax4.axis('off')
        
        summary_data = [
            ['Metric', 'Market Orders', 'Limit Orders'],
            ['Total Orders', len(market_orders), len(limit_orders)],
            ['Executed', len([o for o in market_orders if o.status.value == 'EXECUTED']),
             len([o for o in limit_orders if o.status.value == 'EXECUTED'])],
            ['Pending', len([o for o in market_orders if o.status.value == 'PENDING']),
             len([o for o in limit_orders if o.status.value == 'PENDING'])],
            ['Avg Exec Time', f"{avg_market_time:.2f}s", f"{avg_limit_time:.2f}s"],
        ]
        
        if market_prices:
            summary_data.append(['Avg Price', f"${np.mean(market_prices):.2f}",
                               f"${np.mean(limit_prices):.2f}" if limit_prices else 'N/A'])
        
        table = ax4.table(cellText=summary_data, cellLoc='center', loc='center',
                         colWidths=[0.4, 0.3, 0.3])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Style header row
        for i in range(3):
            table[(0, i)].set_facecolor('#2E86AB')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Comparison chart saved to {save_path}")
        
        plt.show()
    
    def print_order_table(self, orders):
        """Print formatted table of orders"""
        if not orders:
            print("No orders to display")
            return
        
        headers = ['Order ID', 'Type', 'Side', 'Quantity', 'Limit Price', 
                  'Exec Price', 'Status', 'Exec Time']
        
        rows = []
        for order in orders:
            exec_delay = order.get_execution_delay()
            exec_delay_str = f"{exec_delay:.2f}s" if exec_delay else 'N/A'
            
            rows.append([
                order.order_id,
                order.order_type.value,
                order.side.value,
                order.quantity,
                f"${order.limit_price:.2f}" if order.limit_price else 'N/A',
                f"${order.execution_price:.2f}" if order.execution_price else 'N/A',
                order.status.value,
                exec_delay_str
            ])
        
        print("\n" + tabulate(rows, headers=headers, tablefmt='grid'))
    
    def generate_performance_report(self, orders, price_history):
        """
        Generate comprehensive performance report
        
        Args:
            orders: List of Order objects
            price_history: List of price data dicts
        """
        print("\n" + "="*70)
        print("PERFORMANCE REPORT".center(70))
        print("="*70 + "\n")
        
        # Separate by type
        market_orders = [o for o in orders if o.order_type.value == 'MARKET']
        limit_orders = [o for o in orders if o.order_type.value == 'LIMIT']
        
        # Overall statistics
        print("OVERALL STATISTICS:")
        print(f"  Total Orders: {len(orders)}")
        print(f"  Market Orders: {len(market_orders)}")
        print(f"  Limit Orders: {len(limit_orders)}")
        print()
        
        # Market Orders Analysis
        if market_orders:
            executed_market = [o for o in market_orders if o.status.value == 'EXECUTED']
            print("MARKET ORDERS:")
            print(f"  Executed: {len(executed_market)} / {len(market_orders)} "
                  f"({len(executed_market)/len(market_orders)*100:.1f}%)")
            
            if executed_market:
                exec_times = [o.get_execution_delay() for o in executed_market]
                exec_prices = [o.execution_price for o in executed_market]
                print(f"  Avg Execution Time: {np.mean(exec_times):.2f}s")
                print(f"  Avg Execution Price: ${np.mean(exec_prices):.2f}")
                print(f"  Price Range: ${min(exec_prices):.2f} - ${max(exec_prices):.2f}")
            print()
        
        # Limit Orders Analysis
        if limit_orders:
            executed_limit = [o for o in limit_orders if o.status.value == 'EXECUTED']
            pending_limit = [o for o in limit_orders if o.status.value == 'PENDING']
            
            print("LIMIT ORDERS:")
            print(f"  Executed: {len(executed_limit)} / {len(limit_orders)} "
                  f"({len(executed_limit)/len(limit_orders)*100:.1f}%)")
            print(f"  Pending: {len(pending_limit)}")
            
            if executed_limit:
                exec_times = [o.get_execution_delay() for o in executed_limit]
                exec_prices = [o.execution_price for o in executed_limit]
                print(f"  Avg Execution Time: {np.mean(exec_times):.2f}s")
                print(f"  Avg Execution Price: ${np.mean(exec_prices):.2f}")
                print(f"  Price Range: ${min(exec_prices):.2f} - ${max(exec_prices):.2f}")
            print()
        
        # Market Statistics
        if price_history:
            prices = [p['price'] for p in price_history]
            print("MARKET STATISTICS:")
            print(f"  Price Observations: {len(prices)}")
            print(f"  Avg Price: ${np.mean(prices):.2f}")
            print(f"  High: ${max(prices):.2f}")
            print(f"  Low: ${min(prices):.2f}")
            print(f"  Volatility (Std Dev): ${np.std(prices):.2f}")
            print(f"  Range: ${max(prices) - min(prices):.2f}")
        
        print("\n" + "="*70 + "\n")






