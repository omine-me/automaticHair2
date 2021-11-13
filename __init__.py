bl_info = {
    "name": "autoHair2",
    "author": "Omine Taisei",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "3Dビューポート",
    "description": "ヘアモデリングの簡易化",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Particle"
}

if "bpy" in locals():
    import imp
    imp.reload(hairClass)
    imp.reload(main)
    imp.reload(utils)
    imp.reload(update)
    imp.reload(const)
    imp.reload(io)
    imp.reload(cpyutils)
    imp.reload(tensorClass)
else:
    from . import main
    from . import hairClass
    from . import utils
    from . import update
    from . import const
    from . import io
    from . import cpyutils
    from . import tensorClass

import bpy
import numpy as np
from bpy.props import (
    IntProperty,
    FloatProperty,
    # FloatVectorProperty,
    # EnumProperty,
    # BoolProperty,
)

def initProps():
    global np
    scene = bpy.types.Scene
    scene.bTensor = None
    scene.hsys = None
    # scene.autoHairIsCtrl = BoolProperty(
    #     name="Is Control Hair",
    #     description="Is This Hair Control",
    #     default=False,
    #     update=update.setIsCtrl
    # )
    scene.autoHairRoundness = FloatProperty(
        name="Roundness",
        description="Children's roundness",
        default=0.0,
        min=0.0,
        max=1.0,
        # update=io.load("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
    )
    scene.autoHairRadius = FloatProperty(
        name="Radius",
        description="Children's radius",
        default=12.,
        min=0.0,
        # update=io.load("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
    )
    scene.autoHairRandom = FloatProperty(
        name="Random",
        description="Children's randomness",
        default=0.,
        min=0.0,
        # update=io.load("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
    )
    scene.autoHairBraid = FloatProperty(
        name="Braidness",
        description="Children's braidness",
        default=1.,
        min=0.0,
        # update=io.load("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
    )
    scene.autoHairAmp = FloatProperty(
        name="Amplitude",
        description="Children's Amplitude",
        default=.007,
        min=0.0,
        # update=io.load("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
    )
    scene.autoHairFreq = FloatProperty(
        name="Frequency",
        description="Children's Frequency",
        default=25.,
        min=0.0,
        # update=io.load("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
    )
    scene.defaultHairNum = IntProperty(
        name="defaultHairNum",
        description="",
        default=const.DEFAULTHAIRNUM
    )

def delProps():
    scene = bpy.types.Scene
    del scene.bTensor
    del scene.hsys
    del scene.autoHairRadius
    del scene.autoHairRandom
    del scene.autoHairRoundness
    del scene.autoHairBraid
    del scene.autoHairAmp
    del scene.autoHairFreq
    del scene.defaultHairNum

classes = [
    main.AUTOHAIR_OT_New,
    main.AUTOHAIR_OT_Load,
    main.AUTOHAIR_OT_LoadDataFile,
    main.AUTOHAIR_OT_Save,
    main.AUTOHAIR_OT_Unlink,
    main.AUTOHAIR_OT_Translate,
    main.AUTOHAIR_OT_AddCtrlHair,
    main.AUTOHAIR_OT_RemoveCtrlHair,

    main.AUTOHAIR_OT_ShowBraidStart,
    main.AUTOHAIR_OT_ShowBraidEnd,
    main.AUTOHAIR_OT_SetBraidStart,
    main.AUTOHAIR_OT_SetBraidNone,
    main.AUTOHAIR_OT_SetBraidEnd,
    main.AUTOHAIR_PT_Menu,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    initProps()
    print("AutoHair2 registered")


def unregister():
    delProps()
    for c in classes:
        bpy.utils.unregister_class(c)
    print("AutoHair2 unregistered")


if __name__ == "__main__":
    register()