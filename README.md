# Gather data from yfinance, analyse data, add technical analysis & plot

Running example :
    $ python horus.py --market='euraud=x' --period=60 --levels=10 --short='60m' --medium='2h' --long='4h'

For help :
    $ python horus.py -h
    usage: horus.py [-h] --market mk [--period p] [--short s] [--medium m]
                    [--long l] [--levels lv]


    optional arguments:
      -h, --help   show this help message and exit
      --market mk  market you want to check
      --period p   number of days to download
      --short s    short(download) timeframe
      --medium m   medium timeframe
      --long l     long timeframe
      --levels lv  how long should sr levels be (in number of days)

