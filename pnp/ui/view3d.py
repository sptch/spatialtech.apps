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


def register():
    bpy.utils.register_class(VIEW3D_PT_pnp_solver)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_pnp_solver)
