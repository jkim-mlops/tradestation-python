from tradestation_python import TradeStation

ts = TradeStation()
bars = ts.market_data.bars("SMCI", barsback=14)
print(bars)
