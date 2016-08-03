"""
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file         UserErrorMessages.py
#    @brief        This class contains methods for displaying messages
#    @author       remus_avram 
#    @version      0.1
#    @details      This class will contain methods for displaying messages
#    @date         11.2012
#    @test         import UserErrorMessages
#                  errorMessageObj = UserErrorMessages()
#		   errorMessageObj.showWarning(message)
"""



import warnings
from PyQt4 import QtGui, QtCore



class UserErrorMessages(object):
	
	def __init__(self, parent=None):
		self.parent = parent
    
	def showWarning(self, warningString):
		warnings.warn( str(warningString))

	def showError(self, warningString):
		print ('CRITICAL ERROR: ' + warningString)
		
	def showWindowMessage(self,warningString, title, type = "Warning"):
		messageBox = QtGui.QMessageBox(self.parent)
		messageBox.setWindowTitle (title)
		messageBox.setText(warningString)
		if type == "Warning":
			messageBox.setIcon(QtGui.QMessageBox.Warning)
		elif type == "Critical":
			messageBox.setIcon(QtGui.QMessageBox.Critical)
		elif type == "Information":
			messageBox.setIcon(QtGui.QMessageBox.Information)
		
		messageBox.show()
		messageBox.setVisible(True)
		messageBox.raise_()
		messageBox.activateWindow()
		messageBox.exec_()
		
	def showYesNoMessage(self, warningString, title, type="Warning"):
		
		messageBox = QtGui.QMessageBox(self.parent)
		messageBox.setWindowTitle (title)
		messageBox.setText(warningString)
		if type == "Warning":
			messageBox.setIcon(QtGui.QMessageBox.Warning)
		elif type == "Critical":
			messageBox.setIcon(QtGui.QMessageBox.Critical)
		messageBox.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
		messageBox.setDefaultButton(QtGui.QMessageBox.No)
		
		messageBox.show()
		messageBox.setVisible(True)
		messageBox.raise_()
		messageBox.activateWindow()
		if messageBox.exec_() == QtGui.QMessageBox.Yes:
			return True
		else:
			return False
		
		