import sys
sys.path.insert(0, r"C:\Users\katak\Documents\football-signal-hub")
import MetaTrader5 as mt5
from mt5_monitor import check_setups

mt5.initialize()
for pair in ['EURUSD', 'GBPUSD', 'GOLD', 'USDJPY', 'GBPJPY']:
    alerts = check_setups(pair)
    info = mt5.symbol_info_tick(pair)
    sinfo = mt5.symbol_info(pair)
    d = sinfo.digits if sinfo else 5
    if info:
        print(f"{pair}: ${info.bid:.{d}f} | {len(alerts)} alert(s)")
        for a in alerts:
            print(f"  >> {a}")
mt5.shutdown()
