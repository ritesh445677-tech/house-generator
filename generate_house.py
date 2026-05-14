import bpy
import os
import sys

# ====================================================
# ARGUMENTS
# ====================================================

args = sys.argv

if "--" in args:
    args = args[args.index("--") + 1:]
else:
    args = []

print("ARGS:", args)

# ====================================================
# PATHS
# ====================================================

OUTPUT_DIR = "/app/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "house.glb"
)

print("OUTPUT FILE:", OUTPUT_FILE)

# ====================================================
# CLEAR SCENE
# ====================================================

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# remove unused data
for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)

for block in bpy.data.materials:
    bpy.data.materials.remove(block)

# ====================================================
# CREATE FLOOR
# ====================================================

bpy.ops.mesh.primitive_plane_add(
    size=12,
    location=(0, 0, 0)
)

floor = bpy.context.object

floor.name = "Floor"

# ====================================================
# FLOOR MATERIAL
# ====================================================

floor_mat = bpy.data.materials.new(
    name="FloorMaterial"
)

floor_mat.use_nodes = True

bsdf = floor_mat.node_tree.nodes["Principled BSDF"]

bsdf.inputs["Base Color"].default_value = (
    0.15,
    0.15,
    0.15,
    1
)

floor.data.materials.append(floor_mat)

# ====================================================
# WALL MATERIAL
# ====================================================

wall_mat = bpy.data.materials.new(
    name="WallMaterial"
)

wall_mat.use_nodes = True

wall_bsdf = wall_mat.node_tree.nodes[
    "Principled BSDF"
]

wall_bsdf.inputs["Base Color"].default_value = (
    0.8,
    0.8,
    0.8,
    1
)

# ====================================================
# WALLS
# ====================================================

walls = [

    # front
    (0, -6, 1.5, 6, 0.15, 1.5),

    # back
    (0, 6, 1.5, 6, 0.15, 1.5),

    # left
    (-6, 0, 1.5, 0.15, 6, 1.5),

    # right
    (6, 0, 1.5, 0.15, 6, 1.5),
]

for wall in walls:

    x, y, z, sx, sy, sz = wall

    bpy.ops.mesh.primitive_cube_add(
        location=(x, y, z)
    )

    obj = bpy.context.object

    obj.scale = (sx, sy, sz)

    obj.data.materials.append(wall_mat)

# ====================================================
# CENTER ROOM WALL
# ====================================================

bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, 1.5)
)

room_wall = bpy.context.object

room_wall.scale = (0.15, 4, 1.5)

room_wall.data.materials.append(wall_mat)

# ====================================================
# DOOR
# ====================================================

bpy.ops.mesh.primitive_cube_add(
    location=(0, -1.5, 1)
)

door = bpy.context.object

door.scale = (0.2, 1, 1)

door_mat = bpy.data.materials.new(
    name="DoorMaterial"
)

door_mat.use_nodes = True

door_bsdf = door_mat.node_tree.nodes[
    "Principled BSDF"
]

door_bsdf.inputs["Base Color"].default_value = (
    0.4,
    0.2,
    0.1,
    1
)

door.data.materials.append(door_mat)

# ====================================================
# CAMERA
# ====================================================

bpy.ops.object.camera_add(
    location=(0, -18, 14),
    rotation=(1.1, 0, 0)
)

camera = bpy.context.object

bpy.context.scene.camera = camera

# ====================================================
# SUN LIGHT
# ====================================================

bpy.ops.object.light_add(
    type='SUN',
    location=(0, 0, 10)
)

sun = bpy.context.object

sun.data.energy = 3

# ====================================================
# WORLD LIGHT
# ====================================================

world = bpy.context.scene.world

world.use_nodes = True

bg = world.node_tree.nodes["Background"]

bg.inputs[1].default_value = 1.0

# ====================================================
# EXPORT SETTINGS
# ====================================================

# select all mesh objects
bpy.ops.object.select_all(action='SELECT')

# ====================================================
# EXPORT GLB
# ====================================================

try:

    bpy.ops.export_scene.gltf(

        filepath=OUTPUT_FILE,

        export_format='GLB',

        use_selection=False,

        export_apply=True
    )

    print("===================================")
    print("HOUSE GENERATED SUCCESSFULLY")
    print("===================================")

    print("FILE EXISTS:",
          os.path.exists(OUTPUT_FILE))

    print("OUTPUT PATH:",
          OUTPUT_FILE)

except Exception as e:

    print("EXPORT FAILED")
    print(str(e))

# ====================================================
# FINAL DEBUG
# ====================================================

print("OUTPUT DIRECTORY FILES:")

print(os.listdir(OUTPUT_DIR))
