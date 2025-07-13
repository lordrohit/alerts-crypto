import numpy as np

def detect_flag(df):
    recent = df.tail(20)
    closes = recent['close'].values
    direction = closes[-1] - closes[0]

    if direction > 0 and np.std(closes[-5:]) < np.std(closes[:5]):
        return "🚩 Bull Flag"
    elif direction < 0 and np.std(closes[-5:]) < np.std(closes[:5]):
        return "🏴 Bear Flag"
    return None

def detect_wedge(df):
    recent = df.tail(20)
    highs = recent['high'].values
    lows = recent['low'].values

    falling = all(highs[i] > highs[i+1] for i in range(5)) and all(lows[i] > lows[i+1] for i in range(5))
    rising = all(highs[i] < highs[i+1] for i in range(5)) and all(lows[i] < lows[i+1] for i in range(5))

    if falling:
        return "🔻 Falling Wedge (Bullish)"
    elif rising:
        return "🔺 Rising Wedge (Bearish)"
    return None

def detect_head_shoulders(df):
    highs = df['high'].values[-20:]
    if len(highs) < 7:
        return None

    l = highs[-7:]
    if l[0] < l[1] > l[2] and l[3] < l[1] and l[4] < l[5] > l[6]:
        return "🧠 Head & Shoulders"
    return None

def detect_all_patterns(df):
    flag = detect_flag(df)
    wedge = detect_wedge(df)
    hs = detect_head_shoulders(df)
    patterns = [p for p in [flag, wedge, hs] if p]
    return patterns if patterns else None