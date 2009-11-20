# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageViewTemplate.ui'
#
# Created: Fri Nov 20 08:22:10 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(757, 495)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = GraphicsView(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 3, 1)
        self.blackSlider = QtGui.QSlider(self.layoutWidget)
        self.blackSlider.setMaximum(4096)
        self.blackSlider.setOrientation(QtCore.Qt.Vertical)
        self.blackSlider.setInvertedAppearance(False)
        self.blackSlider.setInvertedControls(False)
        self.blackSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.blackSlider.setTickInterval(410)
        self.blackSlider.setObjectName("blackSlider")
        self.gridLayout.addWidget(self.blackSlider, 0, 1, 1, 1)
        self.whiteSlider = QtGui.QSlider(self.layoutWidget)
        self.whiteSlider.setMaximum(4096)
        self.whiteSlider.setProperty("value", 4096)
        self.whiteSlider.setOrientation(QtCore.Qt.Vertical)
        self.whiteSlider.setObjectName("whiteSlider")
        self.gridLayout.addWidget(self.whiteSlider, 0, 2, 1, 2)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.roiBtn = QtGui.QPushButton(self.layoutWidget)
        self.roiBtn.setMaximumSize(QtCore.QSize(40, 16777215))
        self.roiBtn.setCheckable(True)
        self.roiBtn.setObjectName("roiBtn")
        self.gridLayout.addWidget(self.roiBtn, 2, 1, 1, 3)
        self.timeSlider = QtGui.QSlider(self.layoutWidget)
        self.timeSlider.setMaximum(65535)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.gridLayout.addWidget(self.timeSlider, 4, 0, 1, 1)
        self.normBtn = QtGui.QPushButton(self.layoutWidget)
        self.normBtn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.normBtn.setCheckable(True)
        self.normBtn.setObjectName("normBtn")
        self.gridLayout.addWidget(self.normBtn, 4, 1, 1, 2)
        self.normGroup = QtGui.QGroupBox(self.layoutWidget)
        self.normGroup.setObjectName("normGroup")
        self.gridLayout_2 = QtGui.QGridLayout(self.normGroup)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.normSubtractRadio = QtGui.QRadioButton(self.normGroup)
        self.normSubtractRadio.setObjectName("normSubtractRadio")
        self.gridLayout_2.addWidget(self.normSubtractRadio, 0, 2, 1, 1)
        self.normDivideRadio = QtGui.QRadioButton(self.normGroup)
        self.normDivideRadio.setChecked(False)
        self.normDivideRadio.setObjectName("normDivideRadio")
        self.gridLayout_2.addWidget(self.normDivideRadio, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)
        self.normROICheck = QtGui.QCheckBox(self.normGroup)
        self.normROICheck.setObjectName("normROICheck")
        self.gridLayout_2.addWidget(self.normROICheck, 1, 1, 1, 1)
        self.normStartSlider = QtGui.QSlider(self.normGroup)
        self.normStartSlider.setMaximum(65535)
        self.normStartSlider.setOrientation(QtCore.Qt.Horizontal)
        self.normStartSlider.setObjectName("normStartSlider")
        self.gridLayout_2.addWidget(self.normStartSlider, 2, 0, 1, 6)
        self.normStopSlider = QtGui.QSlider(self.normGroup)
        self.normStopSlider.setMaximum(65535)
        self.normStopSlider.setOrientation(QtCore.Qt.Horizontal)
        self.normStopSlider.setObjectName("normStopSlider")
        self.gridLayout_2.addWidget(self.normStopSlider, 3, 0, 1, 6)
        self.normXBlurSpin = QtGui.QDoubleSpinBox(self.normGroup)
        self.normXBlurSpin.setObjectName("normXBlurSpin")
        self.gridLayout_2.addWidget(self.normXBlurSpin, 4, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.normGroup)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 4, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.normGroup)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 4, 3, 1, 1)
        self.normYBlurSpin = QtGui.QDoubleSpinBox(self.normGroup)
        self.normYBlurSpin.setObjectName("normYBlurSpin")
        self.gridLayout_2.addWidget(self.normYBlurSpin, 4, 4, 1, 1)
        self.label_10 = QtGui.QLabel(self.normGroup)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 4, 5, 1, 1)
        self.normTBlurSpin = QtGui.QDoubleSpinBox(self.normGroup)
        self.normTBlurSpin.setObjectName("normTBlurSpin")
        self.gridLayout_2.addWidget(self.normTBlurSpin, 4, 6, 1, 1)
        self.normStopLabel = QtGui.QLabel(self.normGroup)
        self.normStopLabel.setObjectName("normStopLabel")
        self.gridLayout_2.addWidget(self.normStopLabel, 3, 6, 1, 1)
        self.normStartLabel = QtGui.QLabel(self.normGroup)
        self.normStartLabel.setObjectName("normStartLabel")
        self.gridLayout_2.addWidget(self.normStartLabel, 2, 6, 1, 1)
        self.normOffRadio = QtGui.QRadioButton(self.normGroup)
        self.normOffRadio.setChecked(True)
        self.normOffRadio.setObjectName("normOffRadio")
        self.gridLayout_2.addWidget(self.normOffRadio, 0, 3, 1, 1)
        self.normTimeRangeCheck = QtGui.QCheckBox(self.normGroup)
        self.normTimeRangeCheck.setObjectName("normTimeRangeCheck")
        self.gridLayout_2.addWidget(self.normTimeRangeCheck, 1, 3, 1, 1)
        self.normFrameCheck = QtGui.QCheckBox(self.normGroup)
        self.normFrameCheck.setObjectName("normFrameCheck")
        self.gridLayout_2.addWidget(self.normFrameCheck, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.normGroup, 5, 0, 1, 4)
        self.roiPlot = PlotWidget(self.splitter)
        self.roiPlot.setMinimumSize(QtCore.QSize(0, 40))
        self.roiPlot.setObjectName("roiPlot")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "B", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "W", None, QtGui.QApplication.UnicodeUTF8))
        self.roiBtn.setText(QtGui.QApplication.translate("Form", "ROI", None, QtGui.QApplication.UnicodeUTF8))
        self.normBtn.setText(QtGui.QApplication.translate("Form", "Norm", None, QtGui.QApplication.UnicodeUTF8))
        self.normGroup.setTitle(QtGui.QApplication.translate("Form", "Normalization", None, QtGui.QApplication.UnicodeUTF8))
        self.normSubtractRadio.setText(QtGui.QApplication.translate("Form", "Subtract", None, QtGui.QApplication.UnicodeUTF8))
        self.normDivideRadio.setText(QtGui.QApplication.translate("Form", "Divide", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Operation:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Mean:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Blur:", None, QtGui.QApplication.UnicodeUTF8))
        self.normROICheck.setText(QtGui.QApplication.translate("Form", "ROI", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Form", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Form", "T", None, QtGui.QApplication.UnicodeUTF8))
        self.normStopLabel.setText(QtGui.QApplication.translate("Form", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.normStartLabel.setText(QtGui.QApplication.translate("Form", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.normOffRadio.setText(QtGui.QApplication.translate("Form", "Off", None, QtGui.QApplication.UnicodeUTF8))
        self.normTimeRangeCheck.setText(QtGui.QApplication.translate("Form", "Time range", None, QtGui.QApplication.UnicodeUTF8))
        self.normFrameCheck.setText(QtGui.QApplication.translate("Form", "Frame", None, QtGui.QApplication.UnicodeUTF8))

from GraphicsView import GraphicsView
from PlotWidget import PlotWidget
