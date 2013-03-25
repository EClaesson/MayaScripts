# Vibrate.py
# Maya 2013 - Python 2.6.4
# https://github.com/EClaesson/MayaScripts


# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib,imp,os;f=os.path.join(os.path.expanduser('~'),'PMI.py')
if not os.path.exists(f): urllib.urlretrieve('http://goo.gl/M0zWp',f);imp.load_source('pmi',f).installPyMEL()

import pymel.core as pm
import random, pickle

class State():
    _selectedObjects = set()
    _vibrationParams = {'start': 0, 'end': 1, 'X': 1.0, 'Y': 1.0, 'Z': 1.0, 'speed': 1.0}
    _wnd = None

    @staticmethod
    def setWindow(wnd):
        State._wnd = wnd

    @staticmethod
    def load():
        objIn = State._openLoadFile('objects')
        State._selectedObjects = pickle.load(objIn)
        objIn.close()

        vibIn = State._openLoadFile('vibration')
        State._vibrationParams = pickle.load(vibIn)
        vibIn.close()
        
        pm.intField(State._wnd.startField, edit=True, value=State._vibrationParams['start'])
        pm.intField(State._wnd.endField, edit=True, value=State._vibrationParams['end'])
        pm.floatField(State._wnd.xForceField, edit=True, value=State._vibrationParams['X'])
        pm.floatField(State._wnd.yForceField, edit=True, value=State._vibrationParams['Y'])
        pm.floatField(State._wnd.zForceField, edit=True, value=State._vibrationParams['Z'])
        pm.floatField(State._wnd.speedField, edit=True, value=State._vibrationParams['speed'])

        State.refresh()

    @staticmethod
    def dump():
        State.refresh()
        
        objOut = State._openDumpFile('objects')
        pickle.dump(State._selectedObjects, objOut)
        objOut.close()

        vibOut = State._openDumpFile('vibration')
        pickle.dump(State._vibrationParams, vibOut)
        vibOut.close()

    @staticmethod
    def refresh():
        State._vibrationParams['start'] = pm.intField(State._wnd.startField, query=True, value=True)
        State._vibrationParams['end'] = pm.intField(State._wnd.endField, query=True, value=True)
        State._vibrationParams['X'] = pm.floatField(State._wnd.xForceField, query=True, value=True)
        State._vibrationParams['Y'] = pm.floatField(State._wnd.yForceField, query=True, value=True)
        State._vibrationParams['Z'] = pm.floatField(State._wnd.zForceField, query=True, value=True)
        State._vibrationParams['speed'] = pm.floatField(State._wnd.speedField, query=True, value=True)
        
        pm.iconTextScrollList(State._wnd.selectedObjectsList, edit=True, removeAll=True)
        pm.iconTextScrollList(State._wnd.selectedObjectsList, edit=True, append=list(State._selectedObjects))

    @staticmethod
    def addSelectedObjectsFromScene(*args):
        State._selectedObjects = State._selectedObjects.union(map(lambda o: o.name(), pm.ls(long=True, selection=True)))
        State.refresh()
    
    @staticmethod
    def removeSelectedObjectInScene(*args):
        State._selectedObjects -= set(map(lambda o: o.name(), pm.ls(long=True, selection=True)))
        State.refresh()

    @staticmethod
    def removeSelectedObjectsInList(*args):
        State._selectedObjects -= set(pm.iconTextScrollList(State._wnd.selectedObjectsList, query=True, selectItem=True))
        State.refresh()

    @staticmethod
    def removeAllObjects(*args):
        State._selectedObjects.clear()
        State.refresh()
        
    @staticmethod
    def setVibration(*args):
        State.refresh()
        State.dump()
        
        for obj in State._selectedObjects:
            for axis in ['X', 'Y', 'Z']:
                pm.expression(name=State._makeExprName(obj, axis), string=State._makeExpr(obj, axis))
        
    @staticmethod
    def clearVibration(*args):
        for obj in State._selectedObjects:
            for axis in ['X', 'Y', 'Z']:
                pm.delete(State._makeExprName(obj, axis))
        
    @staticmethod
    def _getHomeDir():
        home = os.path.join(os.path.expanduser('~'), 'EClaessonMayaScripts', 'Vibrate')
        
        if not os.path.exists(home):
            os.makedirs(home)

        return home

    @staticmethod
    def _openFile(name, mode):
        return open(os.path.join(State._getHomeDir(), name + '.pkl'), mode + 'b')

    @staticmethod
    def _openDumpFile(name):
        return State._openFile(name, 'w')

    @staticmethod
    def _openLoadFile(name):
        return State._openFile(name, 'r')
        
    @staticmethod
    def _makeExprName(objName, axis):
        return 'VibExpr_' + objName + '_' + axis
        
    @staticmethod
    def _makeExpr(objName, axis):
        return 'float $q = (`currentTime -query`);\nif($q >= ' + str(State._vibrationParams['start']) + ' && $q <=' + str(State._vibrationParams['end']) + ')\n\t' + objName + '.rotate' + axis + '=sin(time*' + str(State._vibrationParams['speed']) + ')*' + str(State._vibrationParams[axis]) + ';'

class VibrateWindow():
    _size = (262, 500)
    
    def __init__(self):
        self._window    = pm.window(title='Vibrate', widthHeight=VibrateWindow._size, sizeable=False, maximizeButton=False)
        self._wrapper   = pm.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, VibrateWindow._size[0]), (2, VibrateWindow._size[0])], height=VibrateWindow._size[1])
        self._form      = pm.formLayout(parent=self._wrapper, height=470)
        self._execBtn   = pm.button(label='Set Vibration', parent=self._wrapper, command=State.setVibration)
        self._clearBtn  = pm.button(label='Clear Vibration', parent=self._wrapper, command=State.clearVibration)
        self._tabs      = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        self._subform   = pm.formLayout(self._form, edit=True, attachForm=((self._tabs, 'top', 0), (self._tabs, 'left', 0), (self._tabs, 'bottom', 0), (self._tabs, 'right', 0)))

        self._tabObjects = pm.rowColumnLayout(numberOfColumns=1)
        pm.button(label='Add selected from scene', command=State.addSelectedObjectsFromScene)
        pm.button(label='Remove selected in scene', command=State.removeSelectedObjectInScene)
        pm.button(label='Remove selected in list', command=State.removeSelectedObjectsInList)
        pm.button(label='Remove all', command=State.removeAllObjects)
        self.selectedObjectsList = pm.iconTextScrollList(allowMultiSelection=True, height=(VibrateWindow._size[1] - 150))
        pm.setParent('..')

        self._tabVibration = pm.rowColumnLayout(numberOfColumns=1)

        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 190)])
        pm.text(label='Start frame:')
        self.startField = pm.intField(minValue=-999999, maxValue=999999, step=1, value=0)
        pm.setParent('..')
        
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 190)])
        pm.text(label='End frame:')
        self.endField = pm.intField(minValue=-999999, maxValue=999999, step=1, value=1)
        pm.setParent('..')
        
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 190)])
        pm.text(label='X Force:')
        self.xForceField = pm.floatField(minValue=0.0, maxValue=999999.9, step=0.1, value=1.0)
        pm.setParent('..')
        
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 190)])
        pm.text(label='Y Force:')
        self.yForceField = pm.floatField(minValue=0.0, maxValue=999999.9, step=0.1, value=1.0)
        pm.setParent('..')
        
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 190)])
        pm.text(label='Z Force:')
        self.zForceField = pm.floatField(minValue=0.0, maxValue=999999.9, step=0.1, value=1.0)
        pm.setParent('..')
        
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 190)])
        pm.text(label='Speed:')
        self.speedField = pm.floatField(minValue=0.0, maxValue=999999.9, step=0.2, value=1.0)
        pm.setParent('..')
        
        pm.tabLayout(self._tabs, edit=True, tabLabel=((self._tabObjects, 'Objects'), (self._tabVibration, 'Vibration')))

    def show(self):
        pm.showWindow()

def openVibrate():
    wnd = VibrateWindow()
    wnd.show()
    State.setWindow(wnd)
    
    try:
        State.load()
    except:
        State.dump()

if __name__ == '__main__':
    openVibrate()