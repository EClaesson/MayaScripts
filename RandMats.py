# RandMats.py
# Maya 2013 - Python 2.6.4
# https://github.com/EClaesson/MayaScripts


# Copyright 2013 Emanuel Claesson

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

class PatternManager():
    _patterns = []

    @staticmethod
    def registerPattern(pattern):
        PatternManager._patterns.append(pattern)

    @staticmethod
    def getPattern(patternName):
        for pat in PatternManager._patterns:
            if pat.name == patternName:
                return pat

        return None

    @staticmethod
    def getAllPatterns():
        return PatternManager._patterns

    @staticmethod
    def getAllPatternNames():
        return map((lambda pat: pat.name), PatternManager._patterns)


class Pattern():
    rNum = -1
    rArr = []


class RandomPattern():
    def __init__(self):
        self.name = 'Random'
        self.params = []

    def getNext(self, last):
        return random.randint(0, last)


class LinearPattern():
    def __init__(self):
        self.name = 'Linear'
        self.params = []

    def getNext(self, last):
        if Pattern.rNum == last or Pattern.rNum == -1:
            Pattern.rNum = 0
        else:
            Pattern.rNum += 1
            
        return Pattern.rNum


class SingleMaterialPattern():
    def __init__(self):
        self.name = 'Single Material'
        self.params = []

    def getNext(self, last):
        if Pattern.rNum == -1:
            Pattern.rNum = random.randint(0, last)
            
        return Pattern.rNum


class NMaterialsPattern():
    def __init__(self):
        self.name = 'N Materials'
        self.params = ['N']

    def getNext(self, last):
        if Pattern.rNum == -1:
            for i in range(0, intRandParamVal(rN)):
                r = -1
                while r == -1 or (r in Pattern.rArr):
                    r = random.randint(0, last)

                randSelArr.append(random.randint(0, last))
                
        return random.choice(Pattern.rArr)


class ReversedLinearPattern():
    def __init__(self):
        self.name = 'Reversed Linear'
        self.params = []

    def getNext(self, last):
        if Pattern.rNum == 0 or Pattern.rNum == -1:
            Pattern.rNum = last
        else: 
            Pattern.rNum -= 1
            
        return Pattern.rNum


class UniformPattern():
    def __init__(self):
        self.name = 'Uniform'
        self.params = []

    def getNext(self, last):
        return random.uniform(0, last)


class LinearShufflePattern():
    def __init__(self):
        self.name = 'Linear Shuffle'
        self.params = []

    def getNext(self, last):
        if Pattern.rArr == []:
            Pattern.rArr = range(last + 1)
            random.shuffle(Pattern.rArr)
            
        return Pattern.rArr.pop()


class RepeatedLinearShufflePattern():
    def __init__(self):
        self.name = 'Repeated Linear Shuffle'
        self.params = []

    def getNext(self, last):
        if Pattern.rArr == []:
            Pattern.rArr = range(last + 1)
            random.shuffle(Pattern.rArr)
            
        if Pattern.rNum == last:
            Pattern.rNum = 0
        else:
            Pattern.rNum += 1
            
        return Pattern.rNum


class State():
    _selectedObjects = _selectedMaterials = set()
    _wnd = None

    @staticmethod
    def setWindow(wnd):
        State._wnd = wnd

    @staticmethod
    def load():
        objIn = State._openLoadFile('objects')
        State._selectedObjects = pickle.load(objIn)
        objIn.close()

        matIn = State._openLoadFile('materials')
        State._selectedMaterials = pickle.load(matIn)
        matIn.close()

        patIn = State._openLoadFile('pattern')
        patList = pickle.load(patIn)
        patIn.close()

        State._wnd.setSelectedPattern(patList.pop())

        patList = patList.pop() + [patList.pop(),]

        for v in [State._wnd.rK, State._wnd.rS, State._wnd.rM, State._wnd.rL, State._wnd.rB, State._wnd.rA]:
            pm.floatField(v, edit=True, value=patList.pop())

        pm.intField(State._wnd.rN, edit=True, value=patList.pop())
        
        State.refresh()
        State._wnd.randomAlgoChanged(None)

    @staticmethod
    def dump():
        objOut = State._openDumpFile('objects')
        pickle.dump(State._selectedObjects, objOut)
        objOut.close()

        matOut = State._openDumpFile('materials')
        pickle.dump(State._selectedMaterials, matOut)
        matOut.close()

        patOut = State._openDumpFile('pattern')
        patList = [State._wnd.getIntValue(State._wnd.rN), map(lambda v: State._wnd.getFloatValue(v) ,[State._wnd.rA, State._wnd.rB, State._wnd.rL, State._wnd.rM, State._wnd.rS, State._wnd.rK]), State._wnd.getSelectedPattern()]
        pickle.dump(patList, patOut)
        patOut.close()

    @staticmethod
    def refresh():
        pm.iconTextScrollList(State._wnd.selectedObjectsList, edit=True, removeAll=True)
        pm.iconTextScrollList(State._wnd.selectedObjectsList, edit=True, append=list(State._selectedObjects))

        pm.iconTextScrollList(State._wnd.selectedMaterialsList, edit=True, removeAll=True)
        pm.iconTextScrollList(State._wnd.selectedMaterialsList, edit=True, append=list(State._selectedMaterials))
        
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
    def addSelectedMaterialsFromHS(*args):
        State._selectedMaterials = State._selectedMaterials.union(map(lambda m: m.name(), pm.ls(long=True, selection=True)))
        State.refresh()
        
    @staticmethod
    def removeSelectedMaterialsInHS(*args):
        State._selectedMaterials -= set(map(lambda m: m.name(), pm.ls(long=True, selection=True)))
        State.refresh()

    @staticmethod
    def removeSelectedMaterialsInList(*args):
        State._selectedMaterials -= set(pm.iconTextScrollList(State._wnd.selectedMaterialsList, query=True, selectItem=True))
        State.refresh()

    @staticmethod
    def removeAllMaterials(*args):
        State._selectedMaterials.clear()
        State.refresh()

    @staticmethod
    def setMaterials(*args):
        if len(State._selectedObjects) == 0:
            ErrorDialog.show('No objects selected!')
        elif len(State._selectedMaterials) == 0:
            ErrorDialog.show('No naterials selected!')
        elif State._wnd.getSelectedPattern == 'N Materials' and State.getIntValue(State._wnd.rN) > len(State._selectedMaterials):
            ErrorDialog.show('N is higher than selected material count!')
        else:
            State.dump()

            Pattern.rNum = -1
            Pattern.rArr = []
            
            for obj in State._selectedObjects:
                pm.select(obj)
                pm.hyperShade(assign=State._randNextMaterial())

    @staticmethod
    def _randNextMaterial():
        rand = PatternManager.getPattern(State._wnd.getSelectedPattern())
        return list(State._selectedMaterials)[rand.getNext(len(State._selectedMaterials) - 1)]

    @staticmethod
    def _getHomeDir():
        home = os.path.join(os.path.expanduser('~'), 'EClaessonMayaScripts', 'RandMats')
        
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

class ErrorDialog():
    @staticmethod
    def show(msg):
        pm.confirmDialog(title='Error', message=msg, icon='critical')

class RandMatsWindow():
    _size = (262, 500)

    def __init__(self):
        self._window    = pm.window(title='RandMats', widthHeight=RandMatsWindow._size, sizeable=False, maximizeButton=False)
        self._wrapper   = pm.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, RandMatsWindow._size[0]), (2, RandMatsWindow._size[0])], height=RandMatsWindow._size[1])
        self._form      = pm.formLayout(parent=self._wrapper, height=470)
        self._execBtn   = pm.button(label='Set Materials', parent=self._wrapper, command=State.setMaterials)
        self._tabs      = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        self._subform   = pm.formLayout(self._form, edit=True, attachForm=((self._tabs, 'top', 0), (self._tabs, 'left', 0), (self._tabs, 'bottom', 0), (self._tabs, 'right', 0)))

        self._tabObjects = pm.rowColumnLayout(numberOfColumns=1)
        pm.button(label='Add selected from scene', command=State.addSelectedObjectsFromScene)
        pm.button(label='Remove selected in scene', command=State.removeSelectedObjectInScene)
        pm.button(label='Remove selected in list', command=State.removeSelectedObjectsInList)
        pm.button(label='Remove all', command=State.removeAllObjects)
        self.selectedObjectsList = pm.iconTextScrollList(allowMultiSelection=True, height=(RandMatsWindow._size[1] - 150))
        pm.setParent('..')

        self._tabMaterials = pm.rowColumnLayout(numberOfColumns=1)
        pm.button(label='Add selected from HyperShade', command=State.addSelectedMaterialsFromHS)
        pm.button(label='Remove selected in HyperShade', command=State.removeSelectedMaterialsInHS)
        pm.button(label='Remove selected in list', command=State.removeSelectedMaterialsInList)
        pm.button(label='Remove all', command=State.removeAllMaterials)
        self.selectedMaterialsList = pm.iconTextScrollList(allowMultiSelection=True, height=(RandMatsWindow._size[1] - 150))
        pm.setParent('..')

        self._tabPatterns = pm.rowColumnLayout(numberOfColumns=1)
        self.patternList = pm.iconTextScrollList(allowMultiSelection=False, height=(RandMatsWindow._size[1] - 300), selectItem='Random', selectCommand=self.randomAlgoChanged,
        append=PatternManager.getAllPatternNames())

        self.rN = RandMatsWindow._createIntRandParam('N')
        self.rA = RandMatsWindow._createFloatRandParam('Alpha')
        self.rB = RandMatsWindow._createFloatRandParam('Beta')
        self.rL = RandMatsWindow._createFloatRandParam('Lambda')
        self.rM = RandMatsWindow._createFloatRandParam('Mu')
        self.rS = RandMatsWindow._createFloatRandParam('Sigma')
        self.rK = RandMatsWindow._createFloatRandParam('Kappa')

        pm.setParent('..')

        pm.tabLayout(self._tabs, edit=True, tabLabel=((self._tabObjects, 'Objects'), (self._tabMaterials, 'Materials'), (self._tabPatterns, 'Pattern')))

    def show(self):
        pm.showWindow()

    def getFloatValue(self, param):
        return pm.floatField(param, query=True, value=True)
    
    def getIntValue(self, param):
        return pm.intField(param, query=True, value=True)

    def getSelectedPattern(self):
        return pm.iconTextScrollList(self.patternList, query=True, selectItem=True)[0]

    def setSelectedPattern(self, pat):
        pm.iconTextScrollList(self.patternList, edit=True, deselectAll=True)
        pm.iconTextScrollList(self.patternList, edit=True, selectItem=pat)

    def enableRandParam(self, param):
        pm.control(param, edit=True, enable=True)

    def disableRandParam(self, param):
        pm.control(param, edit=True, enable=False)

    def setEnabledRandParams(self, enabled, disabled):
        for p in enabled:
            self.enableRandParam(p)
        for p in disabled:
            self.disableRandParam(p)

    @staticmethod
    def _createFloatRandParam(name):
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 200)])
        pm.text(label=name + ':')
        field = pm.floatField(name, minValue=-999999.9, maxValue=999999.9, step=0.05, enable=False)
        pm.setParent('..')
        return field
        
    @staticmethod
    def _createIntRandParam(name):
        pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 200)])
        pm.text(label=name + ':')
        field = pm.intField(name, minValue=-999999, maxValue=999999, step=1, enable=False)
        pm.setParent('..')
        return field

    def randomAlgoChanged(self, *args):
        rAlgo = self.getSelectedPattern()

        enabled = PatternManager.getPattern(rAlgo).params
        disabled = set(['N', 'Alpha', 'Beta', 'Lambda', 'Mu', 'Sigma', 'Kappa']) - set(enabled)

        self.setEnabledRandParams(enabled, disabled)

        State.dump()


def openRandMats():
    for pat in [RandomPattern(),
                LinearPattern(),
                SingleMaterialPattern(),
                NMaterialsPattern(),
                ReversedLinearPattern(),
                UniformPattern(),
                LinearShufflePattern(),
                RepeatedLinearShufflePattern()
                ]:
        PatternManager.registerPattern(pat)

    wnd = RandMatsWindow()
    State.setWindow(wnd)

    try:
        State.load()
    except:
        pass

    wnd.show()


if __name__ == '__main__':
    openRandMats()