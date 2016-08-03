""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Ground_v06.py
#    @brief       This class creates the plan for the ground.


#    @author      remus_avram
#    @date        03.2014
"""



import maya.cmds as mc
import random



class GroundClass(object):
    
    def __init__(self):
        super(GroundClass, self).__init__()
        
        self.length = 0
        self.width = 0
        self.subdivisionsHeight = 0
        self.subdivisionsWidth = 0
        self.totalNumberVertex = 0
        self.type = ''
    
    
    def getLength(self):
        if self.length == 0:
            self.length = mc.getAttr("polyGround.width")
        return int(self.length)
    
    def setLength(self, value):
        self.length = value
        
    def getWidth(self):
        if self.width == 0:
            self.width = mc.getAttr("polyGround.height")
        return int(self.width)
    
    def setWidth(self, value):
        self.width = value
    
    def getSubdivisionsHeight(self):
        if self.subdivisionsHeight == 0:
            self.subdivisionsHeight = mc.getAttr("polyGround.subdivisionsHeight")
        return int(self.subdivisionsHeight)
    
    def setSubdivisionsHeight(self, value):
        self.subdivisionsHeight = value
        
    def getSubdivisionsWidth(self):
        if self.subdivisionsWidth == 0:
            self.subdivisionsWidth = mc.getAttr("polyGround.subdivisionsWidth")
        return int(self.subdivisionsWidth)
    
    def setSubdivisionsWidth(self, value):
        self.subdivisionsWidth = value
    
    def getType(self):
        return self.type
    
    def setType(self, value):
        self.type = value
    
    def getTotalNumberVertex(self):
        self.totalNumberVertex = (self.getSubdivisionsHeight() * self.getSubdivisionsWidth() + self.getSubdivisionsHeight() + self.getSubdivisionsWidth())
        
        return int(self.totalNumberVertex)
    
    def setTotalNumberVertex(self, value):
        self.totalNumberVertex = value
    
    def createPlan (self):
        """ This method creates the form of plane. """
        
        self.subdivisionsHeight = self.length/3
        self.subdivisionsWidth = self.width/3
        # create the plan
        currentPlan = mc.polyPlane ( ch=True, o=True, w=self.length, h=self.width,
                                     subdivisionsX=self.subdivisionsHeight, 
                                     subdivisionsY=self.subdivisionsWidth )
        
        # check if the plan should be Irregular
        if self.type == 'Irregular':
            self.makePlanIrregular(currentPlan[0])
        mc.select( clear=True )
        
        return currentPlan[0], currentPlan[1]
    
    def makePlanIrregular(self, myGround):
        """ This method makes the plan irregular. """
        
        # set the softSelect on and give it the size range
        mc.softSelect ( softSelectEnabled=True )
        mc.softSelect ( ssd=350, sud=0.5 )
        
        for i in range(5):
            # select a random vertexes
            vertexRandom = random.randrange( 0, self.getTotalNumberVertex() )
            
            # select a random value for moving the vertex
            vertexMove = random.randrange( -30, 70 )
            
            # select the vertexes and move it
            mc.select ( myGround + '.vtx[' + str(vertexRandom) + ']', replace=True )
            mc.move ( 0, vertexMove, 0, relative=True )
        
        # set the softSelect off
        mc.softSelect ( softSelectEnabled=False )
        
        mc.select( clear=True )


