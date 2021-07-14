# -*- coding: utf-8 -*-


from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from MainWindow import Ui_MainWindow  # type: ignore
from PyQt5.QtGui import QIcon
import finplot as fplt
from typing import Dict
from datetime import datetime, timedelta
from container.base import stock_data, yf_params, redis_params, Cache


class HorusApp(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.TickerInput.setFocus()
        self.setWindowTitle("Horus")
        self.setWindowIcon(QIcon("logo.jpg"))

        self.myconfig = Cache()
        self.yf_params = yf_params
        self.strategy_params = {}
        self.level_params = {}

        self.plots = []
        self.customize_fplt()
        self.ax = fplt.create_plot(init_zoom_periods=200, maximize=False)
        self.ax.showGrid(True, True)
        self.axs = [self.ax]  # finplot requires this property
        self.axo = self.ax.overlay()
        self.ui.gridLayout.addWidget(self.ax.vb.win, 1, 0)
        fplt.show(qt_exec=False)

        self.ui.TickerInput.returnPressed.connect(self.return_pressed)
        self.ui.LockUnlock.clicked.connect(self.freeze_form)
        self.ui.TickerInput.textChanged.connect(self.input_edit_unfreeze)

        self.show()

    @qtc.pyqtSlot(str)
    def input_edit_unfreeze(self):
        if self.ui.LockUnlock.isChecked():
            self.ui.LockUnlock.setChecked(False)
            self.ui.ContextTab.setEnabled(True)
            self.ui.LevelsTab.setEnabled(True)

    @qtc.pyqtSlot(bool)
    def freeze_form(self):
        if not self.ui.TickerInput.text().upper():
            self.dialog = qtw.QMessageBox.critical(
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
            self.myconfig.remove(self.ui.TickerInput.text().upper())

    @qtc.pyqtSlot()
    def return_pressed(self):
        ticker = self.ui.TickerInput.text().upper()
        if not ticker:
            self.dialog = qtw.QMessageBox.critical(
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
        else:
            fplt._clear_timers()

    def keyPressEvent(self, e):
        if e.key() == qtc.Qt.Key_Escape:
            self.close()
        if e.key() == qtc.Qt.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

    def extract_form_data(self) -> Dict:
        return {
            self.ui.TickerInput.text().upper(): {
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
            **self.yf_params,
            **{
                "tickers": ticker,
                "start": datetime.now() - timedelta(days=data["context"]["period"]),
                "end": datetime.now(),
                "interval": data["context"]["timeframe"],
            },
        }

        self.strategy_params = {
            "contexts": {
                "medium": data["context"]["medium"],
                "long": data["context"]["long"],
            },
        }

        self.level_params = {
            "thickness": data["levels"]["thickness"],
            "spacing": data["levels"]["spacing"],
            "type": data["levels"]["type"],
            "timeframe": data["levels"]["timeframe"],
            "period": data["levels"]["period"],
        }

    def update(self):
        data = stock_data(
            {
                **self.yf_params,
                **{
                    "end": datetime.now(),
                },
            },
            self.strategy_params,
            self.level_params,
        )
        if not data:
            self.dialog = qtw.QMessageBox.critical(
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
                    df[df.close >= df.sma_fast].sma_fast,
                    ax=self.ax,
                    legend="fast",
                    width=1,
                    color="#00ff1e",
                )
            )
            # fast -  # plots[2]
            self.plots.append(
                fplt.plot(
                    df[df.close < df.sma_fast].sma_fast,
                    ax=self.ax,
                    width=1,
                    color="#d00000",
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
                if not contexts["medium"] == "off":
                    # medium +  # plots[5]
                    temp = df[df.close >= df[f"sma_{contexts['medium']}"]][
                        f"sma_{contexts['medium']}"
                    ]
                    if not temp.empty:
                        self.plots.append(
                            fplt.plot(
                                temp,
                                ax=self.ax,
                                legend="medium_trend",
                                width=4,
                                style=".",
                                color="#00ff1eB3",
                            )
                        )
                    # medium -  # plots[6]
                    temp = df[df.close < df[f"sma_{contexts['medium']}"]][
                        f"sma_{contexts['medium']}"
                    ]
                    if not temp.empty:
                        self.plots.append(
                            fplt.plot(
                                temp,
                                ax=self.ax,
                                width=4,
                                style=".",
                                color="#d00000B3",
                            )
                        )
            except IndexError:
                self.dialog = qtw.QMessageBox.information(
                    self,
                    "Info",
                    "Could not generate sma for higher timeframe."
                    "Firstly, If you are plotting stocks use 5m, 15m, 30m timeframe NOT 1h, 2h.\n"
                    "Secondly, check if the above period has enough data to generate 89 sma",
                )
            except Exception as e:
                self.dialog = qtw.QMessageBox.critical(self, "Error", f"Error : {e}")

            try:
                if not contexts["long"] == "off":
                    # long +  # plots[7]
                    temp = df[df.close >= df[f"sma_{contexts['long']}"]][
                        f"sma_{contexts['long']}"
                    ]
                    if not temp.empty:
                        self.plots.append(
                            fplt.plot(
                                temp,
                                ax=self.ax,
                                legend="long_trend",
                                width=7,
                                style=".",
                                color="#00ff1e80",
                            )
                        )
                    # long   # plots[8]
                    temp = df[df.close < df[f"sma_{contexts['long']}"]][
                        f"sma_{contexts['long']}"
                    ]
                    if not temp.empty:
                        self.plots.append(
                            fplt.plot(
                                temp,
                                ax=self.ax,
                                width=7,
                                style=".",
                                color="#d0000080",
                            )
                        )
            except IndexError:
                self.dialog = qtw.QMessageBox.information(
                    self,
                    "Info",
                    "Could not generate sma for higher timeframe."
                    "Firstly, If you are plotting stocks use 5m, 15m, 30m timeframe NOT 1h, 2h.\n"
                    "Secondly, check if the above period has enough data to generate 89 sma",
                )
            except Exception as e:
                self.dialog = qtw.QMessageBox.critical(self, "Error", f"Error : {e}")

            my_list = [x.strftime("%Y-%m-%d %H:%M:%S") for x in df.index.to_list()]
            for indx, row in levels.iterrows():

                if indx.strftime("%Y-%m-%d %H:%M:%S") in my_list:
                    x = df.index[my_list.index(indx.strftime("%Y-%m-%d %H:%M:%S")) :]
                else:
                    x = df.index[
                        my_list.index(
                            (
                                df.loc[
                                    df.index.unique()[
                                        df.index.unique().get_loc(
                                            indx, method="nearest"
                                        )
                                    ]
                                ].name
                            ).strftime("%Y-%m-%d %H:%M:%S")
                        ) :
                    ]

                fplt.plot(
                    x,
                    len(x) * [row.start],
                    ax=self.ax,
                    color="#00fff966",
                    width=4.5,
                )
                fplt.plot(
                    x, len(x) * [row.end], ax=self.ax, color="#00fff966", width=4.5
                )
            fplt.refresh()  # refresh autoscaling when all plots complete
        else:
            self.plots[0].update_data(df["open close high low".split()])

            self.plots[1].update_data(df[df.close >= df.sma_fast].sma_fast)

            self.plots[2].update_data(df[df.close < df.sma_fast].sma_fast)

            self.plots[3].update_data(df[df.close >= df.sma_interval].sma_interval)

            self.plots[4].update_data(df[df.close < df.sma_interval].sma_interval)

            try:
                if not contexts["medium"] == "off":
                    temp = df[df.close >= df[f"sma_{contexts['medium']}"]][
                        f"sma_{contexts['medium']}"
                    ]
                    if not temp.empty:
                        self.plots[5].update_data(temp)
                    temp = df[df.close < df[f"sma_{contexts['medium']}"]][
                        f"sma_{contexts['medium']}"
                    ]
                    if not temp.empty:
                        self.plots[6].update_data(temp)
            except Exception as e:
                print("Error", f"Error : {e}")

            try:
                if not contexts["long"] == "off":
                    temp = df[df.close >= df[f"sma_{contexts['long']}"]][
                        f"sma_{contexts['long']}"
                    ]
                    if not temp.empty:
                        self.plots[7].update_data(temp)
                    temp = df[df.close < df[f"sma_{contexts['long']}"]][
                        f"sma_{contexts['long']}"
                    ]
                    if not temp.empty:
                        self.plots[8].update_data(temp)
            except Exception as e:
                print("Error", f"Error : {e}")

    def customize_fplt(self):
        fplt.legend_border_color = "#000000dd"
        fplt.legend_fill_color = "#00000055"
        fplt.legend_text_color = "#dddddd66"
        fplt.foreground = "#eef"
        fplt.background = "#000000"
        fplt.odd_plot_background = "#f0f0f0"
        fplt.poc_color = "#000060"
        fplt.cross_hair_color = "#ffffff"
        fplt.draw_line_color = "#ffffff"
        fplt.draw_done_color = "#ffffff"
        fplt.clamp_grid = False
        fplt.significant_decimals = 5
        fplt.significant_eps = 1e-5


def apply_style(app: qtw.QApplication) -> qtw.QApplication:
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
    dark_palette.setColor(QPalette.Text, QColor(212, 175, 55))  # Qt.white
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
    import sys
    import os

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = qtw.QApplication(sys.argv)
    app = apply_style(app)
    window = HorusApp()
    window.show()
    sys.exit(app.exec_())
