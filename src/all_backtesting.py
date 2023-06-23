import warnings
# warnings.resetwarnings()
# warnings.simplefilter('ignore', [DeprecationWarning, FutureWarning])
# from bokeh.util.warnings import BokehDeprecationWarning
# warnings.simplefilter('ignore', [BokehDeprecationWarning])

import datetime as dt
import inspect
import os
import pathlib
import pandas as pd
import numpy as np
from backtesting import Backtest
from bokeh.io import save
from strategy.strategy import *
from strategy import strategy

# SAVE_RESULTS_DIR = '/Users/ono/fx_backtest/bt_results'
SAVE_RESULTS_DIR = '/Users/ono/Google Drive/マイドライブ/bt_results'
SAVE_SUBDIR = '.'
START_DATE = '2012-01-01'
END_DATE = '2022-12-31'
PAIRS = [
    # 'AUDCAD',
    # 'AUDJPY',
    # 'AUDUSD',
    # 'CADJPY',
    # 'CHFJPY',
    # 'EURAUD',
    # 'EURCHF',
    # 'EURGBP',
    # 'EURJPY',
    # 'EURUSD',
    # 'GBPCHF',
    # 'GBPJPY',
    # 'GBPUSD',
    # 'USDCHF',
    'USDJPY',
]
PERIODS = [
    # '1d',
    # '4h',
    '1h',
    '30min',
    '15min',
    # '5min',
]
STRATEGIES = []

def get_ohlc_data(pair, period):
    fpath = f'/Users/ono/fx_backtest/hist_data/{pair}_{period}.csv'
    df = pd.read_csv(fpath)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df = df.set_index('DateTime')
    df = df.sort_index()
    df = df[START_DATE:END_DATE]
    return df

def set_strategies():
    global STRATEGIES
    set_strategy_base_clses()
    set_strategy_clses()
    STRATEGIES = list(STRATEGY_CLSES.values())

def main():
    set_strategies()
    for strategy in STRATEGIES:
        for pair in PAIRS:
            for period in PERIODS:
                print(f'backtest({strategy.__name__}, {pair}, {period}) started ... ', end='', flush=True)
                fbase = f'{strategy.__name__}_{pair}_{period}'
                setup, trigger, profit, loss = strategy.__name__.split('_')
                fdir = f'{SAVE_RESULTS_DIR}/{SAVE_SUBDIR}/{setup}/{trigger}/{profit}/{loss}/'
                fpath = f'{fdir}/{fbase}.pkl'
                os.makedirs(fdir, exist_ok=True)
                # if os.path.isfile(fpath):
                #     print('skipped because pkl file existed.')
                #     continue
                df = get_ohlc_data(pair, period)
                bt = Backtest(
                    df, # チャートデータ
                    strategy, # 売買戦略
                    # cash=1_000, # 最初の所持金
                    # commission=.002, # 取引手数料
                    cash=1_000_000, # 最初の所持金
                    commission=.0001, # 取引手数料
                    margin=1.0, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
                    trade_on_close=False, # True：現在の終値で取引，False：次の時間の始値で取引
                    hedging=False, # 両方向の取引を同時に許可しない
                    exclusive_orders=False #自動でポジションをクローズしない
                )
                result = bt.run(pair=pair, period=period, start=START_DATE, end=END_DATE) 

                result = result.drop('_strategy')
                result = result.drop('_equity_curve')
                result = result.drop('_trades')
                trades = result['# Trades'] 
                win_rate = result['Win Rate [%]'] if not np.isnan(result['Win Rate [%]']) else 0
                pf = result['Profit Factor'] if not np.isnan(result['Profit Factor']) else 0
                sqn = result['SQN'] if not np.isnan(result['SQN']) else 0
                padding = ' ' * (5 - len(period))
                # if trades < 100 or pf < 1:
                #     pathlib.Path(fpath).touch()
                # else:
                #     result.to_pickle(fpath)
                result.to_pickle(fpath)
                # fig = bt.plot()
                # fig.children[0].children[0][0].height = 200
                # save(fig, filename=f'{SAVE_RESULTS_DIR}/{fbase}.html')
                print(f'{padding}Trades: {trades:4}, WR: {win_rate:6.2f}, PF: {pf:3.2f}, SQN: {sqn:6.2f} finish.')

if __name__ == '__main__':
    main()