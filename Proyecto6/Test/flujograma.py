#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import E3TRadio
import math
import sip



class flujograma(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "flujograma")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.tabla_de_verdad_constelacion = tabla_de_verdad_constelacion = (0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j)
        self.M = M = len(tabla_de_verdad_constelacion)
        self.bps = bps = int(math.log(M, 2))
        self.Sps = Sps = 8
        self.RS = RS = 32000*4
        self.volumen = volumen = 0.2
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j], [0, 1, 2, 3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.usrp_rate = usrp_rate = 1e6
        self.samp_rate = samp_rate = RS*Sps
        self.noise = noise = 0
        self.h = h = [1]*Sps
        self.fc = fc = 50e6
        self.fase = fase = 60
        self.escala = escala = 128
        self.audio_rate = audio_rate = 48000
        self.RB = RB = RS*bps
        self.GTX = GTX = 0
        self.GRX_lineal = GRX_lineal = 10
        self.GRX = GRX = 0

        ##################################################
        # Blocks
        ##################################################

        self._volumen_range = Range(0, 1, 0.01, 0.2, 200)
        self._volumen_win = RangeWidget(self._volumen_range, self.set_volumen, "'volumen'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volumen_win)
        self._fc_range = Range(50e6, 100e7, 5e6, 50e6, 200)
        self._fc_win = RangeWidget(self._fc_range, self.set_fc, "Freq portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fc_win)
        self._fase_range = Range(-180, 180, 1, 60, 200)
        self._fase_win = RangeWidget(self._fase_range, self.set_fase, "fase", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fase_win)
        self._escala_range = Range(1, 256, 1, 128, 200)
        self._escala_win = RangeWidget(self._escala_range, self.set_escala, "escala", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._escala_win)
        self._GTX_range = Range(0, 30, 1, 0, 200)
        self._GTX_win = RangeWidget(self._GTX_range, self.set_GTX, "Ganancia transmisor", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._GTX_win)
        self._GRX_lineal_range = Range(0, 20, 0.1, 10, 200)
        self._GRX_lineal_win = RangeWidget(self._GRX_lineal_range, self.set_GRX_lineal, "Ganancia RX lineal", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._GRX_lineal_win)
        self._GRX_range = Range(0, 30, 1, 0, 200)
        self._GRX_win = RangeWidget(self._GRX_range, self.set_GRX, "Ganancia RX", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._GRX_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(usrp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(GRX, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(usrp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(fc, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(GTX, 0)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Señal Recibida", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Reducida', 'Escalada', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Señal Inicial", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 0, 0, 2, 1)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_range = Range(0, 1, 0.0125, 0, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, "Ruido", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(Sps, h)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(variable_constellation_0)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(tabla_de_verdad_constelacion, 1)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/labcom/Documentos/2023_2_comu2_G1/Proyecto5/labachata_manuelturizo.wav', True)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(2, gr.GR_MSB_FIRST)
        self.blocks_phase_shift_0 = blocks.phase_shift(fase, False)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bps, gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_3 = blocks.multiply_const_cc(GRX_lineal)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(volumen)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff((1/escala))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1/Sps)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, escala)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.audio_sink_0_0 = audio.sink(44100, '', True)
        self.Menu = Qt.QTabWidget()
        self.Menu_widget_0 = Qt.QWidget()
        self.Menu_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Menu_widget_0)
        self.Menu_grid_layout_0 = Qt.QGridLayout()
        self.Menu_layout_0.addLayout(self.Menu_grid_layout_0)
        self.Menu.addTab(self.Menu_widget_0, 'Time & Freq')
        self.Menu_widget_1 = Qt.QWidget()
        self.Menu_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Menu_widget_1)
        self.Menu_grid_layout_1 = Qt.QGridLayout()
        self.Menu_layout_1.addLayout(self.Menu_grid_layout_1)
        self.Menu.addTab(self.Menu_widget_1, 'Freq')
        self.top_layout.addWidget(self.Menu)
        self.E3TRadio_diezmador_cc_0 = E3TRadio.diezmador_cc(8)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.E3TRadio_diezmador_cc_0, 0), (self.blocks_multiply_const_vxx_3, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.E3TRadio_diezmador_cc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_time_sink_x_2, 1))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.blocks_multiply_const_vxx_3, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_3, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_phase_shift_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "flujograma")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tabla_de_verdad_constelacion(self):
        return self.tabla_de_verdad_constelacion

    def set_tabla_de_verdad_constelacion(self, tabla_de_verdad_constelacion):
        self.tabla_de_verdad_constelacion = tabla_de_verdad_constelacion
        self.set_M(len(self.tabla_de_verdad_constelacion))
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.tabla_de_verdad_constelacion)

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M
        self.set_bps(int(math.log(self.M, 2)))

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps
        self.set_RB(self.RS*self.bps)

    def get_Sps(self):
        return self.Sps

    def set_Sps(self, Sps):
        self.Sps = Sps
        self.set_h([1]*self.Sps)
        self.set_samp_rate(self.RS*self.Sps)
        self.blocks_multiply_const_vxx_0.set_k(1/self.Sps)

    def get_RS(self):
        return self.RS

    def set_RS(self, RS):
        self.RS = RS
        self.set_RB(self.RS*self.bps)
        self.set_samp_rate(self.RS*self.Sps)

    def get_volumen(self):
        return self.volumen

    def set_volumen(self, volumen):
        self.volumen = volumen
        self.blocks_multiply_const_vxx_2.set_k(self.volumen)

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0
        self.digital_constellation_decoder_cb_0.set_constellation(self.variable_constellation_0)

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.usrp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.usrp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise

    def get_h(self):
        return self.h

    def set_h(self, h):
        self.h = h
        self.interp_fir_filter_xxx_0.set_taps(self.h)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.uhd_usrp_sink_0.set_center_freq(self.fc, 0)
        self.uhd_usrp_source_0.set_center_freq(self.fc, 0)

    def get_fase(self):
        return self.fase

    def set_fase(self, fase):
        self.fase = fase
        self.blocks_phase_shift_0.set_shift(self.fase)

    def get_escala(self):
        return self.escala

    def set_escala(self, escala):
        self.escala = escala
        self.blocks_float_to_char_0.set_scale(self.escala)
        self.blocks_multiply_const_vxx_1.set_k((1/self.escala))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate

    def get_RB(self):
        return self.RB

    def set_RB(self, RB):
        self.RB = RB

    def get_GTX(self):
        return self.GTX

    def set_GTX(self, GTX):
        self.GTX = GTX
        self.uhd_usrp_sink_0.set_gain(self.GTX, 0)

    def get_GRX_lineal(self):
        return self.GRX_lineal

    def set_GRX_lineal(self, GRX_lineal):
        self.GRX_lineal = GRX_lineal
        self.blocks_multiply_const_vxx_3.set_k(self.GRX_lineal)

    def get_GRX(self):
        return self.GRX

    def set_GRX(self, GRX):
        self.GRX = GRX
        self.uhd_usrp_source_0.set_gain(self.GRX, 0)




def main(top_block_cls=flujograma, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
