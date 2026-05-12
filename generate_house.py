import bpy
import os

# ====================================================
# OUTPUT FOLDER
# ====================================================

os.makedirs("output", exist_ok=True)

# ====================================================
# CLEAR SCENE
# ====================================================

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ====================================================
# SIMPLE AI GENERATED HOUSE
# (TEMP TEST HOUSE)
# ====================================================

# FLOOR
bpy.ops.mesh.primitive_plane_add(size=12)

floor = bpy.context.object
floor.name = "Floor"

# ====================================================
# WALLS
# ====================================================

walls = [

    (0, -6, 1.5, 6, 0.15, 1.5),
    (0, 6, 1.5, 6, 0.15, 1.5),
    (-6, 0, 1.5, 0.15, 6, 1.5),
    (6, 0, 1.5, 0.15, 6, 1.5),

]

for wall in walls:

    x, y, z, sx, sy, sz = wall

    bpy.ops.mesh.primitive_cube_add(
        location=(x, y, z)
    )

    obj = bpy.context.object

    obj.scale = (sx, sy, sz)

# ====================================================
# ROOMS
# ====================================================

# CENTER WALL
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, 1.5)
)

room_wall = bpy.context.object

room_wall.scale = (0.15, 4, 1.5)

# ====================================================
# DOOR GAP VISUAL
# ====================================================

bpy.ops.mesh.primitive_cube_add(
    location=(0, -1.5, 1)
)

door = bpy.context.object

door.scale = (0.2, 1, 1)

# ====================================================
# MATERIALS
# ====================================================

mat = bpy.data.materials.new(name="WallMaterial")

mat.diffuse_color = (0.8, 0.8, 0.8, 1)

for obj in bpy.data.objects:

    if obj.type == 'MESH':

        obj.data.materials.append(mat)

# ====================================================
# CAMERA
# ====================================================

bpy.ops.object.camera_add(
    location=(0, -18, 14),
    rotation=(1.1, 0, 0)
)

# ====================================================
# LIGHT
# ====================================================

bpy.ops.object.light_add(
    type='SUN',
    location=(0, 0, 10)
)

# ====================================================
# EXPORT GLB
# ====================================================

output_path = os.path.abspath(
    "output/house.glb"
)

bpy.ops.export_scene.gltf(

    filepath=output_path,

    export_format='GLB'
)

print("HOUSE GENERATED")
print(output_path)

# ====================================================
# FUTURE:
# HERE FloorplanToBlender3d INTEGRATION
# ====================================================

"""
FUTURE INTEGRATION:

1. Receive floorplan image
2. Send image to FloorplanToBlender3d
3. Detect:
    - walls
    - rooms
    - windows
    - doors
4. Generate Blender scene
5. Export GLB
6. Return model URL

Repo:
https://github.com/grebtsew/FloorplanToBlender3d
"""