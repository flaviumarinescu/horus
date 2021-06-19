# -*- coding: utf-8 -*-


import pandas as pd
from pandas.core.base import PandasObject
from datetime import datetime, timedelta
from typing import List, Dict, Union
from icecream import ic as print
import yfinance as yf
import numpy as np

try:
    from talib import (
        CDLHAMMER,
        CDLHANGINGMAN,
        CDLENGULFING,
        CDLDARKCLOUDCOVER,
        CDLPIERCING,
        CDLHARAMI,
        CDLHARAMICROSS,
        CDLEVENINGSTAR,
        CDLMORNINGSTAR,
        CDLEVENINGDOJISTAR,
        CDLMORNINGDOJISTAR,
        CDLGRAVESTONEDOJI,
        CDLLONGLEGGEDDOJI,
        CDLSPINNINGTOP,
        CDLHIGHWAVE,
        CDLDOJI,
    )
except Exception as e:
    print(f"Talib not found, do not call candles function : {e}")


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
    "contexts": ["2h", "4h"],
}

level_params = {
    "thickness": 0.007,
    "spacing": 1,
    "type": "filtered",
    "timeframe": "2h",
    "period": 15,
}


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


def strategy89(df: pd.DataFrame, contexts: List[str]) -> pd.DataFrame:
    """
    Adds strategy data to dataframe
    """
    for context in contexts:
        sma = (
            df["close"]
            .change_context(timeframe=context)["close"]
            .rolling(window=89)
            .mean()
        )
        sma.name = f"sma_{context}"
        df = pd.merge(df, sma, how="left", left_index=True, right_index=True)
        df[sma.name].fillna(method="ffill", inplace=True)

    df["sma_interval"] = df.close.rolling(window=89).mean()
    df["sma_9"] = df.close.rolling(window=9).mean()

    if not df.empty:
        return df
    else:
        raise Exception("Not enough data to generate strategy paramenters")


def candles(df: pd.DataFrame) -> pd.DataFrame:
    CANDLESTICK_PATTERNS = {
        "hammer": {"check": CDLHAMMER, "meaning": "trend reversal / bullish"},
        "hanging_man": {"check": CDLHANGINGMAN, "meaning": "trend reversal / bearish"},
        "engulfing": {"check": CDLENGULFING, "meaning": "trend reversal"},
        "dark_cloud": {"check": CDLDARKCLOUDCOVER, "meaning": "bearish"},
        "piercing": {"check": CDLPIERCING, "meaning": "bullish"},
        "harami": {"check": CDLHARAMI, "meaning": "trend exhaustion"},
        "harami_cross": {"check": CDLHARAMICROSS, "meaning": "trend exhaustion"},
        "evening_star": {"check": CDLEVENINGSTAR, "meaning": "bearish"},
        "evening_doji_star": {"check": CDLEVENINGDOJISTAR, "meaning": "bearish"},
        "morning_star": {"check": CDLMORNINGSTAR, "meaning": "bullish"},
        "morning_doji_star": {"check": CDLMORNINGDOJISTAR, "meaning": "bullish"},
        "long_legged_doji": {
            "check": CDLLONGLEGGEDDOJI,
            "meaning": "trend reversal / indecision",
        },
        "gravestone": {
            "check": CDLGRAVESTONEDOJI,
            "meaning": "trend reversal / indecision",
        },
        "spinning_tops": {
            "check": CDLSPINNINGTOP,
            "meaning": "trend reversal / indecision",
        },
        "high_wave": {"check": CDLHIGHWAVE, "meaning": "trend reversal / indecision"},
        "doji": {"check": CDLDOJI, "meaning": "trend reversal / indecision"},
    }

    df_patterns, patterns = (
        pd.DataFrame(
            {
                each: list(
                    CANDLESTICK_PATTERNS[each]["check"](
                        df["open"], df["high"], df["low"], df["close"]
                    )
                )
                for each in CANDLESTICK_PATTERNS
            },
            index=df.index,
        ),
        {each: CANDLESTICK_PATTERNS[each]["meaning"] for each in CANDLESTICK_PATTERNS},
    )

    data = {"Datetime": [], "patterns": []}
    for index, row in df_patterns.iterrows():
        if row.any():
            data["Datetime"].append(index)
            temp = ""
            for pattern in df_patterns[-1:].columns:
                if row[f"{pattern}"]:
                    temp += (
                        f"{pattern}({row[F'{pattern}']})  {patterns[F'{pattern}']}, "
                    )
            data["patterns"].append(temp)

    return pd.DataFrame.from_dict(data).set_index("Datetime")


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
