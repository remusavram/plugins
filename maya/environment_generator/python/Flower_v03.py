""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Flower_v03.py
#    @brief       This class creates the flower.


#    @author      remus_avram
#    @date        12.2013
"""



import maya.cmds as mc
import GroupPanelLayout_v01 as GroupPanelLayout
import random
import maya.mel



class FlowerClass(object):
    
    def __init__(self):
        super(FlowerClass, self).__init__()
        
        self.flowerColorType = ''
        self.flowerTY = 0
        self.flowerColor = 0
        self.currentCore = []
        self.currentPetal = []
        self.currentStalk = []
    
    
    def getFlowerColorType(self):
        return self.flowerColorType
    
    def setFlowerColorType(self, color):
        self.flowerColorType = color
    
    def getFlowerLength(self):
        return self.flowerTY
    
    def setFlowerLength(self):
        self.flowerTY = random.randrange( 10, 15 )
    
    def createCore(self):
        ''' This method creates the core for flower. '''
        
        mc.polySphere( ax=(0, 1, 0) )
        self.currentCore = mc.ls( sl=True )
        mc.scale( 1, 0.5, 1 )
        mc.move( 0, 0.2, 0 )
        
        # delete history
        maya.mel.eval( "DeleteHistory" )
        
        mc.select( clear=True )
        
        return self.currentCore
    
    def createPetals(self):
        '''This method creates the petals of flower. '''
        
        # create the petal
        mc.sphere( ax=(0, 1, 0) );
        mc.move( 0, 0, -1.6 );
        mc.scale( 0.7, 0.3, 1.7 );    
        self.currentPetal = mc.ls( sl=True );
        currentPetal0 = self.currentPetal[0]
    
        # reset the coordinates
        mc.makeIdentity( apply=True, t=1, r=1, s=1, n=0 );
        mc.move( 0, 0, 0, currentPetal0 + '.scalePivot' )
        mc.move( 0, 0, 0, currentPetal0 + '.rotatePivot' )
         
        # move the tip of the petal
        mc.select( currentPetal0 + ".cv[3] [7]" )
        mc.move( 0, 1.5, 0, r=True )
      
        # select the inner part of the petal
        # move them down
        for uCV in range (5,7):  
            for vCV in range (0, 8):
                mc.select( currentPetal0 + ".cv[" + str(uCV) + "] [" + str(vCV) + "]" );
                mc.move( 0, -0.3, 0, r=True )
        
        # delete history
        mc.select( currentPetal0 )
        maya.mel.eval( "DeleteHistory" )
        
        # create the rest of the petals
        numPetals = random.randrange (10, 20);
        mc.select( currentPetal0 )
        degreeApart = ( 360 / numPetals );
        for i in range (0, numPetals):    
            newPetal = mc.duplicate ( rr=True );
            self.currentPetal.append(newPetal)
            mc.rotate( 0, degreeApart, 0, r=True );
            
            # randomly rotate the petals
            petalRX = random.randrange( -5, 5 );
            petalRY = random.randrange( -5, 5 );
            petalRZ = random.randrange( -5, 5 );
            mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
            mc.rotate( petalRX, petalRY, petalRZ, r=True )
            
        return self.currentPetal
        
    def rotateHeadFlower(self, headFlower):
        """ This method rotates and move up the flower. """
        
        # rotate the flower
        mc.select( headFlower );
        flowerRX = random.randrange( -30, 30 );
        flowerRY = random.randrange( -30, 30 );
        flowerRZ = random.randrange( -30, 30 );    
        mc.rotate( flowerRX, flowerRY, flowerRZ, r=True, os=True );
        mc.select( clear=True )
        
    def createStalk(self):
        ''' This method creates the stalk. '''
        
        # y ax is calculated by flower position
        mc.polyPipe( subdivisionsHeight=3 );
        mc.scale( 0.24, self.flowerTY+1, 0.24 )
        mc.move( 0, -self.flowerTY/2, 0 );
        mc.displaySmoothness( divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3 );
        self.currentStalk = mc.ls( sl=True );
        currentStalk0 = self.currentStalk[0]
         
        # bend the stalk
        bendStalkRandomUpX = 1.5 * (1.0 - random.random())
        bendStalkRandomUpZ = 1.5 * (1.0 - random.random())
        for uCV in range (40,60):    
            mc.select( currentStalk0 + ".vtx[" + str(uCV) + "]" );
            mc.move( bendStalkRandomUpX, 0, bendStalkRandomUpZ, r=True );
            mc.select( currentStalk0 + ".vtx[" + str(uCV+60) + "]" );
            mc.move( bendStalkRandomUpX, 0, bendStalkRandomUpZ, r=True );
        
        bendStalkRandomDownX = 1.2 * (1.0 - random.random())
        bendStalkRandomDownZ = 1.2 * (1.0 - random.random())
        for uCV in range (20,40):
            mc.select( currentStalk0 + ".vtx[" + str(uCV) + "]" );
            mc.move( bendStalkRandomDownX, 0, bendStalkRandomDownZ, r=True );
            mc.select( currentStalk0 + ".vtx[" + str(uCV+100) + "]" );
            mc.move( bendStalkRandomDownX, 0, bendStalkRandomDownZ, r=True )
        
        # delete history
        mc.select( currentStalk0 )
        maya.mel.eval( "DeleteHistory" )
        
        mc.select( clear=True )
        
        return self.currentStalk
    
    def flowerPosition(self, flower):
        ''' This method change the position of flower. '''
        
        #move the flower up
        mc.select( flower )
        mc.move( 0, self.flowerTY, 0 )
        
        # Modify -> Freeze Transformation
        mc.makeIdentity( apply=True, t=1, r=1, s=1, n=0, pn=1 )
        
        mc.select( clear=True )



