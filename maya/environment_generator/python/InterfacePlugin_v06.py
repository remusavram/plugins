""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        InterfacePlugin_v06.py
#    @brief       This script is the main script for the environment PluginCreareMediu. 
                  PluginCreareMediu creates:
                    - ground
                    - meadow:
                        - flowers
                        - grass
                        - stones
                    - forest
#    @author      remus_avram
#    @date        12.2013
"""



from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4 import Qt
import os
import sip
import Plugin_v06 as Plugin



# keep the path to the uiFile in a variable
uiFile = os.path.join(os.path.dirname(__file__), '../../ui/PluginCreareMediuUI_v09.ui')


# keep the path of images in variables
labelWhiteFlowerPath = os.path.join(os.path.dirname(__file__), '../../images/WhiteFlower.jpg')
labelOrangeFlowerPath = os.path.join(os.path.dirname(__file__), '../../images/OrangeFlower.jpg')
labelRedFlowerPath = os.path.join(os.path.dirname(__file__), '../../images/RedFlower.jpg')
labelGrassPath = os.path.join(os.path.dirname(__file__), '../../images/Grass.jpg')
labelSmallStonePath = os.path.join(os.path.dirname(__file__), '../../images/SmallStone.jpg')
labelBigStonePath = os.path.join(os.path.dirname(__file__), '../../images/BigStone.jpg')
labelGreenTreePath = os.path.join(os.path.dirname(__file__), '../../images/greenTree.jpg')
labelYellowTreePath = os.path.join(os.path.dirname(__file__), '../../images/yellowTree.jpg')


# keep the changeable names in variables
windowObject = 'PluginWindow'



class InterfacePluginCass(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        super(InterfacePluginCass, self).__init__(parent)
        
        # create object
        self.PluginObject = Plugin.PluginClass()
        
        uic.loadUi(uiFile, self)
        
        # set window name
        self.setObjectName(windowObject)
        
        self.mainWidget = QtGui.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainGrid)
        
        # check if the ground exist when the window is reopening
        if self.PluginObject.checkExistGround() == 1:
            self.meadowGroupBox.setEnabled(True)
            self.forestGroupBox.setEnabled(True)
        
        # check if the forest exist when the window is reopening
        if self.PluginObject.checkExistingForest():
            self.groundGrupBox.setEnabled(False)
            self.meadowGroupBox.setEnabled(False)
            self.generateForestPushButton.setEnabled(False)
        
        # check if meadows exist when the window is reopening and import them in MeadowList
        for i in self.PluginObject.checkExistingMeadow():
            self.listMeadowWidget.addItem('Poiana_' + str(i))
        if self.PluginObject.checkExistingMeadow():
            self.groundGrupBox.setEnabled(False)
            
        # signals/slots for ground
        self.creatIrregularPlanePushButton.clicked.connect(self.createIrregularPlan)
        self.createUniformPlanPushButton.clicked.connect(self.createUniformPlan)
        self.deletePlanPushButton.clicked.connect(self.deletePlan)
        
        # signals/slots for meadow
        self.importSelectedVertexPushButton.clicked.connect(self.importSelectedVertex)
        self.generateMeadowPushButton.clicked.connect(self.generateMeadow)
        self.selectMeadowPushButton.clicked.connect(self.selectMeadow)
        self.deleteSelectedMeadowPushButton.clicked.connect(self.deleteSelectedMeadow)
        self.deleteAllMeadowsPushButton.clicked.connect(self.deleteAllMeadows)
        
        # signals/slots for forest
        self.generateForestPushButton.clicked.connect(self.generateForest)
        self.deleteForestPushButton.clicked.connect(self.deleteForest)
        
        # load images in ui file
        self.loadImage(labelWhiteFlowerPath, self.whiteFlowerImage)
        self.loadImage(labelOrangeFlowerPath, self.orangeFlowerImage)
        self.loadImage(labelRedFlowerPath, self.redFlowerImage)
        self.loadImage(labelGrassPath, self.grassImage)
        self.loadImage(labelSmallStonePath, self.smallStoneImage)
        self.loadImage(labelBigStonePath, self.bigStoneImage)
        self.loadImage(labelGreenTreePath, self.greenTreeImage)
        self.loadImage(labelYellowTreePath, self.yellowTreeImage)
        
        
    def loadImage(self, labelPath, labelName):
        """ This method loads an image in ui file. """
        
        tempImage = QtGui.QImage(labelPath)
        Map = QtGui.QPixmap()
        picture = Map.fromImage(tempImage)
        labelName.setPixmap(picture)
    
    def createIrregularPlan(self):
        """ This method calls createGround() from PluginClass. """
        
        self.PluginObject.createGround(self.lengthSpinBox.value(),
                                       self.widthSpinBox.value(),
                                       'Irregular')
        
        # initialize center Field with 0
        self.centerFieldSpinBox.setValue(0)
        # make meadow and forest Layout available
        self.meadowGroupBox.setEnabled(True)
        self.forestGroupBox.setEnabled(True)
    
    def createUniformPlan(self):
        """ This method calls createGround() from PluginClass. """
        
        self.PluginObject.createGround(self.lengthSpinBox.value(),
                                       self.widthSpinBox.value(),
                                       'Uniform')
        
        # initialize center Field with 0
        self.centerFieldSpinBox.setValue(0)
        # make meadow and forest Layout available
        self.meadowGroupBox.setEnabled(True)
        self.forestGroupBox.setEnabled(True)
    
    def deletePlan(self):
        """ This method deletes the Ground calling deleteGround() from PluginClass. """
        
        response = self.PluginObject.deleteGround()
        # make meadow and forest Layout unavailable
        if response:
            self.meadowGroupBox.setEnabled(False)
            self.forestGroupBox.setEnabled(False)
    
    def importSelectedVertex(self):
        """ This method imports in centerFieldSpinBox the selected vortex. """
        
        numberVertex = self.PluginObject.selectedVertex()
        self.centerFieldSpinBox.setValue(numberVertex)
    
    def generateMeadow(self):
        """ This method calls generateMeadow() from PluginClass. """
        
        # check if it was correct introduced the percent for flowers
        # if not it recalculates
        newValueWhiteFlower, newValueOrangeFlower, newValueRedFlower = self.PluginObject.procentCheck(self.whiteFlowerSpinBox.value(), 
                                                                                                      self.orangeFlowerSpinBox.value(), 
                                                                                                      self.redFlowerSpinBox.value())
        self.orangeFlowerSpinBox.setValue(newValueOrangeFlower)
        self.redFlowerSpinBox.setValue(newValueRedFlower)
        
        respons = self.PluginObject.generateMeadow(self.radiusSpinBox.value(),
                                                   self.whiteFlowerSpinBox.value(), 
                                                   self.orangeFlowerSpinBox.value(),
                                                   self.redFlowerSpinBox.value(), 
                                                   self.flowersDensitySpinBox.value(),
                                                   self.grassDensitySpinBox.value(), 
                                                   self.smallStoneDensitySpinBox.value(),
                                                   self.bigStoneDensitySpinBox.value())
        
        # if the meadow was created then the name of meadow is added in Meadow list
        if respons:
            self.listMeadowWidget.addItem(respons)
        
        # if there is at least one meadow created then the ground Layout is disable
        if self.PluginObject.checkExistingMeadow():
            self.groundGrupBox.setEnabled(False)
    
    def selectMeadow(self):
        """ This method selects the object which is selected in the list. """
        
        toSelect = []
        for item in self.listMeadowWidget.selectedItems():
            toSelect.append(item.text())
        if toSelect:
            self.PluginObject.selectObject('MeadowGroup_' + toSelect[0][7:])
    
    def deleteSelectedMeadow(self):
        """ This method deletes the selected object in the meadow's list. """
        
        toSelect = []
        for item in self.listMeadowWidget.selectedItems():
            toSelect.append(item.text())
            self.listMeadowWidget.takeItem(self.listMeadowWidget.row(item))
        
        if toSelect:
            self.PluginObject.deleteObject('MeadowGroup_' + toSelect[0][7:])
        
        # check if the deleted meadow was the last one
        # and if yes then it makes the ground Layout enable
        if self.PluginObject.checkExistingMeadow() == []:
            self.groundGrupBox.setEnabled(True)
    
    def deleteAllMeadows(self):
        """ This method deletes all meadows. """
        
        respons = self.PluginObject.deleteAllObjectsNamed('MeadowGroup')
        if respons:
            # make the ground Layout enable
            self.groundGrupBox.setEnabled(True)
            self.listMeadowWidget.clear()
    
    def generateForest(self):
        """ This method calls createForest() from PluginClass. """
        
        # check if it was correct introduced the percent for trees
        # if not it recalculates
        newValueGreenTree, newValueYellowTree, tempValue = self.PluginObject.procentCheck(self.greenTreeSpinBox.value(),
                                                                                          self.yellowTreeSpinBox.value())
        
        self.yellowTreeSpinBox.setValue(newValueYellowTree+tempValue)
        
        self.PluginObject.createForest(self.greenTreeSpinBox.value(), self.yellowTreeSpinBox.value())
        
        # make the ground Layout, the meadow Layout and the generateForestPushButton disable 
        self.groundGrupBox.setEnabled(False)
        self.meadowGroupBox.setEnabled(False)
        self.generateForestPushButton.setEnabled(False)
    
    def deleteForest(self):
        """ This method deletes the forest. """
        
        # if the forest is delete make the meadow Layout enable
        if self.PluginObject.deleteForest():
            self.meadowGroupBox.setEnabled(True)
            self.generateForestPushButton.setEnabled(True)
            # check if at least one meadow exist and make the ground Layout disable else enable
            if self.PluginObject.checkExistingMeadow():
                self.groundGrupBox.setEnabled(False)
            else:
                self.groundGrupBox.setEnabled(True)


