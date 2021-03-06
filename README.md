# Gather data from yfinance, analyse data, add technical analysis & plot

![alt text](https://github.com/flaviumarinescu/horus/blob/main/stack.jpg?raw=true)

Can be integrated with any provider by modifying base.py -> stock_data().
Since data is gathered using yfinance, Ticker input must be in yahoo finance style : eurusd=x, eth-usd, gc=f ...

Running example :
```
    $ pip install -r container/requirements.txt   
    $ python horus.py
```
![alt text](https://github.com/flaviumarinescu/horus/blob/main/screen.jpg?raw=true)


Steps to take in order to run telegram notifications:  
1) Install [docker and docker-compose](https://docs.docker.com/compose/install/)  
2) Get Telegram chat_id and bot token from [@BotFather](https://core.telegram.org/bots#botfather)  
3) Create settings.ini file inside container directory with following structure:  
```
        [settings]
        CHAT_ID=<chat_id>
        TELEGRAM_TOKEN=<token>
```

4) Run  
    
```
        $ docker-compose up
```

Full app flow:

1) start horus.py and input ticker eurusd=x
2) play around with context & levels and press enter on ticker field to refresh data
3) once satisfied toggle lock/unlock -> this will save your config (add as many as you like)
4) if telegram notifications are configured and running, you will get a notification every time price gets close to short/medium/long trend 


Tested with python version 3.7.4 & 3.9

This project is a work in progress!
