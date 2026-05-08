# Quick Start Guide

Get started with the Order Execution Simulator in just a few steps!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run Your First Simulation

### Option A: Quick Demo (Recommended for first-time users)

```bash
python main.py --demo
```

This will:
- Fetch real-time data for AAPL
- Create one market order and one limit order
- Monitor execution for 60 seconds
- Show you the comparison results

### Option B: Interactive Mode

```bash
python main.py --interactive
```

This lets you:
- Choose your own stock symbol
- Set order parameters
- Customize simulation duration

## 3. Try Different Stocks

```bash
# Microsoft
python main.py --demo --symbol MSFT

# Tesla
python main.py --demo --symbol TSLA

# Google
python main.py --demo --symbol GOOGL

# Amazon
python main.py --demo --symbol AMZN
```

## 4. Advanced Simulation

For a more comprehensive analysis with multiple orders:

```bash
python main.py --advanced --symbol AAPL --duration 180 --orders 5
```

This creates:
- 5 pairs of orders (market + limit)
- Monitors for 3 minutes
- Generates detailed charts and reports
- Saves visualizations as PNG files

## 5. Explore Examples

Run various usage examples:

```bash
python example_usage.py
```

Then choose from:
1. Basic price fetching
2. Price monitoring
3. Simple order execution
4. Comparison simulation
5. Multiple orders
6. Custom callbacks

## Understanding the Output

### Real-Time Updates

```
[14:30:15] AAPL: $150.23 | Change: +$0.15 (+0.10%)
```

- Shows current time
- Current price
- Change from previous reading

### Order Execution

```
✓ EXECUTED: MARKET BUY 10 AAPL @ $150.25
✓ EXECUTED: LIMIT BUY 10 AAPL @ $149.50 (Limit: $149.50)
```

- Shows when orders are filled
- Execution price
- Order details

### Final Summary

```
EXECUTION COMPARISON SUMMARY
====================================

MARKET ORDER:
  Execution Price: $150.25
  Execution Delay: 0.15s
  Total Cost: $1,502.50

LIMIT ORDER:
  Execution Price: $149.50
  Execution Delay: 45.23s
  Total Cost: $1,495.00

COMPARISON:
  Savings with Limit Order: $7.50
```

## Tips for Best Results

### 1. Run During Market Hours

For the most active price movements:
- **US Markets**: 9:30 AM - 4:00 PM ET (Monday-Friday)
- **Pre-market**: 4:00 AM - 9:30 AM ET
- **After-hours**: 4:00 PM - 8:00 PM ET

### 2. Choose Liquid Stocks

Best results with highly traded stocks:
- ✅ AAPL, MSFT, GOOGL, AMZN, TSLA
- ✅ SPY (S&P 500 ETF)
- ✅ QQQ (NASDAQ ETF)

### 3. Adjust Limit Price Offset

For different trading scenarios:

**Conservative (more likely to execute):**
```bash
python main.py --demo --symbol AAPL --duration 120
# Default: 1% offset
```

**Aggressive (less likely to execute but better price):**
```python
# Edit in code: limit_offset_pct=2.0
```

### 4. Monitor for Longer Periods

For limit orders to have time to execute:

```bash
# 5 minutes
python main.py --advanced --duration 300

# 10 minutes
python main.py --advanced --duration 600
```

## Common Use Cases

### 1. Learning Order Types

```bash
python main.py --demo
```

Perfect for understanding how market vs limit orders work.

### 2. Analyzing Price Volatility

```bash
python main.py --advanced --symbol TSLA --duration 300
```

Tesla is known for volatility - great for seeing limit orders in action.

### 3. Testing Trading Strategies

```bash
python example_usage.py
# Choose example 5: Multiple Orders
```

See how different order types perform simultaneously.

### 4. Real-Time Price Alerts

```bash
python example_usage.py
# Choose example 6: Custom Callback
```

Monitor prices and get alerts on significant changes.

## Troubleshooting

### No price data?

1. Check your internet connection
2. Verify stock symbol is correct
3. Try a different stock (some may not have real-time data)

### Orders not executing?

1. Limit orders may need more time - increase `--duration`
2. Limit price might be too far from current price
3. Market may be closed

### Visualization errors?

```bash
pip install matplotlib --upgrade
```

## Next Steps

1. ✅ Run the quick demo
2. ✅ Try different stocks
3. ✅ Experiment with advanced simulation
4. ✅ Explore the example scripts
5. ✅ Customize for your own analysis

## Need Help?

- Read the full `README.md` for detailed documentation
- Check `example_usage.py` for code examples
- Review the source code - it's well-commented!

---

**Ready to start? Run:**

```bash
python main.py --demo
```

Happy simulating! 🚀📈






