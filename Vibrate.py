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

import random

class State():
    _selectedObjects = set()
    _vibrationParams = {'force': 10, 'speed': 1.0, 'type': 'random'}
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

        State.refresh()

    @staticmethod
    def dump():
        objOut = State._openDumpFile('objects')
        pickle.dump(State._selectedObjects, objOut)
        objOut.close()

        vibOut = State._openDumpFile('vibration')
        pickle.dump(State._vibrationParams, vibOut)
        vibOut.close()

    @staticmethod
    def refresh():

        pm.select(clear=True)

        State.dump()

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
        pass
        
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

class VibrateWindow():
    def __init__(self):
        self._window    = pm.window(title='Vibrate', widthHeight=RandMatsWindow._size, sizeable=False, maximizeButton=False)
        self._wrapper   = pm.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, VibrateWindow._size[0]), (2, VibrateWindow._size[0])], height=VibrateWindow._size[1])
        self._form      = pm.formLayout(parent=self._wrapper, height=470)
        self._execBtn   = pm.button(label='Set Vibration', parent=self._wrapper, command=State.setVibration)
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
        
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 200)])
        pm.text(label='Force:')
        self._paramForce = pm.floatField(minValue=-999999.9, maxValue=999999.9, step=0.05)
        
        .rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 200)])
        pm.text(label='Force:')
        self.Speed = pm.floatField(minValue=-999999.9, maxValue=999999.9, step=0.05)
        pm.setParent('..')

        pm.tabLayout(self._tabs, edit=True, tabLabel=((self._tabObjects, 'Objects'), (self._tabVibration, 'Vibration')))

    def show(self):
        pm.showWindow()

def openVibrate():
    pass

if __name__ == '__main__':
    openVibrate()