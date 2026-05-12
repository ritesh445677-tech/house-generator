import bpy
import os

# create output folder
os.makedirs("output", exist_ok=True)

# clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# floor
bpy.ops.mesh.primitive_plane_add(size=10)

# wall 1
bpy.ops.mesh.primitive_cube_add(location=(0, -5, 1.5))
wall1 = bpy.context.object
wall1.scale = (5, 0.1, 1.5)

# wall 2
bpy.ops.mesh.primitive_cube_add(location=(0, 5, 1.5))
wall2 = bpy.context.object
wall2.scale = (5, 0.1, 1.5)

# wall 3
bpy.ops.mesh.primitive_cube_add(location=(-5, 0, 1.5))
wall3 = bpy.context.object
wall3.scale = (0.1, 5, 1.5)

# wall 4
bpy.ops.mesh.primitive_cube_add(location=(5, 0, 1.5))
wall4 = bpy.context.object
wall4.scale = (0.1, 5, 1.5)

# export GLB
bpy.ops.export_scene.gltf(
    filepath="output/house.glb",
    export_format='GLB'
)

print("DONE")