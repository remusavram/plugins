""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Plugin_v05.py
#    @brief       " This script calls the other classes for creating the Environment "


#    @author      remus_avram
#    @date        03.2014
"""



import Ground_v06 as Ground
import Flower_v03 as Flower
import Grass_v04 as Grass
import Stone_v01 as Stone
import Tree_v03 as Tree
import Position_v08 as Position
import UserErrorMessages
import Shader_v01 as Shader
import GroupPanelLayout_v01 as GroupPanelLayout
import random



class PluginClass (object):
    
    def __init__(self):
        super (PluginClass, self).__init__()
        
        # create objects
        self.messageObject = UserErrorMessages.UserErrorMessages()
        self.groundObject = Ground.GroundClass()
        self.flowerObject = Flower.FlowerClass()
        self.grassObject = Grass.GrassClass()
        self.stoneObject = Stone.StoneClass()
        self.treeObject = Tree.TreeClass()
        self.positionObject = Position.PositionClass()
        self.shaderObject = Shader.ShaderClass()
        self.groupObject = GroupPanelLayout.GroupClass()
        
        # this list is used to keep temporarily results
        self.tempListCreateObject = []
        
        # keep the last object number created;
        # it is used to keep the counter of the same objects; to not overwrite the old ones
        self.numberGenerateMedow = self.groupObject.findLastGroupNumber('MeadowGroup') + 1
        self.numberGenerateFlower = self.groupObject.findLastGroupNumber('Flower') + 1
        self.numberGeneratePetal = self.groupObject.findLastGroupNumber('PetalsGroup') + 1
        self.numberGenerateYellowTree = self.groupObject.findLastGroupNumber('YellowTree') + 1
        self.numberGenerateGreenTree = self.groupObject.findLastGroupNumber('GreenTree') + 1
    
    
    ###########################################   Ground   ###########################################
    
    
    def checkExistGround(self):
        """ This method checks if the ground exists. """
        
        if self.groupObject.checkExistingGroup('Ground'):
            return 1
        return 0
    
    def createGround(self, lengthValue, widthValue, typePlan):
        """ This method calls methods form GroundClass to constructs the ground. """
        
        # first is checked if the plane has already existed;
        # if not it will be created
        if self.checkExistGround() == 0:
            self.groundObject.setLength(lengthValue - 1)
            self.groundObject.setWidth(widthValue - 1)
            self.groundObject.setType(typePlan)
            self.tempListCreateObject, polyPlane = self.groundObject.createPlan()
            self.checkExistingShader('ground')
            self.shaderObject.connectShader(selectedObject=self.tempListCreateObject, nameShader='groundColorBrown')
            self.groupObject.renameObject(object=polyPlane, objectName="polyGround")
            self.groupObject.renameObject(object=self.tempListCreateObject, objectName="Ground")
            
            # find vertexes position; 
            self.positionObject.setSubdivisionsHeight(self.groundObject.getSubdivisionsHeight())
            self.positionObject.setSubdivisionsWidth(self.groundObject.getSubdivisionsWidth())
            self.positionObject.initializeVectors()
            self.positionObject.findVertexPosition()
        else:
            # if the plan exist then it will ask if it is wanted a new plan
            response = self.messageObject.showYesNoMessage(" Do you want to create a new ground?", "Ground")
            # if 'yes' then the plan will be deleted and the method will be recalled
            if response:
                self.groupObject.deleteGroup('Ground')
                self.createGround(lengthValue, widthValue, typePlan)
    
    def deleteGround(self):
        """ This method deletes the ground if it exist. """
        
        # first it checks if the ground exist, and it asks if we are sure to delete it
        if self.checkExistGround() == 1:
            response = self.messageObject.showYesNoMessage("Are you sure you want to delete the existing ground?", "Ground")
            # if 'yes' then it will be deleted and returns 'True'
            if response:
                self.groupObject.deleteGroup('Ground')
                return True
        else:
            # else it won't be deleted and returns 'False'
            self.messageObject.showWindowMessage("There is no object called 'Ground'!", "Ground")
        return False
    
    
    ##########################################   Meadow   ##########################################
    
    
    def generateMeadow(self, radius, whiteFlowerPercent, orangeFlowerPercent, redFlowerPercent, 
                             flowersDensity, grassDensity, smallStoneDensity, bigStoneDensity):
        """ This method generates a meadow. """
        
        # first it checks if it is something to create
        if flowersDensity == grassDensity == smallStoneDensity == bigStoneDensity == 0:
            return False
        
        # check if the shades of meadow exist; it is checked one time if the shades are created
        self.checkExistingShader('meadow')
        
        # create group
        self.groupObject.createGroup('MeadowGroup_' + str(self.numberGenerateMedow))
        
        # create and calculate the position of flowers
        self.groupObject.createGroup('FlowerGroup_' + str(self.numberGenerateMedow))
        checkCreateFlower1 = checkCreateFlower2 = checkCreateFlower3 = True
        checkCreateFlower1 = self.calculateNumberFlower(flowersDensity, whiteFlowerPercent, 'white', radius)
        checkCreateFlower2 = self.calculateNumberFlower(flowersDensity, orangeFlowerPercent, 'orange', radius)
        checkCreateFlower3 = self.calculateNumberFlower(flowersDensity, redFlowerPercent, 'red', radius)
        
        # create and calculate the position of grass
        self.createGrass(grassDensity, radius)
        
        # create and calculate the position of stones
        self.groupObject.createGroup('StoneGroup_' + str(self.numberGenerateMedow))
        checkCreateStoneBig = checkCreateStoneSmall = True
        checkCreateStoneBig = self.createStone(radius, 'Big', bigStoneDensity)
        checkCreateStoneSmall = self.createStone(radius, 'Small', smallStoneDensity)
        
        # add grassGroup, flowerGroup and StoneGroup in MeadowGroup
        # check if the grass is created
        if self.groupObject.checkExistingGroup('GrassGroup_' + str(self.numberGenerateMedow)):
            self.groupObject.addInGroup(groupName='MeadowGroup_' + str(self.numberGenerateMedow), object='GrassGroup_' + str(self.numberGenerateMedow))
        self.groupObject.addInGroup(groupName='MeadowGroup_' + str(self.numberGenerateMedow), object='FlowerGroup_' + str(self.numberGenerateMedow))
        self.groupObject.addInGroup(groupName='MeadowGroup_' + str(self.numberGenerateMedow), object='StoneGroup_' + str(self.numberGenerateMedow))
        
        # checks if all the flowers could be created
        if (checkCreateFlower1 == False) or (checkCreateFlower2 == False) or (checkCreateFlower3 == False) or (checkCreateStoneBig == False) or (checkCreateStoneSmall == False):
            self.messageObject.showWindowMessage( "Flowers or stones density is too large for the selected zone!", "Calculate Position" )
                                                     
        # after the meadow is generated the vertexes belong this meadow will become unavailable
        self.positionObject.makeUnAvailablePositionMeadow(radius, -self.numberGenerateMedow)
        
        # increase the number of generate meadow
        self.numberGenerateMedow = self.numberGenerateMedow + 1
        
        #self.positionObject.checkMethod()
        
        return 'Poiana_' + str(self.numberGenerateMedow-1)
        
    def checkExistingMeadow(self):
        """ This method checks if the respective group exist. """
        
        listGroupNumbers = self.groupObject.findGroupNumbers('MeadowGroup')
        return listGroupNumbers
    
    ############################   Flower   ############################
    
    
    def calculateNumberFlower(self, flowersDensity, percent, color, radius):
        """ This method calculates the number of flowers which should be created. """
        
        if color == 'white':
            coreShader = 'coreColorYellow'
            petalShader = 'petalColorWhite'
        elif color == 'orange':
            coreShader = 'coreColorBrown'
            petalShader = 'petalColorOrange'
        elif color == 'red':
            coreShader = 'coreColorBlack'
            petalShader = 'petalColorRed'
        
        # calculate the percent; create the flower; move the flower in respective position
        x = flowersDensity * percent /100
        for i in range(x):
            currentFlower = self.createFlower(coreShader, petalShader)
            checkCreateFlower = self.positionObject.meadowPosition(radius, currentFlower, self.numberGenerateMedow)
            if checkCreateFlower == False:
                return False
        return True
    
    def createFlower(self, coreShader, petalShader):
        """ This method creates one flower. It calls the methods from FlowerClass. """
        
        # create the flower group
        self.groupObject.createGroup('Flower_' + str(self.numberGenerateFlower))
        
        # calculate the length of every flower
        self.flowerObject.setFlowerLength()
        
        # create core; connects shader; add it in respective flower group; rename the core
        self.tempListCreateObject = self.flowerObject.createCore()
        self.shaderObject.connectShader(selectedObject=self.tempListCreateObject, nameShader=coreShader)
        self.groupObject.addInGroup(groupName='Flower_' + str(self.numberGenerateFlower), object=self.tempListCreateObject)
        self.groupObject.renameObject(object=self.tempListCreateObject, objectName="Core")
        
        # create petals; create a group of petals; connect shader for all the petals
        # add it in respective flower group; rotate the head flower
        self.tempListCreateObject = self.flowerObject.createPetals()
        self.groupObject.createGroup('PetalsGroup_' + str(self.numberGeneratePetal))
        for petal in self.tempListCreateObject:
            self.shaderObject.connectShader(selectedObject=petal, nameShader=petalShader)
            self.groupObject.addInGroup(groupName='PetalsGroup_' + str(self.numberGeneratePetal), object=petal)
            self.groupObject.renameObject(object=petal, objectName="Petal_0")
        self.groupObject.addInGroup(groupName='Flower_' + str(self.numberGenerateFlower), object='PetalsGroup_' + str(self.numberGeneratePetal))
        self.flowerObject.rotateHeadFlower('Flower_' + str(self.numberGenerateFlower))
        
        # create stalk; connect the shader; add it in respective flower group; rename the stalk
        self.tempListCreateObject = self.flowerObject.createStalk()
        self.shaderObject.connectShader(selectedObject=self.tempListCreateObject, nameShader="stalkColorGreen")
        self.groupObject.addInGroup(groupName='Flower_' + str(self.numberGenerateFlower), object=self.tempListCreateObject)
        self.groupObject.renameObject(object=self.tempListCreateObject, objectName="Stalk")
        
        # calculate the first position of flower
        self.flowerObject.flowerPosition('Flower_' + str(self.numberGenerateFlower))
        
        # add the flower in flowrGroup
        self.groupObject.addInGroup(groupName='FlowerGroup_' + str(self.numberGenerateMedow), object='Flower_' + str(self.numberGenerateFlower))
        
        # increase groups numbers
        self.numberGenerateFlower = self.numberGenerateFlower + 1
        self.numberGeneratePetal = self.numberGeneratePetal + 1
        
        return ('Flower_' + str(self.numberGenerateFlower - 1))
    
    
    ############################   Grass   ############################
    
    
    def createGrass(self, grassDensity, radius):
        """ This method creates the grass using methods from GrassClass. """
        
        # add all the grass from a meadow in a list
        temporaryList = []
        # create the grass and calculate the position for each of bunchOfGrass
        for i in range (grassDensity):
            self.tempListCreateObject = self.grassObject.createBunchOfGrass()
            self.tempListCreateObject = self.groupObject.renameObject(object=self.tempListCreateObject, objectName='Grass_')
            temporaryList.append(self.tempListCreateObject)
            self.positionObject.meadowPosition(radius, self.tempListCreateObject, self.numberGenerateMedow)
        # combine all the grass; first check if there are more then one objects
        if len(temporaryList) > 1:
            temporaryList = self.groupObject.combineObjects(temporaryList)
        if len(temporaryList) > 0:
            # connect the shader; the shader is connected one time for all the grass of a meadow
            self.shaderObject.connectShader(selectedObject=temporaryList[0], nameShader="grassColorGreen")
            # rename the object
            self.groupObject.renameObject(object=temporaryList[0], objectName='GrassGroup_' + str(self.numberGenerateMedow))
    
    
    ############################   Stone   ############################
    
    
    def createStone(self, radius, type, numberStones):
        """ This method creates stones using methods from StoneClass. """
        
        # add all the stones from a meadow in a list
        temporaryList = []
        if type == 'Small':
            self.stoneObject.setType('small')
        elif type == 'Big':
            self.stoneObject.setType('big')
        checkCreateStone = True
        
        # create the stones and calculate the position for each of stone
        for i in range (numberStones):
            self.tempListCreateObject = self.stoneObject.createStone()
            self.tempListCreateObject = self.groupObject.renameObject(object=self.tempListCreateObject, objectName='Stone' + type)
            checkCreateStone = self.positionObject.meadowPosition(radius, self.tempListCreateObject, self.numberGenerateMedow)
            # if the position is not found, then it brakes the creation
            if checkCreateStone == False:
                break
            temporaryList.append(self.tempListCreateObject)
        # combine all the stones; first check if there are more then one objects
        if len(temporaryList) > 1:
            temporaryList = self.groupObject.combineObjects(temporaryList)
        if len(temporaryList) > 0:
            # connect the shader; the shader is connected one time for all the big/small stones of a meadow
            self.shaderObject.connectShader(selectedObject=temporaryList[0], nameShader="stoneColorWhite")
            # rename the object
            newName = self.groupObject.renameObject(object=temporaryList[0], objectName='Stone' + type + '_' + str(self.numberGenerateMedow))
            self.groupObject.addInGroup(groupName='StoneGroup_' + str(self.numberGenerateMedow), object=newName)
        
        if checkCreateStone == False:
            return False
        
        return True
    
    ##########################################   Forest   ##########################################
    
    
    def createForest(self, greenTreePercent, yellowTreePercent):
        """ This method creates the forest. """
        
        # check if the shades of forest exist
        self.checkExistingShader('forest')
        
        # create group
        self.groupObject.createGroup('ForestGroup')
        self.groupObject.createGroup('GreenTreeGroup')
        self.groupObject.createGroup('YellowTreeGroup')
        self.groupObject.addInGroup(groupName='ForestGroup', object='GreenTreeGroup')
        self.groupObject.addInGroup(groupName='ForestGroup', object='YellowTreeGroup')
        
        # check all the vertex for superimpose
        for i in range(((self.groundObject.getSubdivisionsHeight())*11), (self.groundObject.getTotalNumberVertex()-(self.groundObject.getSubdivisionsHeight())*11)):
            if self.positionObject.checkPositionSuperimpose(i, 11, 0):
                tempRandom = random.randrange (0, 101)
                if tempRandom <= greenTreePercent:
                    currentTree = self.createTree('green')
                else:
                    currentTree = self.createTree('yellow')
                self.positionObject.treePosition(i, currentTree)
        
    def createTree(self, type):
        """ This method creates a tree. """
        
        if type == 'green':
            # if the tree exist then it will be duplicated otherwise it is imported
            if self.groupObject.checkExistingStringGroup('GreenTree_'):
                newGroupName = self.groupObject.duplicateGroup('GreenTree_' + str(self.groupObject.findLastGroupNumber('GreenTree')))
                self.treeObject.changePosition(newGroupName)
                return newGroupName
            else:
                self.tempListCreateObject = self.treeObject.importTree('green')
                self.shaderObject.connectShader(selectedObject=self.tempListCreateObject[1], nameShader="mainTreeColorBrown")
                self.shaderObject.connectShader(selectedObject=self.tempListCreateObject[2], nameShader="leafColorGreen")
                newGroupName = self.groupObject.renameObject(object=self.tempListCreateObject[0], objectName='GreenTree_' + str(self.numberGenerateYellowTree))
                self.groupObject.renameObject(object=self.tempListCreateObject[1], objectName='TreeMain')
                self.groupObject.renameObject(object=self.tempListCreateObject[2], objectName='TreeFeaf')
                self.groupObject.addInGroup(groupName='GreenTreeGroup', object=newGroupName)
                self.numberGenerateYellowTree += 1
                return newGroupName
        
        elif type == 'yellow':
            # if the tree exist then it will be duplicated otherwise it is imported
            if self.groupObject.checkExistingStringGroup('YellowTree_'):
                newGroupName = self.groupObject.duplicateGroup('YellowTree_' + str(self.groupObject.findLastGroupNumber('YellowTree')))
                self.treeObject.changePosition(newGroupName)
                return newGroupName
            else:
                self.tempListCreateObject = self.treeObject.importTree('yellow')
                self.shaderObject.connectShader(selectedObject=self.tempListCreateObject[1], nameShader="mainTreeColorBrown")
                self.shaderObject.connectShader(selectedObject=self.tempListCreateObject[2], nameShader="leafColorYellow")
                newGroupName = self.groupObject.renameObject(object=self.tempListCreateObject[0], objectName='YellowTree_' + str(self.numberGenerateYellowTree))
                self.groupObject.renameObject(object=self.tempListCreateObject[1], objectName='TreeMain')
                self.groupObject.renameObject(object=self.tempListCreateObject[2], objectName='TreeFeaf')
                self.groupObject.addInGroup(groupName='YellowTreeGroup', object=newGroupName)
                self.numberGenerateYellowTree += 1
                return newGroupName
    
    def deleteForest(self):
        """ This method checks if the forest exist and if yes, then it will delete the forest. """
        
        # first it checks if the forest exist, and it asks if we are sure to delete it
        if self.groupObject.checkExistingGroup('ForestGroup'):
            response = self.messageObject.showYesNoMessage("Are you sure you want to delete the forest?", "Forest")
            if response:
                self.groupObject.deleteGroup('ForestGroup')
                self.positionObject.makePositionAvailable(100)
                return True
        else:
            self.messageObject.showWindowMessage("There is no object called 'Forest'!", "Forest")
            return False
    
    def checkExistingForest(self):
        """ This method checks if the forest exist. """
        
        if self.groupObject.checkExistingGroup('ForestGroup'):
            return True
        return False
    
    
    ##########################################   Shader   ##########################################
    
    
    def checkExistingShader(self, objectType):
        """ This method checks if the shaders exist. """
        
        # check for the ground shader
        if objectType == 'ground':
            if ( self.shaderObject.checkExistShader("groundColorBrown") == 0 ):
                self.shaderObject.createMountainShader(nameShader="groundColorBrown",
                                                       nameTextureShader="groundTextureBrown",
                                                       listSnowColor = [0.50, 0.39, 0.37], 
                                                       listRockColor = [0.075, 0.045, 0.027], 
                                                       amptitude = 2)
        # check for the meadow shader
        if objectType == 'meadow':
            # check for petal shader
            if ( self.shaderObject.checkExistShader("petalColorWhite") == 0 ):
                self.shaderObject.createRampShader(nameShader="petalColorWhite",
                                                   nameTextureShader="petalRampWhite", 
                                                   colorEntryList=[[0.9, 0.55, 0.48],[1, 1, 1],[ 1, 1, 1]], 
                                                   position=[0, 0.2, 1], 
                                                   typeTexture=8)
            if ( self.shaderObject.checkExistShader("petalColorOrange") == 0 ):
                self.shaderObject.createRampShader(nameShader="petalColorOrange",
                                                   nameTextureShader="petalRampOrange", 
                                                   colorEntryList=[[1, 0, 0],[1, 1, 0],[1, 0, 0]], 
                                                   position=[0, 0.5, 1], 
                                                   typeTexture=8)
            if ( self.shaderObject.checkExistShader("petalColorRed") == 0 ):
                self.shaderObject.createRampShader(nameShader="petalColorRed",
                                                   nameTextureShader="petalRampRed", 
                                                   colorEntryList=[[0.9, 0.55, 0.48],[1, 0.19, 0.19],[0.74, 0, 0]], 
                                                   position=[0, 0.2, 1], 
                                                   typeTexture=8)
            # check for the core shader
            if ( self.shaderObject.checkExistShader("coreColorBrown") == 0 ):
                self.shaderObject.createNormalShader(nameShader="coreColorBrown", listColor = [0.4, 0.3, 0.14])
            if ( self.shaderObject.checkExistShader("coreColorYellow") == 0 ):
                self.shaderObject.createNormalShader(nameShader="coreColorYellow", listColor = [1, 0.8, 0])
            if ( self.shaderObject.checkExistShader("coreColorBlack") == 0 ):
                self.shaderObject.createNormalShader(nameShader="coreColorBlack", listColor = [0.16, 0.12, 0])
            
            # check for the stalk shader
            if ( self.shaderObject.checkExistShader("stalkColorGreen") == 0 ):
                self.shaderObject.createNormalShader(nameShader="stalkColorGreen", listColor = [0.16, 0.64, 0.3])
            
            # check for the grass shader
            if ( self.shaderObject.checkExistShader("grassColorGreen") == 0 ):
                self.shaderObject.createNormalShader(nameShader="grassColorGreen", listColor = [0.54, 0.8, 0.054])
        
            # check for the stone shader
            if (self.shaderObject.checkExistShader("stoneColorWhite") == 0):
                self.shaderObject.createRockShader(nameShader="stoneColorWhite",
                                                       nameTextureShader="stoneTextureWhite",
                                                       color1 = [0, 0, 0], 
                                                       color2 = [1, 1, 1], 
                                                       grainSize = 0.07,
                                                       mixRatio = 0.6)
        
        # check for the forest shader
        if objectType == 'forest':
            # check for the main shader
            if ( self.shaderObject.checkExistShader("mainTreeColorBrown") == 0 ):
                self.shaderObject.createNormalShader(nameShader="mainTreeColorBrown", listColor = [0.16, 0.12, 0])
            
            # check for the leaf shader
            if ( self.shaderObject.checkExistShader("leafColorGreen") == 0 ):
                self.shaderObject.createRampShader(nameShader="leafColorGreen",
                                                   nameTextureShader="leafRampGreen", 
                                                   colorEntryList=[[0.1, 0.29, 0.11],[0.09, 0.47, 0.1],[0.44, 0.66, 0.35]], 
                                                   position=[0, 0.5, 1], 
                                                   typeTexture=8)
            if ( self.shaderObject.checkExistShader("leafColorYellow") == 0 ):
                self.shaderObject.createRampShader(nameShader="leafColorYellow",
                                                   nameTextureShader="leafRampYellow", 
                                                   colorEntryList=[[0.25, 0.42, 0.01],[0.69, 0.85, 0.28],[0.66, 0.75, 0.28]], 
                                                   position=[0, 0.5, 1], 
                                                   typeTexture=8)
    
    
    ##########################################   Position   ##########################################
    
    
    def selectedVertex(self):
        """ This method returns the selected vertex. """
        
        # if it wasn't selected a correct vertex then it will print a message
        if ( self.positionObject.findNumberSelectedVertex() == False ):
            self.messageObject.showWindowMessage( "Select a vertex to be imported!", "Ground" )
            return 0
        # else it returns the number of selected vertex
        else:
            x = self.positionObject.findNumberSelectedVertex()
            return int(x)
    
    
    ##########################################   Others Methods   ##########################################
    
    
    def procentCheck(self, variable1=0, variable2=0, variable3=0):
        """ This method checks if the sum of values is 100 and if not it will recalculate. """
        
        
        if variable1 == 100:
            return variable1, 0, 0
        
        if (variable1 + variable2 >= 100):
            variable2 = 100 - variable1
            return variable1, variable2, 0
        
        if (variable1 + variable2 + variable3 != 100):
            variable3 = 100 - variable1 - variable2
            return variable1, variable2, variable3
        else:
            return variable1, variable2, variable3
    
    def selectObject(self, selectObject):
        """ This method calls selectGroup() from GroupClass. """
        
        self.groupObject.selectGroup(selectObject)
    
    def deleteObject(self, nameObject):
        """ This method calls deleteGroup() from GroupClass. """
        
        self.groupObject.deleteGroup(nameObject)
        self.positionObject.makePositionAvailable(int(nameObject[12:]))
    
    def deleteAllObjectsNamed(self, nameObject):
        """ This method deletes all objects which their name contain a respective string. """
        
        response = self.messageObject.showYesNoMessage("Are you sure you want to delete existing meadows?", "Meadow")
        if response:
            meadowList = self.groupObject.checkExistingStringGroup(nameObject)
            for item in meadowList:
                self.deleteObject(item)
            return True
        return False












