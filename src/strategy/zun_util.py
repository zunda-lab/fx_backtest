import pandas as pd
import os
import talib as ta

def overnow(indicator, baseline):
    return indicator[-2] < baseline and baseline < indicator[-1]

def undernow(indicator, baseline):
    return baseline < indicator[-2]  and indicator[-1] < baseline

def get_ohlc_data(pair, period, start, end):
    fpath = f'/Users/ono/fx_backtest/hist_data/{pair}_{period}.csv'
    df = pd.read_csv(fpath)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df = df.set_index('DateTime')
    df = df.sort_index()
    df = df[start:end]
    return df

def get_recent_period(period):
    periods = {
        '1m': 12,
        '1w': 24,
        '1d': 20,
        '4h': 6 * 5,
        '1h': 24,
        '30min': 2 * 24,
        '15min': 4 * 12,
        '5min': 12 * 4,
        '1min': 60,
    }
    return periods[period]


def get_highest_recent_price(prices, period):
    recent_period = get_recent_period(period)
    timeperiod = recent_period if recent_period < len(prices) else len(prices)
    highests = ta.MAX(prices, timeperiod=timeperiod)
    return highests[-1]

def get_lowest_recent_price(prices, period):
    recent_period = get_recent_period(period)
    timeperiod = recent_period if recent_period < len(prices) else len(prices)
    lowests = ta.MIN(prices, timeperiod=timeperiod)
    return lowests[-1]


def get_mtf_scaling_factor(period, distance):
    # periods = {
    #     '1m': 0,
    #     '1w': 1,
    #     '1d': 2,
    #     '4h': 3,
    #     '1h': 4,
    #     '30min': 5,
    #     '15min': 6,
    #     '5min': 7,
    #     '1min': 8,
    # }
    # minutes = [
    #     30 * 24 * 60,
    #     7 * 24 * 60,
    #     1 * 24 * 60,
    #     4 * 60,
    #     1 * 60,
    #     30,
    #     15,
    #     5,
    #     1,
    # ]
    # i = periods[period]
    # return minutes[i - distance] / minutes[i]

    periods = {
        '1m': 0,
        '1w': 1,
        '1d': 2,
        '4h': 3,
        '1h': 4,
        '30min': 5,
        '15min': 6,
        '5min': 7,
        '1min': 8,
    }

    np_periods = {
        0: '1M',
        1: '1W',
        2: '1D',
        3: '4H',
        4: '1H',
        5: '30T',
        6: '15T',
        7: '5T',
        8: '1T',
    }
    i = periods[period]
    return np_periods[i - distance]

def get_sl_by_pips(entry_price, sl_pips, is_long):
    if is_long:
        sl = entry_price - pips_to_price(entry_price, sl_pips)
    else:
        sl = entry_price + pips_to_price(entry_price, sl_pips)
    return sl

def get_tp_by_pips(entry_price, tp_pips, is_long):
    if is_long:
        tp = entry_price + pips_to_price(entry_price, tp_pips)
    else:
        tp = entry_price - pips_to_price(entry_price, tp_pips)
    return tp

def pips_to_price(sample_price, pips):
    if str(sample_price).index('.') >= 3:  # JPY pair
        multiplier = 0.01
    else:
        multiplier = 0.0001
    return pips * multiplier

def price_to_pips(price):
    if str(price).index('.') >= 3:  # JPY pair
        multiplier = 0.01
    else:
        multiplier = 0.0001
    pips = round(price / multiplier)
    return int(pips)

def resample_dummy_func(series):
    return series

