import pandas as pd
from enum import Enum
from dataclasses import dataclass
from math import floor

SYMBOLS= ["SPY"]

"""

"""
@dataclass
class Order:
    class Side(Enum):
        Buy = 1
        Sell = 2
    symbol: str
    side: Side 
    quantity: int


class BacktestingOrderGateway:
    positions_: pd.Series
    simulation_data_: pd.DataFrame
    tick_num_: int

    def __init__(self, simulation_data: pd.DataFrame):
        self.tick_num_ = 0
        self.simulation_data_ = simulation_data
        self.positions_ = pd.Series(index=SYMBOLS)

    # advance one tick (so that the current prices are the next)
    def advance(self):
        assert self.tick_num_ < self.simulation_data_.shape[0], "advanced past historical data count"
        self.tick_num_ += 1

    def place_order(self, order: Order) -> None:
        assert order.symbol in SYMBOLS, f'unknown symbol: {order.symbol}'

    def pnl(self)-> float:
        """
        Return the PNL up to the current tick.

        This assumes that we liquidate all of our current position
        """
        return 0
"""
    
"""
class OrderGateway:
    positions_: pd.Series
    def __init__(self):
        self.positions_ = pd.Series(index=SYMBOLS)
    def place_order(self, order: Order):
        pass
    def positions(self) -> pd.Series:
        return self.positions_.copy(deep=True)

class Quoter:
    def __init__(self, config, historical_data: pd.DataFrame):
        pass
    def update(self, new_prices: pd.Series):
        pass
    def quotes(self) -> pd.DataFrame:
        return pd.DataFrame()

class Strategy:
    def __init__(self, config, historical_data: pd.DataFrame, gateway):
        self.gateway_ = gateway
        pass
    def update(self, new_prices: pd.Series):
        """
        Called every tick with the new prices from that tick        
        """
        pass
    @staticmethod
    def make(config, historical_data: pd.DataFrame, gateway):
        return Strategy(config, historical_data, gateway)

def run_event_loop(new_prices: pd.Series):
    pass

def backtest_quoter(config, historical_data: pd.DataFrame, make_stgy) -> pd.Series:
    """
    make_stgy is a function f: (Config, historical_data, gateway) -> Strategy

    Returns our PNL after each tick (of the backtest). Please don't just get the 
    tail of this list.
    """
    total_ticks = historical_data.shape[0]

    TRAINING_PCT = .80
    training_ticks = floor(TRAINING_PCT * total_ticks)
    testing_ticks = total_ticks - training_ticks

    training_data = historical_data.iloc[0:training_ticks, :]
    testing_data = historical_data.iloc[training_ticks:, :]

    gateway = BacktestingOrderGateway(testing_data)
    stgy = make_stgy(config, training_data, gateway)

    pnl_table = pd.Series(index=range(testing_ticks))
    for tick_num in range(testing_ticks):
        stgy.update()
        pnl_table[tick_num] = gateway.pnl()

    return pnl_table


if __name__ == "__main__":
    pass
