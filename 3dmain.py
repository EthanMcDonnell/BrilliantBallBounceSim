import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from pygame import mixer

# Initialize pygame and sound
pygame.init()
mixer.init()
sound = mixer.Sound("jump.wav")

# Screen dimensions
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Adjust the perspective
gluPerspective(60, (width / height), 0.1, 50.0)


# Set up the camera position and view

glLoadIdentity()
gluPerspective(60, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -6.0)

# Enable lighting
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)  # Main light
#glClearColor(1.0, 1.0, 1.0, 1.0)
# Light 0 (main light)
glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 10.0, 1.0])  # Position
glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])    # Diffuse light
glLightfv(GL_LIGHT0, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])   # Specular light
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])    # Ambient light


# Material properties for the ball
glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])  # Red
glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Reflective
glMaterialf(GL_FRONT, GL_SHININESS, 50)  # Shiny

# Ball class


class Ball:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.1, -0.1, 0.1])
        self.gravity = np.array([0.0, -0.005, 0.0])
        self.radius = 0.5
        self.sphere_radius = 2.5

    def update(self):
        self.velocity += self.gravity
        self.position += self.velocity

        if np.linalg.norm(self.position) + self.radius > self.sphere_radius:
            pygame.mixer.Sound.play(sound)
            normal = self.position / np.linalg.norm(self.position)
            penetration = np.linalg.norm(
                self.position) + self.radius - self.sphere_radius
            self.position -= penetration * normal
            self.velocity -= 2 * np.dot(self.velocity, normal) * normal

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, self.radius, 64, 64)
        gluDeleteQuadric(quad)
        glPopMatrix()


def draw_grid():
    grid_size = 50  # Increase grid size for better visibility
    grid_step = 1   # Step between grid lines

    # Set grid color to gray
    glColor3f(0.7, 0.7, 0.7)

    # Draw grid lines along the X and Z axes at the bottom of the sphere (y = -sphere_radius)
    for x in range(-grid_size, grid_size + 1, grid_step):
        glBegin(GL_LINES)
        # Y position adjusted to the bottom of the outer sphere
        glVertex3f(x, -ball.sphere_radius, -grid_size)
        # Y position adjusted to the bottom of the outer sphere
        glVertex3f(x, -ball.sphere_radius, grid_size)
        glEnd()

    for z in range(-grid_size, grid_size + 1, grid_step):
        glBegin(GL_LINES)
        # Y position adjusted to the bottom of the outer sphere
        glVertex3f(-grid_size, -ball.sphere_radius, z)
        # Y position adjusted to the bottom of the outer sphere
        glVertex3f(grid_size, -ball.sphere_radius, z)
        glEnd()

def draw_glass_sphere(radius):
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.6, 0.8, 1.0, 0.3])  # Glass
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 128, 128)
    gluDeleteQuadric(quad)
    glDisable(GL_BLEND)
    glPopMatrix()


    # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 0.3])  # Specular reflection
    #   # Shininess for the glass effect

    # glPushMatrix()
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glDepthMask(GL_FALSE)  # Disable depth writing for transparency
    # #glDisable(GL_LIGHTING)  # Disable lighting for transparency artifacts
    # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [
    #              0.6, 0.8, 1.0, 0.3])  # Glass material
    # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [
    #              0.2, 0.2, 0.2, 0.2])  # Reduce specular for glass
    # glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 20)
    # quad = gluNewQuadric()
    # gluQuadricNormals(quad, GLU_SMOOTH)
    # gluSphere(quad, radius, 128, 128)
    # gluDeleteQuadric(quad)
    # glEnable(GL_LIGHTING)  # Re-enable lighting
    # glDepthMask(GL_TRUE)  # Re-enable depth writing
    # glDisable(GL_BLEND)
    # glPopMatrix()



# Initialize ball
ball = Ball()

clock = pygame.time.Clock()

# Initialize transformations (only once)
#glLoadIdentity()  # Reset the matrix at the start
#glTranslatef(0.0, 0.0, -12.0)  # Set initial camera position
# Camera parameters

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
    # Translate camera to the new position
    #glTranslatef(-camera_x, -camera_y, -camera_z)
    gluLookAt(camera_x, camera_y, camera_z,
          0.0, 0.0, 0.0,
          0.0, 1.0, 0.0)
    
    # Draw the background grid
    draw_grid()
    # Update and render the ball
    ball.update()
    ball.draw()

    # Optionally, render other objects like the glass sphere
    draw_glass_sphere(ball.sphere_radius)  # Your method to draw glass sphere

    # Swap buffers to display the rendered frame
    pygame.display.flip()

    clock.tick(60)
