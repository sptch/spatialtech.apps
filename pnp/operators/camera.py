"""
Camera operators
"""

import bpy
from pnp.solvepnp import *


class SolvePnP(bpy.types.Operator):
    bl_idname = "pnp.solve_pnp"
    bl_label = "Solve PnP"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Solve PnP"

    def execute(self, context):

        solve_pnp(*get_scene_info(self, context))

        return {"FINISHED"}


def register():
    bpy.utils.register_class(SolvePnP)


def unregister():
    bpy.utils.unregister_class(SolvePnP)
