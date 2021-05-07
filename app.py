import finplot as fplt
from base import stock_data
import pandas as pd
from datetime import datetime, timedelta
from typing import List


def update_plot(df: pd.DataFrame, levels: pd.DataFrame, contexts: List[str]):
    now = datetime.now()

    if not plots:
        # first time we create the plots
        global ax

        plots["candles"] = fplt.candlestick_ochl(
            df["open close high low".split()], candle_width=0.7
        )
        plots["candles"].colors.update(
            dict(
                bull_body="#14adf8",
                bull_shadow="#14adf8",
                bull_frame="#14adf8",
                bear_body="#148bf8",
                bear_shadow="#148bf8",
                bear_frame="#148bf8",
            )
        )
        plots["fast_+"] = fplt.plot(
            df[df.close >= df.sma_9].sma_9,
            ax=ax,
            legend="fast",
            width=1,
            color="#00ff1e",
        )
        plots["fast_-"] = fplt.plot(
            df[df.close < df.sma_9].sma_9, ax=ax, width=1, color="#d00000"
        )
        plots["short_trend_+"] = fplt.plot(
            df[df.close >= df.sma_interval].sma_interval,
            ax=ax,
            legend="short_trend",
            width=2.5,
            color="#00ff1e",
        )
        plots["short_trend_-"] = fplt.plot(
            df[df.close < df.sma_interval].sma_interval,
            ax=ax,
            width=2.5,
            color="#d00000",
        )
        plots["medium_trend_+"] = fplt.plot(
            df[df.close >= df[f"sma_{contexts[0]}"]][f"sma_{contexts[0]}"],
            ax=ax,
            legend="medium_trend",
            width=4,
            style=".",
            color="#00ff1eB3",
        )
        plots["medium_trend_-"] = fplt.plot(
            df[df.close < df[f"sma_{contexts[0]}"]][f"sma_{contexts[0]}"],
            ax=ax,
            width=4,
            style=".",
            color="#d00000B3",
        )
        plots["long_trend_+"] = fplt.plot(
            df[df.close >= df[f"sma_{contexts[1]}"]][f"sma_{contexts[1]}"],
            ax=ax,
            legend="long_trend",
            width=7,
            style=".",
            color="#00ff1e80",
        )
        plots["long_trend_-"] = fplt.plot(
            df[df.close < df[f"sma_{contexts[1]}"]][f"sma_{contexts[1]}"],
            ax=ax,
            width=7,
            style=".",
            color="#d0000080",
        )
        plots["volume"] = fplt.volume_ocv(
            df[["open", "close", "volume"]], ax=ax.overlay()
        )
        plots["volume"].colors.update(
            dict(
                bull_body="#00ff1e40",
                bull_frame="#00ff1e66",
                bear_body="#d0000040",
                bear_frame="#d0000066",
            )
        )

        my_list = [x.strftime("%Y-%m-%d %H:%M:%S") for x in df.index.to_list()]
        for indx, row in levels.iterrows():
            try:
                x = df.index[my_list.index(indx.strftime("%Y-%m-%d %H:%M:%S")):]
            except ValueError:
                print(f"Unable to plot s/r : {row.start}-> {row.end}")
            else:
                fplt.plot(x, len(x) * [row.start], ax=ax, color="#00fff966", width=4.5)
                fplt.plot(x, len(x) * [row.end], ax=ax, color="#00fff966", width=4.5)
    else:
        if (
            int(now.strftime("%M")) == 3
            or int(now.strftime("%M")) == 18
            or int(now.strftime("%M")) == 33
            or int(now.strftime("%M")) == 48
        ):
            plots["candles"].update_data(df["open close high low".split()], gfx=False)
            plots["fast_+"].update_data(df[df.close >= df.sma_9].sma_9, gfx=False)
            plots["fast_-"].update_data(df[df.close < df.sma_9].sma_9, gfx=False)
            plots["short_trend_+"].update_data(
                df[df.close >= df.sma_interval].sma_interval, gfx=False
            )
            plots["short_trend_-"].update_data(
                df[df.close < df.sma_interval].sma_interval, gfx=False
            )
            plots["medium_trend_+"].update_data(
                df[df.close >= df[f"sma_{contexts[0]}"]][f"sma_{contexts[0]}"],
                gfx=False,
            )
            plots["medium_trend_-"].update_data(
                df[df.close < df[f"sma_{contexts[0]}"]][f"sma_{contexts[0]}"],
                gfx=False,
            )
            plots["long_trend_+"].update_data(
                df[df.close >= df[f"sma_{contexts[1]}"]][f"sma_{contexts[1]}"],
                gfx=False,
            )
            plots["long_trend_-"].update_data(
                df[df.close < df[f"sma_{contexts[1]}"]][f"sma_{contexts[1]}"],
                gfx=False,
            )
            plots["volume"].update_data(df[["open close volume".split()]], gfx=False)
            for key in plots.keys():
                plots[key].update_gfx()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="App")
    parser.add_argument(
        "--market",
        metavar="mk",
        type=str,
        nargs=None,
        required=True,
        help="market you want to check",
    )
    parser.add_argument(
        "--period",
        metavar="p",
        type=int,
        nargs=None,
        default=59,
        help="number of days to download",
    )
    parser.add_argument(
        "--short",
        metavar="s",
        type=str,
        nargs=None,
        default="60m",
        help="short(download) timeframe",
    )
    parser.add_argument(
        "--medium",
        metavar="m",
        type=str,
        nargs=None,
        default="2h",
        help="medium timeframe",
    )
    parser.add_argument(
        "--long",
        metavar="l",
        type=str,
        nargs=None,
        default="4h",
        help="long timeframe",
    )
    parser.add_argument(
        "--levels",
        metavar="lv",
        type=int,
        nargs=None,
        default=10,
        help="how long should sr levels be (in number of days)",
    )

    args = parser.parse_args()
    print(f"Loading with {args}")

    yf_params = {
        "tickers": args.market,
        "start": datetime.now() - timedelta(days=args.period),
        "end": datetime.now(),
        "interval": args.short,
        "rounding": False,
        "prepost": False,
        "progress": False,
        "group_by": "ticker",
    }

    strategy_params = {
        "contexts": [args.medium, args.long],
    }

    level_params = {
        "thickness": 0.007,
        "spacing": 1,
        "type": "filtered",
        "timeframe": "2h",
        "period": args.levels,
    }

    df, levels = stock_data(yf_params, strategy_params, level_params)

    plots = {}
    ax = fplt.create_plot(yf_params["tickers"], rows=1, yscale="liniar")

    update_plot(df, levels, contexts=strategy_params["contexts"])
    fplt.timer_callback(update_plot, 30)
    fplt.show()
