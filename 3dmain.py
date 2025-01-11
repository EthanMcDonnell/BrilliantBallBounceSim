import pygame
from pygame.locals import *
import numpy as np
from pygame import mixer
from pydub import AudioSegment
import yt_dlp
import os
import time
from graphics import *
import random
from yt_dlp import YoutubeDL
from panda3d.core import PointLight, DirectionalLight, TransparencyAttrib, Material
from panda3d.core import Point3
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

width, height = 600, 600

# Ensure the song is downloaded
# Scroll

def download_song(link):
    option = {'final_ext': 'mp3',
              'format': 'bestaudio/best',
              'postprocessors': [{'key': 'FFmpegExtractAudio',
                                  'nopostoverwrites': False,
                                  'preferredcodec': 'mp3',
                                  'preferredquality': '5'}],
              'outtmpl': '%(title)s.%(ext)s',
              'ffmpeg_location': '/usr/local/bin/ffmpeg'}
    try:
        print("Downloading Song")
        with yt_dlp.YoutubeDL(option) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"Error: {e}")
        pass


song_name = "øneheart x reidenshi - snowfall"
song_file = song_name + ".mp3"
if not os.path.exists(song_file):
    download_song("https://www.youtube.com/watch?v=LlN8MPS7KQs")

# Initialize pygame and sound
pygame.init()
mixer.init()

# Load the song at the beginning
song = mixer.music.load(song_file)
sound = mixer.Sound("angelic-ding.mp3")
sound.set_volume(0.01)

# Global variable to track the song's position
song_position = 0  # This will store the current position in the song in seconds

# Screen dimensions
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)


class Ball:
    def __init__(self):
        # random.random()
        self.position = np.array([
            random.random(), random.random(), random.random()])  # [x, y, z]
        self.velocity = np.array([0.15, 0.15, -0.15])  # z is vertical
        # Gravity affects z-direction
        self.gravity = np.array([0.0, 0.0, -0.010])
        self.radius = 0.2
        self.sphere_radius = 3
        self.song_position = 0  # Track current position in the song
        self.last_play_time = 0
        self.play_length = 0.2
        self.volume_interval = 0.1
        self.curr_play_time = 0
        self.music_playing = False
        self.pause_over_start = False
        self.is_fading_in = False
        self.is_fading_out = False
        self.color_change_speed = 0.05  # Speed of the rainbow effect
        self.time_offset = random.random()  # Randomize starting color

    # use time=current_time * self.color_change_speed
    def slow_rainbow_color(self, time):
        """Returns a color cycling through the rainbow."""
        r = abs(sin(2*time + self.time_offset))
        g = abs(sin(2*time + self.time_offset + 2*pi / 3))
        b = abs(sin(2*time + self.time_offset + 4*pi / 3))

        return (r, g, b)
    
    def random_rainbow_color(self):
        """Returns a random color."""
        r = random.random()  # Random float between 0 and 1
        g = random.random()  # Random float between 0 and 1
        b = random.random()  # Random float between 0 and 1
        return (r, g, b)


    def update_color(self):
        """Updates the ball color to a rainbow effect."""
        current_time = time.perf_counter()
        rainbow_color = self.slow_rainbow_color(current_time)

        # Set the color to the ball's material or rendering
        self.render.set_color(
            rainbow_color[0], rainbow_color[1], rainbow_color[2], 1)  # Full opacity

    def play_song_segment(self):
        """Play a segment of the song on each bounce."""
        current_time = time.perf_counter()
        print("HIT w/ SOUND")
        pygame.mixer.Sound.play(sound)

        # Check if the song should resume or start
        if not self.music_playing:
            if self.pause_over_start:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play(loops=0, start=self.song_position)
            pygame.mixer.music.set_volume(0)  # Start with zero volume
            self.is_fading_in = True
            self.is_fading_out = False

        self.last_play_time = current_time

    def update_song(self):
        current_time = time.perf_counter()

        if pygame.mixer.music.get_busy():
            # Gradually increase the volume for fade-in
            if self.is_fading_in and not self.music_playing:
                
                print("FADING IN")
                new_volume = pygame.mixer.music.get_volume() + self.volume_interval
                if new_volume >= 1.0:  # Stop fading in when max volume is reached
                    self.music_playing = True
                    new_volume = 1.0
                    self.is_fading_in = False
                pygame.mixer.music.set_volume(new_volume)

            # Check if the play length has been exceeded
            if (current_time - self.last_play_time) >= self.play_length:
                self.is_fading_out = True
                self.music_playing = False

            # Gradually decrease the volume for fade-out
            if self.is_fading_out and not self.music_playing:
                print("FADING OUT")
                new_volume = pygame.mixer.music.get_volume() - self.volume_interval
                if new_volume <= 0.0:  # Stop fading out when volume reaches zero
                    new_volume = 0.0
                    self.is_fading_out = False
                    self.song_position += pygame.mixer.music.get_pos() / 1000.0
                    pygame.mixer.music.pause()  # Pause instead of stopping
                    self.pause_over_start = True  # Indicate pause state
                pygame.mixer.music.set_volume(new_volume)

    def update(self):
        self.velocity += self.gravity
        self.position += self.velocity
        self.update_song()

        # Check for collision with the wall (sphere boundary)
        if np.linalg.norm(self.position) + self.radius > self.sphere_radius:
            normal = self.position / np.linalg.norm(self.position)
            penetration = np.linalg.norm(
                self.position) + self.radius - self.sphere_radius
            self.position -= penetration * normal
            self.velocity -= 2 * np.dot(self.velocity, normal) * normal
            self.play_song_segment()
            self.update_color()

    def draw(self, game_render):
        self.render = create_sphere(game_render, (0.,0.,0.), self.radius)









class My3DApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Set up the environment
        self.set_background_color(0, 0, 0)  # RGB for black
        # self.axis = self.loader.loadModel('zup-axis')
        # self.axis.reparentTo(self.render)
        # self.axis.setPos(0, 0, 0)
        # self.axis.setScale(1)

        self.ball = Ball()
        self.ball.draw(self.render)
        self.taskMgr.add(self.update_ball, "update_ball")

        # Set up lights
        self.setup_lighting()

        # Outer sphere
        self.outer_sphere = create_sphere(
            self.render, (0, 0, 0), self.ball.sphere_radius, wireframe=True)
        self.setup_outer_sphere_material()
        
        # Adjust the camera's position and orientation
        self.camera.set_pos(0, 0, 100)
        self.camera.look_at(self.outer_sphere)

        # Enable shadows
        self.render.set_shader_auto()
        self.render.set_light(self.render.attach_new_node(
            DirectionalLight('dir_light')))

        # Add a spinning camera task
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Add dynamic light that follows the ball
        self.setup_dynamic_ball_light()


    def setup_lighting(self):
        """Sets up the general lighting for the scene."""
        # Ambient light for base illumination
        ambient_light = AmbientLight("ambient_light")
        ambient_light.set_color((0.2, 0.2, 0.2, 1))  # Less bright ambient light
        self.render.set_light(self.render.attach_new_node(ambient_light))

        # Directional light for shading
        dir_light = DirectionalLight("directional_light")
        # Reduced intensity to make it less bright
        dir_light.set_color((0.3, 0.3, 0.3, 1))
        dir_light_np = self.render.attach_new_node(dir_light)
        dir_light_np.set_pos(-5, -5, 10)
        dir_light_np.look_at(0, 0, 0)
        self.render.set_light(dir_light_np)

        # Point light for localized illumination
        point_light = PointLight("point_light")
        point_light.set_color((0.4, 0.4, 0.4, 0.8))  # Keep point light intensity
        point_light.attenuation = (1,0,0)
        point_light.set_shadow_caster(True)
        self.render.set_shader_auto()
        point_light_np = self.render.attach_new_node(point_light)
        point_light_np.set_pos(0, 0, 22.5)
        self.render.set_light(point_light_np)


    def setup_dynamic_ball_light(self):
        """Set up a dynamic light that follows the ball."""
        # Point light for the ball
        self.ball_light = PointLight("ball_light")
        self.ball_light.set_color((0.5, 0.8, 1.0, 1))  # Light blue color
        self.ball_light_np = self.render.attach_new_node(self.ball_light)
        self.ball_light_np.set_pos(self.ball.position[0], self.ball.position[1], self.ball.position[2] + 3)
        self.render.set_light(self.ball_light_np)

        # Add a spotlight effect for dramatic lighting
        self.ball_spotlight = Spotlight("ball_spotlight")
        self.ball_spotlight.set_color((1.0, 1.0, 0.8, 1))  # Warm yellowish color
        self.ball_spotlight.set_exponent(1.0)  # More focused beam
        self.ball_spotlight_np = self.render.attach_new_node(self.ball_spotlight)
        self.ball_spotlight_np.set_pos(self.ball.position[0], self.ball.position[1], self.ball.position[2] + 5)
        self.ball_spotlight_np.look_at(self.ball.render)
        self.render.set_light(self.ball_spotlight_np)
        
    def update_dynamic_ball_light(self):
        """Update the ball's dynamic light position."""
        # self.ball_light_np.set_pos(self.ball.position[0], self.ball.position[1], self.ball.position[2] + 3)
        # self.ball_spotlight_np.set_pos(self.ball.position[0], self.ball.position[1], self.ball.position[2] + 5)
        # self.ball_spotlight_np.look_at(self.ball.render)

    def setup_outer_sphere_material(self):
        """Sets up the material for the outer sphere."""
        # Enable transparency with a more transparent sphere
        self.outer_sphere.set_transparency(TransparencyAttrib.MAlpha)
        self.outer_sphere.set_depth_offset(1)
        # Disable depth testing for transparency to make the wireframe visible from the back
        self.outer_sphere.set_depth_write(True)  # Disable depth writing
        self.outer_sphere.set_depth_test(False)   # Disable depth testing

        # Set the sphere's material to have a higher level of transparency
        material = Material()
        material.set_shininess(50.0)  # Higher shininess for a reflective look
        material.set_emission((0.2, 0.2, 0.4, 0.5))  # Subtle glow effect
        self.outer_sphere.set_material(material)

        # Adjust alpha and color for more transparency
        self.outer_sphere.set_color(0.8, 0.9, 1.0, 0.1)  # Make it more transparent
        self.outer_sphere.set_shader_auto()

        # Disable backface culling to allow inside visibility
        self.outer_sphere.set_two_sided(True)  # Render both sides of the sphere
        

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.set_pos(10 * sin(angleRadians), -
                            20.0 * cos(angleRadians), 10)
        self.camera.look_at(self.outer_sphere)
        return Task.cont

    def update_ball(self, task):
        # Update ball's physics
        self.ball.update()

        # Update sphere's position in Panda3D based on ball's physics
        ball_pos = Point3(
            self.ball.position[0],  # X remains X
            self.ball.position[1],  # Y remains Y
            self.ball.position[2]   # Z remains Z
        )
        self.ball.render.set_pos(ball_pos)

        # Update the ball's dynamic light position
        self.update_dynamic_ball_light()

        return task.cont


# Initialize the Pygame clock
clock = pygame.time.Clock()

app = My3DApp()

# Adjust camera and animation parameters if necessary
while True:
    app.task_mgr.step()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(60)
