"""
Camera operators
"""

import bpy
from pnp.solvepnp import *
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Scene


class SolvePnP(bpy.types.Operator):
    bl_idname = "pnp.solve_pnp"
    bl_label = "Solve PnP"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Solve PnP"

    def execute(self, context):

        solve_pnp(*get_scene_info(self, context))

        return {"FINISHED"}

import bpy

# class ShowCameraPerspective(bpy.types.Operator):
#     """Show Camera Perspective"""
#     bl_idname = "camera.show_perspective"
#     bl_label = "Show Camera Perspective"
#     bl_options = {"REGISTER", "UNDO"}
    
#     def execute(self, context):
#          # Get the active camera object
#         camera = context.scene.camera
        
#          # Switch to camera view
#         bpy.ops.view3d.view_camera()

        
#         return {"FINISHED"}
# ## separate button 

class ShowCameraPerspective(bpy.types.Operator):
        """Show Camera Perspective"""
        bl_idname = "camera.show_perspective"
        bl_label = "Show Camera Perspective"
        bl_options = {"REGISTER", "UNDO"}

        # Add a property to specify the camera to switch to
        #camera = bpy.props.PointerProperty(type=bpy.types.Object)
        def execute(self, context):
            camera = context.scene.camera

    # Switch to the camera perspective
            bpy.ops.view3d.view_camera()

            return {"FINISHED"}
## button which select camera and set it as active camer 

class OpenGoogle(bpy.types.Operator):
    bl_idname = "test.select_camera"
    bl_label = "Google"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        select_camera(self, context)
        return {"FINISHED"}
class SolveError(bpy.types.Operator):
    bl_idname = "test.pnp_hash"
    bl_label = "Solve Error"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        pnp_hash(self, context)
        #print(pnp_hash(self, context))

        return {"FINISHED"}

# class SolveError_1(bpy.types.Operator):
#     bl_idname = "test.pnp_hash"
#     bl_label = "Solve Error"
#     bl_options = {"REGISTER", "UNDO"}

#     def execute(self, context):
#         context.scene.my_string_2 = pnp_hash(self, context)

#         return {"FINISHED"}
class New_Solve(bpy.types.Operator):
    bl_idname = "test.solve_err"
    bl_label = "Solve Error"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        solve_err(*get_scene_info(self, context))
        #print(solve_err(*get_scene_info(self, context)))
        return {"FINISHED"}

class Cam(bpy.types.Operator):
    bl_idname = "test.cam"
    bl_label = "Solve Error"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'CAMERA':
                cam(obj)
                break

        return {"FINISHED"}







def register():
    bpy.utils.register_class(SolvePnP)
    #bpy.utils.register_class(SolveError)
    bpy.utils.register_class(ShowCameraPerspective)
    bpy.utils.register_class(OpenGoogle)
    bpy.utils.register_class(SolveError)
    #bpy.utils.register_class(SolveError_1)
    bpy.utils.register_class(New_Solve)
    bpy.utils.register_class(Cam)

def unregister():
    bpy.utils.unregister_class(SolvePnP)
    #bpy.utils.unregister_class(SolveError)
    bpy.utils.unregister_class(ShowCameraPerspective)
    bpy.utils.unregister_class(OpenGoogle)
    bpy.utils.unregister_class(SolveError)
    #bpy.utils.unregister_class(SolveError_1)
    bpy.utils.unregister_class(New_Solve)
    bpy.utils.unregister_class(Cam)