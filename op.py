import bpy


class GLENN_OT_SymmetrizeMesh(bpy.types.Operator):
    "Bisects and symmetrizes the mesh along a specified axis"
    bl_idname = "catalyst.mesh_symmetrize"
    bl_label = "Symmetrize Mesh"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
        ],
        default="X",
    )

    flip: bpy.props.BoolProperty(
        name="Flip",
        description="Inverts the axis comparison",
        default=False,
    )

    value: bpy.props.FloatProperty(
        name="Value",
        description="The axis position to compare against",
        default=0.0,
    )

    add_modifier: bpy.props.BoolProperty(
        name="Add Modifier",
        description="Add a mirror modifier",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context: bpy.types.Context):
        mode = context.mode
        if mode != "EDIT_MESH":
            bpy.ops.object.mode_set(mode="EDIT")

        obj = context.active_object
        bpy.ops.mesh.select_all(action="SELECT")

        axes = ["X", "Y", "Z"]
        idx = axes.index(self.axis)

        norm = (1, 0, 0)
        if self.axis == "Y":
            norm = (0, 1, 0)
        elif self.axis == "Z":
            norm = (0, 0, 1)

        clear_inner = not self.flip
        clear_outer = self.flip

        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=norm,
                            clear_inner=clear_inner, clear_outer=clear_outer)

        if self.add_modifier:
            mod = obj.modifiers.get("Mirror")
            if mod is None:
                mod = obj.modifiers.new(name="Mirror", type="MIRROR")

            mod.use_axis[idx] = True
            mod.use_clip = True
        else:
            dir = f"POSITIVE_{self.axis}" if not self.flip else f"NEGATIVE_{self.axis}"
            bpy.ops.mesh.symmetrize(direction=dir, threshold=self.value)

        if mode != "EDIT_MESH":
            bpy.ops.object.mode_set(mode=mode)

        return {"FINISHED"}
