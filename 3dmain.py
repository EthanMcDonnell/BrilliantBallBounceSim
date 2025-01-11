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




def download_song(link):
    option = {'final_ext': 'mp3',
              'format': 'bestaudio/best',
              'postprocessors': [{'key': 'FFmpegExtractAudio',
                                  'nopostoverwrites': False,
                                  'preferredcodec': 'mp3',
                                  'preferredquality': '5'}],
              'outtmpl': 'song.%(ext)s',
              'ffmpeg_location': '/usr/local/bin/ffmpeg'}
    try:
        print("Downloading Song")
        with yt_dlp.YoutubeDL(option) as ydl:
            ydl.download([link])
    except:
        print(Exception)
        pass

if not os.path.exists("song.mp3"):
    download_song("https://www.youtube.com/watch?v=jCTnF1ACYlk")

# Initialize pygame and sound
pygame.init()
mixer.init()

# Load the song at the beginning
song = mixer.music.load("song.mp3")
sound = mixer.Sound("angelic-ding.mp3")
sound.set_volume(0.01)

# Global variable to track the song's position
song_position = 0  # This will store the current position in the song in seconds

# Screen dimensions
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

init_graphics()


class Ball:
    def __init__(self):
        self.position = np.array([random.random(), random.random(), random.random()])
        self.velocity = np.array([0.10, -0.10, 0.10])
        self.gravity = np.array([0.0, -0.005, 0.0])
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
            self.music_playing = True
            self.is_fading_in = True
            self.is_fading_out = False

        self.last_play_time = current_time


    def update_song(self):
        current_time = time.perf_counter()

        if self.music_playing and pygame.mixer.music.get_busy():
            # Gradually increase the volume for fade-in
            if self.is_fading_in:
                new_volume = pygame.mixer.music.get_volume() + self.volume_interval
                if new_volume >= 1.0:  # Stop fading in when max volume is reached
                    new_volume = 1.0
                    self.is_fading_in = False
                pygame.mixer.music.set_volume(new_volume)

            # Check if the play length has been exceeded
            if (current_time - self.last_play_time) >= self.play_length:
                self.is_fading_out = True

            # Gradually decrease the volume for fade-out
            if self.is_fading_out:
                new_volume = pygame.mixer.music.get_volume() - self.volume_interval
                if new_volume <= 0.0:  # Stop fading out when volume reaches zero
                    new_volume = 0.0
                    self.is_fading_out = False
                    self.music_playing = False
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

    def draw(self):
        draw_small_ball(self.position, self.radius)

        

# Initialize ball
ball = Ball()
clock = pygame.time.Clock()

# Camera parameters
distance = 8.0  # Distance from the sphere
rotation_speed = 10  # Speed of camera rotation

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply dynamic camera movement based on time (for rotation)
    time_passed = pygame.time.get_ticks() / 1000.0
    rotation_angle = time_passed * rotation_speed  # Rotation speed adjusted by time

    # Reset transformations and set perspective
    glLoadIdentity()
    gluPerspective(60, (width / height), 0.1, 100.0)

    # Calculate camera position using spherical coordinates
    camera_x = distance * np.sin(np.radians(rotation_angle))
    camera_z = distance * np.cos(np.radians(rotation_angle))
    camera_y = 3.0  # You can modify this for vertical rotation if needed

    # Apply the camera translation (moving the camera to the new position)
    gluLookAt(camera_x, camera_y, camera_z,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

    # Draw the background grid
    draw_grid(ball.sphere_radius)
    # Update and render the ball
    ball.update()
    ball.draw()

    # Optionally, render other objects like the glass sphere
    draw_glass_sphere(ball.sphere_radius)

    # Swap buffers to display the rendered frame
    pygame.display.flip()

    clock.tick(60)
