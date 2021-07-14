# -*- coding: utf-8 -*-


import pandas as pd
from pandas.core.base import PandasObject
from datetime import datetime, timedelta
from typing import Dict, Union
import yfinance as yf
import os
import numpy as np
import pickle
from abc import ABC, abstractmethod
import redis


yf_params = {
    "tickers": "eurusd=x",
    "start": datetime.now() - timedelta(days=70),
    "end": datetime.now() - timedelta(days=1),
    "interval": "60m",
    "rounding": False,
    "prepost": False,
    "progress": False,
    "group_by": "ticker",
}

strategy_params = {
    "contexts": {"medium": "2h", "long": "4h"},
}

level_params = {
    "thickness": 0.007,
    "spacing": 1,
    "type": "filtered",
    "timeframe": "2h",
    "period": 15,
}

redis_params = {"host": "redis", "db": 1, "charset": "utf-8", "port": 6379}


class Analysis(ABC):
    @staticmethod
    @abstractmethod
    def analysis(*args, **kwargs) -> pd.DataFrame:
        pass


class Technical(Analysis):
    def analysis(df: pd.DataFrame, contexts: dict, tol: float = 0.005) -> pd.DataFrame:
        df = df.copy()
        tol = (df.high.max() - df.low.min()) * tol

        df.loc[(df.close < df["sma_interval"]), "interval_position"] = -1
        df.loc[(df.close > df["sma_interval"]), "interval_position"] = 1
        df.loc[
            ((df.low - tol) <= df["sma_interval"])
            & ((df.high + tol) >= df["sma_interval"]),
            "interval_position",
        ] = 0

        if contexts["long"] != "off":
            df.loc[(df.close < df[f"sma_{contexts['long']}"]), "long_position"] = -1
            df.loc[(df.close > df[f"sma_{contexts['long']}"]), "long_position"] = 1
            df.loc[
                ((df.low - tol) <= df[f"sma_{contexts['long']}"])
                & ((df.high + tol) >= df[f"sma_{contexts['long']}"]),
                "long_position",
            ] = 0

        if contexts["medium"] != "off":
            df.loc[(df.close < df[f"sma_{contexts['medium']}"]), "medium_position"] = -1
            df.loc[(df.close > df[f"sma_{contexts['medium']}"]), "medium_position"] = 1
            df.loc[
                ((df.low - tol) <= df[f"sma_{contexts['medium']}"])
                & ((df.high + tol) >= df[f"sma_{contexts['medium']}"]),
                "medium_position",
            ] = 0

        df.loc[(df.close < df["sma_fast"]), "fast_position"] = -1
        df.loc[(df.close > df["sma_fast"]), "fast_position"] = 1
        df.loc[
            ((df.low - tol / 2) <= df["sma_fast"])
            & ((df.high + tol / 2) >= df["sma_fast"]),
            "fast_position",
        ] = 0

        return df


class Candle(Analysis):
    def analysis(
        df: pd.DataFrame,
        percentiles: dict = {
            "small_body": 20,
            "big_body": 90,
            "long_wick": 90,
        },
    ) -> pd.DataFrame:
        df = df.copy()

        df["up"] = df.open > df.close
        df["body"] = abs(df.close - df.open)
        df["up_wick"] = 0.0
        df["up_wick"].where(df.up == True, df.high - df.close, inplace=True)

        df["up_wick"].where(df.up == False, df.high - df.open, inplace=True)
        df["down_wick"] = 0.0
        df["down_wick"].where(df.up == True, df.open - df.low, inplace=True)
        df["down_wick"].where(df.up == False, df.close - df.low, inplace=True)

        series = []
        for index, row in df.iterrows():
            tmp = []
            if df.loc[index]["down_wick"] > np.percentile(
                df["down_wick"], percentiles["long_wick"]
            ):
                tmp.append("long down wick")

            if df.loc[index]["up_wick"] > np.percentile(
                df["up_wick"], percentiles["long_wick"]
            ):
                tmp.append("long up wick")

            if df.loc[index]["body"] > np.percentile(
                df["body"], percentiles["big_body"]
            ):
                tmp.append("big body")

            if df.loc[index]["body"] < np.percentile(
                df["body"], percentiles["small_body"]
            ):
                tmp.append("small body")

            tmp = ", ".join(tmp)

            series.append(tmp)

        df["candle"] = series
        return df[["candle"]]


class Cache:
    def __init__(self):
        if not os.path.exists("container/myconfig"):
            self.data = {}
            with open("container/myconfig", "wb") as file:
                pickle.dump(self.data, file)
        else:
            with open("container/myconfig", "rb") as file:
                self.data = pickle.load(file)

    def load(self, ticker: str):
        return self.data.get(ticker, None)

    def save(self, data) -> None:
        self.data.update(data)
        with open("container/myconfig", "wb") as file:
            pickle.dump(self.data, file)

    def remove(self, ticker: str) -> None:
        del self.data[ticker]
        with open("container/myconfig", "wb") as handle:
            pickle.dump(self.data, handle)


class RedisConnection(object):
    def __init__(self, **kwargs):
        self.redis = redis.Redis(**kwargs)
        self.redis.ping()  # will raise ConnectionError if redis not found

    def __enter__(self):
        return self.redis

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.redis


def clean(df: pd.DataFrame, dropna: str = "any") -> pd.DataFrame:
    """
    df :       pd.DataFrame
    dropna :   'all', 'any', None

    Output:
    - a dataframe object with a DateTimeIndex and
        (open, high, low, close, volume) as columns

    What it does:
    - transforms column names to lower-case
    - set the column that contains 'date' to index and
        transforms index to pd.datetime object
    - drops columns that contain 'any' nan values
    - selectes only columns needed for ohlcv
    - removes & resets time-zone to Bucharest
    -
    """
    df.columns = map(str.lower, df.columns)
    date_column = df.columns[df.columns.str.contains("date")]
    if not date_column.empty:
        df.set_index(date_column.values[0], inplace=True)
    df.index = pd.to_datetime(df.index)

    if df.index.tz:
        df = df.tz_convert("Europe/Bucharest")
        df = df.tz_localize(None)

    if dropna:
        df.dropna(how=dropna, inplace=True)
    df = df.reindex(columns=["open", "high", "low", "close", "volume"])

    if not df.empty:
        i = df.index[-1].time()  # since data is from yahoo finance... we need to adapt
        if not (i.second == 0 and (i.minute == 30 or i.minute == 0)):
            return df[:-1]
        else:
            return df
    else:
        raise Exception("DataFrame came empty")


def change_context(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Change DataFrame timeframe
    """
    df = df.resample(timeframe).agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    )
    df.dropna(how="any", inplace=True)
    return df


def strategy89(df: pd.DataFrame, contexts: dict) -> pd.DataFrame:
    """
    Adds strategy data to dataframe
    """
    for context in list(contexts.values()):
        if context != "off":
            sma = (
                df.change_context(timeframe=context)["close"].rolling(window=89).mean()
            )
            sma.name = f"sma_{context}"
            df = pd.merge(df, sma, how="left", left_index=True, right_index=True)
            df[sma.name].fillna(method="ffill", inplace=True)

    df["sma_interval"] = df.close.rolling(window=89).mean()
    df["sma_fast"] = df.close.rolling(window=9).mean()

    if not df.empty:
        return df
    else:
        raise Exception("Not enough data to generate strategy paramenters")


def find_levels(
    df: pd.DataFrame,
    type: str = "filtered",  # filter useses the following two arguments,
    # w/o it all levels are displayed
    spacing: float = 1.2,  # increasing spacing will increase number of levels
    thickness: float = 0.01,  # increase space between upper and lower portion
    # of supply/demand area (as % of price magnitude)
    timeframe: str = "1h",  # pandas compatible timeframe
    period: int = 5,  # how many DAYS to look back for s/r levels
    start: datetime = datetime.now(),  # from here it begins counting back < period >
) -> pd.DataFrame:
    def isSupport(df, i):
        support = (
            df["low"][i] < df["low"][i - 1]
            and df["low"][i] < df["low"][i + 1]
            and df["low"][i + 1] < df["low"][i + 2]
            and df["low"][i - 1] < df["low"][i - 2]
        )
        return support

    def isResistance(df, i):
        resistance = (
            df["high"][i] > df["high"][i - 1]
            and df["high"][i] > df["high"][i + 1]
            and df["high"][i + 1] > df["high"][i + 2]
            and df["high"][i - 1] > df["high"][i - 2]
        )
        return resistance

    def isFarFromLevel(l, s):
        return np.sum([abs(l - x) < s for x in levels]) == 0

    df = df.change_context(timeframe=timeframe)[
        (start - timedelta(days=period)).strftime("%Y-%m-%d") : start.strftime(
            "%Y-%m-%d"
        )
    ]

    levels = []
    mirror = []
    if type == "raw":
        for i in range(2, df.shape[0] - 2):
            if isSupport(df, i):
                levels.append((i, df["low"][i]))
                mirror.append((i, df["low"][i], "s"))
            elif isResistance(df, i):
                levels.append((i, df["high"][i]))
                mirror.append((i, df["high"][i], "r"))
    elif type == "filtered":
        s = np.mean(df["high"] - df["low"]) / spacing
        for i in range(2, df.shape[0] - 2):
            if isSupport(df, i):
                l = df["low"][i]
                if isFarFromLevel(l, s):
                    levels.append((i, l))
                    mirror.append((i, l, "s"))
            elif isResistance(df, i):
                l = df["high"][i]
                if isFarFromLevel(l, s):
                    levels.append((i, l))
                    mirror.append((i, l, "r"))

    level_size = (df.high.max() - df.low.min()) * thickness

    temp = []
    for level in mirror:
        temp.append(
            (
                df.index[level[0]],
                level[1] - 2 * level_size
                if level[2] == "r"
                else level[1] + 2 * level_size,
                level[1],
            )
        )

    return pd.DataFrame(temp, columns=["Datetime", "start", "end"]).set_index(
        "Datetime"
    )


PandasObject.clean = clean
PandasObject.change_context = change_context
PandasObject.add_strategy = strategy89
PandasObject.find_levels = find_levels


def stock_data(
    yf_params: Dict, strategy_params: Dict, level_params: Dict
) -> Union[Dict, None]:
    try:
        df = yf.download(**yf_params)
        df = df.clean()
        levels = df.find_levels(**level_params)
        # Make sure interval and contexts are compatible
        df = df.add_strategy(**strategy_params)
    except Exception as e:
        print(f"Exception raised while trying to obtain data : {e}")
    else:
        # Should return valid output
        return {"df": df, "levels": levels}
    # In case something goes wrong, will return None
    return None


if __name__ == "__main__":
    data = stock_data(yf_params, strategy_params, level_params)
    print(data["levels"])

