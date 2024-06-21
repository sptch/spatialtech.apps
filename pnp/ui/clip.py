"""
clip module
"""
import copy
import bpy
from pnp.solvepnp import *
from bpy.types import (
    Panel,
)
from pnp.properties.scene import *

Region = "TOOLS" if bpy.app.version < (2, 80, 0) else "UI"


class CLIP_PT_solver(Panel):
    bl_space_type = "CLIP_EDITOR"
    bl_region_type = Region
    bl_category = "PnP Solver"
    bl_context = "objectmode"
    bl_label = "Solver"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_props = scene.scene_properties
        clip = context.space_data.clip
        camera = clip.tracking.camera
        col = layout.column()
        row = layout.row()
        #col.prop(context.scene, "pnp_string")

        row = layout.row()
        row = layout.column(heading="3D Markers Collection", align=True)
        row.prop(context.scene, "pnp_collection")
        row = layout.row()
        row.prop(scene_props, "live_camera_track", icon="OUTLINER_OB_CAMERA")
        #col.label(text="Online Obj" f": {bpy.data.objects[context.scene.my_string_2].name}")
        #row.prop(scene_props, "pnp_hash", icon="INFO")
        # # camera.focal_length = 100
        # # print(a)
        # # camera.focal_length = 200
        # # print(a)
        # bpy.data.movieclips[clip.name].tracking.camera.focal_length = 100
        # print(a)
        # col.label(text="Online" f": {solve_error(camera.focal_length, context.scene.campnp_msg)}")
        # #print(solve_error(camera.focal_length, context.scene.campnp_msg))

        # # row = layout.row()
        # # row.operator("test.solve_error", context.scene, "my_string")

        row = layout.row()
        row.operator("pnp.solve_pnp", icon="CAMERA_DATA")
        row = layout.row()
        row.label(text=context.scene.campnp_msg)


class CLIP_PT_pnp_lens(Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = Region
    bl_category = "PnP Solver"
    bl_label = "Lens"
    #bl_parent_id = 'CLIP_PT_tracking_camera'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        #get clip from another space_data

        clip = context.space_data.clip

        camera = clip.tracking.camera
        # b = []
        # print(b)
        # col = layout.column()
        # col.prop(camera, "focal_length")
        # while camera.focal_length < 1000:
        #     a = copy.copy(context.scene.campnp_msg)
        #     camera.focal_length += 10
        #     if context.scene.campnp_msg > a:
        #         b.append(a)
        #     context.scene.campnp_msg = a
        # print(b)
        col = layout.column()
        col.prop(camera, "focal_length")
        col = layout.column()
        col.prop(clip.tracking.camera, "principal_point_pixels", text="Optical Center")
        col.operator("clip.set_center_principal", text="Set Center")

        col = layout.column()
        col.prop(camera, "distortion_model", text="Lens Distortion")
        if camera.distortion_model == 'POLYNOMIAL':
            col = layout.column(align=True)
            col.prop(camera, "k1")
            col.prop(camera, "k2")
            col.prop(camera, "k3")
        elif camera.distortion_model == 'DIVISION':
            col = layout.column(align=True)
            col.prop(camera, "division_k1")
            col.prop(camera, "division_k2")
        elif camera.distortion_model == 'NUKE':
            col = layout.column(align=True)
            col.prop(camera, "nuke_k1")
            col.prop(camera, "nuke_k2")
        elif camera.distortion_model == 'BROWN':
            col = layout.column(align=True)
            col.prop(camera, "brown_k1")
            col.prop(camera, "brown_k2")
            col.prop(camera, "brown_k3")
            col.prop(camera, "brown_k4")
            col.separator()
            col.prop(camera, "brown_p1")
            col.prop(camera, "brown_p2")


class CLIP_PT_pnp_track(Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = "PnP Solver"
    bl_label = "Markers"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        sc = context.space_data
        clip = context.space_data.clip
        act_track = clip.tracking.tracks.active
        row = layout.row()

        row.operator("clip.add_marker_at_click", text="Add Marker", icon='ADD')
        #row.operator("clip.delete_marker", text="Delete Marker", icon='REMOVE')
    
        if not act_track:
            layout.active = False
            layout.label(text="No active track")
            return
        row = layout.row()
        row.prop(act_track, "name", text="")
        

        #row = layout.row()
        #row.prop(context.scene, "my_string_1", text="3D Marker")
 # see which 3d marker is selected

               
        

        sub = row.row(align=True)

        sub.template_marker(sc, "clip", sc.clip_user, act_track, compact=True)

        icon = 'LOCKED' if act_track.lock else 'UNLOCKED'
        sub.prop(act_track, "lock", text="", icon=icon)

        layout.template_track(sc, "scopes")

class CLIP_PT_pnp_track_1(Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = "PnP Solver"
    bl_label = "3D Markers"
    def draw(self, context):
        layout = self.layout
        clip = context.space_data.clip
        obj = context.active_object
        row = layout.row()

        #row.operator("clip.add_marker_at_click", text="Add Marker", icon='ADD')
        if not obj:
            layout.active = False
            layout.label(text="No active object")
            return
        if not obj.type == 'EMPTY':
            layout.active = False
            layout.label(text="No active object")
            return
        ## check if marker in colelction Marker
        if not obj.name in bpy.data.collections['Marker'].objects:
            layout.active = False
            layout.label(text="No active object")
            return
        row = layout.row()
        row.prop(obj,"name",  text="")
# class CLIP_PT_pnp_track_2(Panel):
#     bl_space_type = 'CLIP_EDITOR'
#     bl_region_type = 'UI'
#     bl_category = "PnP Solver"
#     bl_label = "3D Markers"

#     # define a property group to store the active object
#     class PnP_props(bpy.types.PropertyGroup):
#         active_obj: bpy.props.StringProperty(
#             name="Active Object",
#             description="The name of the active object",
#             default=""
#         )
#     def update_active_obj(self, context):
#         obj = context.active_object
#         if obj and obj.type == 'EMPTY':
#             context.scene.pnp_props.active_obj = obj.name
#         else:
#             context.scene.pnp_props.active_obj = ""

#     # draw the panel
#     def draw(self, context):
#         layout = self.layout

#         # update the active object property
#         self.update_active_obj(context)

#         # show the name of the active object
#         row = layout.row()
#         row.label(text=context.scene.pnp_props.active_obj)


def register():
    bpy.utils.register_class(CLIP_PT_solver)
    bpy.utils.register_class(CLIP_PT_pnp_lens)
    bpy.utils.register_class(CLIP_PT_pnp_track)
    bpy.utils.register_class(CLIP_PT_pnp_track_1)
    #bpy.utils.register_class(CLIP_PT_pnp_track_2)
    #bpy.utils.register_class(CLIP_PT_pnp_track_2.PnP_props)
    #bpy.types.Scene.pnp_props = bpy.props.PointerProperty(type=CLIP_PT_pnp_track_2.PnP_props)

def unregister():
    bpy.utils.unregister_class(CLIP_PT_solver)
    bpy.utils.unregister_class(CLIP_PT_pnp_lens)
    bpy.utils.unregister_class(CLIP_PT_pnp_track)
    bpy.utils.unregister_class(CLIP_PT_pnp_track_1)
    #bpy.utils.unregister_class(CLIP_PT_pnp_track_2)
    #bpy.utils.unregister_class(CLIP_PT_pnp_track_2.PnP_props)
    #del bpy.types.Scene.pnp_props
