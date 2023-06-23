from backtesting.lib import crossover
from backtesting.lib import resample_apply
from backtesting.lib import OHLCV_AGG
from backtesting import Strategy
from backtesting._util import _Array
import talib as ta
from .zun_util import get_mtf_scaling_factor
from .zun_util import resample_dummy_func

class StrategySetupNon:
    def setup_init(self):
        pass

    def setup_next(self):
        return True

class StrategySetupMav:

    def setup_init(self):
        match self.setup_method_no:
            case 0 | 1:
                self.ma_l = self.I(ta.SMA,
                                self.data.Close,
                                timeperiod=75)
                self.ma_s = self.I(ta.SMA,
                                self.data.Close,
                                timeperiod=25)
            case 2 | 3:
                self.mtf_distance = 2
                np_period = get_mtf_scaling_factor(self.period, self.mtf_distance)
                self.ma_l = resample_apply(np_period, ta.SMA, self.data.Close, timeperiod=75)
                self.ma_s = resample_apply(np_period, ta.SMA, self.data.Close, timeperiod=25)
            case 4 | 5:
                self.ma_l = self.I(ta.SMA,
                                self.data.Close,
                                timeperiod=200)
                self.ma_m = self.I(ta.SMA,
                                self.data.Close,
                                timeperiod=75)
                self.ma_s = self.I(ta.SMA,
                                self.data.Close,
                                timeperiod=25)
            case 6 | 7:
                self.mtf_distance = 2
                np_period = get_mtf_scaling_factor(self.period, self.mtf_distance)
                self.ma_s = resample_apply(np_period, ta.SMA, self.data.Close, timeperiod=25)
                self.ma_m = resample_apply(np_period, ta.SMA, self.data.Close, timeperiod=75)
                self.ma_l = resample_apply(np_period, ta.SMA, self.data.Close, 200)

    def setup_next(self):
        match self.setup_method_no:
            case 0 | 2:
                is_approve = self.ma_l[-1] < self.ma_s[-1]
            case 1 | 3:
                is_approve = self.ma_s[-1] < self.ma_l[-1]
            case 4 | 6:
                is_approve = self.ma_l[-1] < self.ma_s[-1] and self.ma_l[-1] < self.ma_m[-1]
            case 5 | 7:
                is_approve = self.ma_s[-1] < self.ma_l[-1] and self.ma_s[-1] < self.ma_m[-1]
        return is_approve


class StrategySetupBbd:
    bb_n = 14
    bb_d = 2
    mtf_distance = 2

    def setup_init(self):
        match self.setup_method_no:
            case 0 | 1:
                self.upper, self.middle, self.lower = self.I(ta.BBANDS, 
                                                            self.data.Close,
                                                            timeperiod=self.bb_n,
                                                            nbdevup=self.bb_d,
                                                            nbdevdn=self.bb_d,
                                                            matype=0)
            case 2 | 3:
                self.mtf_distance = 2
                np_period = get_mtf_scaling_factor(self.period, self.mtf_distance)
                self.upper, self.middle, self.lower = resample_apply(np_period,
                                                                    ta.BBANDS, 
                                                                    self.data.Close,
                                                                    timeperiod=self.bb_n,
                                                                    nbdevup=self.bb_d,
                                                                    nbdevdn=self.bb_d,
                                                                    matype=0)

    def setup_next(self):
        match self.setup_method_no:
            case 0 | 2:
                is_approve = self.upper[-3] < self.data.Close[-3] and \
                            self.upper[-2] < self.data.Close[-2] and \
                            self.upper[-1] < self.data.Close[-1]
            case 1 | 3:
                is_approve = self.data.Close[-3] < self.lower[-3] and \
                            self.data.Close[-2] < self.lower[-2] and \
                            self.data.Close[-1] < self.lower[-1]
        return is_approve

class StrategySetupSar:
    sar_a = 0.02

    def setup_init(self):
        match self.setup_method_no:
            case 0 | 1:
                self.sar = self.I(ta.SAR, 
                                self.data.High,
                                self.data.Low,
                                acceleration=self.sar_a,
                                maximum=0)

    def setup_next(self):
        match self.setup_method_no:
            case 0:
                is_approve = self.sar[-1] < self.data.Low[-1]
            case 1:
                is_approve = self.data.High[-1] < self.sar[-1]
        return is_approve

class StrategySetupAdx:
    adx_n = 14
    pdi_n = 14
    mdi_n = 14
    adx_lo = 25
    mtf_distance = 2

    def setup_init(self):
        match self.setup_method_no:
            case 0 | 1 | 2:
                self.adx = self.I(ta.ADX, 
                                self.data.High,
                                self.data.Low,
                                self.data.Close,
                                timeperiod=self.adx_n)
                self.pdi = self.I(ta.PLUS_DI, 
                                self.data.High,
                                self.data.Low,
                                self.data.Close,
                                timeperiod=self.pdi_n)
                self.mdi = self.I(ta.MINUS_DI, 
                                self.data.High,
                                self.data.Low,
                                self.data.Close,
                                timeperiod=self.mdi_n)
            case 3 | 4 | 5:
                self.mtf_distance = 2
                np_period = get_mtf_scaling_factor(self.period, self.mtf_distance)
                high = resample_apply(np_period, resample_dummy_func, self.data.High)
                low = resample_apply(np_period, resample_dummy_func, self.data.Low)
                close = resample_apply(np_period, resample_dummy_func, self.data.Close)
                self.adx = self.I(ta.ADX, 
                                high,
                                low,
                                close,
                                timeperiod=self.adx_n)
                self.pdi = self.I(ta.PLUS_DI, 
                                high,
                                low,
                                close,
                                timeperiod=self.pdi_n)
                self.mdi = self.I(ta.MINUS_DI, 
                                high,
                                low,
                                close,
                                timeperiod=self.mdi_n)

    def setup_next(self):
        match self.setup_method_no:
            case 0 | 3:
                # 上昇トレンド
                is_approve = self.mdi[-1] < self.pdi[-1] and self.adx_lo < self.adx[-1]
            case 1 | 4:
                # 下降トレンド
                is_approve = self.pdi[-1] < self.mdi[-1] and self.adx_lo < self.adx[-1]
                # レンジ相場
            case 2 | 5:
                is_approve = self.mdi[-1] <= self.pdi[-1] or self.adx[-1] <= self.adx_lo
        return is_approve

