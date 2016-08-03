""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file         MayaUserErrorMessages.py
#    @brief        This class will contain methods for displaying messages in maya
#    @author       remus_avram
#    @version      0.1
#    @details      This class will contain methods for displaying messages
#    @date         11.2012
#    @test         import MayaUserErrorMessages
#                  errorMessageObj = MayaUserErrorMessages()
#		   errorMessageObj.showWarning(message)
"""



import maya.cmds as cmds
import UserErrorMessages



class MayaUserErrorMessages(UserErrorMessages.UserErrorMessages):
    
    def __init__(self, parent=None):
		super(MayaUserErrorMessages, self).__init__(parent)
	
    
    def showWarning(self, warningString):
        cmds.warning(warningString)
	
    def showError(self, warningString):
        cmds.error(warningString)

