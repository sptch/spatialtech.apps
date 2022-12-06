# Blender Add-on Template
# Contributor(s): Mykola Holovko (mykola@spatialtech.info)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
bl_info = {
    "name": "PnP Camera Solver",
    "description": "Pnp Camera Solver",
    "author": "Mykola Holovko",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3d View > Sidebar > PnpSolver",
    "warning": "",  # used for warning icon and text in add-ons panel
    "wiki_url": "http://my.wiki.url",
    "tracker_url": "http://my.bugtracker.url",
    "support": "COMMUNITY",
    "category": "3D View"
}


#
# Add additional functions here
#


def register():
    from . import properties
    from . import ui
    from . import operators
    from . import callbacks

    properties.register()
    operators.register()
    ui.register()
    callbacks.register()


def unregister():
    from . import properties
    from . import ui
    from . import operators
    from . import callbacks

    properties.unregister()
    operators.unregister()
    ui.unregister()
    callbacks.unregister()


if __name__ == '__main__':
    register()
