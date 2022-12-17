"""
view3d module
"""

import bpy
from bpy.types import (
    Panel,
)


Region = "TOOLS" if bpy.app.version < (2, 80, 0) else "UI"

class VIEW3D_PT_pnp_solver(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "PnP Solver"
    bl_context = "objectmode"
    bl_label = "Solver"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_props = scene.scene_properties

        row = layout.row()

        # select collection
        row = layout.column(heading="3D Markers Collection", align=True)
        row.prop(context.scene, "pnp_collection")

        row.prop(scene_props, "live_camera_track", icon="OUTLINER_OB_CAMERA")

        row = layout.row()
        row.operator("pnp.solve_pnp", icon="CAMERA_DATA")

class OBJECT_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    bl_category = 'Cameras'
    bl_label = "Online Show"
    camera_name = bpy.props.StringProperty(
        name="Camera",
        description="The name of the camera to use"
    )

    def draw(self, context):
        col = self.layout.column(align=True)
        layout = self.layout
        obj = context.object
        row = layout.row()
        scene = bpy.context.scene
        camera = scene.camera
        col.prop(context.scene, "my_string")
        col.label(text="Online Obj" f": {bpy.data.objects[obj.name].name}") 
        for i in bpy.data.cameras:
                if context.scene.my_string in i.name:
                    col.label(text="Camera" f": {bpy.data.cameras[i.name].name}")
                    if bpy.data.cameras[i.name].background_images:
                        if isinstance(bpy.data.cameras[i.name].background_images[0].alpha, float):
                            col.prop(bpy.data.cameras[i.name].background_images[0], "alpha", text="Opacity", slider=True)
                            col.operator('camera.show_perspective',text='Show Camera',icon='CAMERA_DATA')
                        if isinstance(bpy.data.cameras[i.name].background_images[0].display_depth, str):
                            col.prop(bpy.data.cameras[i.name].background_images[0], "display_depth", text="Depth") 
                        if isinstance(bpy.data.cameras[i.name].background_images[0].source, str):
                            col.prop(bpy.data.cameras[i.name].background_images[0], "source", text="Source")
                            if bpy.data.cameras[i.name].background_images[0].source == 'MOVIE_CLIP':
                                col.prop(bpy.data.cameras[i.name].background_images[0], "clip", text="Clip")

class CAMERA_PT_panel(Panel):
       #bl_idname = "test.solve_err"
       bl_context = "objectmode"
       bl_label = "Camera Panel"
       bl_space_type = "VIEW_3D"
       bl_region_type = "UI"
       bl_category = "XUI"
    
       def draw(self, context):
            layout = self.layout

            for obj in bpy.data.objects:
                if obj.type == 'CAMERA':
                    icon = 'CAMERA_DATA'
                    if obj == context.active_object:
                        icon = 'OUTLINER_OB_CAMERA'
                    layout.operator("test.cam", text=obj.name, icon=icon)
                    layout.operator("test.cam", text=obj.name, icon=icon)


             
                # Set the camera as the target of the button

# class OBJECTS_PT_panel_1(Panel):
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_context = 'objectmode'
#     bl_category = 'Sum of numbers'
#     bl_label = "Category"
    
#     def draw(self, context):
#         col = self.layout.column(heading="Heading", align=True)
#         col.operator("test.pnp_hash", text="")
        #col.operator("test.open_google", text="Open Google", icon='URL')

# class Camera_PT_ON(Panel):
#     bl_context = "objectmode"
#     bl_label = "Camera Panel"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "XUI"
        
#     def draw(self, context):



                        
            

def register():
    bpy.utils.register_class(VIEW3D_PT_pnp_solver)
    bpy.utils.register_class(OBJECT_PT_panel)
    bpy.utils.register_class(CAMERA_PT_panel)
    #bpy.utils.register_class(OBJECTS_PT_panel_1)   
        

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_pnp_solver)
    bpy.utils.unregister_class(OBJECT_PT_panel)
    bpy.utils.unregister_class(CAMERA_PT_panel)
    #bpy.utils.unregister_class(OBJECTS_PT_panel_1)
