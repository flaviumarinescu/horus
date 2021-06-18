# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'horus.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1145, 554)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setToolTip("")
        MainWindow.setAccessibleName("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.GridLayout = QtWidgets.QGridLayout()
        self.GridLayout.setObjectName("GridLayout")
        self.ControlTabWidged = QtWidgets.QTabWidget(self.centralwidget)
        self.ControlTabWidged.setEnabled(True)
        self.ControlTabWidged.setMinimumSize(QtCore.QSize(900, 75))
        self.ControlTabWidged.setMaximumSize(QtCore.QSize(900, 75))
        self.ControlTabWidged.setObjectName("ControlTabWidged")
        self.MarketTab = QtWidgets.QWidget()
        self.MarketTab.setObjectName("MarketTab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.MarketTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Market_horizontalLayout = QtWidgets.QHBoxLayout()
        self.Market_horizontalLayout.setObjectName("Market_horizontalLayout")
        self.TickerLabel = QtWidgets.QLabel(self.MarketTab)
        self.TickerLabel.setObjectName("TickerLabel")
        self.Market_horizontalLayout.addWidget(
            self.TickerLabel, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.TickerInput = QtWidgets.QLineEdit(self.MarketTab)
        self.TickerInput.setEnabled(True)
        self.TickerInput.setToolTip("")
        self.TickerInput.setToolTipDuration(-1)
        self.TickerInput.setInputMask("")
        self.TickerInput.setText("")
        self.TickerInput.setMaxLength(10)
        self.TickerInput.setFrame(True)
        self.TickerInput.setReadOnly(False)
        self.TickerInput.setObjectName("TickerInput")
        self.Market_horizontalLayout.addWidget(self.TickerInput)
        self.RefreshLabel = QtWidgets.QLabel(self.MarketTab)
        self.RefreshLabel.setObjectName("RefreshLabel")
        self.Market_horizontalLayout.addWidget(
            self.RefreshLabel, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.RefreshSpin = QtWidgets.QSpinBox(self.MarketTab)
        self.RefreshSpin.setObjectName("RefreshSpin")
        self.Market_horizontalLayout.addWidget(
            self.RefreshSpin, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.LockUnlock = QtWidgets.QRadioButton(self.MarketTab)
        self.LockUnlock.setEnabled(True)
        self.LockUnlock.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.LockUnlock.setObjectName("LockUnlock")
        self.Market_horizontalLayout.addWidget(
            self.LockUnlock, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.horizontalLayout_2.addLayout(self.Market_horizontalLayout)
        self.ControlTabWidged.addTab(self.MarketTab, "")
        self.ContextTab = QtWidgets.QWidget()
        self.ContextTab.setEnabled(True)
        self.ContextTab.setObjectName("ContextTab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.ContextTab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Context_horizontalLayout = QtWidgets.QHBoxLayout()
        self.Context_horizontalLayout.setObjectName("Context_horizontalLayout")
        self.TimeframeLabelContext = QtWidgets.QLabel(self.ContextTab)
        self.TimeframeLabelContext.setMaximumSize(QtCore.QSize(81, 16777215))
        self.TimeframeLabelContext.setObjectName("TimeframeLabelContext")
        self.Context_horizontalLayout.addWidget(
            self.TimeframeLabelContext, 0, QtCore.Qt.AlignVCenter
        )
        self.TimeframeComboContext = QtWidgets.QComboBox(self.ContextTab)
        self.TimeframeComboContext.setObjectName("TimeframeComboContext")
        self.TimeframeComboContext.addItem("")
        self.TimeframeComboContext.addItem("")
        self.TimeframeComboContext.addItem("")
        self.Context_horizontalLayout.addWidget(
            self.TimeframeComboContext, 0, QtCore.Qt.AlignVCenter
        )
        self.PeriodLabelContext = QtWidgets.QLabel(self.ContextTab)
        self.PeriodLabelContext.setMaximumSize(QtCore.QSize(52, 16777215))
        self.PeriodLabelContext.setObjectName("PeriodLabelContext")
        self.Context_horizontalLayout.addWidget(
            self.PeriodLabelContext, 0, QtCore.Qt.AlignVCenter
        )
        self.PeriodSpinContext = QtWidgets.QSpinBox(self.ContextTab)
        self.PeriodSpinContext.setMinimum(1)
        self.PeriodSpinContext.setMaximum(999)
        self.PeriodSpinContext.setProperty("value", 59)
        self.PeriodSpinContext.setObjectName("PeriodSpinContext")
        self.Context_horizontalLayout.addWidget(
            self.PeriodSpinContext, 0, QtCore.Qt.AlignVCenter
        )
        self.MediumTimeframeLabel = QtWidgets.QLabel(self.ContextTab)
        self.MediumTimeframeLabel.setMaximumSize(QtCore.QSize(60, 16777215))
        self.MediumTimeframeLabel.setObjectName("MediumTimeframeLabel")
        self.Context_horizontalLayout.addWidget(
            self.MediumTimeframeLabel, 0, QtCore.Qt.AlignVCenter
        )
        self.MediumTimeframeCombo = QtWidgets.QComboBox(self.ContextTab)
        self.MediumTimeframeCombo.setEnabled(True)
        self.MediumTimeframeCombo.setMaxCount(10)
        self.MediumTimeframeCombo.setObjectName("MediumTimeframeCombo")
        self.MediumTimeframeCombo.addItem("")
        self.MediumTimeframeCombo.addItem("")
        self.MediumTimeframeCombo.addItem("")
        self.MediumTimeframeCombo.addItem("")
        self.MediumTimeframeCombo.addItem("")
        self.MediumTimeframeCombo.addItem("")
        self.MediumTimeframeCombo.addItem("")
        self.Context_horizontalLayout.addWidget(
            self.MediumTimeframeCombo, 0, QtCore.Qt.AlignVCenter
        )
        self.LongTimeframeLabel = QtWidgets.QLabel(self.ContextTab)
        self.LongTimeframeLabel.setMaximumSize(QtCore.QSize(42, 16777215))
        self.LongTimeframeLabel.setObjectName("LongTimeframeLabel")
        self.Context_horizontalLayout.addWidget(
            self.LongTimeframeLabel, 0, QtCore.Qt.AlignVCenter
        )
        self.LongTimeframeCombo = QtWidgets.QComboBox(self.ContextTab)
        self.LongTimeframeCombo.setMaxCount(10)
        self.LongTimeframeCombo.setObjectName("LongTimeframeCombo")
        self.LongTimeframeCombo.addItem("")
        self.LongTimeframeCombo.addItem("")
        self.LongTimeframeCombo.addItem("")
        self.LongTimeframeCombo.addItem("")
        self.LongTimeframeCombo.addItem("")
        self.LongTimeframeCombo.addItem("")
        self.LongTimeframeCombo.addItem("")
        self.LongTimeframeCombo.addItem("")
        self.Context_horizontalLayout.addWidget(
            self.LongTimeframeCombo, 0, QtCore.Qt.AlignVCenter
        )
        self.horizontalLayout_4.addLayout(self.Context_horizontalLayout)
        self.ControlTabWidged.addTab(self.ContextTab, "")
        self.LevelsTab = QtWidgets.QWidget()
        self.LevelsTab.setObjectName("LevelsTab")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.LevelsTab)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.Levels_horizontalLayout = QtWidgets.QHBoxLayout()
        self.Levels_horizontalLayout.setObjectName("Levels_horizontalLayout")
        self.PeriodLabelLevels = QtWidgets.QLabel(self.LevelsTab)
        self.PeriodLabelLevels.setMaximumSize(QtCore.QSize(50, 16777215))
        self.PeriodLabelLevels.setObjectName("PeriodLabelLevels")
        self.Levels_horizontalLayout.addWidget(self.PeriodLabelLevels)
        self.PeriodSpinLevels = QtWidgets.QSpinBox(self.LevelsTab)
        self.PeriodSpinLevels.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.PeriodSpinLevels.setSpecialValueText("")
        self.PeriodSpinLevels.setMinimum(0)
        self.PeriodSpinLevels.setMaximum(999)
        self.PeriodSpinLevels.setProperty("value", 5)
        self.PeriodSpinLevels.setObjectName("PeriodSpinLevels")
        self.Levels_horizontalLayout.addWidget(self.PeriodSpinLevels)
        self.TimeframeLabelLevels = QtWidgets.QLabel(self.LevelsTab)
        self.TimeframeLabelLevels.setMaximumSize(QtCore.QSize(88, 16777215))
        self.TimeframeLabelLevels.setObjectName("TimeframeLabelLevels")
        self.Levels_horizontalLayout.addWidget(self.TimeframeLabelLevels)
        self.TimeframeComboLevels = QtWidgets.QComboBox(self.LevelsTab)
        self.TimeframeComboLevels.setMaxCount(10)
        self.TimeframeComboLevels.setObjectName("TimeframeComboLevels")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.TimeframeComboLevels.addItem("")
        self.Levels_horizontalLayout.addWidget(self.TimeframeComboLevels)
        self.TypeLabel = QtWidgets.QLabel(self.LevelsTab)
        self.TypeLabel.setMaximumSize(QtCore.QSize(40, 16777215))
        self.TypeLabel.setObjectName("TypeLabel")
        self.Levels_horizontalLayout.addWidget(self.TypeLabel)
        self.TypeCombo = QtWidgets.QComboBox(self.LevelsTab)
        self.TypeCombo.setMinimumSize(QtCore.QSize(80, 0))
        self.TypeCombo.setMaxVisibleItems(2)
        self.TypeCombo.setMaxCount(4)
        self.TypeCombo.setObjectName("TypeCombo")
        self.TypeCombo.addItem("")
        self.TypeCombo.addItem("")
        self.Levels_horizontalLayout.addWidget(self.TypeCombo)
        self.ThicknessLabel = QtWidgets.QLabel(self.LevelsTab)
        self.ThicknessLabel.setMaximumSize(QtCore.QSize(78, 16777215))
        self.ThicknessLabel.setObjectName("ThicknessLabel")
        self.Levels_horizontalLayout.addWidget(self.ThicknessLabel)
        self.ThicknessSpin = QtWidgets.QDoubleSpinBox(self.LevelsTab)
        self.ThicknessSpin.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ThicknessSpin.setSpecialValueText("")
        self.ThicknessSpin.setPrefix("")
        self.ThicknessSpin.setDecimals(3)
        self.ThicknessSpin.setSingleStep(0.001)
        self.ThicknessSpin.setProperty("value", 0.007)
        self.ThicknessSpin.setObjectName("ThicknessSpin")
        self.Levels_horizontalLayout.addWidget(self.ThicknessSpin)
        self.SpacingLabel = QtWidgets.QLabel(self.LevelsTab)
        self.SpacingLabel.setMaximumSize(QtCore.QSize(65, 16777215))
        self.SpacingLabel.setObjectName("SpacingLabel")
        self.Levels_horizontalLayout.addWidget(self.SpacingLabel)
        self.SpacingSpin = QtWidgets.QDoubleSpinBox(self.LevelsTab)
        self.SpacingSpin.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.SpacingSpin.setSpecialValueText("")
        self.SpacingSpin.setPrefix("")
        self.SpacingSpin.setDecimals(1)
        self.SpacingSpin.setSingleStep(0.1)
        self.SpacingSpin.setProperty("value", 1.0)
        self.SpacingSpin.setObjectName("SpacingSpin")
        self.Levels_horizontalLayout.addWidget(self.SpacingSpin)
        self.horizontalLayout_6.addLayout(self.Levels_horizontalLayout)
        self.ControlTabWidged.addTab(self.LevelsTab, "")
        self.GridLayout.addWidget(self.ControlTabWidged, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.GridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStatusTip("")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.ControlTabWidged.setCurrentIndex(0)
        self.TimeframeComboContext.setCurrentIndex(2)
        self.MediumTimeframeCombo.setCurrentIndex(4)
        self.LongTimeframeCombo.setCurrentIndex(4)
        self.TimeframeComboLevels.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TickerLabel.setText(_translate("MainWindow", "Ticker"))
        self.TickerInput.setStatusTip(
            _translate(
                "MainWindow",
                "Market name. All modifications from Context & Levels will take effect only AFTER PRESSING ENTER on this field.",
            )
        )
        self.TickerInput.setPlaceholderText(
            _translate("MainWindow", "Write ticker and press enter ")
        )
        self.RefreshLabel.setText(_translate("MainWindow", "Refresh (seconds)"))
        self.RefreshSpin.setStatusTip(
            _translate(
                "MainWindow", "How often should graph be refreshed. 0 to disable"
            )
        )
        self.LockUnlock.setStatusTip(
            _translate(
                "MainWindow",
                "If enabled, locks and saves all Context and Levels settings for this ticker.",
            )
        )
        self.LockUnlock.setText(_translate("MainWindow", "Lock/Unlock"))
        self.ControlTabWidged.setTabText(
            self.ControlTabWidged.indexOf(self.MarketTab),
            _translate("MainWindow", "Market"),
        )
        self.TimeframeLabelContext.setText(_translate("MainWindow", "Timeframe"))
        self.TimeframeComboContext.setStatusTip(
            _translate("MainWindow", "Downloaded data timeframe from provider.")
        )
        self.TimeframeComboContext.setCurrentText(_translate("MainWindow", "60m"))
        self.TimeframeComboContext.setItemText(0, _translate("MainWindow", "5m"))
        self.TimeframeComboContext.setItemText(1, _translate("MainWindow", "15m"))
        self.TimeframeComboContext.setItemText(2, _translate("MainWindow", "60m"))
        self.PeriodLabelContext.setText(_translate("MainWindow", "Period"))
        self.PeriodSpinContext.setStatusTip(
            _translate(
                "MainWindow",
                "How many days to download from provider. Careful with provider.",
            )
        )
        self.MediumTimeframeLabel.setText(_translate("MainWindow", "Medium"))
        self.MediumTimeframeCombo.setStatusTip(
            _translate(
                "MainWindow",
                "Medium timeframe - should be 2-4x previous. Must be compatible with pandas resample function.",
            )
        )
        self.MediumTimeframeCombo.setCurrentText(_translate("MainWindow", "2h"))
        self.MediumTimeframeCombo.setItemText(0, _translate("MainWindow", "off"))
        self.MediumTimeframeCombo.setItemText(1, _translate("MainWindow", "15min"))
        self.MediumTimeframeCombo.setItemText(2, _translate("MainWindow", "30min"))
        self.MediumTimeframeCombo.setItemText(3, _translate("MainWindow", "1h"))
        self.MediumTimeframeCombo.setItemText(4, _translate("MainWindow", "2h"))
        self.MediumTimeframeCombo.setItemText(5, _translate("MainWindow", "3h"))
        self.MediumTimeframeCombo.setItemText(6, _translate("MainWindow", "4h"))
        self.LongTimeframeLabel.setText(_translate("MainWindow", "Long"))
        self.LongTimeframeCombo.setStatusTip(
            _translate(
                "MainWindow",
                "Long timeframe - should be 2-4x previous. Must be compatible with pandas resample function.",
            )
        )
        self.LongTimeframeCombo.setCurrentText(_translate("MainWindow", "3h"))
        self.LongTimeframeCombo.setItemText(0, _translate("MainWindow", "off"))
        self.LongTimeframeCombo.setItemText(1, _translate("MainWindow", "30min"))
        self.LongTimeframeCombo.setItemText(2, _translate("MainWindow", "1h"))
        self.LongTimeframeCombo.setItemText(3, _translate("MainWindow", "2h"))
        self.LongTimeframeCombo.setItemText(4, _translate("MainWindow", "3h"))
        self.LongTimeframeCombo.setItemText(5, _translate("MainWindow", "4h"))
        self.LongTimeframeCombo.setItemText(6, _translate("MainWindow", "8h"))
        self.LongTimeframeCombo.setItemText(7, _translate("MainWindow", "1d"))
        self.ControlTabWidged.setTabText(
            self.ControlTabWidged.indexOf(self.ContextTab),
            _translate("MainWindow", "Context"),
        )
        self.PeriodLabelLevels.setText(_translate("MainWindow", "Period"))
        self.PeriodSpinLevels.setStatusTip(
            _translate(
                "MainWindow",
                "Counting backwards, how many days to consider. 0 to disable",
            )
        )
        self.TimeframeLabelLevels.setText(_translate("MainWindow", "Timeframe"))
        self.TimeframeComboLevels.setStatusTip(
            _translate(
                "MainWindow",
                "On what timeframe should data be resampled before calculating levels. Must be compatible with pandas resample function.",
            )
        )
        self.TimeframeComboLevels.setCurrentText(_translate("MainWindow", "3h"))
        self.TimeframeComboLevels.setItemText(0, _translate("MainWindow", "5min"))
        self.TimeframeComboLevels.setItemText(1, _translate("MainWindow", "15min"))
        self.TimeframeComboLevels.setItemText(2, _translate("MainWindow", "30min"))
        self.TimeframeComboLevels.setItemText(3, _translate("MainWindow", "1h"))
        self.TimeframeComboLevels.setItemText(4, _translate("MainWindow", "2h"))
        self.TimeframeComboLevels.setItemText(5, _translate("MainWindow", "3h"))
        self.TimeframeComboLevels.setItemText(6, _translate("MainWindow", "4h"))
        self.TimeframeComboLevels.setItemText(7, _translate("MainWindow", "8h"))
        self.TimeframeComboLevels.setItemText(8, _translate("MainWindow", "1d"))
        self.TypeLabel.setText(_translate("MainWindow", "Type"))
        self.TypeCombo.setStatusTip(
            _translate(
                "MainWindow",
                "Raw type may overlap levels. Filtered removes overlaping levels based on spacing value.",
            )
        )
        self.TypeCombo.setCurrentText(_translate("MainWindow", "filtered"))
        self.TypeCombo.setItemText(0, _translate("MainWindow", "filtered"))
        self.TypeCombo.setItemText(1, _translate("MainWindow", "raw"))
        self.ThicknessLabel.setText(_translate("MainWindow", "Thickness"))
        self.ThicknessSpin.setStatusTip(
            _translate(
                "MainWindow",
                "Increase space between upper and lower portion of supply/demand area (as % of price magnitude)",
            )
        )
        self.SpacingLabel.setText(_translate("MainWindow", "Spacing"))
        self.SpacingSpin.setStatusTip(
            _translate(
                "MainWindow", "Increasing spacing will increase number of levels"
            )
        )
        self.ControlTabWidged.setTabText(
            self.ControlTabWidged.indexOf(self.LevelsTab),
            _translate("MainWindow", "Levels"),
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
