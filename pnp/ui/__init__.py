from . import view3d
from . import clip


def register():
    view3d.register()
    clip.register()


def unregister():
    view3d.unregister()
    clip.unregister()
