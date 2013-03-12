# RandMats
# Maya 2013 - Python 2.6.4
# https://github.com/EClaesson/RandMats

import maya.cmds as cmds
import random

selectedObjects = set()
selectedMaterials = set()

selectedObjectsList = None
selectedMaterialsList = None

rAlgo = ''
rN = rA = rB = rL = rM = rS = rK = None

randSel = 0
randSelArr = []

randomAlgorithms = None

def updateSelectedObjects():
    global selectedObjects
    cmds.iconTextScrollList(selectedObjectsList, edit=True, removeAll=True)
    cmds.iconTextScrollList(selectedObjectsList, edit=True, append=list(selectedObjects))
    cmds.select(clear=True)
    
def updateSelectedMaterials():
    global selectedMaterials
    cmds.iconTextScrollList(selectedMaterialsList, edit=True, removeAll=True)
    cmds.iconTextScrollList(selectedMaterialsList, edit=True, append=list(selectedMaterials))
    cmds.select(clear=True)

def addSelectedObjectsFromScene(*args):
    global selectedObjects
    selectedObjects = selectedObjects.union(cmds.ls(long=True, selection=True))
    updateSelectedObjects()
    
def removeSelectedObjectInScene(*args):
    global selectedObjects
    selectedObjects -= set(cmds.ls(long=True, selection=True))
    updateSelectedObjects()

def removeSelectedObjectsInList(*args):
    global selectedObjects
    global selectedObjectsList
    selectedObjects -= set(cmds.iconTextScrollList(selectedObjectsList, query=True, selectItem=True))
    updateSelectedObjects()

def removeAllObjects(*args):
    global selectedObjects
    selectedObjects.clear()
    updateSelectedObjects()

def addSelectedMaterialsFromHS(*args):
    global selectedMaterials
    selectedMaterials = selectedMaterials.union(cmds.ls(long=True, selection=True))
    updateSelectedMaterials()
    
def removeSelectedMaterialsInHS(*args):
    global selectedMaterials
    selectedMaterials -= set(cmds.ls(long=True, selection=True))
    updateSelectedMaterials()

def removeSelectedMaterialsInList(*args):
    global selectedMaterials
    global selectedMaterialsList
    selectedMaterials -= set(cmds.iconTextScrollList(selectedMaterialsList, query=True, selectItem=True))
    updateSelectedMaterials()

def removeAllMaterials(*args):
    global selectedMaterials
    selectedMaterials.clear()
    updateSelectedMaterials()

def _randParam(name):
    cmds.rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 200)])
    cmds.text(label=name + ':')
    field = cmds.floatField(minValue=-999999.9, maxValue=999999.9, step=0.05, enable=False)
    cmds.setParent('..')
    return field
    
def _intRandParam(name):
    cmds.rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 200)])
    cmds.text(label=name + ':')
    field = cmds.intField(minValue=-999999, maxValue=999999, step=1, enable=False)
    cmds.setParent('..')
    return field
    
def randParamVal(param):
    return cmds.intField(param, query=True, value=True)
    
def intRandParamVal(param):
    return cmds.floatField(param, query=True, value=True)

def enableRandParam(param):
    cmds.control(param, edit=True, enable=True)

def disableRandParam(param):
    cmds.control(param, edit=True, enable=False)

def setEnabledRandParams(disabled, enabled):
    for p in enabled:
        enableRandParam(p)
    for p in disabled:
        disableRandParam(p)

def randomAlgoChanged(*args):
    global rAlgo
    rAlgo = cmds.iconTextScrollList(randomAlgorithms, query=True, selectItem=True)[0]

    if rAlgo in ['Random', 'Linear', 'Single Material', 'Reversed Linear', 'Linear Shuffle', 'Repeated Linear Shuffle', 'Uniform']:
        setEnabledRandParams([rN, rA, rB, rL, rM, rS, rK], [])
    elif rAlgo == 'N Materials':
        setEnabledRandParams([rA, rB, rL, rM, rS, rK], [rN])

def randNextMaterial():
    global randSel
    global randSellArr
    
    last = len(selectedMaterials) - 1
    i = 0
    
    if rAlgo == 'Random':
        i = random.randint(0, last)
    elif rAlgo == 'Linear':
        if randSel == last or randSel == -1:
            randSel = 0
        else:
            randSel += 1
            
        i = randSel
    elif rAlgo == 'Single Material':
        if randSel == -1:
            randSel = random.randint(0, last)
            
        i = randSel
    elif rAlgo == 'N Materials':
        if randSel == -1:
            for i in range(0, intRandParam(rN)):
                r = -1
                while r == -1 or (r in randSelArr):
                    r = random.randint(0, last)

                randSelArr.append(random.randint(0, last))
                
        i = random.choice(randSelArr)
    elif rAlgo == 'Reversed Linear':
        if randSel == 0 or randSel == -1:
            randSel = last
        else: 
            randSel -= 1
            
        i = randSel
        
    elif rAlgo == 'Uniform':
        i = random.uniform(0, last)
    elif rAlgo == 'Linear Shuffle':
        if randSelArr == []:
            randSelArr = range(last + 1)
            random.shuffle(randSelArr)
            
        i = randSelArr.pop()
    elif rAlgo == 'Repeated Linear Shuffle':
        if randSelArr == []:
            randSelArr = range(last + 1)
            random.shuffle(randSelArr)
            
        if randSel == last:
            randSel = 0
        else:
            randsel += 1
            
        i = randSel
        
    return list(selectedMaterials)[i]

def setMaterials(*args):
    global randSel
    global randSelArr
    
    randSel = -1
    randSelArr = []
    
    for obj in selectedObjects:
        cmds.select(obj)
        cmds.hyperShade(assign=randNextMaterial())

cmds.window(title='RandMats', widthHeight=(262, 500), sizeable=False, maximizeButton=False)
wrapper = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, 262), (2, 262)], height=500)
form = cmds.formLayout(parent=wrapper, height=470)
execBtn = cmds.button(label='Set Materials', parent=wrapper, command=setMaterials)
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout(form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))

childObjs = cmds.rowColumnLayout(numberOfColumns=1)
cmds.button(label='Add selected from scene', command=addSelectedObjectsFromScene)
cmds.button(label='Remove selected in scene', command=removeSelectedObjectInScene)
cmds.button(label='Remove selected in list', command=removeSelectedObjectsInList)
cmds.button(label='Remove all', command=removeAllObjects)
selectedObjectsList = cmds.iconTextScrollList(allowMultiSelection=True, height=350)
cmds.setParent('..')

childMats = cmds.rowColumnLayout(numberOfColumns=1)
cmds.button(label='Add selected from HyperShade', command=addSelectedMaterialsFromHS)
cmds.button(label='Remove selected in HyperShade', command=removeSelectedMaterialsInHS)
cmds.button(label='Remove selected in list', command=removeSelectedMaterialsInList)
cmds.button(label='Remove all', command=removeAllMaterials)
selectedMaterialsList = cmds.iconTextScrollList(allowMultiSelection=True, height=350)
cmds.setParent('..')

childPats = cmds.rowColumnLayout(numberOfColumns=1)
randomAlgorithms = cmds.iconTextScrollList(allowMultiSelection=False, height=200, append=[
    'Random', 'Linear', 'Single Material', 'N Materials', 'Reversed Linear', 'Uniform', 'Linear Shuffle',
    'Repeated Linear Shuffle'],
    selectCommand=randomAlgoChanged)

rN = _intRandParam('N')
# rA = _randParam('Alpha')
# rB = _randParam('Beta')
# rL = _randParam('Lambda')
# rM = _randParam('Mu')
# rS = _randParam('Sigma')
# rK = _randParam('Kappa')
cmds.setParent('..')

cmds.tabLayout(tabs, edit=True, tabLabel=((childObjs, 'Objects'), (childMats, 'Materials'), (childPats, 'Pattern')))
cmds.showWindow()