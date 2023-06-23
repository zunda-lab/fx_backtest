from .zun_util import get_sl_by_pips

class StrategyLoss:

    def loss_next(self):
        eval(f'self.loss_next_{self.loss_method_no:03}')()
        
class StrategyLossFix(StrategyLoss):

    def loss_init(self):
        pass

    def loss_next_000(self):
        trade = self.trades[0]
        pips = 100
        sl = get_sl_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.sl = sl

    def loss_next_001(self):
        trade = self.trades[0]
        pips = 150
        sl = get_sl_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.sl = sl

    def loss_next_002(self):
        losses = {
            '1m': 100,
            '1w': 100,
            '1d': 100,
            '4h': 75,
            '1h': 75,
            '30min': 75,
            '15min': 50,
            '5min': 50,
            '1min': 50,
        }
        # losses = {
        #     '1m': 100,
        #     '1w': 100,
        #     '1d': 100,
        #     '4h': 75,
        #     '1h': 75,
        #     '30min': 75,
        #     '15min': 50,
        #     '5min': 50,
        #     '1min': 50,
        # }
        trade = self.trades[0]
        pips = losses[self.period]
        sl = get_sl_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.sl = sl

    def loss_next_003(self):
        trade = self.trades[0]
        pips = 50
        sl = get_sl_by_pips(trade.entry_price, pips, is_long=trade.is_long)
        trade.sl = sl

    def loss_next_004(self):
        pass
