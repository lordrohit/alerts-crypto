import os import requests import pandas as pd import matplotlib.pyplot as plt import mplfinance as mpf from ta.trend import EMAIndicator from ta.momentum import RSIIndicator from dotenv import load_dotenv from datetime import datetime from telegram import Update, InputFile from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes import asyncio

load_dotenv()

ENV variables

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") BINANCE_API_KEY = os.getenv("BINANCE_API_KEY") BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY") BASE_URL = "https://fapi.binance.com"

Fetch historical candle data

def get_ohlcv(symbol, interval="15m", limit=100): url = f"{BASE_URL}/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}" res = requests.get(url).json() df = pd.DataFrame(res, columns=['time','open','high','low','close','volume','c1','c2','c3','c4','c5','c6']) df = df[['time','open','high','low','close','volume']].astype(float) df['time'] = pd.to_datetime(df['time'], unit='ms') return df

Create chart and save image

def create_chart(df, symbol): df_chart = df.copy() df_chart.set_index('time', inplace=True) df_chart.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True) mpf.plot(df_chart, type='candle', style='charles', title=symbol, volume=True, mav=(20, 50), savefig=f"{symbol}_chart.png") return f"{symbol}_chart.png"

Basic signal logic

def generate_signal(df): df['EMA20'] = EMAIndicator(df['close'], window=20).ema_indicator() df['EMA50'] = EMAIndicator(df['close'], window=50).ema_indicator() df['RSI'] = RSIIndicator(df['close'], window=14).rsi() latest = df.iloc[-1] if latest['EMA20'] > latest['EMA50'] and latest['RSI'] < 70: return "Buy" elif latest['EMA20'] < latest['EMA50'] and latest['RSI'] > 30: return "Sell" return "Neutral"

Handle /start command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("🤖 Welcome to the Pro Crypto Bot! Use /analyze <symbol> (e.g. /analyze BTCUSDT)")

Handle /analyze command

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE): if len(context.args) == 0: await update.message.reply_text("❗Please provide a symbol. Example: /analyze BTCUSDT") return symbol = context.args[0].upper() try: df = get_ohlcv(symbol) signal = generate_signal(df) chart_path = create_chart(df, symbol)

caption = f"📊 Analysis for {symbol}\nSignal: {signal}"
    with open(chart_path, 'rb') as chart:
        await update.message.reply_photo(photo=chart, caption=caption)
except Exception as e:
    await update.message.reply_text(f"⚠️ Error: {e}")

Main bot runner

if name == "main": app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analyze", analyze))

print("🤖 Bot is running...")
app.run_polling()

