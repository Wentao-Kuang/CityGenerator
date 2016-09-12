# -*- coding: utf-8 -*-
"""
Created on Tue Sep 01 00:03:39 2015

Comp409 assignment2 part1 city generator

@author: Wentao Kuang
studentId:300314565

"""
import sys
import maya.cmds as cmds
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender
import random



kPluginCmdName = "cityG"
Render_worker = OpenMayaRender.MHardwareRenderer.theRenderer()
GL_worker = Render_worker.glFunctionTable()

class City_Generator(OpenMayaMPx.MPxCommand):
    
    '''Initialize.'''  
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)        
        #self.createWindow()
        
    '''After loaded the pulgin and excute command of this pulgin will excute this function'''    
    def doIt(self,argList):
        self.createWindow()
        
    # I like to keep all the iportant UI elements in a dictionary.
    UIElements = {}    
    
    '''This function creates the window.''' 
    def createWindow(self):       
        self.UIElements['window'] = cmds.window()
        self.UIElements['main_layout'] = cmds.columnLayout( adjustableColumn=True )
        self.UIElements['widthtxt'] = cmds.text(label=('city width'))
        self.UIElements['width'] = cmds.textField('width',tx='500',fn='fixedWidthFont',bgc=(0,0,0))
        self.UIElements['depthtxt'] = cmds.text(label=('city depth'))
        self.UIElements['depth'] = cmds.textField('depth',tx='500',fn='fixedWidthFont',bgc=(0,0,0))
        self.UIElements['maxBuildingHeighttxt'] = cmds.text(label=('Maximum Building Height'))
        self.UIElements['maxBuildingHeight'] = cmds.textField('maxBuildingHeight',tx='60',fn='fixedWidthFont',bgc=(0,0,0))
        self.UIElements['buildingGaptxt'] = cmds.text(label=('buildingGap'))
        self.UIElements['buildingGap'] = cmds.textField('buildingGap',tx='3',fn='fixedWidthFont',bgc=(0,0,0))
        self.UIElements['streetWidthtxt'] = cmds.text(label=('streetWidth'))
        self.UIElements['streetWidth'] = cmds.textField('streetWidth',tx='30',fn='fixedWidthFont',bgc=(0,0,0))
        self.UIElements['regionWidthtxt'] = cmds.text(label=('region width'))
        self.UIElements['regionWidth'] = cmds.textField('regionWidth',tx='100',fn='fixedWidthFont',bgc=(0,0,0))   
        self.UIElements['regionDepthtxt'] = cmds.text(label=('region Depth'))
        self.UIElements['regionDepth'] = cmds.textField('regionDepth',tx='100',fn='fixedWidthFont',bgc=(0,0,0))
        self.UIElements['car'] = cmds.checkBox(label="add cars", value=True)
        self.UIElements['tree'] = cmds.checkBox(label="add trees", value=True)        
        self.UIElements['buildCity'] =cmds.button(label=('buildCity'),command=self.buildCityListener)
        cmds.showWindow( self.UIElements['window'] )


    '''
    This function listen the button buildcity, 

    '''   
    def buildCityListener(self ,*args):
        cityWidth=int(cmds.textField('width',q=True,tx=True))
        cityDepth=int(cmds.textField('depth',q=True,tx=True))
        maxBuildingHeight=int(cmds.textField('maxBuildingHeight',q=True,tx=True))
        buildingGap=int(cmds.textField('buildingGap',q=True,tx=True))
        streetWidth=int(cmds.textField('streetWidth',q=True,tx=True))
        regionWidth=int(cmds.textField('regionWidth',q=True,tx=True))
        regionDepth=int(cmds.textField('regionDepth',q=True,tx=True))
        car=cmds.checkBox(self.UIElements['car'],q=True,v=True)
        tree=cmds.checkBox(self.UIElements['tree'],q=True,v=True)
        self.createCity(cityWidth, cityDepth, maxBuildingHeight, buildingGap,streetWidth ,regionWidth,regionDepth,car,tree)
        
    #Counters
    buildingCounter=0
    treeCounter=0
    carCounter=0

    '''
    function to create city
    '''
    def createCity(self,cityWidth, cityDepth, maxBuildingHeight, buildingGap,streetWidth,regionWidth,regionDepth,car,tree):
        #create a ground plane
        cmds.polyPlane(w=(cityWidth+streetWidth), h=(cityDepth+streetWidth), n="ground")
        print('create groud')
        cmds.move((cityWidth+streetWidth) / 2 , 0, (cityDepth+streetWidth) / 2)
        #define counters for the region space        
        regionW=0
        regionD=0
        
        #generate the whole city with many regions
        while(regionW<cityWidth):
            regionD=0
            #generate a region with some buildings
            while(regionD<cityDepth):
                self.createRegion(regionW,regionD,regionWidth,regionDepth,buildingGap,maxBuildingHeight)
                regionD=(regionD+regionDepth+streetWidth)
                self.createStreetRow(regionW,regionD,regionWidth,regionDepth,streetWidth,car,tree)
                self.createStreetColumn(regionW,regionD,regionWidth,regionDepth,streetWidth,car,tree)
            regionW=(regionW+regionWidth+streetWidth)
        print("finished")
            
    '''
    function to create street with cars and trees on xrey
    '''     
    def createStreetRow(self,regionW,regionD,regionWidth,regionDepth,streetWidth,car,tree):
        cmds.polyPlane(w=regionDepth,h=streetWidth,n="streetRow")
        cmds.move(regionW+(regionDepth/2),1,regionD-(streetWidth/2))
        treeDepthCounter=regionDepth
        treeWidthCounter=regionW
        carDepthCounter=regionDepth
        carWidthCounter=regionW
        if(tree):
            #generate trees on the street
            treeGap=random.randrange(10,30)
            while((treeDepthCounter-(treeGap/2))>0):          
                treeName=self.createTree()
                print("create "+treeName)
                self.moveTree(treeName,treeWidthCounter+(treeGap/2),1.5,regionD)
                treeName=self.createTree()
                print("create "+treeName)
                self.moveTree(treeName,treeWidthCounter+(treeGap/2),1.5,regionD-streetWidth)
                treeWidthCounter=treeWidthCounter+treeGap
                treeDepthCounter=treeDepthCounter-treeGap
        if(car):
            #generate cars on the street
            while(carDepthCounter>0):
                carGap=random.randrange(5,40)
                carName=self.createCarRow()
                print("create "+carName)
                self.moveCar(carName,carWidthCounter+(carGap/2),1.5,regionD-(streetWidth/4))
                carName=self.createCarRow()
                print("create "+carName)
                self.moveCar(carName,carWidthCounter+(random.randrange(5,carGap+1)/2),1.5,regionD-(3*streetWidth/4))
                carWidthCounter=carWidthCounter+carGap
                carDepthCounter=carDepthCounter-carGap            
            
    '''
    function to create street with cars and trees on zrey
    '''                             
    def createStreetColumn(self,regionW,regionD,regionWidth,regionDepth,streetWidth,car,tree):
        cmds.polyPlane(w=streetWidth,h=(regionDepth+streetWidth),n="streetColumn")
        cmds.move(regionW+(streetWidth/2)+regionWidth,1,regionD-((regionDepth+streetWidth)/2))
        treeDepthCounter=regionDepth
        treeWidthCounter=regionW
        carDepthCounter=regionDepth
        if(tree):
            #generate trees with a random gap
            treeGap=random.randrange(10,30)
            while((treeDepthCounter-(treeGap/2))>0):
                treeName=self.createTree()
                print("create "+treeName)
                self.moveTree(treeName,treeWidthCounter+regionWidth,1.5,regionD-treeDepthCounter-streetWidth+(treeGap/2))           
                treeName=self.createTree()
                print("create "+treeName)
                self.moveTree(treeName,treeWidthCounter+regionWidth+streetWidth,1.5,regionD-treeDepthCounter-streetWidth+(treeGap/2))
                treeDepthCounter=treeDepthCounter-treeGap
        if(car):
            #generate cars on the street
            while(carDepthCounter>0):
                carGap=random.randrange(10,40)
                carName=self.createCarColumn()
                print("create "+carName)
                self.moveCar(carName,regionW+regionWidth+(streetWidth/4),1.5,regionD-carDepthCounter-streetWidth+(carGap/2))
                carName=self.createCarColumn()
                print("create "+carName)
                self.moveCar(carName,regionW+regionWidth+(3*streetWidth/4),1.5,regionD-carDepthCounter-streetWidth+(random.randrange(10,carGap+1)/2))
                carDepthCounter=carDepthCounter-carGap         
            
        
    '''
    generate a region with buildings
    '''
    def createRegion(self,regionW,regionD,regionWidth,regionDepth,buildingGap,maxBuildingHeight):
        # max and min size of buildings 
        buildingMaxWidth = 20
        buildingMaxDepth = 20
        buildingMinWidth = 5
        buildingMinDepth = 5
        buildingMinHeight = 15
        regionD=regionD+10
        regionW=regionW+10
        regionDepthA=regionDepth
        regionDA=regionD
        #make sure the region have enough space for a building
        while(regionWidth>20):
            regionDepth=regionDepthA
            regionD=regionDA
            while(regionDepth>20):
                #generate some radom value for the building size and type
                height=random.randrange(buildingMinHeight, maxBuildingHeight)
                width=random.randrange(buildingMinWidth, buildingMaxWidth)
                depth=random.randrange(buildingMinDepth, buildingMaxDepth)
                buildingType=random.randrange(0,4)
                buildingName=self.createBuildings(width,depth,height,buildingType)
                print("create "+buildingName)
                self.moveBuilding(buildingName,regionW+(width/2),(height/2)+1, regionD+(depth/2))
                regionDepth=(regionDepth-buildingGap-20)
                regionD=(regionD+buildingGap+20)
            regionWidth=(regionWidth-buildingGap-20)
            regionW=(regionW+buildingGap+20)
   
    '''
    funtion to create ugly trees
    '''
    def createTree(self):
        treeName = "Tree_"+str(self.treeCounter)
        cmds.polyCube(w=1, d=1, h=3, n=treeName)			
        cmds.polyExtrudeFacet(str(treeName)+".f[1]", kft = False, ls = (4, 4, 0))
        cmds.polyExtrudeFacet(str(treeName)+".f[1]", kft = False, ltz = 4)
        self.treeCounter=self.treeCounter+1
        return treeName

    '''
    function to move the tree
    '''
    def moveTree(self,treeName, x, y, z):
        cmds.select(treeName)
        cmds.move(x, y, z)
        cmds.select( cl = True)
     
    '''
    function to create ugly cars
    '''
    def createCarRow(self,):
        carName = "Car_"+str(self.carCounter)
        cmds.polyCube(w=4, d=2, h=1, n=carName)			
        cmds.polyExtrudeFacet(str(carName)+".f[1]", kft = False, ls = (0.8, 0.5, 0))
        cmds.polyExtrudeFacet(str(carName)+".f[1]", kft = False, ltz = 0.8)
        self.carCounter=self.carCounter+1
        return carName
    def createCarColumn(self,):
        carName = "Car_"+str(self.carCounter)
        cmds.polyCube(w=2, d=4, h=1, n=carName)	
        cmds.polyExtrudeFacet(str(carName)+".f[1]", kft = False, ls = (0.8, 0.5, 0))
        cmds.polyExtrudeFacet(str(carName)+".f[1]", kft = False, ltz = 0.8)
        self.carCounter=self.carCounter+1
        return carName

    '''
    function to move the car
    '''
    def moveCar(self,carName, x, y, z):
        cmds.select(carName)
        cmds.move(x, y, z)
        cmds.select( cl = True)    
    
    '''
    function to create some defined buildings
    '''
    def createBuildings(self,width,depth,height,buildingType):
        buildingName = "Building_" + str(self.buildingCounter)	
        #building type number 1, just a block building.
        if(buildingType == 0):
            cmds.polyCube(w=width, d=depth, h=height, n=str(buildingName))
			
        #building type number 2, block building with one or two extra block tops.	
        elif(buildingType == 1):		
		cmds.polyCube(w=width, d=depth, h=height, n=str(buildingName))			
		for i in range(0, random.randrange(1,3)):
			cmds.polyExtrudeFacet(str(buildingName) + ".f[1]", kft = False, ls = (0.8, 0.8, 0))
			cmds.polyExtrudeFacet(str(buildingName) + ".f[1]", kft = False, ltz = 20)	
			
        #building type number 3, block building with windows.	
        elif(buildingType == 2):
            cmds.polyCube(w=width, d=depth, h=height, sx=10, sy=10, sz=10, n=str(buildingName))						
            sides = []
            #select everything except the top and bottom of the building
            for i in range(0, 8):
                if(i != 1 and i != 3):
                    sides.append(str(buildingName) + ".f[" + str(i*100) + ":" + str((100*(i+1)) - 1) + "]")
            #extrude the faces to create windows
            cmds.polyExtrudeFacet(sides[0], sides[1], sides[2], sides[3], sides[4], sides[5], kft = False, ls = (0.8, 0.8, 0))
            windows = cmds.ls(sl = True)
            cmds.polyExtrudeFacet(windows[1], windows[2], windows[3], kft = False, ltz = -0.2)
            cmds.select(str(buildingName))
   
        #building type number 4, block building with windows.
        else:
            cmds.polyCylinder(r=width/2,sx=10, sy=15, sz=5, h=height, n=str(buildingName))						
            sides = []
            #select everything except the top and bottom of the building
            cmds.polyExtrudeFacet(str(buildingName)+ ".f[40:189]", kft = False, ls = (0.8, 0.8, 0))
            cmds.polyExtrudeFacet(str(buildingName)+ ".f[40:189]", kft = False, ltz = -0.1)
            cmds.select(str(buildingName))
        self.buildingCounter=self.buildingCounter+1
        return buildingName
      
    '''
    function to move the building
    '''
    def moveBuilding(self,buildingName, x, y, z):
        cmds.select(buildingName)
        cmds.move(x, y, z)
        cmds.select( cl = True)
    
# End of class

'''Creator'''
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( City_Generator() )
    
'''Initialize the script plug-in'''
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

'''Uninitialize the script plug-in'''
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )

demo = City_Generator()
demo.createWindow()