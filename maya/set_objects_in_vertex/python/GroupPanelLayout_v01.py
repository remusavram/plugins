""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        GroupPanelLayout_v01.py
#    @brief       This class works with groups. (creates, renames, deletes)


#    @author      remus_avram
#    @date        12.2013
"""



import maya.cmds as mc
import maya.mel



class GroupClass(object):
    
    def __init__(self):
        super(GroupClass, self).__init__()
    
    
    def createGroup(self, groupName):
        """ This method creates a group. """
        
        mc.select( clear=True )
        maya.mel.eval('doGroup 0 1 1')
        mc.rename ('null1', groupName)
        mc.select( clear=True )
    
    def renameObject(self, object, objectName):
        """ This method renames a group. """
        
        mc.select( object )
        newName = mc.rename( objectName )
        mc.select( clear=True )
        return newName
    
    def addInGroup(self, groupName, object):
        """ This method adds an object in a group. """
        
        mc.parent( object, groupName )
        mc.select( clear=True )
    
    def checkExistingGroup(self, groupName):
        """ This method checks if the group exists. """
        
        groupList = mc.ls()
        if groupName in groupList:
            return True
        return False
    
    def checkExistingStringGroup(self, stringName):
        """ This method checks if there are groups which contain in their names a respective string
        and return the list with this groups. """
        
        tempList = []
        
        groupList = mc.ls()
        for tempItem in groupList:
            if tempItem[:len(stringName)] == stringName:
                tempList.append(tempItem)
        return tempList
    
    def findGroupNumbers(self, groupName):
        """ This method finds numbers of the group. """
        
        tempList = []
        lastNumberList = []
        
        tempList = self.checkExistingStringGroup(groupName)
        
        for tempItem in tempList:
            if tempItem[len(groupName)+1:].isdigit():
                lastNumberList.append(tempItem[len(groupName)+1:])
        return lastNumberList
    
    def findLastGroupNumber(self, groupName):
        """ This method finds the last number of group. """
        
        lastNumberList = []
        lastNumberList = self.findGroupNumbers(groupName)
        
        biggestNumber = 0
        for i in lastNumberList:
            if biggestNumber < int(i):
                biggestNumber = int(i)
        return biggestNumber
    
    def combineObjects(self, listOfObjects):
        """ This method combines the objects from a list. """
        
        for i in listOfObjects:
            mc.select( i, add=True )
        combinedList = mc.polyUnite()
        
        # delete history
        maya.mel.eval( "DeleteHistory" )
        
        return combinedList
    
    def deleteGroup(self, nameGroup):
        """ This method deletes a group. """
        
        mc.delete(nameGroup)
    
    def selectGroup(self, groupName):
        """ This method selects the group with respective name. """
        
        mc.select(groupName)

    def selectObjectsFromGroup(self, groupName):
        """ This method selects the objects from the group with respective name. """
        
        for object in groupName:
            mc.select(object,  add=True)

    def returnListObjectsFromGroup(self, groupName):
        """ This method returns a list with all objects in a respective group. """

        listObjects = []
        for object in groupName:
            listObjects.append(object)

        return listObjects

    
    def duplicateGroup(self, groupName):
        """ This method duplicates a group. """
        
        mc.select( groupName )
        newGroupName = mc.duplicate ( rr=True )
        mc.select( clear=True )
        
        return newGroupName



