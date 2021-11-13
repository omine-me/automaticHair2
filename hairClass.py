# import bpy, mathutils
# import numpy as np
# from .utils import *
# from . import const, cpyutils
# import datetime

import numpy as np
import bpy, math, scipy.io
from mathutils import *
from .const import *

# import sys
# sys.path.append("C:/Users/omine/AppData/Roaming/Blender Foundation/Blender/3.0/scripts/addons/autoHair")
from . import cpyutils, utils, tensorClass

class HairSystem:
    def getArrayNum(self, loc):
        arrayNum = (loc - BASELOC)/INTERVAL
        arrayNum = (math.floor(arrayNum[0]), math.floor(arrayNum[1]), math.floor(arrayNum[2]))
        if arrayNum[2] == 128:
            arrayNum[2] == 127
        braid = bpy.context.scene.bTensor.braid[arrayNum[0],arrayNum[1],arrayNum[2]]
        if arrayNum == (64, 60, 113):
            braid = True
            print("exist!")
        return arrayNum, braid

    def distance(self, pos1, pos2):
        return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1]) + abs(pos1[2]-pos2[2])

    def getNearHairNum(self, pos, psys, mainHair):
        nearestHairKey = {}
        for i in range(psys.settings.count):
            if i == mainHair:
                continue
            minDis = 9999
            minKey = -1
            for j in range(1,psys.settings.hair_step+1):
                dis = self.distance(pos, psys.particles[i].hair_keys[j].co)
                if dis < minDis:
                    minDis = dis
                    minKey = j
            # if minDis < .1: #some sort of constant
            if minDis < .08: #some sort of constant
                nearestHairKey[i] = minKey if minKey > 3 else 4 #when minKey is too low, root to beginning of braid will be too sraight
        return nearestHairKey

    def setKeyRot(self, psys, i):
        global utils, cpyutils
        rot=[[1,0,0,0] for i in range(psys.settings.hair_step+1)]
        prevTan = list(utils.sub_norm_v3_v3v3(i.hair_keys[1].co, i.hair_keys[0].co))
        for s in range(2, psys.settings.hair_step+1):
            rot[s-1][:], prevTan = cpyutils.set_key_rotation(list(i.hair_keys[s].co), list(i.hair_keys[s-1].co), list(prevTan), list(rot[s-2][:]))
        rot[-1][:] = rot[-2][:]
        return rot

    def interpolate(self, pos0, posb, idx, len):
        return pos0 + (posb - pos0) * idx/ len

    def checkIfInside(self, pos):
        global np 
        _, cPos, nor, _ = bpy.context.active_object.closest_point_on_mesh(pos)
        if np.dot(nor, cPos-pos)>0:
            cPos += nor * 0.01 #some sort of constant. scale
            return cPos
        return pos
    def getSelected(self):
        bpy.ops.particle.selected()
        s = {}
        psys = bpy.context.active_object.particle_systems.active
        for i in range(psys.settings.count):
            for j in range(psys.settings.hair_step+1):
                if psys.particles[i].hair_keys[j].is_selected: #use bpy.data
                    s.setdefault(i,[]).append(j)
        return s
    def __init__(self, filepath):
        #batchsize = 4
        bpy.types.Scene.bTensor = tensorClass.TensorClass()
        #original 
        file=filepath
        # file=("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
        #file=("C:/Users/omine/Downloads/Ori_out.mat")
        #file=("C:/opencv/VSproject/OpenCV/x64/Debug/result/Ori_out.mat")
        Vox = scipy.io.loadmat(file)['Ori']
        Vox = np.array(Vox)
        # print(Vox.shape)

        rV = Vox[:, :, 0:96]
        gV = Vox[:, :, 96:192]
        bV = Vox[:, :, 192:288]
        rV = np.expand_dims(rV, axis=3)
        gV = np.expand_dims(gV, axis=3)
        bV = np.expand_dims(bV, axis=3)
        Vox = np.concatenate((rV, bV, gV), axis=3)

        Vox = Vox.transpose((0,2,1,3))

        # print(Vox.shape)

        GTV = Vox

        obj = bpy.data.objects['HeadModel']

        bpy.context.view_layer.objects.active = obj
        bpy.context.object.particle_systems.active_index = bpy.context.object.particle_systems.find("forMatApply")
        bpy.ops.particle.particle_edit_toggle()
        bpy.data.scenes["Scene"].tool_settings.particle_edit.display_step = 7
        bpy.data.scenes["Scene"].tool_settings.particle_edit.use_preserve_length = False
        eobj = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        psys = eobj.particle_systems["forMatApply"]

        # braidHairNum = set()#b |= set(dict.keys())
        braidHairNum = {}

        #for i in range(psys.settings.count):
        for idx, i in enumerate(psys.particles):
            # if idx in braidHairNum:
            #     continue
            # isBraidProcessed = False
            braidStart = -1
            braidEnd = -1
            braidStarted = False
            # breakUsed = False
            for j in range(psys.settings.hair_step): #[j+1] is accessed below
                keyPos = i.hair_keys[j].co
                a, isBraid = self.getArrayNum(keyPos)
                if isBraid == 1 and not braidStarted:
                    braidStart = j
                    braidStarted = True
                # elif isBraid == -1:
                    # braidEnd = j
                    braidEnd = 48
                
                try:
                    orientation = GTV[a[0], a[1], a[2],:]
                except Exception as e:
                    print(e)
                    break
        #        print(orientation)
                if not orientation.any(): #when orientation==(0,0,0) remaining keys are positioned at the same position of the latest key.
                    # print("any",j)
                    for k in range(j+1, psys.settings.hair_step+1):
                        i.hair_keys[k].co = i.hair_keys[j].co
                    # breakUsed = True
                    break
                i.hair_keys[j+1].co = i.hair_keys[j].co + Vector((orientation[0],orientation[1],orientation[2]))*0.01
            if not braidStart == -1:
                braidHairNum[idx] = [braidStart, braidEnd]
        
        # import random

        ### braid process ###
        for hidx, binfo in braidHairNum.items(): 
            if binfo[1] == -1:
                binfo[1] = 999
            print("braidProcess")
            i = psys.particles[hidx]
            keyPos = i.hair_keys[binfo[0]].co
            rot = self.setKeyRot(psys, i)
            bDict = self.getNearHairNum(keyPos, psys, i)
            # print(bDict.values())
            for k, v in bDict.items():
                # v = 8
                rootDiff = psys.particles[k].hair_keys[0].co - i.hair_keys[0].co
                # rootDiff = (random.random()*.03*2-1,random.random()*.03*2-1,random.random()*.03*2-1)
                # rootDiff = (0,0,0)
                for vi in range(v, psys.settings.hair_step+1):
                    # psys.particles[k].hair_keys[vi].co = i.hair_keys[vi].co
                    # psys.particles[k].hair_keys[vi].co = self.checkIfInside(Vector(cpyutils.offset_child(list(rootDiff),
                    # print(vi, binfo[1])
                    # psys.particles[k].hair_keys[vi].co = (Vector(cpyutils.offset_child(list(rootDiff),
                    #                                                                     12., #radius
                    #                                                                     list(rot[vi][:]),
                    #                                                                     list(i.hair_keys[vi].co),
                    #                                                                     0.,#roundness
                    #                                                                     vi,
                    #                                                                     psys.settings.hair_step+1,
                    #                                                                     0,#random
                    #                                                                     1. if vi < binfo[1] else 0.,#braid
                    #                                                                     .007,#amp
                    #                                                                     25.#freq
                    #                                                                     )))
                    psys.particles[k].hair_keys[vi].co = (Vector(cpyutils.offset_child(list(rootDiff),
                                                                                        bpy.context.scene.autoHairRadius, #radius
                                                                                        list(rot[vi][:]),
                                                                                        list(i.hair_keys[vi].co),
                                                                                        0.,#bpy.context.scene.autoHairRoundness,#roundness
                                                                                        vi,
                                                                                        psys.settings.hair_step+1,
                                                                                        bpy.context.scene.autoHairRandom,#random
                                                                                        bpy.context.scene.autoHairBraid if vi < binfo[1] else 0.,#braid
                                                                                        bpy.context.scene.autoHairAmp,#amp
                                                                                        bpy.context.scene.autoHairFreq#freq
                                                                                        )))
                pos0 = psys.particles[k].hair_keys[0].co
                posb = i.hair_keys[v].co# - rootDiff
                for vi in range(1, v):
                    psys.particles[k].hair_keys[vi].co = self.checkIfInside(self.interpolate(pos0, posb, vi, v))
                    # psys.particles[k].hair_keys[vi].co = i.hair_keys[vi].co
                # braidHairNum |= set(bDict.keys())
                # isBraidProcessed = True
        utils.particleEditNotify()
        print("end")