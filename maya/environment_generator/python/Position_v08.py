""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Position_v07.py
#    @brief       This class calculates the position of objects.


#    @author      remus_avram
#    @date        03.2013
"""



import maya.cmds as mc
import random
import math
import Ground_v06 as Ground



# define global variables
global vectorPositionXZ
global vectorPositionY
global vectorPositionAvailable
global vectorPositionXZTemp


class PositionClass(Ground.GroundClass):
    """ 
        This class is a subclass of GroundClass() because it uses some attributes and some
        methods from this class: length, width, getSubdivisionsHeight(), setSubdivisionsHeight(),totalNumberVertex(), etc. 
    """
    
    def __init__(self):
        super(PositionClass, self).__init__()
        
        self.importedVertex = 0
        
    
    def findNumberSelectedVertex(self):
        """ This method returns the selected vertex in plan. """
        
        vertexList = mc.ls(sl=True)
        # if it is nothing selected or it is something else selected then return False
        if ( vertexList == [] ):
            return False
        elif (vertexList[0][0:11] != 'Ground.vtx[' ):
            return False
        elif ( ':' in vertexList[0][11:-1] ):
            # if there are more vertexes selected, it imports the first one
            import re
            vertexTempList =  re.findall(r'\d+', vertexList[0])
            self.importedVertex = int(vertexTempList[0])
            return self.importedVertex
        else:
            self.importedVertex = int(vertexList[0][11:-1])
            return self.importedVertex
    
    def initializeVectors(self):
        """ This method initializes vectors with 0 for all the vertexes from plan. """
        
        global vectorPositionXZ, vectorPositionY, vectorPositionAvailable
        
        vectorPositionXZ = []
        vectorPositionY = []
        vectorPositionAvailable = []
        
        for i in range (self.getTotalNumberVertex()+1):
            # In this vector will be kept the position of all vertexes.
            vectorPositionXZ.append([0, 0])
            vectorPositionY.append(0)
            vectorPositionAvailable.append(0)
    
    def findVertexPosition(self):
        """ This method finds the position of all vertexes and it keeps them in the vector. """
        
        global vectorPositionXZ, vectorPositionY
        
        # select all the vertexes
        mc.select('Ground.vtx[0:' + str( self.getTotalNumberVertex()+1) + ']', r=True )
        # scale the vertexes to obtain the distance from center to the real position.
        mc.scale ( 0.000001, 1, 0.000001, r=True )
        # keep the vertexes positions (x,y,z) in the vectors
        for i in range(self.getTotalNumberVertex()+1):
            vectorPositionXZ[i][0] = round(-1 * (mc.getAttr ( 'GroundShape.pnts[' + str(i) + '].pntx' )))
            vectorPositionXZ[i][1] = round(-1 * (mc.getAttr ( 'GroundShape.pnts[' + str(i) + '].pntz' )))
            vectorPositionY[i] = -round(-1 * (mc.getAttr ( 'GroundShape.pnts[' + str(i) + '].pnty' )))
            
        # bring the plan to the normal form
        for i in range(self.getTotalNumberVertex()+1):
            mc.setAttr ( 'GroundShape.pnts[' + str(i) + '].pntx', 0 )
            mc.setAttr ( 'GroundShape.pnts[' + str(i) + '].pntz', 0 )
        
        self.vectorPositionTemp()
        
        mc.select( clear=True )
    
    def vectorPositionTemp(self):
        """ This method calculates a temp vector position ((poz-2)/3). """
        
        global vectorPositionXZ, vectorPositionY, vectorPositionXZTemp
        
        vectorPositionXZTemp = []
        for item in vectorPositionXZ:
            vectorPositionXZTemp.append(list(item))
        for i in range(self.getTotalNumberVertex()+1):
            vectorPositionXZTemp[i][0] = int(vectorPositionXZTemp[i][0]/3)
            vectorPositionXZTemp[i][1] = int(vectorPositionXZTemp[i][1]/3)
    
    def calculateDistance(self, objectTX, objectTZ):
        """ This metog calculate the distance from point to center. """
        
        global vectorPositionXZ
        
        distance = math.sqrt(pow(vectorPositionXZ[self.importedVertex][0] - objectTX, 2) + pow(vectorPositionXZ[self.importedVertex][1] - objectTZ ,2))
        
        return distance
    
    def calculateXZ(self, radius):
        """ This method calculates random X and Z position. """
        
        global vectorPositionXZ
        radius *= 3
        
        # check if the chosen coordinators are in the circle inscribed in the square
        # calculate the distance from point to center
        distance = radius + 300
        while distance >= (radius):
            objectTX = int((random.randrange(vectorPositionXZ[self.importedVertex][0]-radius, vectorPositionXZ[self.importedVertex][0]+radius))/3)
            objectTZ = int((random.randrange(vectorPositionXZ[self.importedVertex][1]-radius, vectorPositionXZ[self.importedVertex][1]+radius))/3)
            distance = self.calculateDistance(objectTX*3, objectTZ*3)
        
        return objectTX, objectTZ, distance
    
    def meadowPosition(self, radius, object, numberGenerateMedow):
        """ This method sets the position for all the objects in the meadow. """
        
        global vectorPositionXZ, vectorPositionY, vectorPositionXZTemp
        
        mc.select( object )
        
        objectTX, objectTZ, distance = self.calculateXZ(radius)
        
        # find objectTY using objectTX and objectTZ
        # and also check if there is ground where the user want to create meadow
        createCheck = 1
        tryNumber = 0
        while createCheck == 1:
            if [objectTX, objectTZ] in vectorPositionXZTemp:
                vertexNumber = vectorPositionXZTemp.index([objectTX, objectTZ])
                objectTY = vectorPositionY[vertexNumber]
                # check if the object is a flower, stone or grass
                # if it is a flower or a stone then check the 'superimpose'
                if self.checkSuperimpose(object, vertexNumber, numberGenerateMedow):
                    # after the position is found, it moves the object
                    mc.move( objectTX*3, objectTY, objectTZ*3 )
                    createCheck = 0
                    break
                else:
                    objectTX, objectTZ, distance = self.calculateXZ(radius)
                    tryNumber += 1
            
            # if the position isn't found, then it is needed to decrease the distance
            # this happened when the radius of the meadow exceeds the plan
            if objectTX < 0:
                objectTX = objectTX + 1
            else:
                objectTX = objectTX - 1
            if objectTZ < 0:
                objectTZ = objectTZ + 1
            else:
                objectTZ = objectTZ - 1
                
            if tryNumber > 10:
                mc.delete( object )
                return False
        
        mc.select( clear=True )
        
        return True
    
    def treePosition(self, position, object):
        """ This method calculates the position of each tree. """
        
        global vectorPositionXZ, vectorPositionY
        
        mc.select( object )
        mc.move(vectorPositionXZ[position][0], vectorPositionY[position], vectorPositionXZ[position][1])
        self.makeVertexesUnavailable(position, 11, 100)
        mc.select( clear=True )
        
    def checkSuperimpose(self, object, vertexNumber, numberGenerateMedow):
        """ This method checks if the object is not positioned over another object. """
        
        if object[0:6] == 'Flower':
            if self.checkPositionSuperimpose(vertexNumber, 1, 0) or self.checkPositionSuperimpose2(vertexNumber, 1):
                self.makeVertexesUnavailable(vertexNumber, 1, numberGenerateMedow)
                return True
        
        if object[0:8] == 'StoneBig':
            if self.checkPositionSuperimpose(vertexNumber, 3, 0) or self.checkPositionSuperimpose2(vertexNumber, 3):
                self.makeVertexesUnavailable(vertexNumber, 3, numberGenerateMedow)
                return True
            
        if object[0:10] == 'StoneSmall':
            if self.checkPositionSuperimpose(vertexNumber, 2, 0) or self.checkPositionSuperimpose2(vertexNumber, 2):
                self.makeVertexesUnavailable(vertexNumber, 2, numberGenerateMedow)
                return True
                    
        if object[0:5] == 'Grass':
            return True
        
        return False
    
    def checkPositionSuperimpose(self, vertexNumber, size, available):
        """ This method checks if all the vertexes in a square are free (0). """
        
        global vectorPositionAvailable
        
        if (vertexNumber>=(self.getSubdivisionsHeight())*size) and (vertexNumber<=(self.getTotalNumberVertex()-(self.getSubdivisionsHeight())*size)):
            for i in range(size*2):
                for j in range(size*2):
                    if (vectorPositionAvailable[int(vertexNumber+(i-size)*(self.getSubdivisionsHeight())+(j-size))] != available):
                        return False
        else:
            return False
        return True
    
    def checkPositionSuperimpose2(self, vertexNumber, size):
        """ This method checks if all the vertexes in a square are free (0). """
        
        global vectorPositionAvailable
        
        if (vertexNumber>=(self.getSubdivisionsHeight())*size) and (vertexNumber<=(self.getTotalNumberVertex()-(self.getSubdivisionsHeight())*size)):
            for i in range(size*2):
                for j in range(size*2):
                    if (vectorPositionAvailable[int(vertexNumber+(i-size)*(self.getSubdivisionsHeight())+(j-size))] > 0):
                        return False
        else:
            return False
        return True
    
    def makeVertexesUnavailable(self, vertexNumber, size, numberGenerateMedow):
        """ This method makes the vertexes unavailable when the position is taken. """
        
        global vectorPositionAvailable
        
        for j in range(size*2):
            for k in range(size*2):
                vectorPositionAvailable[int(vertexNumber+(j-size)*(self.getSubdivisionsHeight())+(k-size))] = numberGenerateMedow
    
    def makeUnAvailablePositionMeadow(self, radius, availableNumber):
        """ This method makes the rest of the vertexes of a meadow unavailable/available after it is created. """
        
        global vectorPositionXZ, vectorPositionAvailable
        radius *= 3
        
        for j in range(radius*2):
            for k in range(radius*2):
                tempVar = int(self.importedVertex + (j-radius) * (self.getSubdivisionsHeight()) + (k-radius))
                if (tempVar<=self.getTotalNumberVertex()) and (tempVar > 0):
                    distance = self.calculateDistance(vectorPositionXZ[tempVar][0], vectorPositionXZ[tempVar][1])
                    if (distance < radius):
                        if vectorPositionAvailable[tempVar] == 0:
                            vectorPositionAvailable[tempVar] = availableNumber
    
    def makePositionAvailable(self, available):
        """ This method makes the position available. """
        
        global vectorPositionAvailable
        
        for i in range(self.getTotalNumberVertex()+1):
            if (vectorPositionAvailable[i] == available) or (vectorPositionAvailable[i] == -available):
                vectorPositionAvailable[i] = 0
    
    def checkMethod(self):
        """ This method is just for testing the positionVector. It prints the positionVector as a matrix. """
        
        global vectorPositionAvailable
        
        list = []
        for i in range(self.getTotalNumberVertex()+1):
            list.append(vectorPositionAvailable[i])
            if i % (self.getSubdivisionsHeight() + 1.) == 0:
                print list
                list = []
        print list



