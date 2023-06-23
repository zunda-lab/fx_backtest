
import datetime as dt
import pandas as pd
from backtesting import Backtest
from bokeh.io import save
from strategy.zun_util import get_ohlc_data
from strategy.strategy import *
# from strategy.strategy_base import *


START_DATE = '2012-01-01'
END_DATE = '2022-12-31'
PAIRS = [
    'AUDCAD',
    'AUDJPY',
    'AUDUSD',
    'CADJPY',
    'CHFJPY',
    'EURAUD',
    'EURCHF',
    'EURGBP',
    'EURJPY',
    'EURUSD',
    'GBPCHF',
    'GBPJPY',
    'GBPUSD',
    'USDCHF',
    'USDJPY',
]
PERIODS = [
    '1d',
    '4h',
    '1h',
    '30min',
    '15min',
    '5min',
]
STRATEGIES = []

def set_strategies():
    global STRATEGIES
    set_strategy_base_clses()
    set_strategy_clses()
    STRATEGIES = list(STRATEGY_CLSES.values())

def main():
    pair = 'USDJPY'
    period = '4h'

    set_strategies()
    # strategy = STRATEGY_CLSES['Mav000_Mav000_Fix000_Fix000']
    # strategy = STRATEGY_CLSES['Adx003_Bko003_Fix002_Fix002']
    strategy = STRATEGY_CLSES['Bbd002_Bbd006_Fix003_Fix003']

    # print(STRATEGY_CLSES.keys())
    df = get_ohlc_data(pair, period, START_DATE, END_DATE)
    bt = Backtest(
        df, # チャートデータ
        strategy, # 売買戦略
        cash=1_000_000, # 最初の所持金
        commission=.0001, # 取引手数料
        margin=1.0, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
        trade_on_close=False, # True：現在の終値で取引，False：次の時間の始値で取引
        hedging=False, # 両方向の取引を同時に許可しない
        exclusive_orders=False #自動でポジションをクローズしない
    )
    result = bt.run(pair=pair, period=period, start=START_DATE, end=END_DATE)
    
    print(result)
    # bt.plot(resample=False)
    print(result._trades)
    # print(result._trades.to_string())

if __name__ == '__main__':
    main()