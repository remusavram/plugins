""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Tree_v02.py
#    @brief       This class imports a tree from another scene.


#    @author      remus_avram
#    @date        01.2014
"""



import maya.cmds as mc
import random
import os



# keep the path of maya's scenes in variables
tree1Path = os.path.join(os.path.dirname(__file__), '../../mayaScene/birchBlowing1.mb')
tree2Path = os.path.join(os.path.dirname(__file__), '../../mayaScene/birchBlowing2.mb')


# global variables
if 'importNumber' not in globals():
    importNumber = 0


class TreeClass(object):
    
    def __init__(self):
        super(TreeClass, self).__init__()
        
        self.currentTree = [0,0,0]
    
    
    def importTree(self, colorType):
        """ This method imports a tree from a Maya scene. """
        
        global importNumber
        importNumber += 1
        
        # import the tree from another maya scene
        if colorType == 'green':
            mc.file(tree1Path, namespace='import' + str(importNumber), i=True)
        
        elif colorType == 'yellow':
            mc.file(tree2Path, namespace='import' + str(importNumber), i=True)
        
        # return the created tree
        allObjects = mc.ls()
        if 'import' + str(importNumber) + ':birchBlowing1' in allObjects:
            self.currentTree[0] = 'import' + str(importNumber) + ':birchBlowing1'
            self.currentTree[1] = 'import' + str(importNumber) + ':birchBlowing1Main'
            self.currentTree[2] = 'import' + str(importNumber) + ':birchBlowing1Leaf'
        elif 'import' + str(importNumber) + ':birchBlowing2' in allObjects:
            self.currentTree[0] = 'import' + str(importNumber) + ':birchBlowing2'
            self.currentTree[1] = 'import' + str(importNumber) + ':birchBlowing2Main'
            self.currentTree[2] = 'import' + str(importNumber) + ':birchBlowing2Leaf'
        
        return self.currentTree
    
    def changePosition(self, currentTree):
        """ This method changes the rotation and size position of the current tree. """
        
        mc.select( currentTree[0] )
        
        treeRY = random.randrange ( 0, 360 )
        mc.rotate( 0, treeRY, 0, r=True, os=True )
        
        treeS = 0.01 * random.randrange ( 92, 108 )
        mc.scale( treeS, treeS, treeS, r=True )
        
        mc.select( clear=True )

