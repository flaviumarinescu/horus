from multiprocessing import Process
import telebot
import pickle
import redis
from base import redis_params
from decouple import config


redis_conn = redis.Redis(**redis_params)

bot = telebot.TeleBot(
    config("TELEGRAM_TOKEN"),
    parse_mode=None,
)
CHAT_ID = config("CHAT_ID")

cache = {}


def do_notify(data: dict) -> None:
    message = ""

    for market in data:
        df = (
            data[market]
            .iloc[-2:][
                ["candle", "interval_position", "medium_position", "long_position"]
            ]
            .copy()
        )
        if not df.equals(cache.get(market, None)):
            cache[market] = df.copy()
            last = df.iloc[-1][
                ["interval_position", "medium_position", "long_position"]
            ].values
            before_last = df.iloc[-2][
                ["interval_position", "medium_position", "long_position"]
            ].values
            if not (list(last) == list(before_last)):
                df = df.replace({-1: "bellow", 0: "touch", 1: "above"})
                message += f"{market}\n@{df.iloc[-1].name.strftime('%Y-%m-%d %H:%M')}\n"
                message += f"Candles   : {df.candle.values}\n"
                message += f"Interval    : {df.iloc[-2].interval_position} -> {df.iloc[-1].interval_position}\n"
                message += f"Medium   : {df.iloc[-2].medium_position} -> {df.iloc[-1].medium_position}\n"
                message += f"Long         : {df.iloc[-2].long_position} -> {df.iloc[-1].long_position}\n"
                message += "\n"

    if message:
        bot.send_message(CHAT_ID, message, parse_mode=None)


def sub(channel: str) -> None:
    pubsub = redis_conn.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message.get("type") == "message":
            data = pickle.loads(message.get("data"))
            do_notify(data)


if __name__ == "__main__":
    Process(target=sub, args=("telegram",)).start()
