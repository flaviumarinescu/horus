# Gather data from yfinance, analyse data, add technical analysis & plot

![alt text](https://github.com/flaviumarinescu/horus/blob/main/stack.jpg?raw=true)

Can be integrated with any provider by modifying base.py -> stock_data().
Since data is gathered using yfinance, Ticker input must be in yahoo finance style : eurusd=x, eth-usd, gc=f ...

Running example :
```
    $ python horus.py
```
![alt text](https://github.com/flaviumarinescu/horus/blob/main/screen.jpg?raw=true)


To run telegram notifications (docker and docker-compose needed):
    1) Create settings.ini file inside main directory with following structure
```
        [settings]
        CHAT_ID=<chat_id>
        TELEGRAM_TOKEN=<token>
```
        [get id and token from @BotFather](https://core.telegram.org/bots#botfather)

    2) Run
```
        $ docker-compose up
```
Tested with python version 3.7.4
