import bpy, bmesh, math
import numpy as np
from mathutils import *
from .const import *

class TensorClass:
    def getArrayNum(self,loc):
        global math
        arrayNum = (loc - BASELOC)/INTERVAL
        arrayNum = [math.floor(arrayNum[0]), math.floor(arrayNum[1]), math.floor(arrayNum[2])]
        # if arrayNum[2] == 128:
        #     arrayNum[2] == 127
        # return arrayNum[0],arrayNum[1],arrayNum[2]
        return arrayNum

    def __init__(self):
        #braid tensor
        self.braid = np.zeros([128,96,128])
        self.braid[64, 60, 113] = 1.

        if not bpy.context.mode == "OBJECT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.data.objects['HairGAN:Points'].hide_viewport = False
        bpy.context.view_layer.objects.active = ob = bpy.data.objects['HairGAN:Points']
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.reveal()
        self.me = ob.data
        bm = bmesh.from_edit_mesh(self.me)
        self.arrayNum = np.empty([len(bm.verts),3],np.int8)
        for i, v in enumerate(bm.verts):
            self.arrayNum[i] = self.getArrayNum(v.co)
        bpy.ops.object.mode_set(mode = 'OBJECT')

    def showBraid(self, braidNum):
        # context = bpy.context
        # ob = context.active_object
        if not bpy.context.mode == "OBJECT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['HairGAN:Points'].hide_viewport = False
        bpy.context.view_layer.objects.active = ob = bpy.data.objects['HairGAN:Points']
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.reveal()
        self.me = ob.data
        bm = bmesh.from_edit_mesh(self.me)
        for i, v in enumerate(bm.verts):
            a = self.arrayNum[i]
            v.select_set(not(self.braid[a[0],a[1],a[2]] == braidNum))
            # v.select_set(not(self.braid[self.getArrayNum(v.co)] == braidNum))
        bm.select_mode |= {'VERT'}
        bm.select_flush_mode()
        bmesh.update_edit_mesh(self.me)
        bpy.ops.mesh.hide()
    
    def setBraidNone(self):
        # context = bpy.context
        # ob = context.active_object
        # self.me = ob.data
        bm = bmesh.from_edit_mesh(self.me)
        for i, v in enumerate(bm.verts):
            if v.select:
                a = self.arrayNum[i]
                self.braid[a[0],a[1],a[2]] = 0.
        bm.select_mode |= {'VERT'}
        bm.select_flush_mode()
        bmesh.update_edit_mesh(self.me)
        bpy.ops.mesh.hide()