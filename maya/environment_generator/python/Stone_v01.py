""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Stone_v01.py
#    @brief       This class creates a stone object.


#    @author      remus_avram
#    @date        12.2013
"""



import maya.cmds as mc
import random
import maya.mel



class StoneClass(object):
    
    def __init__(self):
        super(StoneClass, self).__init__()
        
        self.currentStone = []
        self.typeStone = 'big'
    
    
    def getType(self):
        return self.typeStone
    
    def setType(self, value):
        self.typeStone = value
    
    def createStone(self):
        """ This method creates the form of stone. """
        
        # create a sphere
        subdivisionsX = 40
        subdivisionsY = 50
        if self.typeStone == 'small':
            size = 6.
        if self.typeStone == 'big':
            size = 9.
        self.currentStone = mc.polySphere(sx=subdivisionsX, sy=subdivisionsY, r=size)
        
        # change its form
        mc.scale( 1, 0.5, 0.6, r=True )
        mc.move( 0, size/3.4, 0, r=True )
        stoneRY = random.randrange ( 0, 360 )
        mc.rotate( 0, stoneRY, 0, r=True, os=True )
        
        mc.softSelect( softSelectEnabled=True, ssd=4, sud=0.5 )
        #mc.softSelect( ssd=0.6, sud=0.3 )
        
        for i in range(20):
            vertexNumber = random.randrange(0, self.totalNumberVertexSphere(subdivisionsX, subdivisionsY))
            moveX = size/200 * random.randrange ( 10, 20 )
            moveY = size/200 * random.randrange ( 5, 20 )
            moveZ = size/200 * random.randrange ( 5, 20 )
            mc.select (self.currentStone[0] + '.vtx[' + str(vertexNumber) + ']')
            mc.move( moveX, moveY, moveZ, r=True)
            
        mc.softSelect( softSelectEnabled=False )
        mc.displaySmoothness( divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3 )
        
        # Modify -> Freeze Transformation
        mc.select( self.currentStone[0] )
        mc.makeIdentity( apply=True, t=1, r=1, s=1, n=0, pn=1 )
        
        # delete history
        maya.mel.eval( "DeleteHistory" )
        
        mc.select( clear=True )
        
        return self.currentStone[0]
    
    def totalNumberVertexSphere(self, subdivisionsX, subdivisionsY):
        """ This method calculates the total number of vertexes. """
        
        return ( subdivisionsX * subdivisionsY - subdivisionsX + 1 )
    
