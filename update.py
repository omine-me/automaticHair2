import bpy, mathutils, math
from . import utils, hairClass
from .const import *

def setBraidStart(context):
    global math
    obj = bpy.data.objects['HeadModel']
    bpy.context.view_layer.objects.active = obj
    bpy.context.object.particle_systems.active_index = bpy.context.object.particle_systems.find("forMatApply")
    # bpy.ops.particle.particle_edit_toggle()
    eobj = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    psys = eobj.particle_systems["forMatApply"]

    selected = context.scene.hsys.getSelected()
    for k, v in selected.items():
        # this should not allow multiple operation per one hair...
        arrayNum = (psys.particles[k].hair_keys[v[0]].co - BASELOC)/INTERVAL
        arrayNum = (math.floor(arrayNum[0]), math.floor(arrayNum[1]), math.floor(arrayNum[2]))
        try:
            bpy.context.scene.bTensor.braid[arrayNum[0],arrayNum[1],arrayNum[2]] = 1.
        except IndexError:
            pass
    
def setBraidEnd(context):
    global math
    obj = bpy.data.objects['HeadModel']
    bpy.context.view_layer.objects.active = obj
    bpy.context.object.particle_systems.active_index = bpy.context.object.particle_systems.find("forMatApply")
    # bpy.ops.particle.particle_edit_toggle()
    eobj = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    psys = eobj.particle_systems["forMatApply"]

    selected = context.scene.hsys.getSelected()
    for k, v in selected.items():
        # this should not allow multiple operation per one hair...
        arrayNum = (psys.particles[k].hair_keys[v[0]].co - BASELOC)/INTERVAL
        arrayNum = (math.floor(arrayNum[0]), math.floor(arrayNum[1]), math.floor(arrayNum[2]))
        for x in range(-1,2):
            for y in range(-1,2):
                for z in range(-1,2):
                    try:
                        bpy.context.scene.bTensor.braid[arrayNum[0]+x,arrayNum[1]+y,arrayNum[2]+z] = -1.
                    except IndexError:
                        pass

def setPosUpdate(context):
    hsys = context.scene.hsysCtrl
    hsys._particleEditMode()
    hsys._setDepsgpaph()
    selected = hsys.getSelected()
    context.scene.hsysCtrl.updatePos(selected.keys())

def setRadius(self, context):
    hsys = context.scene.hsysCtrl
    # print(hsys.ctrlHair[0].keys[1].co)
    hsys._particleEditMode()
    hsys._setDepsgpaph()
    selected = hsys.getSelected()
    # hsys._setDepsgpaph()
    # print(hsys.ctrlHair[0].keys[1].co)
    context.scene.hsysTar._particleEditMode()
    context.scene.hsysTar._setDepsgpaph()
    for p, k in selected.items():
        for c in k:
            # print(p, c)
            hsys.ctrlHair[p].keys[c].radius = context.scene.autoHairRadius
        # print(hsys.ctrlHair[p].keys[1].co)
        context.scene.hsysTar._offsetChild(hsys.ctrlHair[p])
    utils.particleEditNotify()
    hsys._particleEditMode()
    # hsys._setDepsgpaph()

def setRandom(self, context):
    hsys = context.scene.hsysCtrl
    hsys._particleEditMode()
    hsys._setDepsgpaph()
    selected = hsys.getSelected()
    # hsys._setDepsgpaph()
    context.scene.hsysTar._particleEditMode()
    context.scene.hsysTar._setDepsgpaph()
    for p, k in selected.items():
        for c in k:
            hsys.ctrlHair[p].keys[c].random = context.scene.autoHairRandom
        context.scene.hsysTar._offsetChild(hsys.ctrlHair[p])
    utils.particleEditNotify()
    hsys._particleEditMode()
    # hsys._setDepsgpaph()

def setRoundness(self, context):
    hsys = context.scene.hsysCtrl
    hsys._particleEditMode()
    hsys._setDepsgpaph()
    selected = hsys.getSelected()
    # hsys._setDepsgpaph()
    context.scene.hsysTar._particleEditMode()
    context.scene.hsysTar._setDepsgpaph()
    for p, k in selected.items():
        hsys.ctrlHair[p].roundness = context.scene.autoHairRoundness
        context.scene.hsysTar._offsetChild(hsys.ctrlHair[p])
    utils.particleEditNotify()
    hsys._particleEditMode()
    # hsys._setDepsgpaph()

def setBraid(self, context):
    hsys = context.scene.hsysCtrl
    hsys._particleEditMode()
    hsys._setDepsgpaph()
    selected = hsys.getSelected()
    # hsys._setDepsgpaph()
    context.scene.hsysTar._particleEditMode()
    context.scene.hsysTar._setDepsgpaph()
    for p, k in selected.items():
        for c in k:
            hsys.ctrlHair[p].keys[c].braid = context.scene.autoHairBraid
        context.scene.hsysTar._offsetChild(hsys.ctrlHair[p])
    utils.particleEditNotify()
    hsys._particleEditMode()
    # hsys._setDepsgpaph()

def setAmp(self, context):
    hsys = context.scene.hsysCtrl
    hsys._particleEditMode()
    hsys._setDepsgpaph()
    selected = hsys.getSelected()
    context.scene.hsysTar._particleEditMode()
    context.scene.hsysTar._setDepsgpaph()
    # hsys._setDepsgpaph()
    for p, k in selected.items():
        for c in k:
            hsys.ctrlHair[p].keys[c].amp = context.scene.autoHairAmp
        context.scene.hsysTar._offsetChild(hsys.ctrlHair[p])
    utils.particleEditNotify()
    hsys._particleEditMode()
    # hsys._setDepsgpaph()

def setFreq(self, context):
    hsys = context.scene.hsysCtrl
    hsys._particleEditMode()
    hsys._setDepsgpaph()
    selected = hsys.getSelected()
    # hsys._setDepsgpaph()
    context.scene.hsysTar._particleEditMode()
    context.scene.hsysTar._setDepsgpaph()
    for p, k in selected.items():
        for c in k:
            hsys.ctrlHair[p].keys[c].freq = context.scene.autoHairFreq
        context.scene.hsysTar._offsetChild(hsys.ctrlHair[p])
    utils.particleEditNotify()
    hsys._particleEditMode()
    # hsys._setDepsgpaph()

def setHair(context):
    obj = bpy.data.objects['HeadModel']
    if not bpy.context.mode == "PARTICLE":
        bpy.context.view_layer.objects.active = obj
        bpy.context.object.particle_systems.active_index = bpy.context.object.particle_systems.find("forMatApply")
        bpy.ops.particle.particle_edit_toggle()
    eobj = obj.evaluated_get(context.evaluated_depsgraph_get())
    context.scene.hsys.setHair(eobj.particle_systems["forMatApply"])