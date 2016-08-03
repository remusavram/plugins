""" 
#    @path        D:\Programare\Python\Projects\2014.04.26
#    @file        setObjectsInVertex_v01.py
#    @brief       This script takes one object and put it in evry vertex of another object.


#    @author      remus_avram
#    @date        05.2014
"""



from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4 import Qt
import os
import sip

import maya.cmds as mc
import UserErrorMessages
import GroupPanelLayout_v01 as GroupPanelLayout


# keep the path to the uiFile in a variable
uiFile = os.path.join(os.path.dirname(__file__), '../ui/PluginInterface_v02.ui')

# keep the changeable names in variables
windowObject = 'PluginWindow'


class InterfacePluginClass(QtGui.QMainWindow):
	"""
	This class imports .ui file and creates the window for the plugin.
	"""

	def __init__(self, parent=None):
		super(InterfacePluginClass, self).__init__(parent)

		self.listNewObjects = []

		# load ".ui" file
		uic.loadUi(uiFile, self)

		# create objects
		self.messageObject = UserErrorMessages.UserErrorMessages()
		self.groupObject = GroupPanelLayout.GroupClass()

		# set window name
		self.setObjectName(windowObject)

		self.mainWidget = QtGui.QWidget()
		self.setCentralWidget(self.mainWidget)
		self.mainWidget.setLayout(self.mainGrid)

		# signals/slots
		self.pushButtonImportMainObject.clicked.connect(self.importMainObject)
		self.pushButtonImportUsedObject.clicked.connect(self.importUsedObject)
		self.pushButtonGenerateForm.clicked.connect(self.generateForm)
		self.horizontalSliderResizeUsedObject.valueChanged.connect(self.resizeObject)


	def importMainObject(self):
		""" 
		This method imports the main selected object.
		"""

		selectedObject = mc.ls(sl=True)
		if selectedObject == []:
			self.messageObject.showWindowMessage( "Please select an object!", "Select" )
		else:
			self.lineEditMainObject.clear()
			self.lineEditMainObject.insert(selectedObject[0])


	def importUsedObject(self):
		""" 
		This method imports the selected object which will be used.
		"""

		selectedObject = mc.ls(sl=True)
		if selectedObject == []:
			self.messageObject.showWindowMessage( "Please select an object!", "Select" )
		else:
			self.lineEditUsedObject.clear()
			self.lineEditUsedObject.insert(selectedObject[0])


	def generateForm(self) :
		"""
		This method returns the position of all vertices of an object. 
		"""
 		
		vtxWorldPosition = []
		mainObject = self.lineEditMainObject.displayText()
		usedObject = self.lineEditUsedObject.displayText()
		
		if mainObject:	
			# create a group for the new objects
			self.groupObject.createGroup("NewObjectsGroup")
			mc.SnapToPoint()

			vtxIndexList = mc.getAttr( mainObject+".vrts", multiIndices=True )
		 
			for i in vtxIndexList :
				curPointPosition = mc.xform( str(mainObject)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True ) 
				mc.select( usedObject )
				newObject = mc.duplicate ( rr=True )
				self.groupObject.addInGroup("NewObjectsGroup", newObject)
				self.listNewObjects.append(newObject)
				mc.move(curPointPosition[0], curPointPosition[1], curPointPosition[2], newObject, rpr=True)

			mc.SnapToPoint()
		else:
			self.messageObject.showWindowMessage( "Please import objects!", "Select" )
	 
		mc.select( clear=True )


	def resizeObject(self):
		""" 
		This method resizes the object.
		"""

		getScale = self.spinBoxResizeUsedObject.value()

		for object in self.listNewObjects:
			mc.setAttr(object[0]+".scaleX", float(getScale)/100 )
			mc.setAttr(object[0]+".scaleY", float(getScale)/100 )
			mc.setAttr(object[0]+".scaleZ", float(getScale)/100 )







