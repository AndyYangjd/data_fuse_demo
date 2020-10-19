import os

import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg

from ..ui.ui_birdview import Ui_birdview
from ..ui import resource_rc
from ..data.extract_xlsx import getData


class BirdView(Ui_birdview, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BirdView, self).__init__(parent)
        self.setupUi(self)
        self._initUI()
        self._initVars()

        self.onPause()

    @QtCore.pyqtSlot()
    def on_btnOpenFile_clicked(self):
        file_pth, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select xlsx", "", "xlsx(*.xlsx)")
        if file_pth is not None:
            file_name = os.path.basename(file_pth)
            self.lab_file_name.setText(file_name)
            self._getData(file_pth)
            self.have_file = True

    def _getData(self, file_pth_):
        self.data = getData(file_pth_)

    def _initUI(self):
        self._setPen()
        # create vb to show data
        self._createVB()
        self.vbox_bd.addWidget(self.bd)

        # define btns
        iconsize = QtCore.QSize(30, 30)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/cycle.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.cycle_btn = QtWidgets.QToolButton()
        self.cycle_btn.setIcon(icon)
        self.cycle_btn.setIconSize(iconsize)
        self.cycle_btn.setAutoRaise(True)
        self.cycle_btn.setToolTip('Play cycle')
        self.cycle_btn.clicked.connect(self.onCycle)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/play.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.play_btn = QtWidgets.QToolButton()
        self.play_btn.setIcon(icon)
        self.play_btn.setIconSize(iconsize)
        self.play_btn.setAutoRaise(True)
        self.play_btn.setToolTip('Play')
        self.play_btn.clicked.connect(self.onPlay)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/pause.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.pause_btn = QtWidgets.QToolButton()
        self.pause_btn.setIcon(icon)
        self.pause_btn.setIconSize(iconsize)
        self.pause_btn.setAutoRaise(True)
        self.pause_btn.setToolTip('Pause')
        self.pause_btn.setVisible(False)
        self.pause_btn.clicked.connect(self.onPause)

        # define slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._updateFromSliderValueChange)

        # define spin to show current frame
        self.sBox_current_frame_num = QtWidgets.QSpinBox()
        self.sBox_current_frame_num.setMinimum(0)
        self.sBox_current_frame_num.setSingleStep(1)
        self.sBox_current_frame_num.valueChanged.connect(
            self._updateSliderFromSBox)

        # define the media-grid-layout which defined in map.ui
        self.media_grid.addWidget(self.cycle_btn, 0, 0)
        self.media_grid.addWidget(self.play_btn, 0, 1)
        self.media_grid.addWidget(self.pause_btn, 0, 1)
        # self.media_grid.addWidget(self.single_btn, 0, 2)
        self.media_grid.addWidget(self.slider, 0, 2)
        self.media_grid.addWidget(self.sBox_current_frame_num, 0, 3)

        # set col stretch
        for i in range(4):
            self.media_grid.setColumnMinimumWidth(i, 0)
            self.media_grid.setColumnStretch(i, 1)

        self.media_grid.setColumnStretch(2, 100)
        self.media_grid.setColumnStretch(3, 1)

    def _initVars(self):
        self.i_current_frame_num = 0

        self.slider.setMaximum(38)
        self.slider.setValue(0)

        self.sBox_current_frame_num.setMaximum(38)
        self.all_items_need_to_remove = []
        self.have_file = False

    def _setPen(self):
        """ define some pen
        """
        self.background_Pen = QtGui.QPen(QtCore.Qt.white, 0.05,
                                         QtCore.Qt.SolidLine,
                                         QtCore.Qt.SquareCap,
                                         QtCore.Qt.MiterJoin)
        self.infLine_Pen = QtGui.QPen(QtCore.Qt.white, 0.1,
                                      QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                      QtCore.Qt.MiterJoin)
        self.pos_color = (255, 0, 0)
        self.pos_Pen = QtGui.QPen(QtCore.Qt.red, 0.1, QtCore.Qt.SolidLine,
                                  QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
        self.vel_color = (255, 255, 0)
        self.vel_Pen = QtGui.QPen(QtCore.Qt.yellow, 0.1, QtCore.Qt.SolidLine,
                                  QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)

    def _createVB(self):
        """
        create a vb to show xy-view
        :return:
        """
        self.bd = pg.GraphicsLayoutWidget()

        # set left-axis
        left_axis = pg.AxisItem(orientation='left', pen=(255, 255, 255))
        left_axis.setLabel(text='X', units='m')
        left_axis.setTickSpacing(5,1)
        left_axis.enableAutoSIPrefix(False)
        self.bd.ci.addItem(left_axis, 0, 0)

        # set vb
        self.vb = pg.ViewBox(name='Birdview')
        self.bd.ci.addItem(self.vb, 0, 1)

        # set bottom-axis
        bottom_axis = pg.AxisItem(orientation='bottom', pen=(255, 255, 255))
        bottom_axis.setLabel(text='Y', units='m')
        bottom_axis.setTickSpacing(5, 1)
        bottom_axis.enableAutoSIPrefix(False)
        self.bd.ci.addItem(bottom_axis, 1, 1)

        # set stretch
        layout = self.bd.ci.layout
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        for i in range(2):
            layout.setRowPreferredHeight(i, 0)
            layout.setRowMinimumHeight(i, 0)
            layout.setRowSpacing(i, 10)
            layout.setRowStretchFactor(i, 1000)
        layout.setRowStretchFactor(1, 1)

        for i in range(2):
            layout.setColumnPreferredWidth(i, 0)
            layout.setColumnMinimumWidth(i, 0)
            layout.setColumnSpacing(i, 0)
            layout.setColumnStretchFactor(i, 1)
        layout.setColumnStretchFactor(1, 1000)

        # linx axis
        left_axis.linkToView(self.vb)
        bottom_axis.linkToView(self.vb)

        # invert left-axis
        self.vb.invertX()

        # set the default range
        self.vb.setXRange(-200, 200)
        self.vb.setYRange(0, 200)

        # add grid
        grid = pg.GridItem()
        self.vb.addItem(grid)

        # add inf-line
        h_line = pg.InfiniteLine(pos=(0, 0), angle=0, pen=self.background_Pen)
        v_line = pg.InfiniteLine(pos=(0, 0), angle=90, pen=self.background_Pen)
        self.vb.addItem(h_line)
        self.vb.addItem(v_line)

    def onPlay(self):
        # True means in play-status
        self.b_play = True
        self.b_pause = False

        self._updateBtns()
        self._play()

    def onPause(self):
        # True means current is pause-status
        self.b_pause = True
        self.b_play = False
        self.b_cycle = False

        self._updateBtns()
        self._updateSlider()
        self._updateVB()

    def onCycle(self):
        self.b_cycle = True
        self.onPlay()

    def _updateFromSliderValueChange(self, i_current_slider_num):
        # update current-frame-num
        self.i_current_frame_num = i_current_slider_num
        # update spin-box
        self.sBox_current_frame_num.setValue(i_current_slider_num)
        # update vb
        self._updateVB()

    def _updateSliderFromSBox(self, i_current_sbox_num):
        self.slider.setValue(i_current_sbox_num)

    def _updateBtns(self):
        """ update the btn-state
        """
        if self.b_pause:  # pause-status
            # set play-btn
            self.play_btn.setVisible(True)
            self.play_btn.setEnabled(True)
            self.play_btn.setCheckable(True)
            # set pause-btn
            self.pause_btn.setVisible(False)
            self.pause_btn.setEnabled(False)
            self.pause_btn.setCheckable(False)
            # set cycle-btn
            self.cycle_btn.setEnabled(True)
            self.cycle_btn.setCheckable(True)
            # set slider
            self.slider.setEnabled(True)
            # set sbox
            self.sBox_current_frame_num.setEnabled(True)
        else:  # play-status
            # set play-btn
            self.play_btn.setVisible(False)
            self.play_btn.setEnabled(False)
            self.play_btn.setCheckable(False)
            # set pause-btn
            self.pause_btn.setVisible(True)
            self.pause_btn.setEnabled(True)
            self.pause_btn.setCheckable(True)
            # set cycle-btn
            self.cycle_btn.setEnabled(False)
            self.cycle_btn.setCheckable(False)
            # set slider
            self.slider.setEnabled(False)
            # set sbox
            self.sBox_current_frame_num.setEnabled(False)

    def _updateSlider(self):
        has_frame = self.i_current_frame_num >= 0
        if has_frame:
            self.slider.setValue(self.i_current_frame_num)
        else:
            self.slider.setMaximum(0)

    def _updateVB(self):
        """
        When the current-value changed, update the vb.
        """
        if self.i_current_frame_num == 38 or self.have_file == False:
            pass
        else:
            # clear the previous data-item
            for item in self.all_items_need_to_remove:
                self.vb.removeItem(item)
            # for item in self.vb.addedItems:
            #     if isinstance(item, pg.PlotDataItem):
            #         self.vb.removeItem(item)
            #     elif isinstance(item, pg.PlotCurveItem):
            #         self.vb.removeItem(item)
            #     elif isinstance(item, pg.CurvePoint):
            #         self.vb.removeItem(item)

            self.all_items_need_to_remove = []

            current_x_list = self.data[self.i_current_frame_num]["x"]
            current_y_list = self.data[self.i_current_frame_num]["y"]
            current_vx_list = self.data[self.i_current_frame_num]["vx_comp"]
            current_vy_list = self.data[self.i_current_frame_num]["vy_comp"]

            current_x_list = np.array(current_x_list)
            current_y_list = np.array(current_y_list)
            current_vx_list = np.array(current_vx_list)
            current_vy_list = np.array(current_vy_list)

            # draw pos
            pos_pen = self.pos_Pen
            color = self.pos_color

            rotated_x_list = np.zeros_like(current_x_list)
            rotated_y_list = np.zeros_like(current_y_list)
            for row in range(len(current_x_list)):
                rotated_x_list[row], rotated_y_list[
                    row] = self._transformCoord(
                        (current_x_list[row], current_y_list[row]))

            pos_curve = pg.ScatterPlotItem(x=rotated_x_list,
                                           y=rotated_y_list,
                                           pen=pos_pen,
                                           symbolBrush=color,
                                           symbolPen='w',
                                           symbol='o',
                                           symbolSize=10)

            # set ZValue will show in the front of scene
            pos_curve.setZValue(100)
            self.vb.addItem(pos_curve, ignoreBounds=False)
            self.all_items_need_to_remove.append(pos_curve)

            # draw vel
            pos_pen = self.vel_Pen
            color = self.vel_color

            plt_x_list = current_x_list + current_vx_list
            plt_y_list = current_y_list + current_vy_list

            for row in range(len(plt_x_list)):
                rotated_plt_x, rotated_plt_y = self._transformCoord(
                    (plt_x_list[row], plt_y_list[row]))
                vel_line = pg.PlotCurveItem(
                    x=[rotated_x_list[row], rotated_plt_x],
                    y=[rotated_y_list[row], rotated_plt_y],
                    pen=self.vel_Pen,
                    antialias=True)
                self.vb.addItem(vel_line, ignoreBounds=False)
                self.all_items_need_to_remove.append(vel_line)

    def _play(self):
        if self.b_play:
            if self.i_current_frame_num == 38:  # arrive to end
                if self.b_cycle:  # in cycle-status
                    self.i_current_frame_num = 0
                    self._play()
                else:  # in end-status
                    self.onPause()
            else:  # play-status
                self._updateVB()
                self._updateSlider()

                self.timer = QtCore.QTimer()
                # self.timer.setInterval(self.ts_period)
                self.timer.setSingleShot(True)
                self.timer.start(300)
                self.timer.timeout.connect(self._updateFrameNum)

    def _updateFrameNum(self):
        self.i_current_frame_num += 1
        self._play()

    def _transformCoord(self, true_pos):
        true_x, true_y = true_pos
        return (true_y, true_x)