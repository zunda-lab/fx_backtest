from enum import Enum
import sys
from backtesting import Strategy
from .trigger import *
from .setup import *
from .profit import *
from .loss import *

class Order(Enum):
    BUY = 1
    SELL = 2
    BOTH = 9

SETUPS = {
    'Non': {
        0: {'order': Order.BOTH},
    },
    'Mav': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
        4: {'order': Order.BUY},
        5: {'order': Order.SELL},
        6: {'order': Order.BUY},
        7: {'order': Order.SELL},
    },
    'Bbd': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
    },
    'Sar': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
    },
    'Adx': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BOTH},
        3: {'order': Order.SELL},
        4: {'order': Order.BUY},
        5: {'order': Order.BOTH},
    },
}

TRIGGERS = {
    # 'Tst': {
    #     0: {'order': Order.BOTH},
    # },
    'Rsi': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
    },
    'Mac': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
    },
    'Stc': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
        4: {'order': Order.BUY},
        5: {'order': Order.SELL},
    },
    'Rci': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
        4: {'order': Order.BUY},
        5: {'order': Order.SELL},
    },
    'Mav': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
        4: {'order': Order.BUY},
        5: {'order': Order.SELL},
    },
    'Bko': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
    },
    'Bbd': {
        0: {'order': Order.BUY},
        1: {'order': Order.SELL},
        2: {'order': Order.BUY},
        3: {'order': Order.SELL},
        4: {'order': Order.BUY},
        5: {'order': Order.SELL},
        6: {'order': Order.BUY},
        7: {'order': Order.SELL},
    },
}

PROFITS = {
    'Fix': {
        # 0: {'order': Order.BOTH},
        # 1: {'order': Order.BOTH},
        # 2: {'order': Order.BOTH},
        3: {'order': Order.BOTH},
        # 4: {'order': Order.BOTH},
    },
    # 'Rsi': {
    #     0: {'order': Order.BUY},
    #     1: {'order': Order.SELL},
    # },
    # 'Mac': {
    #     0: {'order': Order.BUY},
    #     1: {'order': Order.SELL},
    # },
    # 'Stc': {
    #     0: {'order': Order.BOTH},
    #     1: {'order': Order.BOTH},
    # },
    # 'Rci': {
    #     0: {'order': Order.BUY},
    #     1: {'order': Order.SELL},
    # },
    # 'Mav': {
    #     0: {'order': Order.BUY},
    #     1: {'order': Order.SELL},
    # },
    # 'Bko': {
    #     0: {'order': Order.BOTH},
    #     1: {'order': Order.BOTH},
    # },
}

LOSSES = {
    'Fix': {
        # 0: {'order': Order.BOTH},
        # 1: {'order': Order.BOTH},
        # 2: {'order': Order.BOTH},
        3: {'order': Order.BOTH},
        # 4: {'order': Order.BOTH},
    },
}

STRATEGY_BASE_CLSES = {}
STRATEGY_CLSES = {}

class StrategyBase(Strategy):
    setup = None
    trigger = None
    start = None
    end = None
    pair = None
    period = None
    period_mtf = None
    is_mtf = None
    mtf_distance = None
    is_long = None

    def init(self):
        self.setup_init()
        self.trigger_init()
        self.profit_init()
        self.loss_init()

    def next(self):
        # print(self.data.Open.df.index[-1])
        hour = self.data.Open.df.index[-1].hour
        # print(hour)
        if hour < 9 or 17 < hour:
        # if hour < 9 or 22 < hour:
            return
        if self.position:
            self.profit_next()
            self.loss_next()
        if self.setup_next():
            self.trigger_next()
        # if self.position:
        #     self.profit_next()
        #     self.loss_next()
        # else:
        #     if self.setup_next():
        #         self.trigger_next()

def set_strategy_base_clses():
    for setup_name in SETUPS.keys():
        for trigger_name in TRIGGERS.keys():
            for profit_name in PROFITS.keys():
                for loss_name in LOSSES.keys():
                    cls_name, cls = gen_strategy_base_cls(setup_name, trigger_name, profit_name, loss_name)
                    STRATEGY_BASE_CLSES[cls_name] = cls
    # print(STRATEGY_BASE_CLSES)

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

def gen_strategy_base_cls(setup_name, trigger_name, profit_name, loss_name):
    cls_name = f'Strategy{setup_name}{trigger_name}{profit_name}{loss_name}'
    l = [str_to_class('StrategyBase'),
                str_to_class(f'StrategySetup{setup_name}'),
                str_to_class(f'StrategyTrigger{trigger_name}'),
                str_to_class(f'StrategyProfit{profit_name}'),
                str_to_class(f'StrategyLoss{loss_name}'),]
    base_cls = tuple(l)
    cls = type(cls_name, base_cls, {})
    return cls_name, cls

def set_strategy_clses():
    for setup_name in SETUPS.keys():
        for setup_method_no, setup_method_attr in SETUPS[setup_name].items():
            for trigger_name in TRIGGERS.keys():
                for trigger_method_no, trigger_method_attr in TRIGGERS[trigger_name].items():
                    for profit_name in PROFITS.keys():
                        for profit_method_no, profit_method_attr in PROFITS[profit_name].items():
                            for loss_name in LOSSES.keys():
                                for loss_method_no, loss_method_attr in LOSSES[loss_name].items():
                                    setup_order = setup_method_attr['order']
                                    trigger_order = trigger_method_attr['order']
                                    profit_order = profit_method_attr['order']
                                    loss_order = loss_method_attr['order']
                                    if is_gen_strategy_cls(setup_order, trigger_order, profit_order, loss_order):
                                        cls_name, cls = gen_strategy_cls(setup_name,
                                                                        setup_method_no,
                                                                        trigger_name,
                                                                        trigger_method_no,
                                                                        profit_name,
                                                                        profit_method_no,
                                                                        loss_name,
                                                                        loss_method_no)
                                        STRATEGY_CLSES[cls_name] = cls

def is_gen_strategy_cls(setup_order, trigger_order, profit_order, loss_order):
    result = False
    judge_orders = []
    for order in [setup_order, trigger_order, profit_order, loss_order]:
        if order != Order.BOTH:
            judge_orders.append(order)
    if not judge_orders:
        result = True
    else:    
        if len(set(judge_orders)) == 1:
            result = True
    return result

def gen_strategy_cls(
        setup_name, setup_method_no,
        trigger_name, trigger_method_no,
        profit_name, profit_method_no,
        loss_name, loss_method_no):
    cls_name = f'{setup_name}{setup_method_no:03}_{trigger_name}{trigger_method_no:03}_{profit_name}{profit_method_no:03}_{loss_name}{loss_method_no:03}'
    base_cls_name = f'Strategy{setup_name}{trigger_name}{profit_name}{loss_name}'
    l = [STRATEGY_BASE_CLSES[base_cls_name]]
    base_cls = tuple(l)
    d = dict(setup_method_no=setup_method_no,
             trigger_method_no=trigger_method_no,
             profit_method_no=profit_method_no,
             loss_method_no=loss_method_no)
    cls = type(cls_name, base_cls, d)
    return cls_name, cls

