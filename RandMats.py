# RandMats
# Maya 2013 - Python 2.6.4
# https://github.com/EClaesson/RandMats

import maya.cmds as cmds
import random

objSelWnd = None
matSelWnd = None

selObjs = None
selMats = None

cmds.select(clear=True)
openObjSelWnd()

def _str(obj):
    return str(obj).replace("u'", "'").replace(": ", "->").replace("'", "").replace("|", "")

def objectsSelectedButton(*args):
    global selObjs
    selObjs = cmds.ls(long=True, selection=True)
    print "Selected objects: " + _str(selObjs)
    cmds.select(clear=True)
    cmds.toggleWindowVisibility(objSelWnd)
    openMatSelWnd()

def materialSelectedButton(*args):
    global selMats
    selMats = cmds.ls(long=True, selection=True)
    print "Selected materials: " + _str(selMats)
    cmds.select(clear=True)
    cmds.toggleWindowVisibility(matSelWnd)
    assignMaterials()

def openMatSelWnd():
    global matSelWnd
    matSelWnd = cmds.window(title="RandMats", sizeable=False, minimizeButton=True, maximizeButton=False)
    cmds.flowLayout()
    cmds.button("     Select your materials and click here     ", command=materialSelectedButton)
    cmds.showWindow(matSelWnd)

def openObjSelWnd():
    global objSelWnd
    objSelWnd = cmds.window(title="RandMats", sizeable=False, minimizeButton=True, maximizeButton=False)
    cmds.flowLayout()
    cmds.button("     Select your objects and click here     ", command=objectsSelectedButton)
    cmds.showWindow(objSelWnd)
    
def assignMaterials():
    assignResult = {}
    
    for obj in selObjs:
        cmds.select(obj)
        mat = random.choice(selMats)
        assignResult[obj] = mat
        cmds.hyperShade(assign=mat)
        
    print "RandMats result: " + _str(assignResult)