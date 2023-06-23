import talib as ta

def TWO_SMA(close, ns, nl):
    smaS = ta.SMA(close, timeperiod=ns)
    smaL = ta.SMA(close, timeperiod=nl)
    return smaS, smaL

def THREE_SMA(close, ns, nm, nl):
    smaS = ta.SMA(close, timeperiod=ns)
    smaM = ta.SMA(close, timeperiod=nm)
    smaL = ta.SMA(close, timeperiod=nl)
    return smaS, smaM, smaL

def BB(close, n, nu, nd):
    upper, middle, lower = ta.BBANDS(close, timeperiod=n, nbdevup=nu, nbdevdn=nd, matype=0)
    return upper, middle, lower

def MACD(close, fastperiod, slowperiod, signalperiod):
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    return macd, macdsignal, macdhist

def RSI(close, ns, nl):
    rsi_s = ta.RSI(close, timeperiod=ns)
    rsi_l = ta.RSI(close, timeperiod=nl)
    return rsi_s, rsi_l

import numpy as np

def RCI(close: np.ndarray,
        timeperiod: int = 9) -> np.ndarray:
    rci = np.full_like(close, np.nan)
    rank_period = np.arange(1, timeperiod + 1)
    for i in range(timeperiod - 1, len(close)):
        rank_price = close[i - timeperiod + 1:i + 1]
        rank_price = np.argsort(np.argsort(rank_price)) + 1
        aa = 6 * sum((rank_period - rank_price)**2)
        bb = timeperiod * (timeperiod**2 - 1)
        rci[i] = (1 - aa / bb) * 100
    return rci

def vr(df, window=26, type=1):
    """
    Volume Ratio (VR)
    Formula:
    VR[A] = SUM(av + cv/2, n) / SUM(bv + cv/2, n) * 100
    VR[B] = SUM(av + cv/2, n) / SUM(av + bv + cv, n) * 100
    Wako VR = SUM(av - bv - cv, n) / SUM(av + bv + cv, n) * 100
        av = volume if close > pre_close else 0
        bv = volume if close < pre_close else 0
        cv = volume if close = pre_close else 0
    """
    df['av'] = np.where(df['close'].diff() > 0, df['volume'], 0)
    avs = df['av'].rolling(window=window, center=False).sum()
    df['bv'] = np.where(df['close'].diff() < 0, df['volume'], 0)
    bvs = df['bv'].rolling(window=window, center=False).sum()
    df['cv'] = np.where(df['close'].diff() == 0, df['volume'], 0)
    cvs = df['cv'].rolling(window=window, center=False).sum()
    df.drop(['av', 'bv', 'cv'], inplace=True, axis=1)
    if type == 1: # VR[A]
       vr = (avs + cvs / 2) / (bvs + cvs / 2) * 100  
    elif type == 2: # VR[B]
       vr = (avs + cvs / 2) / (avs + bvs + cvs) * 100
    else: # Wako VR
       vr = (avs - bvs - cvs) / (avs + bvs + cvs) * 100
    return vr

