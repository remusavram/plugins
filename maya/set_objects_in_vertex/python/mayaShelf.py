import sys
import maya.cmds as mc

pathToDir = r'D:/Programare/Python/Projects/2014.04.26/python'

if pathToDir not in sys.path:
    sys.path.append(pathToDir)

try:
    reload(setObjectsInVertex)

except:    
    import setObjectsInVertex_v01 as setObjectsInVertex



def getMainWIndow():
    """ This procedure is used to keep the new window in front all the time, until it's closed. """
    
    import maya.OpenMayaUI as mui   
    pointer = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(pointer), QtCore.QObject)

if mc.window('PluginWindow', q=True, exists=True):
        mc.deleteUI('PluginWindow')

print ( '\n\n\n\n' + '='*30 + '  OUTPUT  ' + '='*30 + '\n\n\n\n' )

win = setObjectsInVertex.InterfacePluginClass(getMainWIndow())
win.show()