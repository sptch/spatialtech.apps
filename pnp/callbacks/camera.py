"""
camera callbacks
"""


import bpy
from pnp.solvepnp import *

# provide context to handler

# select clips by name


def select_clip_by_name(name):
    for clip in bpy.data.movieclips:
        if clip.name == name:
            clip.select = True
        else:
            clip.select = False


def live_camera_track_callback(scene):
    """
    Live Camera Track callback
    """
    # manualy provide context
    context = bpy.context

    if scene.scene_properties.live_camera_track:
        solve_pnp(*get_scene_info("", bpy.context))

        print('Live Camera Track')


def register():
    bpy.app.handlers.load_pre.append(live_camera_track_callback)
    bpy.app.handlers.depsgraph_update_pre.append(live_camera_track_callback)


def unregister():
    bpy.app.handlers.load_pre.remove(live_camera_track_callback)
    bpy.app.handlers.depsgraph_update_pre.remove(live_camera_track_callback)
