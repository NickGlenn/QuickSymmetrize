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

from .op import GLENN_OT_SymmetrizeMesh
import bpy

bl_info = {
    "name": "Quick Symmetrize",
    "author": "Nick Glenn",
    "description": "Simple tool for quickly symmetrizing meshes",
    "blender": (4, 0, 0),
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}


def menu_func(self, context):
    obj = context.active_object
    if obj is not None and obj.type == "MESH":
        self.layout.separator()
        self.layout.operator(GLENN_OT_SymmetrizeMesh.bl_idname)


def register():
    bpy.utils.register_class(GLENN_OT_SymmetrizeMesh)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(GLENN_OT_SymmetrizeMesh)
