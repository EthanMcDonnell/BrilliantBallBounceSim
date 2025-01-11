from math import pi, sin, cos
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from procedural3d import *


def create_sphere(game_render, position, radius, wireframe=False):
    # Create a small red sphere (diffuse red, specular white)
    sphere = SphereMaker(
        center=position,
        radius=radius,
        smooth=True,
        thickness=.1,
        inverted=False,
        vertex_color=None,
        has_uvs=True,
    )
    
    sphere = game_render.attach_new_node(sphere.generate())
    if wireframe:
        sphere.set_render_mode_filled_wireframe((1., 1., 1., 1.))
    return sphere

    # def setup_lighting(self):
    #     # Ambient light (for brighter scene)
    #     ambient_light = AmbientLight('ambient_light')
    #     ambient_light.set_color((0.4, 0.4, 0.4, 1.0))  # Light color
    #     ambient_node = self.render.attach_new_node(ambient_light)
    #     self.render.set_light(ambient_node)

    #     # Directional light (from above)
    #     directional_light = DirectionalLight('directional_light')
    #     directional_light.set_color((0.8, 0.8, 0.8, 1.0))  # White light
    #     directional_node = self.render.attach_new_node(directional_light)
    #     directional_node.set_hpr(45, -45, 0)  # Angle the light
    #     self.render.set_light(directional_node)


    # def draw_small_ball(self, position, radius):
    #     # Create a small red sphere (diffuse red, specular white)
    #     sphere = SphereMaker(
    #         center=(0., 0., -.7),
    #         radius=2.,
    #         segments={
    #             "horizontal": 40,
    #             "vertical": 10,
    #             "bottom_cap": 3,
    #             "top_cap": 3,
    #             "slice_caps": 2
    #         },
    #         smooth=True,
    #         bottom_clip=.1,
    #         top_clip=.8,
    #         slice=125.,
    #         thickness=.2,
    #         inverted=False,
    #         vertex_color=None,
    #         has_uvs=True,
    #         tex_units={
    #             "main": (6., 6.),
    #             "inner_main": (6., 6.),
    #             "bottom_cap": (6., 6.),
    #             "top_cap": (6., 6.),
    #             "inner_bottom_cap": (6., 6.),
    #             "inner_top_cap": (6., 6.),
    #             "slice_start_cap": (6., 6.),
    #             "slice_end_cap": (6., 6.)
    #         },
    #         tex_offset={
    #             "slice_start_cap": (.2, 0.)
    #         },
    #         tex_rotation={
    #             "main": 20.,
    #             "inner_main": -40.,
    #             "bottom_cap": 160.,
    #             "inner_bottom_cap": 160.,
    #             "slice_start_cap": 90.,
    #             "slice_end_cap": 60.
    #         },
    #         tex_scale={
    #             "slice_end_cap": (1.5, 1.5)
    #         }
    #     )

    #     sphere = self.render.attach_new_node(sphere.generate())
    #     sphere.set_x(-5.)
    #     sphere.set_h(-150.)
    #     sphere.set_scale(radius)

    #     # Set materials (equivalent to OpenGL materials)
    #     mat = Material()
    #     mat.set_diffuse((1.0, 0.0, 0.0, 1.0))  # Red
    #     mat.set_specular((1.0, 1.0, 1.0, 1.0))  # White
    #     mat.set_shininess(50)
    #     sphere.set_material(mat)

    #     sphere.reparent_to(self.render)
        
    
    # def draw_glass_sphere(self, radius):
    #     # Create a glass sphere with transparency
    #     sphere = SphereMaker(
    #         center=(0., 0., -.7),
    #         radius=2.,
    #         segments={
    #             "horizontal": 40,
    #             "vertical": 10,
    #             "bottom_cap": 3,
    #             "top_cap": 3,
    #             "slice_caps": 2
    #         },
    #         smooth=True,
    #         bottom_clip=.1,
    #         top_clip=.8,
    #         slice=125.,
    #         thickness=.2,
    #         inverted=False,
    #         vertex_color=None,
    #         has_uvs=True,
    #         tex_units={
    #             "main": (6., 6.),
    #             "inner_main": (6., 6.),
    #             "bottom_cap": (6., 6.),
    #             "top_cap": (6., 6.),
    #             "inner_bottom_cap": (6., 6.),
    #             "inner_top_cap": (6., 6.),
    #             "slice_start_cap": (6., 6.),
    #             "slice_end_cap": (6., 6.)
    #         },
    #         tex_offset={
    #             "slice_start_cap": (.2, 0.)
    #         },
    #         tex_rotation={
    #             "main": 20.,
    #             "inner_main": -40.,
    #             "bottom_cap": 160.,
    #             "inner_bottom_cap": 160.,
    #             "slice_start_cap": 90.,
    #             "slice_end_cap": 60.
    #         },
    #         tex_scale={
    #             "slice_end_cap": (1.5, 1.5)
    #         }
    #     )

    #     sphere = self.render.attach_new_node(sphere.generate())
    #     sphere.set_x(-5.)
    #     sphere.set_h(-150.)
    #     sphere.set_scale(radius)

    #     # Set materials (transparent blue)
    #     mat = Material()
    #     mat.set_diffuse((0.6, 0.8, 1.0, 0.5))  # Transparent blue
    #     mat.set_specular((0.8, 0.8, 0.8, 1.0))  # Reflective highlights
    #     mat.set_shininess(90)
    #     sphere.set_material(mat)

    #     sphere.reparent_to(self.render)

    # def draw_grid(self):
    #     return
    #     # # Simple grid drawing for testing
    #     # grid_size = 30
    #     # grid_step = 1
    #     # for x in range(-grid_size, grid_size + 1, grid_step):
    #     #     self.render_line(Point3(x, -1, -grid_size),
    #     #                      Point3(x, -1, grid_size))
    #     # for z in range(-grid_size, grid_size + 1, grid_step):
    #     #     self.render_line(Point3(-grid_size, -1, z),
    #     #                      Point3(grid_size, -1, z))

    # def render_line(self, start, end):
    #     return
    #     # Simple line rendering
    #     line = self.loader.load_model('models/empty')
    #     line.set_pos(start)
    #     line.set_scale(end - start)
    #     line.reparent_to(self.render)

