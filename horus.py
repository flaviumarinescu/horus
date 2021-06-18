# -*- coding: utf-8 -*-


from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from MainWindow import Ui_MainWindow
from PyQt5.QtGui import QIcon

import finplot as fplt
import pickle
from typing import Dict, Union
import os
from datetime import datetime, timedelta
from base import stock_data
from icecream import ic as print


class HorusApp(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Horus")
        self.setWindowIcon(QIcon("logo.jpg"))
        self.myconfig = Config()

        self.yf_params = {}
        self.strategy_params = {}
        self.level_params = {}

        self.plots = []
        self.ax = fplt.create_plot(init_zoom_periods=100, maximize=False)
        self.axs = [self.ax]  # finplot requires this property
        self.axo = self.ax.overlay()
        self.ui.gridLayout.addWidget(self.ax.vb.win, 1, 0)
        fplt.show(qt_exec=False)

        self.show()
        self.ui.TickerInput.returnPressed.connect(self.return_pressed)
        self.ui.LockUnlock.clicked.connect(self.freeze_form)

    @qtc.pyqtSlot(bool)
    def freeze_form(self):
        if not self.ui.TickerInput.text():
            qtw.QMessageBox.critical(
                self,
                "Error",
                "Please provide a ticker",
            )
            self.ui.LockUnlock.setChecked(False)
            return
        if self.ui.LockUnlock.isChecked():
            self.ui.ContextTab.setEnabled(False)
            self.ui.LevelsTab.setEnabled(False)
            self.myconfig.save(self.extract_form_data())
        else:
            self.ui.ContextTab.setEnabled(True)
            self.ui.LevelsTab.setEnabled(True)
            self.myconfig.remove(self.ui.TickerInput.text())

    @qtc.pyqtSlot()
    def return_pressed(self):
        ticker = self.ui.TickerInput.text()
        if not ticker:
            qtw.QMessageBox.critical(
                self,
                "Error",
                "Please provide a ticker",
            )
            return

        if ticker in self.myconfig.data:
            self.config_to_form(ticker)

        self.plots = []
        self.process_form(ticker)
        self.update()

        refresh = int(self.ui.RefreshSpin.value())
        if refresh:
            self.ui.LockUnlock.setChecked(True)
            self.freeze_form()
            fplt.timer_callback(self.update, refresh)

    def extract_form_data(self) -> Dict:
        return {
            self.ui.TickerInput.text(): {
                "refresh": int(self.ui.RefreshSpin.value()),
                "context": {
                    "timeframe": self.ui.TimeframeComboContext.currentText(),
                    "period": int(self.ui.PeriodSpinContext.value()),
                    "medium": self.ui.MediumTimeframeCombo.currentText(),
                    "long": self.ui.LongTimeframeCombo.currentText(),
                },
                "levels": {
                    "period": int(self.ui.PeriodSpinLevels.value()),
                    "timeframe": self.ui.TimeframeComboLevels.currentText(),
                    "type": self.ui.TypeCombo.currentText(),
                    "thickness": float(self.ui.ThicknessSpin.value()),
                    "spacing": float(self.ui.SpacingSpin.value()),
                },
            }
        }

    def config_to_form(self, ticker: str) -> None:
        self.ui.TimeframeComboContext.setCurrentText(
            self.myconfig.data[ticker]["context"]["timeframe"]
        )
        self.ui.PeriodSpinContext.setValue(
            self.myconfig.data[ticker]["context"]["period"]
        )
        self.ui.MediumTimeframeCombo.setCurrentText(
            self.myconfig.data[ticker]["context"]["medium"]
        )
        self.ui.LongTimeframeCombo.setCurrentText(
            self.myconfig.data[ticker]["context"]["long"]
        )
        self.ui.PeriodSpinLevels.setValue(
            self.myconfig.data[ticker]["levels"]["period"]
        )
        self.ui.TimeframeComboLevels.setCurrentText(
            self.myconfig.data[ticker]["levels"]["timeframe"]
        )
        self.ui.TypeCombo.setCurrentText(self.myconfig.data[ticker]["levels"]["type"])
        self.ui.ThicknessSpin.setValue(
            self.myconfig.data[ticker]["levels"]["thickness"]
        )
        self.ui.SpacingSpin.setValue(self.myconfig.data[ticker]["levels"]["spacing"])
        self.ui.ContextTab.setEnabled(False)
        self.ui.LevelsTab.setEnabled(False)
        self.ui.LockUnlock.setChecked(True)

    def process_form(self, ticker: str) -> None:
        data = self.extract_form_data()[ticker]
        self.yf_params = {
            "tickers": ticker,
            "start": datetime.now() - timedelta(days=data["context"]["period"]),
            "end": datetime.now(),
            "interval": data["context"]["timeframe"],
            "rounding": False,
            "prepost": False,
            "progress": False,
            "group_by": "ticker",
        }

        self.strategy_params = {
            "contexts": [],
        }

        if data["context"]["medium"] != "off":
            self.strategy_params["contexts"].append(data["context"]["medium"])
        if data["context"]["long"] != "off":
            self.strategy_params["contexts"].append(data["context"]["long"])

        self.level_params = {
            "thickness": data["levels"]["thickness"],
            "spacing": data["levels"]["spacing"],
            "type": data["levels"]["type"],
            "timeframe": data["levels"]["timeframe"],
            "period": data["levels"]["period"],
        }

    def update(self):
        data = stock_data(self.yf_params, self.strategy_params, self.level_params)
        if not data:
            qtw.QMessageBox.critical(
                self,
                "Error",
                "Request returned empty, please check input params or provider",
            )
            return
        df, levels, contexts = (
            data["df"],
            data["levels"],
            self.strategy_params["contexts"],
        )
        self.setWindowTitle(self.yf_params["tickers"])

        if not self.plots:
            self.ax.reset()  # remove previous plots
            self.axo.reset()  # remove previous plots
            # plots[0]
            self.plots.append(
                fplt.candlestick_ochl(
                    df["open close high low".split()], candle_width=0.7
                )
            )
            self.plots[-1].colors.update(
                dict(
                    bull_body="#14adf8",
                    bull_shadow="#14adf8",
                    bull_frame="#14adf8",
                    bear_body="#148bf8",
                    bear_shadow="#148bf8",
                    bear_frame="#148bf8",
                )
            )

            # fast +  # plots[1]
            self.plots.append(
                fplt.plot(
                    df[df.close >= df.sma_9].sma_9,
                    ax=self.ax,
                    legend="fast",
                    width=1,
                    color="#00ff1e",
                )
            )
            # fast -  # plots[2]
            self.plots.append(
                fplt.plot(
                    df[df.close < df.sma_9].sma_9, ax=self.ax, width=1, color="#d00000"
                )
            )

            # short +  # plots[3]
            self.plots.append(
                fplt.plot(
                    df[df.close >= df.sma_interval].sma_interval,
                    ax=self.ax,
                    legend="short_trend",
                    width=2.5,
                    color="#00ff1e",
                )
            )
            # short -  # plots[4]
            self.plots.append(
                fplt.plot(
                    df[df.close < df.sma_interval].sma_interval,
                    ax=self.ax,
                    width=2.5,
                    color="#d00000",
                )
            )

            try:
                if len(contexts):
                    # medium +  # plots[5]
                    self.plots.append(
                        fplt.plot(
                            df[df.close >= df[f"sma_{contexts[0]}"]][
                                f"sma_{contexts[0]}"
                            ],
                            ax=self.ax,
                            legend="medium_trend",
                            width=4,
                            style=".",
                            color="#00ff1eB3",
                        )
                    )
                    # medium -  # plots[6]
                    self.plots.append(
                        fplt.plot(
                            df[df.close < df[f"sma_{contexts[0]}"]][
                                f"sma_{contexts[0]}"
                            ],
                            ax=self.ax,
                            width=4,
                            style=".",
                            color="#d00000B3",
                        )
                    )
            except IndexError:
                qtw.QMessageBox.information(
                    self,
                    "Info",
                    "Could not generate sma for higher timeframe."
                    "Firstly, If you are plotting stocks use 5m, 15m, 30m timeframe NOT 1h, 2h.\n"
                    "Secondly, check if the above period has enough data to generate 89 sma",
                )
            except Exception as e:
                qtw.QMessageBox.critical(self, "Error", f"Error : {e}")

            try:
                if len(contexts) == 2:
                    # long +  # plots[7]
                    self.plots.append(
                        fplt.plot(
                            df[df.close >= df[f"sma_{contexts[1]}"]][
                                f"sma_{contexts[1]}"
                            ],
                            ax=self.ax,
                            legend="long_trend",
                            width=7,
                            style=".",
                            color="#00ff1e80",
                        )
                    )
                    # long   # plots[8]
                    self.plots.append(
                        fplt.plot(
                            df[df.close < df[f"sma_{contexts[1]}"]][
                                f"sma_{contexts[1]}"
                            ],
                            ax=self.ax,
                            width=7,
                            style=".",
                            color="#d0000080",
                        )
                    )
            except IndexError:
                qtw.QMessageBox.information(
                    self,
                    "Info",
                    "Could not generate sma for higher timeframe."
                    "Firstly, If you are plotting stocks use 5m, 15m, 30m timeframe NOT 1h, 2h.\n"
                    "Secondly, check if the above period has enough data to generate 89 sma",
                )
            except Exception as e:
                qtw.QMessageBox.critical(self, "Error", f"Error : {e}")

            fplt.refresh()  # refresh autoscaling when all plots complete

        else:
            self.plots[0].update_data(df["open close high low".split()])

            self.plots[1].update_data(df[df.close >= df.sma_9].sma_9)

            self.plots[2].update_data(df[df.close < df.sma_9].sma_9)

            self.plots[3].update_data(df[df.close >= df.sma_interval].sma_interval)

            self.plots[4].update_data(df[df.close < df.sma_interval].sma_interval)

            try:
                if len(contexts):
                    self.plots[5].update_data(
                        df[df.close >= df[f"sma_{contexts[0]}"]][f"sma_{contexts[0]}"]
                    )
                    self.plots[6].update_data(
                        df[df.close < df[f"sma_{contexts[0]}"]][f"sma_{contexts[0]}"]
                    )
            except Exception as e:
                print("Error", f"Error : {e}")

            try:
                if len(contexts) == 2:
                    self.plots[7].update_data(
                        df[df.close >= df[f"sma_{contexts[1]}"]][f"sma_{contexts[1]}"]
                    )

                    self.plots[8].update_data(
                        df[df.close < df[f"sma_{contexts[1]}"]][f"sma_{contexts[1]}"]
                    )
            except Exception as e:
                print("Error", f"Error : {e}")

        my_list = [x.strftime("%Y-%m-%d %H:%M:%S") for x in df.index.to_list()]
        for indx, row in levels.iterrows():
            try:
                x = df.index[my_list.index(indx.strftime("%Y-%m-%d %H:%M:%S")) :]
            except ValueError as e:
                print(f"Unable to plot s/r : {row.start}-> {row.end} : {e}")
            else:
                fplt.plot(
                    x, len(x) * [row.start], ax=self.ax, color="#00fff966", width=4.5
                )
                fplt.plot(
                    x, len(x) * [row.end], ax=self.ax, color="#00fff966", width=4.5
                )
        # fplt.refresh()  # refresh autoscaling when all plots complete


class Config:
    def __init__(self):
        if not os.path.exists("myconfig"):
            self.data = {}
            with open("myconfig", "wb") as file:
                pickle.dump(self.data, file)
        else:
            with open("myconfig", "rb") as file:
                self.data = pickle.load(file)

    def load(self, ticker: str) -> Union[Dict, None]:
        return self.data.get(ticker, None)

    def save(self, data: Dict) -> None:
        self.data.update(data)
        with open("myconfig", "wb") as file:
            pickle.dump(self.data, file)

    def remove(self, ticker: str) -> None:
        del self.data[ticker]
        with open("myconfig", "wb") as handle:
            pickle.dump(self.data, handle)


def apply_style(app):
    from PyQt5.QtGui import QPalette, QColor
    from PyQt5.QtCore import Qt

    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(212, 175, 55))  # Qt.white
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, QColor(212, 175, 55))  # Qt.white
    dark_palette.setColor(QPalette.Text, QColor(212, 175, 55))  #  Qt.white
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(212, 175, 55))
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(
        QPalette.Disabled, QPalette.ButtonText, Qt.darkGray
    )  # Qt.white
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    app.setPalette(dark_palette)
    return app


if __name__ == "__main__":
    app = qtw.QApplication([])
    app = apply_style(app)
    window = HorusApp()
    window.show()
    app.exec_()
