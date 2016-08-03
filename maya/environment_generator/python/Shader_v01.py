""" 
#    @path        D:\Programare\Python\ProiectLicenta\trunk\apps\Plugin\app\python\PluginCreareMediu
#    @file        Shader_v01.py
#    @brief       This class creates shaders.


#    @author      remus_avram
#    @date        12.2013
"""



import maya.cmds as mc



class ShaderClass(object):
    
    def __init__(self):
        super(ShaderClass, self).__init__()
    
    
    def connectShader(self, selectedObject, nameShader):
        """ This method connects the shader to an object. """
        
        mc.select( selectedObject );
        mc.pickWalk( d='down' );
        selectedObjectList = mc.ls( sl=True );
        mc.sets( selectedObjectList[0], edit=True, forceElement=nameShader + 'SG' );
        mc.select( clear=True )
    
    def checkExistShader(self, shader):
        """ This method checks if the shader is already created. """
        
        shads = mc.ls( mat=True );
        if shader in shads:
            return 1
        return 0
    
    def createNormalShader(self, nameShader, listColor):
        """ This method creates a normal shader. """
        
        mc.shadingNode( 'lambert', asShader=True, name=nameShader );
        mc.sets( renderable=True, noSurfaceShader=True, empty=True, name= nameShader + 'SG' );
        mc.connectAttr( nameShader + '.outColor', nameShader + 'SG.surfaceShader', force=True );
        mc.setAttr( nameShader + ".color", listColor[0], listColor[1], listColor[2], type='double3' );
        mc.select( clear=True )
    
    def createMountainShader(self, nameShader, nameTextureShader, listSnowColor, listRockColor, amptitude):
        """ This method creates a Mountain shader. """
        
        mc.shadingNode( 'lambert', asShader=True, name=nameShader );
        mc.shadingNode( 'mountain', asTexture=True, name=nameTextureShader );
        mc.sets ( renderable=True, noSurfaceShader=True, empty=True, name=nameShader + "SG" ); 
        mc.connectAttr( nameShader + '.outColor', nameShader + 'SG.surfaceShader', force=True) ;
        mc.connectAttr( nameTextureShader + '.outColor', nameShader + '.color' )
        
        mc.setAttr( nameTextureShader + ".snowColor", listSnowColor[0], listSnowColor[1], listSnowColor[2], type='double3' );
        mc.setAttr( nameTextureShader + ".rockColor", listRockColor[0], listRockColor[1], listRockColor[2], type='double3' );
        mc.setAttr( nameTextureShader + ".amplitude", amptitude )
        mc.select( clear=True )
    
    def createRampShader(self, nameShader, nameTextureShader, colorEntryList, position, typeTexture):
        """ This method creates a Ramp shader. """
        
        mc.shadingNode( 'lambert', asShader=True, name=nameShader );
        mc.shadingNode( 'ramp', asTexture=True, name=nameTextureShader );
        mc.sets( renderable=True, noSurfaceShader=True, empty=True, name= nameShader + 'SG' );
        mc.connectAttr( nameShader + '.outColor', nameShader + 'SG.surfaceShader', force=True );
        mc.connectAttr( nameTextureShader + '.outColor', nameShader + '.color', force=True );
        
        mc.setAttr( nameTextureShader + ".colorEntryList[1].color", colorEntryList[0][0], colorEntryList[0][1], colorEntryList[0][2], type="double3" );
        mc.setAttr( nameTextureShader + ".colorEntryList[1].position", position[0] );
        
        mc.setAttr( nameTextureShader + ".colorEntryList[2].color", colorEntryList[1][0], colorEntryList[1][1], colorEntryList[1][2], type="double3" );
        mc.setAttr( nameTextureShader + ".colorEntryList[2].position", position[1] );
        
        mc.setAttr( nameTextureShader + ".colorEntryList[3].color", colorEntryList[2][0], colorEntryList[2][1], colorEntryList[2][2], type="double3" );
        mc.setAttr( nameTextureShader + ".colorEntryList[3].position", position[2] ); 
        
        mc.setAttr( nameTextureShader + ".type", typeTexture )
        mc.select( clear=True )
    
    def createRockShader(self, nameShader, nameTextureShader, color1, color2, grainSize, mixRatio):
        """ This method creates a Rock shader. """
    
        mc.shadingNode( 'lambert', asShader=True, name=nameShader )
        mc.shadingNode( 'rock', asTexture=True, name=nameTextureShader )
        mc.sets ( renderable=True, noSurfaceShader=True, empty=True, name=nameShader + "SG" )
        mc.connectAttr( nameShader + '.outColor', nameShader + 'SG.surfaceShader', force=True) ;
        mc.connectAttr( nameTextureShader + '.outColor', nameShader + '.color' )
        
        mc.setAttr( nameTextureShader + ".color1", color1[0], color1[1], color1[2], type='double3' );
        mc.setAttr( nameTextureShader + ".color2", color2[0], color2[1], color2[2], type='double3' );
        mc.setAttr( nameTextureShader + ".grainSize", grainSize )
        mc.setAttr( nameTextureShader + ".mixRatio", mixRatio )
        mc.select( clear=True )

