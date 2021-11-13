import bpy
import numpy as np
from . import utils, update, io, cpyutils, tensorClass
from .hairClass import *
from bpy.props import (
    # IntProperty,
    FloatProperty,
    # FloatVectorProperty,
    # EnumProperty,
    BoolProperty,
    StringProperty,
)

class AUTOHAIR_OT_New(bpy.types.Operator):

    bl_idname = "autohair.new"
    bl_label = "New AutoHair"
    bl_description = "New Hair Particles"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.types.Scene.hsysCtrl = HairCtrlSystem([0,5], utils.importBaseObj())
        bpy.context.scene.hsysCtrl.setArrayedChild()

        return {'FINISHED'}

class AUTOHAIR_OT_Unlink(bpy.types.Operator):

    bl_idname = "autohair.unlink"
    bl_label = "Unlink"
    bl_description = "Delete AutoHair from Particle System (Currently for Memory Saving)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

class AUTOHAIR_OT_Load(bpy.types.Operator):

    bl_idname = "autohair.load"
    bl_label = "Load MAT File"
    bl_description = "Load MAT File"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        name="File Path",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        description="",
    )
    filter_glob: StringProperty(
        default="*.mat",
        options={'HIDDEN'},
    )

    # def invoke(self, context, event):
    #     context.window_manager.fileselect_add(self)
    #     return {'RUNNING_MODAL'}

    def execute(self, context):
        # io.load(self.filepath)
        io.load("C:/opencv/VSproject/OpenCV/x64/Debug/out/00100/00100Ori_gt.mat")
        return {'FINISHED'}

class AUTOHAIR_OT_LoadDataFile(bpy.types.Operator):

    bl_idname = "autohair.load_data_file"
    bl_label = "Load .data File"
    bl_description = "Load DATA File"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        name="File Path",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        description="",
    )
    filter_glob: StringProperty(
        default="*.data",
        options={'HIDDEN'},
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        io.load_data_file(self.filepath)
        return {'FINISHED'}

class AUTOHAIR_OT_Save(bpy.types.Operator):

    bl_idname = "autohair.save"
    bl_label = "Save"
    bl_description = "Save NPZ File"
    bl_options = {'REGISTER', 'UNDO'}
    # ファイル指定のプロパティを定義する
    filepath: StringProperty(
        name="File Path",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        description="",
    )
    # filename: StringProperty(
    #     name="File Name",
    #     default="",
    #     maxlen=1024,
    #     description="",
    # )
    # directory: StringProperty(
    #     name="Directory Path",
    #     default="",
    #     maxlen=1024,
    #     subtype='FILE_PATH',
    #     description="",
    # )

    # changing default filename doesn't work...
    filename: StringProperty(
        name="001.npz",
        default="",
    )
    # 読み込みの拡張子を指定する
    # filter_glob を指定しておくと window_manager.fileselect_add が拡張子をフィルタする
    filter_glob: StringProperty(
        default="*.npz",
        options={'HIDDEN'},
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        io.save(self.filepath)
        return {'FINISHED'}

class AUTOHAIR_OT_Translate(bpy.types.Operator):

    bl_idname = "autohair.translate"
    bl_label = "Update Position"
    bl_description = "Update positions of Target Hair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        update.setPosUpdate(context)
        # print(context.scene.hsysCtrl.ctrlHair[0].keys[1].co)
        return {'FINISHED'}

class AUTOHAIR_OT_ShowBraidStart(bpy.types.Operator):

    bl_idname = "autohair.show_braid_start"
    bl_label = "Show Braid Start"
    bl_description = "Show Braid Start"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.bTensor.showBraid(1.)
        # print(context.scene.hsysCtrl.ctrlHair[0].keys[1].co)
        return {'FINISHED'}
class AUTOHAIR_OT_ShowBraidEnd(bpy.types.Operator):

    bl_idname = "autohair.show_braid_end"
    bl_label = "Show Braid End"
    bl_description = "Show Braid End"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.bTensor.showBraid(-1.)
        # print(context.scene.hsysCtrl.ctrlHair[0].keys[1].co)
        return {'FINISHED'}

class AUTOHAIR_OT_SetBraidStart(bpy.types.Operator):

    bl_idname = "autohair.set_braid_start"
    bl_label = "Set Braid Start"
    bl_description = "Set Braid Start"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        update.setBraidStart(context)
        return {'FINISHED'}

class AUTOHAIR_OT_SetBraidEnd(bpy.types.Operator):

    bl_idname = "autohair.set_braid_end"
    bl_label = "Set Braid End"
    bl_description = "Set Braid End"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        update.setBraidEnd(context)
        return {'FINISHED'}
class AUTOHAIR_OT_SetBraidNone(bpy.types.Operator):

    bl_idname = "autohair.set_braid_none"
    bl_label = "Set Braid None"
    bl_description = "Set Braid None"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.bTensor.setBraidNone()
        return {'FINISHED'}

class AUTOHAIR_OT_AddCtrlHair(bpy.types.Operator):

    bl_idname = "autohair.add_ctrl_hair"
    bl_label = "Add Hair"
    bl_description = "Add Selected Hair to Control Hair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        update.setCtrlHair(context, True)
        return {'FINISHED'}
class AUTOHAIR_OT_RemoveCtrlHair(bpy.types.Operator):

    bl_idname = "autohair.remove_ctrl_hair"
    bl_label = "Remove Hair"
    bl_description = "Remove Selected Hair from Control Hair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        update.setCtrlHair(context, False)
        return {'FINISHED'}

class AUTOHAIRPanel:
    bl_space_type = 'VIEW_3D'           # パネルを登録するスペース
    bl_region_type = 'UI'               # パネルを登録するリージョン
    bl_category = "AutoHair2"        # パネルを登録するタブ名

class AUTOHAIR_PT_Menu(AUTOHAIRPanel, bpy.types.Panel):
    bl_label = "AutoHair2"         # パネルのヘッダに表示される文字列
    bl_idname = "AUTOHAIR_PT_Menu"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Start from here:")
        # layout.operator(AUTOHAIR_OT_New.bl_idname)
        layout.operator(AUTOHAIR_OT_Load.bl_idname)
        layout.operator(AUTOHAIR_OT_LoadDataFile.bl_idname)
        layout.separator()
        layout.operator(AUTOHAIR_OT_SetBraidStart.bl_idname)
        layout.operator(AUTOHAIR_OT_SetBraidEnd.bl_idname)
        layout.operator(AUTOHAIR_OT_ShowBraidStart.bl_idname)
        layout.operator(AUTOHAIR_OT_SetBraidNone.bl_idname)
        layout.operator(AUTOHAIR_OT_ShowBraidEnd.bl_idname)
        # layout.operator(AUTOHAIR_OT_Unlink.bl_idname)
        layout.separator()
        layout.prop(scene, "autoHairRadius")
        layout.prop(scene, "autoHairRandom")
        layout.prop(scene, "autoHairBraid")
        layout.prop(scene, "autoHairAmp")
        layout.prop(scene, "autoHairFreq")