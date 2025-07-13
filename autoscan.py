import requests
import time
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from patterns import detect_all_patterns
from strategy import calculate_trade_levels
from main import get_ohlcv, create_chart, send_photo, TELEGRAM_CHAT_ID

BASE_URL = "https://fapi.binance.com"

def get_all_futures_symbols():
    url = f"{BASE_URL}/fapi/v1/exchangeInfo"
    data = requests.get(url).json()
    return [s['symbol'] for s in data['symbols'] if s['contractType'] == 'PERPETUAL' and s['symbol'].endswith("USDT")]

def scan_symbol(symbol, context):
    try:
        df = get_ohlcv(symbol, interval="15m", limit=100)
        df['EMA20'] = EMAIndicator(df['close'], window=20).ema_indicator()
        df['EMA50'] = EMAIndicator(df['close'], window=50).ema_indicator()
        df['RSI'] = RSIIndicator(df['close'], window=14).rsi()

        patterns = detect_all_patterns(df)
        levels = calculate_trade_levels(df)

        if patterns and levels['rr'] >= 1.5 and df['volume'].iloc[-1] > df['volume'].mean():
            chart = create_chart(df, symbol)
            caption = (
                f"🚨 Auto Signal: {symbol} (15m)\n"
                f"🧠 Pattern: {', '.join(patterns)}\n"
                f"📈 Entry: {levels['entry']}\n"
                f"🛡 SL: {levels['sl']}\n"
                f"🎯 TP: {levels['tp']}\n"
                f"⚖ R:R = {levels['rr']}\n"
                f"📊 Confidence: HIGH 🔥"
            )
            send_photo(context, chart, caption)
    except Exception as e:
        print(f"[{symbol}] Scan error: {e}")

def run_auto_scan(context):
    print("🔁 Running auto scan for all symbols...")
    symbols = get_all_futures_symbols()
    for symbol in symbols:
        time.sleep(1.2)  # avoid rate-limit
        scan_symbol(symbol, context)