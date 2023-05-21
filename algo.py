
from blueshift.api import schedule_function, order_target_percent, symbol
from blueshift.api import date_rules, order_target, time_rules
from blueshift.library.library import init_prune_tracking, place_order, finish_prune_tracking
from blueshift.library.library import squareoff, get_history, alpha_function


def initialize(context):
    context.universe = [symbol('ADANIGREEN')]
    context.rsi = {}
    context.my_9ema = {}
    context.p = {}
    schedule_function(scheduled_func_388434, date_rules.month_end(
        days_offset=0), time_rules.market_open(hours=0, minutes=5))
    schedule_function(scheduled_func_388452, date_rules.every_day(),
        time_rules.market_open(hours=0, minutes=5))


def scheduled_func_388434(context, data):
    init_prune_tracking(context, 'SCHEDULE')
    context.history_1d = get_history(data, context.universe, ['close'], 65,
        '1d')
    for asset in context.universe:
        context.my_9ema[asset] = alpha_function(context.history_1d, asset,
            func='exponential_moving_average', kwargs={'lookback': 50})
        context.p[asset] = alpha_function(context.history_1d, asset, func=
            'ohlcv', kwargs={'field': 'close'})
    for asset in context.universe:
        if context.p[asset] < context.my_9ema[asset]:
            squareoff(context)
            place_order(context, asset, order_target_percent, -1, None,
                'SCHEDULE')
    finish_prune_tracking(context, 'SCHEDULE')


def scheduled_func_388452(context, data):
    init_prune_tracking(context, 'SCHEDULE')
    for asset in context.universe:
        place_order(context, asset, order_target, 36000, None, 'SCHEDULE')
    finish_prune_tracking(context, 'SCHEDULE')
