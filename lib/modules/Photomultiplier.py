
from lib.modules.Module import Module
from PyQt4 import QtGui, QtCore
from pyqtgraph.ImageView import ImageView
import InterfaceCombo
import pyqtgraph.parametertree as PT
import numpy as NP
import time

class Photomultiplier(Module):
    def __init__(self, manager, name, config):
        Module.__init__(self, manager, name, config) 
        self.win = QtGui.QMainWindow()
        self.win.show()
        self.win.setWindowTitle('Photomultiplier')
        self.w1 = QtGui.QSplitter()
        #self.l1 = QtGui.QHBoxLayout()
        #self.w1.setLayout(self.l1)
        self.w1.setOrientation(QtCore.Qt.Horizontal)
        self.w2 = QtGui.QWidget()
        self.l2 = QtGui.QVBoxLayout()
        self.w2.setLayout(self.l2)
        
        self.win.setCentralWidget(self.w1)
        self.w1.addWidget(self.w2)
        
        self.view = ImageView()
        self.w1.addWidget(self.view)
        self.tree = PT.ParameterTree()
        self.l2.addWidget(self.tree)
        self.run_button = QtGui.QPushButton('Run')
        self.l2.addWidget(self.run_button)
        self.win.resize(800, 450)
        self.param = PT.Parameter(name = 'param', children=[
            dict(name='Sample Rate', type='float', value=100000., suffix='Hz', dec = True, minStep=100., step=0.5, limits=[10000., 1000000.], siPrefix=True),
            dict(name='Image Width', type='int', value=256),
            dict(name='Image Height', type='int', value=256),
            dict(name='Xmin', type='float', value=-1.0, suffix='V', dec=True, minStep=1e-3, limits=[-5, 5], step=0.5, siPrefix=True),
            dict(name='Xmax', type='float', value=1.0, suffix='V', dec=True, minStep=1e-3, limits=[-5, 5], step=0.5, siPrefix=True),
            dict(name='Ymin', type='float', value=-1.0, suffix='V', dec=True, minStep=1e-3, limits=[-5, 5], step=0.5, siPrefix=True),
            dict(name='Ymax', type='float', value=1.0, suffix='V', dec=True, minStep=1e-3, limits=[-5, 5], step=0.5, siPrefix=True),
            dict(name='Pockels', type='float', value= 0.1, suffix='V', dec=True, minStep=1e-3, limits=[0, 1.5], step=0.1, siPrefix=True),
            dict(name='Frame Time', type='float', readonly=True, value=0.0),
            dict(name="Z-Stack", type="bool", value=False, children=[
                dict(name='Stage', type='interface', interfaceTypes='stage'),
                dict(name="Step Size", type="float", value=5e-6, suffix='m', dec=True, minStep=1e-7, step=0.5, limits=[1e-9,1], siPrefix=True),
                dict(name="Steps", type='int', value=10, step=1, limits=[1,None]),
                dict(name="Depth", type="float", value=0, readonly=True, suffix='m', siPrefix=True)
            ])
        ])
        
        self.tree.setParameters(self.param)
        self.param.sigTreeStateChanged.connect(self.update)
        self.update()
        self.run_button.clicked.connect(self.PMT_Run)
        self.Manager = manager
        
    def PMT_Run(self):
        if self.param['Z-Stack']:
            stage = self.manager.getDevice(self.param['Z-Stack', 'Stage'])
            images = []
            nSteps = self.param['Z-Stack', 'Steps']
            for i in range(nSteps):
                img = self.takeImage()[NP.newaxis, ...]
                images.append(img)
                if i < nSteps-1:
                    ## speed 20 is quite slow; timeouts may occur if we go much slower than that..
                    stage.moveBy([0.0, 0.0, self.param['Z-Stack', 'Step Size']], speed=20, block=True)  
            imgData = NP.concatenate(images, axis=0)
        else:
            imgData = self.takeImage()

        self.view.setImage(imgData)
        #info = self.param.getValues()
        #if not self.param['Z-Stack']:
            #info['Z-Stack'] = False
        info = {}
        dh = self.manager.getCurrentDir().writeFile(imgData, '2pImage.ma', info=info, autoIncrement=True)


    def takeImage(self):
        height = self.param['Image Height']
        width = self.param['Image Width']
        imagePts = height * width
        saw1 = NP.linspace(self.param['Xmin'], self.param['Xmax'], width)
        xScan = NP.tile(saw1, (1, height))[0,:]
        yvals = NP.linspace(self.param['Ymin'], self.param['Ymax'], height)
        yScan = NP.empty(imagePts)
        for y in range(height):
            yScan[y*width:(y+1)*width] = yvals[y]
        cmd= {'protocol': {'duration': imagePts/self.param['Sample Rate']},
              'DAQ' : {'rate': self.param['Sample Rate'], 'numPts': imagePts}, 
              'Scanner-Raw': {
                  'XAxis' : {'command': xScan},
                  'YAxis' : {'command': yScan}
                  },
              'Laser-2P': {'pCell' : {'preset': self.param['Pockels']}},
              'PMT' : {
                  'Input': {'record': True},
                #  'PlateVoltage': {'record' : False, 'recordInit': True}
                  }
            }
        # take some data
        task = self.Manager.createTask(cmd)
        task.execute(block = False)
        while not task.isDone():
            time.sleep(0.1)
        data = task.getResult()
        imgData = data['PMT']['Input'].view(NP.ndarray)
        imgData = imgData.reshape((width, height))
        return imgData
  
    def update(self):
        self.param['Frame Time'] = self.param['Image Width']*self.param['Image Height']/self.param['Sample Rate']
        self.param['Z-Stack', 'Depth'] = self.param['Z-Stack', 'Step Size'] * (self.param['Z-Stack', 'Steps']-1)
        
        