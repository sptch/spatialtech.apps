
"""
clip module
"""

import bpy
from bpy.types import (
    Panel,
)

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

        row = layout.row()
        row = layout.column(heading="3D Markers Collection", align=True)
        row.prop(context.scene, "pnp_collection")

        row = layout.row()
        row.prop(scene_props, "live_camera_track", icon="OUTLINER_OB_CAMERA")

        row = layout.row()
        row.operator("pnp.solve_pnp", icon="CAMERA_DATA")
        row = layout.row()
        row.label(text=context.scene.campnp_msg)


class CLIP_PT_pnp_lens(Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = Region
    bl_category = "PnP Solver"
    bl_label = "Lens"
    # bl_parent_id = 'CLIP_PT_tracking_camera'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # get clip from another space_data

        clip = context.space_data.clip

        camera = clip.tracking.camera

        col = layout.column()

        col.prop(camera, "focal_length")

        col = layout.column()
        col.prop(clip.tracking.camera, "principal", text="Optical Center")
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

        sc = context.space_data
        clip = context.space_data.clip
        act_track = clip.tracking.tracks.active
        row = layout.row()
        row.operator("clip.add_marker_at_click", text="Add Marker", icon='ADD')

        if not act_track:
            layout.active = False
            layout.label(text="No active track")
            return

        row = layout.row()
        row.prop(act_track, "name", text="")

        sub = row.row(align=True)

        sub.template_marker(sc, "clip", sc.clip_user, act_track, compact=True)

        icon = 'LOCKED' if act_track.lock else 'UNLOCKED'
        sub.prop(act_track, "lock", text="", icon=icon)

        layout.template_track(sc, "scopes")


def register():
    bpy.utils.register_class(CLIP_PT_solver)
    bpy.utils.register_class(CLIP_PT_pnp_lens)
    bpy.utils.register_class(CLIP_PT_pnp_track)


def unregister():
    bpy.utils.unregister_class(CLIP_PT_solver)
    bpy.utils.unregister_class(CLIP_PT_pnp_lens)
    bpy.utils.unregister_class(CLIP_PT_pnp_track)
