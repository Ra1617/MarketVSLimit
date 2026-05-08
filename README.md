# Order Execution Simulator

A real-time order execution simulator that compares **Market Orders** vs **Limit Orders** using live market data from Yahoo Finance (yfinance).

## 🎯 Features

- **Real-Time Data**: Fetches live market prices using yfinance
- **Order Types**: 
  - **Market Orders**: Execute immediately at current market price
  - **Limit Orders**: Execute only when price conditions are met
- **Live Monitoring**: Continuous price tracking with customizable intervals
- **Execution Comparison**: Side-by-side analysis of both order types
- **Visualization**: 
  - Price charts with execution points
  - Comparison analytics
  - Performance metrics
- **Multiple Modes**:
  - Quick Demo
  - Advanced Simulation (multiple orders)
  - Interactive Mode

## 📦 Installation

### Requirements

- Python 3.8+
- pip

### Setup

1. Clone or download this repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Quick Demo (60 seconds)

```bash
python main.py --demo
```

This runs a simple simulation comparing one market order vs one limit order.

### Advanced Simulation

```bash
python main.py --advanced --symbol AAPL --duration 180 --orders 5
```

Creates multiple order pairs and provides comprehensive analysis with visualizations.

**Parameters:**
- `--symbol`: Stock ticker (default: AAPL)
- `--duration`: Simulation duration in seconds (default: 120)
- `--orders`: Number of order pairs to create (default: 5)

### Interactive Mode

```bash
python main.py --interactive
```

Customize your simulation through interactive prompts.

### Custom Simulation

```bash
python main.py --symbol TSLA --duration 300
```

## 📊 Output

The simulator provides:

1. **Live Price Updates**
   - Real-time price monitoring
   - Bid/Ask spread (when available)
   - Price changes and volatility

2. **Order Execution Details**
   - Execution price and time
   - Execution delays
   - Slippage calculations
   - Cost comparison

3. **Visualizations** (saved as PNG files)
   - `execution_chart.png`: Price history with execution points
   - `comparison_chart.png`: Performance comparison between order types

4. **Performance Reports**
   - Execution rates
   - Average execution times
   - Price statistics
   - Detailed order tables

## 🏗️ Project Structure

```
.
├── main.py                 # Main entry point
├── real_time_data.py       # Real-time data fetching
├── order_executor.py       # Order execution logic
├── visualizer.py          # Visualization and reporting
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 📖 How It Works

### Market Orders

- Execute **immediately** at the current market price
- Guaranteed execution (in liquid markets)
- May experience slippage during volatile conditions
- Use the **Ask** price for buys, **Bid** price for sells

### Limit Orders

- Execute **only** when price conditions are met
- Buy Limit: Executes when price ≤ limit price
- Sell Limit: Executes when price ≥ limit price
- May not execute if price never reaches the limit
- Provides price protection

## 💡 Example Scenarios

### Scenario 1: Buying Stock

```
Current Price: $150.00

Market Order (BUY 10 shares):
- Executes immediately at $150.05 (ask price)
- Total Cost: $1,500.50

Limit Order (BUY 10 shares @ $149.00):
- Waits for price to drop
- Executes at $149.00 when price drops
- Total Cost: $1,490.00
- Savings: $10.50
```

### Scenario 2: Selling Stock

```
Current Price: $150.00

Market Order (SELL 10 shares):
- Executes immediately at $149.95 (bid price)
- Total Revenue: $1,499.50

Limit Order (SELL 10 shares @ $151.00):
- Waits for price to rise
- Executes at $151.00 when price rises
- Total Revenue: $1,510.00
- Extra Revenue: $10.50
```

## 📈 Real-Time Data Notes

- **Data Source**: Yahoo Finance via yfinance library
- **Update Frequency**: Configurable (default: 5 seconds)
- **Market Hours**: Best results during market hours (9:30 AM - 4:00 PM ET)
- **Data Delay**: Free data may have 15-20 minute delay
- **Intraday Data**: Uses 1-minute candles for most recent prices

## 🎓 Key Concepts

### Execution Delay
Time between order submission and execution. Market orders typically execute faster than limit orders.

### Slippage
Difference between expected price and actual execution price. Positive slippage means paying more (buy) or receiving less (sell) than expected.

### Bid-Ask Spread
- **Bid**: Highest price buyers are willing to pay
- **Ask**: Lowest price sellers are willing to accept
- **Spread**: Difference between bid and ask

### Execution Rate
Percentage of submitted orders that get executed. Market orders typically have 100% execution rate.

## ⚙️ Configuration Options

Edit the main.py or pass parameters:

- `symbol`: Stock ticker symbol
- `duration`: How long to monitor (seconds)
- `update_interval`: Time between price updates (seconds)
- `limit_offset_pct`: Percentage offset for limit price
- `quantity`: Number of shares per order

## 🔍 Advanced Features

### Custom Callbacks

You can define custom callbacks for price updates:

```python
from real_time_data import LivePriceMonitor

def my_callback(price_data):
    print(f"Price: {price_data['price']}")
    # Your custom logic here

monitor = LivePriceMonitor('AAPL')
monitor.start_monitoring(callback=my_callback, duration=60, interval=5)
```

### Manual Order Management

```python
from order_executor import OrderExecutor, OrderSide
from real_time_data import RealTimeDataFetcher

executor = OrderExecutor()
fetcher = RealTimeDataFetcher('AAPL')

# Create orders
market_order = executor.create_market_order('AAPL', OrderSide.BUY, 10)
limit_order = executor.create_limit_order('AAPL', OrderSide.BUY, 10, 149.00)

# Process market data
current_price = fetcher.get_current_price()
executor.process_market_data('AAPL', current_price)
```

## 🐛 Troubleshooting

### "No data available"
- Check your internet connection
- Verify the stock symbol is correct
- Try during market hours for best results

### "Module not found"
```bash
pip install -r requirements.txt
```

### Visualization errors
Make sure matplotlib is properly installed:
```bash
pip install matplotlib --upgrade
```

## 📝 License

This project is for educational purposes. Use at your own risk. This is not financial advice.

## 🤝 Contributing

Feel free to fork, modify, and use this project for learning about order execution and market dynamics.

## 📚 Further Reading

- [Understanding Order Types](https://www.investopedia.com/investing/basics-trading-stock-know-your-orders/)
- [Market Orders vs Limit Orders](https://www.investopedia.com/ask/answers/100314/whats-difference-between-market-order-and-limit-order.asp)
- [yfinance Documentation](https://pypi.org/project/yfinance/)

## ⚠️ Disclaimer

This simulator uses delayed market data and is intended for educational purposes only. It does not execute real trades. Always consult with a financial advisor before making investment decisions.

---

**Happy Trading! 📊✨**






