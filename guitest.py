#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 15:48:20 2016

@author: Oscar Tegmyr
oscar.tegmyr@gmail.com
"""
import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import read_chn

def load_spec(fname):    
    spec_obj    = read_chn.gamma_data(fname)
    spec_array  = spec_obj.hist_array
    #Make some nice way to access the other properties from spec_obj, like a dictionary
    return spec_array

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=20, height=4, dpi=100):
        fig         = Figure(figsize=(width, height), dpi=dpi)
        self.axes   = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    def compute_initial_figure(self):    
        self.axes.plot()


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #=== Menubar === 
        self.menuBar        = QtGui.QMenuBar()
        self.file_menu      = QtGui.QMenu('&File', self)
        self.settings_menu  = QtGui.QMenu('&Settings', self)
        self.analysis_menu  = QtGui.QMenu('&Analysis', self)
        self.help_menu      = QtGui.QMenu('&Help', self)
        self.menuBar.addMenu(self.file_menu)
        self.menuBar.addMenu(self.settings_menu)
        self.menuBar.addMenu(self.analysis_menu)
        self.menuBar.addMenu(self.help_menu)
        self.file_menu.addAction('&Load spectrum', self.file_load_spec)
        self.file_menu.addAction('&Export spectrum', self.file_load_spec)
        self.help_menu.addAction('&Documentation', self.documentation)

        self.main_widget    = QtGui.QWidget(self)
        l                   = QtGui.QHBoxLayout(self.main_widget)
        self.sc             = MyStaticMplCanvas(self.main_widget, width=100, height=6, dpi=100)
        self.slider         = QtGui.QSlider(self.main_widget)
        
        
        
        l.addWidget(self.sc)
        l.addWidget(self.slider)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
           
    def file_load_spec(self):
        self.file_name      = QtGui.QFileDialog.getOpenFileName(self,"Load Spectrum File", "/home","Spectrum Files (*.chn *.bin)");    
        array               = load_spec(self.file_name)
        self.sc.axes.plot(array)
        self.sc.draw()
        
    def documentation(self):
       pass


qApp    = QtGui.QApplication(sys.argv)
aw      = ApplicationWindow()
aw.setWindowTitle('Ortec GUI')
aw.show()
sys.exit(qApp.exec_())