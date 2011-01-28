# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from lib.analysis.AnalysisModule import AnalysisModule
import lib.analysis.modules.EventDetector as EventDetector
#from flowchart import *
import os
from advancedTypes import OrderedDict
import debug
#import FileLoader

class Photostim(AnalysisModule):
    def __init__(self, host):
        self.dbIdentity = "Photostim"  ## how we identify to the database; this determines which tables we own

        self.ctrl = QtGui.QLabel("CTRL")
        self.scanItems = {}
        
        ## create event detector
        fcDir = os.path.join(os.path.abspath(os.path.split(__file__)[0]), "flowcharts")
        self.detector = EventDetector.EventDetector(host, flowchartDir=fcDir)
        
        ## override some of its elements
        self.detector.setElement('File Loader', self)
        self.detector.setElement('Database', self)
        
        ## Create element list, importing some gui elements from event detector
        elems = self.detector.listElements()
        self._elements_ = OrderedDict([
            ('Database', {'type': 'database', 'tables': {self.dbIdentity: 'Photostim_events'}, 'host': self}),
            ('Canvas', {'type': 'canvas', 'pos': ('right',), 'size': (400,400)}),
            ('Detection Opts', elems['Detection Opts'].setParams(pos=('bottom', 'Database'), size= (200,500))),
            ('File Loader', {'type': 'fileInput', 'size': (200, 300), 'pos': ('above', 'Database'), 'host': self}),
            ('Data Plot', elems['Data Plot'].setParams(pos=('bottom', 'Canvas'), size=(800,200))),
            ('Filter Plot', elems['Filter Plot'].setParams(pos=('bottom', 'Data Plot'), size=(800,200))),
            ('Output Table', elems['Output Table'].setParams(pos=('below', 'Filter Plot'), size=(800,200))),
            ('Stats', {'type': 'dataTree', 'size': (800,200), 'pos': ('below', 'Output Table')}),
            ('Map Opts', {'type': 'ctrl', 'object': self.ctrl, 'pos': ('left', 'Canvas'), 'size': (200,400)}),
        ])

        AnalysisModule.__init__(self, host)
        self.detector.flowchart.sigOutputChanged.connect(self.detectorOutputChanged)

        #self.loader = self.getElement('File Loader')
        #self.table = self.getElement('Output Table')
        #self.dbui = self.getElement('Database')
        #self.flowchart.sigOutputChanged.connect(self.outputChanged)
        #self.dbui.sigStoreToDB.connect(self.storeClicked)

    #def elementChanged(self, element, old, new):
        #name = element.name()
        #if name == 'File Loader':
            #pass
            ##if old is not None:
                ##old.sigFileLoaded.disconnect(self.fileLoaded)
            ##obj.sigFileLoaded.connect(self.fileLoaded)
        #elif name == 'Database':
            #pass
            ##if old is not None:
                ##old.sigStoreToDB.connect(self.storeClicked)
            ##obj.sigStoreToDB.connect(self.storeClicked)
        

        
    def loadFileRequested(self, fh):
        canvas = self.getElement('Canvas')
        try:
            if fh.isFile():
                canvas.addFile(fh)
            else:
                scan = canvas.addFile(fh)
                self.scanItems[fh] = scan
                scan.item.sigPointClicked.connect(self.scanPointClicked)
            return True
        except:
            debug.printExc("Error loading file %s" % fh.name())
            return False
    
    def storeToDB(self):
        pass


    def scanPointClicked(self, point):
        #print "click!", point.data
        self.detector.loadFileRequested(point.data)
        
    def detectorOutputChanged(self):
        table = self.getElement('Stats')
        stats = self.detector.flowchart.output()['stats']
        print stats
        table.setData(stats)
        