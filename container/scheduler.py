from huey import crontab, SqliteHuey
import pickle
from base import stock_data, yf_params, Technical, Candle, RedisConnection, redis_params
from datetime import datetime, timedelta
import pandas as pd


huey = SqliteHuey(filename="/tmp/huey.db")


@huey.periodic_task(
    crontab(month="*", day="*", day_of_week="*", hour="*", minute="*/2")
)
def refresh_data():
    res = {}

    with open("myconfig", "rb") as file:
        MARKETS = pickle.load(file)
        print(MARKETS.keys())

    for market in MARKETS:
        tmp = MARKETS[market]
        data = stock_data(
            yf_params={
                **yf_params,
                **{
                    "tickers": market,
                    "interval": tmp["context"]["timeframe"],
                    "start": datetime.now() - timedelta(days=tmp["context"]["period"]),
                    "end": datetime.now(),
                },
            },
            strategy_params={
                "contexts": {key: tmp["context"].get(key) for key in ["medium", "long"]}
            },
            level_params=tmp["levels"],
        )

        if data:
            df, _ = data["df"], data["levels"]

            analysis = pd.concat(
                [
                    Technical.analysis(
                        df,
                        contexts={
                            key: tmp["context"].get(key) for key in ["medium", "long"]
                        },
                    ),
                    Candle.analysis(df),
                ],
                axis=1,
            )

            res[market] = analysis

    with RedisConnection(**redis_params) as conn:
        conn.publish("telegram", pickle.dumps(res))

