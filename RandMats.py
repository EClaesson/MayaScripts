# RandMats
# Maya 2013 - Python 2.6.4
# https://github.com/EClaesson/RandMats

import maya.cmds as cmds
import random

selectedObjects = set()
selectedMaterials = []

selectedObjectsList = None
selectedMaterialsList = None

rAlgo = ''
rN = rA = rB = rL = rM = rS = rK = None

randomAlgorithms = None

def updateSelectedObjects():
    global selectedObjects
    cmds.iconTextScrollList(selectedObjectsList, edit=True, removeAll=True)
    cmds.iconTextScrollList(selectedObjectsList, edit=True, append=list(selectedObjects))
    cmds.select(clear=True)
    
def updateSelectedMaterials():
    global selectedMaterials
    cmds.iconTextScrollList(selectedMaterialsList, edit=True, removeAll=True)
    cmds.iconTextScrollList(selectedMaterialsList, edit=True, append=selectedMaterials)
    cmds.ls(clear=True)

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
    selectedMAterials = selectedMAterials.union(cmds.ls(long=True, selection=True))
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
    field = cmds.floatField(minValue=-999999.9, maxValue=999999.9, step=0.05)
    cmds.setParent('..')
    return field
    
def _intRandParam(name):
    cmds.rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 200)])
    cmds.text(label=name + ':')
    field = cmds.intField(minValue=-999999, maxValue=999999, step=1)
    cmds.setParent('..')
    return field

def enableRandParam(param):
    cmds.control(param, edit=True, enable=True)

def disableRandParam(param):
    cmds.control(param, edit=True, enable=False)

def randomAlgoChanged(*args):
    global rAlgo
    rAlgo = cmds.iconTextScrollList(randomAlgorithms, query=True, selectItem=True)[0]

    if rAlgo in ['Random', 'Linear', 'Single Material', 'Reversed Linear', 'Linear Shuffle', 'Repeated Linear Shuffle', 'Uniform']:
        for p in [rN, rA, rB, rL, rM, rS, rK]:
            disableRandParam(p)
    elif rAlgo == 'N Materials':
        for p in [rA, rB, rL, rM, rS, rK]:
            disableRandParam(p)
        enableRandParam(rN)
    elif rAlgo in ['BetaVariate', 'GammaVariate', 'WeiBullVariate']:
        for p in [rN, rL, rM, rS, rK]:
            disableRandParam(p)
        for p in [rA, rB]:
            enableRandParam(p)
    elif rAlgo == 'ExpoVariate':
        for p in [rN, rA, rB, rM, rS, rK]:
            disableRandParam(p)
        enableRandParam(rL)
    elif rAlgo in ['Gaussian', 'LogNormVariate', 'NormalVariate']:
        for p in [rN, rA, rB, rL, rK]:
            disableRandParam(p)
        for p in [rM, rS]:
            enableRandParam(p)
    elif rAlgo == 'VonMisesVariate':
        for p in [rN, rA, rB, rL, rS]:
            disableRandParam(p)
        for p in [rM, rK]:
            enableRandParam(p)
    elif rAlgo == 'ParetoVariate':
        for p in [rN, rB, rL, rM, rS, rK]:
            disableRandParam(p)
        enableRandParam(nA)

def setMaterials(*args):
    for obj in selectedObjects:
        cmds.select(obj)
        # TODO: Implement rand algos
        mat = random.choice(selectedMaterials)
        cmds.hyperShade(assign=mat)

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
    'Repeated Linear Shuffle', 'Triangular', 'BetaVariate', 'ExpoVariate', 'GammaVariate', 'Gaussian',
    'LogNormVariate', 'NormalVariate', 'VonMisesVariate', 'ParetoVariate', 'WeiBullVariate'],
    selectCommand=randomAlgoChanged)

rN = _intRandParam('N')
rA = _randParam('Alpha')
rB = _randParam('Beta')
rL = _randParam('Lambda')
rM = _randParam('Mu')
rS = _randParam('Sigma')
rK = _randParam('Kappa')
cmds.setParent('..')

cmds.tabLayout(tabs, edit=True, tabLabel=((childObjs, 'Objects'), (childMats, 'Materials'), (childPats, 'Pattern')))
cmds.showWindow()