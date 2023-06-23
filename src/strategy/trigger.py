from backtesting.lib import crossover
from backtesting.lib import resample_apply
from backtesting.lib import OHLCV_AGG
from backtesting import Strategy
from backtesting._util import _Array
import talib as ta
from .zun_talib import RCI
from .zun_util import get_mtf_scaling_factor, overnow, undernow
from .zun_util import get_sl_by_pips, get_tp_by_pips

ORDER_SIZE = 1000

class StrategyTrigger:
    def trigger_next(self):
        eval(f'self.trigger_next_{self.trigger_method_no:03}')()

class StrategyTriggerTst(StrategyTrigger):
    is_buy = True

    def trigger_init(self):
        pass

    def trigger_next_000(self):
        if self.is_buy:
            self.buy(size=ORDER_SIZE)
            self.is_buy = False
        else:
            self.sell(size=ORDER_SIZE)
            self.is_buy = True

class StrategyTriggerRsi(StrategyTrigger):
    def trigger_init(self):
        self.rsi14 = self.I(ta.RSI,
                          self.data.Close,
                          timeperiod=14)

    # 逆張り
    def trigger_next_000(self):
        if undernow(self.rsi14, 30):
            self.buy(size=ORDER_SIZE)

    # 逆張り
    def trigger_next_001(self):
        if overnow(self.rsi14, 70):
            self.sell(size=ORDER_SIZE)

    # 順張り
    def trigger_next_002(self):
        if overnow(self.rsi14, 70):
            self.buy(size=ORDER_SIZE)

    # 順張り
    def trigger_next_003(self):
        if undernow(self.rsi14, 30):
            self.sell(size=ORDER_SIZE)

class StrategyTriggerMac(StrategyTrigger):
    def trigger_init(self):
        self.macd, self.sig, self.hist = self.I(ta.MACD,
                           self.data.Close,
                          fastperiod=12,
                          slowperiod=26,
                          signalperiod=9)
        
    # MACDがシグナルを上抜けで買い
    def trigger_next_000(self):
        if 0 < self.macd[-1] and crossover(self.macd, self.sig) and \
           self.macd[-2] < self.macd[-1] and self.sig[-2] < self.sig[-1]:
            self.buy(size=ORDER_SIZE)

    # シグナルがMACDを上抜けで買い
    def trigger_next_001(self):
        if self.macd[-1] < 0 and crossover(self.sig, self.macd) and \
           self.macd[-1] < self.macd[-2] and self.sig[-1] < self.sig[-2]:
            self.sell(size=ORDER_SIZE)

class StrategyTriggerStc(StrategyTrigger):
    def trigger_init(self):
        self.slowk, self.slowd = self.I(ta.STOCH,
                                        self.data.High,
                                        self.data.Low,
                                        self.data.Close,
                                        fastk_period=5,
                                        slowk_period=3,
                                        slowk_matype=0,
                                        slowd_period=3,
                                        slowd_matype=0)
        self.fastk, self.fastd = self.I(ta.STOCHF,
                              self.data.High,
                              self.data.Low,
                              self.data.Close,
                              fastk_period=5,
                              fastd_period=3,
                              fastd_matype=0)

    # 売られすぎゾーンでのゴールデンクロス発生で買い
    def trigger_next_000(self):
        if self.slowk[-1] < 20 and \
           self.slowd[-1] < 20 and \
           crossover(self.slowk, self.slowd):
            self.buy(size=ORDER_SIZE)

    # 買われすぎゾーンでのデッドクロス発生で売り
    def trigger_next_001(self):
        if 80 < self.slowk[-1] and \
           80 < self.slowd[-1] and \
           crossover(self.slowd, self.slowk):
            self.sell(size=ORDER_SIZE)

    # 売られすぎゾーンでのゴールデンクロス発生で買い
    def trigger_next_002(self):
        if self.slowk[-1] < 20 and \
           self.slowd[-1] < 20 and \
           crossover(self.slowd, self.fastd):
            self.buy(size=ORDER_SIZE)

    # 買われすぎゾーンでのデッドクロス発生で売り
    def trigger_next_003(self):
        if 80 < self.slowk[-1] and \
           80 < self.slowd[-1] and \
           crossover(self.fastd, self.slowd):
            self.sell(size=ORDER_SIZE)

    # 売られすぎゾーンを超え上昇で買い
    def trigger_next_004(self):
        if self.fastd[-2] < 20 and \
           self.slowd[-2] < 20 and \
           20 < self.fastd[-1] and \
           20 < self.slowd[-1]:
            self.buy(size=ORDER_SIZE)

    # 買われすぎゾーンを超え下降で買い
    def trigger_next_005(self):
        if 80 < self.fastd[-2] and \
           80 < self.slowd[-2] and \
           self.fastd[-1] < 80 and \
           self.slowd[-1] < 80:
            self.sell(size=ORDER_SIZE)

class StrategyTriggerRci(StrategyTrigger):
    def trigger_init(self):
        self.rci9 = self.I(RCI,
                          self.data.Close,
                          timeperiod=9)
        self.rci26 = self.I(RCI,
                          self.data.Close,
                          timeperiod=26)
        self.rci52 = self.I(RCI,
                          self.data.Close,
                          timeperiod=52)

    def trigger_next_000(self):
        if -80 < self.rci9[-2] and self.rci9[-1] < -80:
            self.buy(size=ORDER_SIZE)

    def trigger_next_001(self):
        if self.rci9[-2] < 80 and 80 < self.rci9[-1]:
            self.sell(size=ORDER_SIZE)

    def trigger_next_002(self):
        if self.rci9[-4] < 0 and self.rci9[-3] < 0 and \
           0 < self.rci9[-2] and 0 < self.rci9[-1]:
            self.buy(size=ORDER_SIZE)

    def trigger_next_003(self):
        if 0 < self.rci9[-4] and 0 < self.rci9[-3] and \
           self.rci9[-2] < 0 and self.rci9[-1] < 0:
            self.sell(size=ORDER_SIZE)

    def trigger_next_004(self):
        if self.rci9 < 0 and crossover(self.rci9, self.rci52):
            self.buy(size=ORDER_SIZE)

    def trigger_next_005(self):
        if 0 < self.rci9 and crossover(self.rci52, self.rci9):
            self.sell(size=ORDER_SIZE)

class StrategyTriggerMav(StrategyTrigger):


    def trigger_init(self):
        self.ma5 = self.I(ta.EMA,
                            self.data.Close,
                            timeperiod=5)
        self.ma20 = self.I(ta.EMA,
                            self.data.Close,
                            timeperiod=20)
        self.ma25 = self.I(ta.EMA,
                            self.data.Close,
                            timeperiod=25)
        self.ma75 = self.I(ta.EMA,
                            self.data.Close,
                            timeperiod=75)

    # 移動平均線が終値上抜けで買い
    def trigger_next_000(self):
        if crossover(self.ma20, self.data.Close):
            self.buy(size=ORDER_SIZE)

    # 終値が移動平均線上抜けで売り
    def trigger_next_001(self):
        if crossover(self.data.Close, self.ma20):
            self.sell(size=ORDER_SIZE)

    # 短期移動平均線が中期移動平均線上抜けで買い
    def trigger_next_002(self):
        if crossover(self.ma25, self.ma75) and \
           self.ma25[-2] < self.ma25[-1] and \
           self.ma75[-2] < self.ma75[-1]:
            self.buy(size=ORDER_SIZE)

    # 中期移動平均線が短期移動平均線上抜けで売り
    def trigger_next_003(self):
        if crossover(self.ma75, self.ma25) and \
           self.ma25[-1] < self.ma25[-2] and \
           self.ma75[-1] < self.ma75[-2]:
            self.sell(size=ORDER_SIZE)

    # 超短期移動平均線が短期移動平均線上抜けで買い
    def trigger_next_004(self):
        if crossover(self.ma5, self.ma25) and \
           self.ma5[-2] < self.ma5[-1] and \
           self.ma25[-2] < self.ma25[-1]:
            self.buy(size=ORDER_SIZE)

    # 短期移動平均線が超短期移動平均線上抜けで売り
    def trigger_next_005(self):
        if crossover(self.ma25, self.ma5) and \
           self.ma5[-1] < self.ma5[-2] and \
           self.ma25[-1] < self.ma25[-2]:
            self.sell(size=ORDER_SIZE)

class StrategyTriggerBbd(StrategyTrigger):
    def trigger_init(self):
        self.upper2, self.middle2, self.lower2 = self.I(ta.BBANDS, 
                                                        self.data.Close,
                                                        timeperiod=21,
                                                        nbdevup=2,
                                                        nbdevdn=2,
                                                        matype=0)
        self.upper3, self.middle3, self.lower3 = self.I(ta.BBANDS, 
                                                        self.data.Close,
                                                        timeperiod=21,
                                                        nbdevup=3,
                                                        nbdevdn=3,
                                                        matype=0)
        self.highest20 = self.I(ta.MAX,
                            self.data.Close,
                            timeperiod=20)
        self.lowest20 = self.I(ta.MIN,
                            self.data.Close,
                            timeperiod=20)

    def trigger_next_000(self):
        if self.upper2[-1] < self.data.Close[-1]:
            self.buy(size=ORDER_SIZE)

    def trigger_next_001(self):
        if self.data.Close[-1] < self.lower2[-1]:
            self.sell(size=ORDER_SIZE)

    def trigger_next_002(self):
        if self.highest20[-1] < self.upper2[-1]:
            self.buy(size=ORDER_SIZE)

    def trigger_next_003(self):
        if self.lower2 < self.lowest20[-1]:
            self.sell(size=ORDER_SIZE)

    def trigger_next_004(self):
        if self.data.Close[-1] < self.lower3[-1]:
            self.buy(size=ORDER_SIZE)

    def trigger_next_005(self):
        if self.upper3[-1] < self.data.Close[-1]:
            self.sell(size=ORDER_SIZE)

    def trigger_next_006(self):
        if self.lower3[-1] < self.lowest20[-1]:
            self.buy(size=ORDER_SIZE)

    def trigger_next_007(self):
        if self.highest20[-1] < self.upper3[-1]:
            self.sell(size=ORDER_SIZE)

class StrategyTriggerBko(StrategyTrigger):
    def trigger_init(self):
        self.highest20 = self.I(ta.MAX,
                            self.data.Close,
                            timeperiod=20)
        self.lowest20 = self.I(ta.MIN,
                            self.data.Close,
                            timeperiod=20)
        # self.highest10 = self.I(ta.MAX,
        #                     self.data.Close,
        #                     timeperiod=100)
        # self.lowest10 = self.I(ta.MIN,
        #                     self.data.Close,
        #                     timeperiod=100)

    # 直近高値のブレイクアウト
    def trigger_next_000(self):
        if self.highest20[-2] < self.data.Close[-1]:
            self.buy(size=ORDER_SIZE)

    # 直近安値のブレイクアウト
    def trigger_next_001(self):
        if self.data.Close[-1] < self.lowest20[-2]:
            self.sell(size=ORDER_SIZE)

    # 直近安値のブレイクアウト＋終値連続上昇（逆張り）
    def trigger_next_002(self):
        if self.data.Close[-1] < self.lowest20[-4] and \
            self.data.Close[-3] < self.data.Close[-2] and \
            self.data.Close[-2] < self.data.Close[-1]:
            self.buy(size=ORDER_SIZE)

    # 直近高値のブレイクアウト＋終値連続下降（逆張り）
    def trigger_next_003(self):
        if self.highest20[-4] < self.data.Close[-1] and \
            self.data.Close[-2] < self.data.Close[-3] and \
            self.data.Close[-1] < self.data.Close[-2]:
            self.sell(size=ORDER_SIZE)
