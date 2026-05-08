"""
Real-time data fetcher for order execution simulation
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time


class RealTimeDataFetcher:
    """Fetches real-time market data using yfinance"""
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        
    def get_current_price(self):
        """Get the current market price"""
        try:
            # Try to get real-time price from fast_info
            data = self.ticker.fast_info
            current_price = data.get('lastPrice', None)
            
            if current_price is None or current_price == 0:
                # Fallback: get most recent price from 1-minute data
                hist = self.ticker.history(period='1d', interval='1m')
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
            
            return current_price
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None
    
    def get_live_data(self, period='1d', interval='1m'):
        """
        Get live intraday data
        
        Args:
            period: Time period ('1d', '5d', etc.)
            interval: Data interval ('1m', '5m', '15m', '1h')
        """
        try:
            data = self.ticker.history(period=period, interval=interval)
            return data
        except Exception as e:
            print(f"Error fetching live data: {e}")
            return pd.DataFrame()
    
    def get_bid_ask_spread(self):
        """Get current bid/ask prices if available"""
        try:
            info = self.ticker.info
            bid = info.get('bid', None)
            ask = info.get('ask', None)
            return bid, ask
        except Exception as e:
            print(f"Error fetching bid/ask: {e}")
            return None, None
    
    def get_market_info(self):
        """Get current market information"""
        try:
            data = self.ticker.fast_info
            info = {
                'symbol': self.symbol,
                'current_price': data.get('lastPrice', None),
                'previous_close': data.get('previousClose', None),
                'open': data.get('open', None),
                'day_high': data.get('dayHigh', None),
                'day_low': data.get('dayLow', None),
                'volume': data.get('lastVolume', None),
                'timestamp': datetime.now()
            }
            return info
        except Exception as e:
            print(f"Error fetching market info: {e}")
            return None
    
    def stream_prices(self, duration_seconds=60, update_interval=5):
        """
        Stream prices for a specified duration
        
        Args:
            duration_seconds: How long to stream (seconds)
            update_interval: Time between updates (seconds)
        
        Yields:
            dict: Price data with timestamp
        """
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            price = self.get_current_price()
            if price:
                yield {
                    'price': price,
                    'timestamp': datetime.now()
                }
            time.sleep(update_interval)


class LivePriceMonitor:
    """Monitor live prices and track changes"""
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.fetcher = RealTimeDataFetcher(symbol)
        self.price_history = []
        
    def start_monitoring(self, callback=None, duration=300, interval=5):
        """
        Start monitoring prices
        
        Args:
            callback: Function to call on each price update
            duration: Monitoring duration in seconds
            interval: Update interval in seconds
        """
        print(f"\n{'='*60}")
        print(f"Starting live monitoring for {self.symbol}")
        print(f"Duration: {duration}s | Update interval: {interval}s")
        print(f"{'='*60}\n")
        
        for price_data in self.fetcher.stream_prices(duration, interval):
            self.price_history.append(price_data)
            
            if callback:
                callback(price_data)
            else:
                self._default_display(price_data)
    
    def _default_display(self, price_data):
        """Default display for price updates"""
        timestamp = price_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        price = price_data['price']
        
        # Calculate change if we have history
        change_str = ""
        if len(self.price_history) > 1:
            prev_price = self.price_history[-2]['price']
            change = price - prev_price
            change_pct = (change / prev_price) * 100
            change_str = f" | Change: ${change:+.2f} ({change_pct:+.2f}%)"
        
        print(f"[{timestamp}] {self.symbol}: ${price:.2f}{change_str}")
    
    def get_price_statistics(self):
        """Get statistics from monitored prices"""
        if not self.price_history:
            return None
        
        prices = [p['price'] for p in self.price_history]
        
        return {
            'count': len(prices),
            'current': prices[-1],
            'high': max(prices),
            'low': min(prices),
            'average': sum(prices) / len(prices),
            'volatility': pd.Series(prices).std(),
            'start_time': self.price_history[0]['timestamp'],
            'end_time': self.price_history[-1]['timestamp']
        }






