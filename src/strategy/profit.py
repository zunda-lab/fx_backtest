from backtesting.lib import crossover
import talib as ta
from .zun_talib import RCI
from .zun_util import overnow, undernow
from .zun_util import get_tp_by_pips

class StrategyProfit:
    def profit_next(self):
        eval(f'self.profit_next_{self.profit_method_no:03}')()

class StrategyProfitFix(StrategyProfit):

    def profit_init(self):
        pass
        
    def profit_next_000(self):
        trade = self.trades[0]
        pips = 150
        tp = get_tp_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.tp = tp

    def profit_next_001(self):
        trade = self.trades[0]
        pips = 100
        tp = get_tp_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.tp = tp

    def profit_next_002(self):
        profits = {
            '1m': 150,
            '1w': 150,
            '1d': 150,
            '4h': 100,
            '1h': 100,
            '30min': 100,
            '15min': 50,
            '5min': 50,
            '1min': 50,
        }
        # profits = {
        #     '1m': 150,
        #     '1w': 150,
        #     '1d': 150,
        #     '4h': 100,
        #     '1h': 100,
        #     '30min': 100,
        #     '15min': 50,
        #     '5min': 50,
        #     '1min': 50,
        # }
        self.period
        trade = self.trades[0]
        pips = profits[self.period]
        tp = get_tp_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.tp = tp

    def profit_next_003(self):
        trade = self.trades[0]
        pips = 50
        tp = get_tp_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.tp = tp

    def profit_next_004(self):
        self.position.close()

class StrategyProfitRsi(StrategyProfit):
    rsi_n = 20
    rsi_hi = 75
    rsi_lo = 25

    def profit_init(self):
        self.rsi = self.I(ta.RSI,
                          self.data.Close,
                          timeperiod=self.rsi_n)
        
    def profit_next_000(self):
        if overnow(self.rsi, self.rsi_hi):
            self.position.close()

    def profit_next_001(self):
        if undernow(self.rsi, self.rsi_lo):
            self.position.close()

class StrategyProfitMac(StrategyProfit):
    macd_fn = 12
    macd_sn = 26
    macd_sg = 9

    def profit_init(self):
        self.macd, self.sig, self.hist = self.I(ta.MACD,
                           self.data.Close,
                          fastperiod=self.macd_fn,
                          slowperiod=self.macd_sn,
                          signalperiod=self.macd_sg)
        
    def profit_next_000(self):
        if self.macd[-1] < 0 and crossover(self.sig, self.macd):
            self.position.close()

    def profit_next_001(self):
        if 0 < self.macd[-1] and crossover(self.macd, self.sig):
            self.position.close()

class StrategyProfitStc(StrategyProfit):
    stoch_fk = 5
    stoch_sk = 3
    stoch_sd = 3
    stoch_hi = 80
    stoch_lo = 20

    def profit_init(self):
        self.slowk, self.slowd = self.I(ta.STOCH,
                                        self.data.High,
                                        self.data.Low,
                                        self.data.Close,
                                        fastk_period=self.stoch_fk,
                                        slowk_period=self.stoch_sk,
                                        slowk_matype=0,
                                        slowd_period=self.stoch_sd,
                                        slowd_matype=0)

    def profit_next_000(self):
        if self.stoch_hi < self.slowk[-1] and \
            self.stoch_hi < self.slowd[-1] and \
            undernow(self.slowk, self.slowd):
            self.position.close()

    def profit_next_001(self):
        if self.slowk[-1] < self.stoch_lo and \
            self.slowd[-1] < self.stoch_lo and \
            crossover(self.slowk, self.slowd):
            self.position.close()

class StrategyProfitRci(StrategyProfit):
    rci_n = 9
    rci_hi = 80
    rci_lo = -80

    def profit_init(self):
        self.rci = self.I(RCI,
                          self.data.Close,
                          timeperiod=self.rci_n)
        
    def profit_next_000(self):
        if self.rci[-2] < self.rci_hi and self.rci_hi < self.rci[-1]:
            self.position.close()

    def profit_next_001(self):
        if self.rci_lo < self.rci[-2] and self.rci[-1] < self.rci_lo:
            self.position.close()

class StrategyProfitMav(StrategyProfit):
    ma_n = 20

    def profit_init(self):
        self.ma = self.I(ta.SMA,
                            self.data.Close,
                            timeperiod=self.ma_n)
        
    def profit_next_000(self):
        if crossover(self.data.Close, self.ma):
            self.position.close()

    def profit_next_001(self):
        if crossover(self.ma, self.data.Close):
            self.position.close()

class StrategyProfitBko(StrategyProfit):

    def profit_init(self):
        self.highest20 = self.I(ta.MAX,
                            self.data.Close,
                            timeperiod=20)
        self.lowest20 = self.I(ta.MIN,
                            self.data.Close,
                            timeperiod=20)

    def profit_next_000(self):
        if self.data.Close[-1] < self.lowest20[-2]:
            self.position.close()

    def profit_next_001(self):
        if self.highest20[-2] < self.data.Close[-1]:
            self.position.close()
