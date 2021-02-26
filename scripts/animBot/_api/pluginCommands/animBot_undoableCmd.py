




import sys
import _ctypes

import maya.OpenMayaMPx as OpenMayaMPx


o_____O__l___l____0__O__l___O_o_____o____1_0__l__1___o_____1_____0_____1_o_o_____l____O____o_O = "animBot_undoableCmd"

try:
    long
except NameError:
    
    long = int


class o_O__1___l__1____o_1___l___o__0__1____o_____o____O_____l_____o(OpenMayaMPx.MPxCommand):

    def isUndoable(o_o_____O_O___o____0____0___O):
        
        return True

    def doIt(o_o_____O_O___o____0____0___O, args):
        



        o__l___O____O_____1_o__0__o___l__o___l___0__0_1_l_o = long(args.asString(0), 0)
        o_o_____O_O___o____0____0___O.o_o____l___O____0___o__o____l_1 = _ctypes.PyObj_FromPtr(o__l___O____O_____1_o__0__o___l__o___l___0__0_1_l_o)

        o_o___l_____1__o_____o_____l____0____1_0_____0___l__o__l_o_l = long(args.asString(1), 0)
        o_o_____O_O___o____0____0___O.o_0___0__O__0___0 = _ctypes.PyObj_FromPtr(o_o___l_____1__o_____o_____l____0____1_0_____0___l__o__l_o_l)

        if o_o_____O_O___o____0____0___O.o_0___0__O__0___0 is not None:
            o_o_____O_O___o____0____0___O.o_0___0__O__0___0.doIt()

    def redoIt(o_o_____O_O___o____0____0___O):
        if o_o_____O_O___o____0____0___O.o_o____l___O____0___o__o____l_1 is not None:
            o_o_____O_O___o____0____0___O.o_o____l___O____0___o__o____l_1.redoIt()

        if o_o_____O_O___o____0____0___O.o_0___0__O__0___0 is not None:
            o_o_____O_O___o____0____0___O.o_0___0__O__0___0.doIt()

    def undoIt(o_o_____O_O___o____0____0___O):
        if o_o_____O_O___o____0____0___O.o_o____l___O____0___o__o____l_1 is not None:
            o_o_____O_O___o____0____0___O.o_o____l___O____0___o__o____l_1.undoIt()

        if o_o_____O_O___o____0____0___O.o_0___0__O__0___0 is not None:
            o_o_____O_O___o____0____0___O.o_0___0__O__0___0.undoIt()




def cmdCreator():
    
    return OpenMayaMPx.asMPxPtr(o_O__1___l__1____o_1___l___o__0__1____o_____o____O_____l_____o())


def initializePlugin(o_1___0_____0__O____1_____l_l____O_l):
    
    plugin = OpenMayaMPx.MFnPlugin(o_1___0_____0__O____1_____l_l____O_l, "animBot", "1.0", "Any")
    try:
        plugin.registerCommand(o_____O__l___l____0__O__l___O_o_____o____1_0__l__1___o_____1_____0_____1_o_o_____l____O____o_O, cmdCreator)
    except:
        sys.stderr.write("Failed to register command: " + o_____O__l___l____0__O__l___O_o_____o____1_0__l__1___o_____1_____0_____1_o_o_____l____O____o_O)


def uninitializePlugin(o_1___0_____0__O____1_____l_l____O_l):
    
    plugin = OpenMayaMPx.MFnPlugin(o_1___0_____0__O____1_____l_l____O_l)
    try:
        plugin.deregisterCommand(o_____O__l___l____0__O__l___O_o_____o____1_0__l__1___o_____1_____0_____1_o_o_____l____O____o_O)
    except:
        sys.stderr.write("Failed to unregister command: " + o_____O__l___l____0__O__l___O_o_____o____1_0__l__1___o_____1_____0_____1_o_o_____l____O____o_O)


