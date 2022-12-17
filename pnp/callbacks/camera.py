"""
camera callbacks
"""


import bpy
from pnp.solvepnp import *

# provide context to handleer
import copy
def live_camera_track_callback(scene):
    context = bpy.context
    self = context.scene
    if scene.scene_properties.live_camera_track:
        print(1)
        if str(pnp_hash(self, context)) != scene.pnp_string:
            print(2)
            solve_pnp(*get_scene_info("", bpy.context))
            scene.pnp_string = str(pnp_hash(self, context))
    return

# def show_elem(scene):
#     if scene.live_show:
#         context = bpy.context
#         self = context.scene
#         count = pnp_hash(self, context)
#         scene.my_string_2 = count
#         return
def register():
    bpy.app.handlers.load_pre.append(live_camera_track_callback)
    bpy.app.handlers.depsgraph_update_pre.append(live_camera_track_callback)
    # bpy.app.handlers.load_pre.append(show_elem)
    # bpy.app.handlers.depsgraph_update_post.append(show_elem)


def unregister():
    bpy.app.handlers.load_pre.remove(live_camera_track_callback)
    bpy.app.handlers.depsgraph_update_pre.remove(live_camera_track_callback)
    # bpy.app.handlers.load_pre.remove(show_elem)
    # bpy.app.handlers.depsgraph_update_post.remove(show_elem)
    
