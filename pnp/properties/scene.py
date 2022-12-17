"""
Scene properties
"""

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Scene

class SceneProperties(bpy.types.PropertyGroup):
    # register scene boolean property live_camera_track

    live_camera_track: BoolProperty(
        name="Live Camera Track",
        description="Live Camera Track",
        default=False,
    )
    campnp_msg: StringProperty(
        name="Message",
        description="Message",
        default="",
    )



def register():
    bpy.utils.register_class(SceneProperties)
    bpy.types.Scene.scene_properties = PointerProperty(type=SceneProperties)
    bpy.types.Scene.pnp_collection = bpy.props.PointerProperty(
        name="",
        type=bpy.types.Collection)
    bpy.types.Scene.campnp_msg = bpy.props.StringProperty(
        name="",
        default="",
        description="Camera PnP Solver Message")

        

    bpy.types.Scene.pnp_clip_name = bpy.props.StringProperty(
        name="",
        default="",
        description="Camera PnP Solver Clip Name")
    bpy.types.Scene.my_string = bpy.props.StringProperty(name="Search", default="")
    bpy.types.Scene.my_string_1 = bpy.props.StringProperty(name="Ser", default="")
    bpy.types.Scene.pnp_string = bpy.props.StringProperty(name="String", default="")


def unregister():
    del bpy.types.Scene.scene_properties
    bpy.utils.unregister_class(SceneProperties)
    del bpy.types.Scene.pnp_collection
    del bpy.types.Scene.campnp_msg
    del bpy.types.Scene.my_string
    del bpy.types.Scene.my_string_1
    del bpy.types.Scene.pnp_string