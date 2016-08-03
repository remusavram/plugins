""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Grass_v04.py
#    @brief       This class creates the geometry for the grass.


#    @author      remus_avram
#    @date        01.2014
"""



import maya.cmds as mc
import random
import maya.mel



class GrassClass(object):
    
    def __init__(self):
        super(GrassClass, self).__init__()
        
        self.currentBlade = []
        self.currentBunch = []
        self.grassHeight = 0
        
        
    def createBladeOfGrass(self):
        """ This method creates a blade of grass. """
        
        # random the high of blade
        self.grassHeight = 0.2 * random.randrange ( 6, 10 );
        
        # create the plane of blade
        mc.polyPlane( axis=(0, 0, 0), subdivisionsX=2, subdivisionsY=6, height=4 );
        mc.move( 0, 2, 0 )
        self.currentBlade = mc.ls( sl=True );
        
        # create the form of blade
        mc.displaySmoothness( divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3 );
        mc.select( self.currentBlade[0] + ".vtx[18:20]", r=True ) ;
        mc.softSelect( softSelectEnabled=True, ssd=20, sud=0.5 );
        mc.scale( 0.1, 1, 1, p=(0, 9.86, 0), r=True );
        mc.softSelect( ssd=8.08, sud=0.5 );
        
        # bend the grass
        bendGrassRandom = 15 * (3.0 - random.random())
        mc.rotate( bendGrassRandom, 0, 0, os=True, r=True, p=(0, 9.18, 0) );
        mc.select( self.currentBlade )
        extrudeFace = mc.polyExtrudeFacet( self.currentBlade[0] + ".f[0:11]", constructionHistory=1, keepFacesTogether=1, pvx=0, pvy=4.84, pvz=0.14, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30 );
        mc.setAttr( extrudeFace[0] + ".localTranslate", 0, 0, 0.05, type='double3' );
        mc.softSelect( softSelectEnabled=False )
        
        # scale the blade
        mc.select( self.currentBlade )
        mc.scale( 1, self.grassHeight, 1, r=True )
        
        # delete history
        maya.mel.eval( "DeleteHistory" )
        
        # change the position
        self.changePositionBlade()
        
        return self.currentBlade
    
    def changePositionBlade(self):
        """ This method change the position of blade. """
        
        # move the grass up
        mc.select( self.currentBlade )
        mc.move( 0, self.grassHeight*2.0 -1.5, 0 )
        
        # rotate the grass
        grassRY = random.randrange ( 0, 360 )
        mc.rotate( 0, grassRY, 0, r=True, os=True )
        
        # Modify -> Freeze Transformation
        mc.makeIdentity( apply=True, t=1, r=1, s=1, n=0, pn=1 )
    
    def changePositionBanch(self, newBlade):
        """ This method change the position of blades to create a bunch. """
        
        mc.select( newBlade )
        
        # rotate the blade
        grassRY = random.randrange ( 0, 360 )
        mc.rotate( 0, grassRY, 0, r=True, os=True )
        
        # move the grass near
        grassTX = random.randrange ( -3, 3 );
        grassTZ = random.randrange ( -3, 3 ); 
        mc.move( grassTX, 0, grassTZ )
    
    def createBunchOfGrass(self):
        """ This method creates a bunch of grass. """
        
        # keep one blade in a list
        self.currentBunch = self.createBladeOfGrass()
        
        # duplicate the blade
        currentBunch0 = self.currentBunch
        mc.select( currentBunch0 )
        for i in range (10):
            newBlade = mc.duplicate ( rr=True )
            self.currentBunch.append(newBlade)
            self.changePositionBanch(newBlade)
        
        for i in self.currentBunch:
            mc.select( i, add=True )
        self.currentBunch = mc.polyUnite()
        
        # delete history
        maya.mel.eval( "DeleteHistory" )
        
        return self.currentBunch[0]


