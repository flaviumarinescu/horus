from base import yf_params, strategy_params, level_params, stock_data
import pytest
import pandas as pd


@pytest.fixture
def supply_non_working_params():
    # since entire stock_data breakable calls are inside a try except, any modifications to
    # levels_params and strategy params will result in a return of None; this should happen
    # because inputed parameters should be compatible with pandas and in most cases pandas will
    # return empty df
    return {
        "yf_params": {**yf_params, **{"tickers": "NOT_EXISTENT"}},
        "strategy_params": strategy_params,
        "level_params": level_params,
    }


@pytest.fixture
def supply_working_params():
    return {
        "yf_params": yf_params,
        "strategy_params": strategy_params,
        "level_params": level_params,
    }


def test_stock_data(supply_working_params, supply_non_working_params):
    data = stock_data(
        supply_working_params["yf_params"],
        supply_working_params["strategy_params"],
        supply_working_params["level_params"],
    )
    assert type(data["df"]) == pd.DataFrame, "stock_data() did not return pd.DataFrame"
    assert (
        type(data["levels"]) == pd.DataFrame
    ), "stock_data() did not return pd.DataFrame"
    assert not data["df"].empty, "stock_data() returned empty df"

    data = stock_data(
        supply_non_working_params["yf_params"],
        supply_non_working_params["strategy_params"],
        supply_non_working_params["level_params"],
    )
    assert not data, "stock_data() did not return None, upstream df was generated"
