def calculate_trade_levels(df):
  latest_close = df['close'].iloc[-1]
  atr = df['high'].rolling(14).max() - df['low'].rolling(14).min()
  atr_val = atr.iloc[-1]

  sl = latest_close - atr_val * 0.8
  tp = latest_close + (latest_close - sl) * 2

  risk = latest_close - sl
  reward = tp - latest_close
  rr = round(reward / risk, 2) if risk > 0 else 0

  return {
      "entry": round(latest_close, 3),
      "sl": round(sl, 3),
      "tp": round(tp, 3),
      "rr": rr
  }