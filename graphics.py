from OpenGL.GL import *
from OpenGL.GLU import *

width, height = 800, 600

def init_graphics():
        
    # Adjust the perspective
    gluPerspective(60, (width / height), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -6.0)

    # Enable lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  # Main light
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 10.0, 1.0])  # Position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])    # Diffuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])   # Specular light
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])    # Ambient light

    # Material properties for the ball
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])  # Red
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Reflective
    glMaterialf(GL_FRONT, GL_SHININESS, 50)  # Shiny
    
    
def draw_small_ball(position, radius):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 64, 64)
    gluDeleteQuadric(quad)
    glPopMatrix()
    

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
    
    
def draw_grid(down_offset):
    grid_size = 50  # Increase grid size for better visibility
    grid_step = 1   # Step between grid lines

    # Set grid color to gray
    glColor3f(0.7, 0.7, 0.7)

    # Draw grid lines along the X and Z axes at the bottom of the sphere (y = -sphere_radius)
    for x in range(-grid_size, grid_size + 1, grid_step):
        glBegin(GL_LINES)
        glVertex3f(x, -down_offset, -grid_size)
        glVertex3f(x, -down_offset, grid_size)
        glEnd()

    for z in range(-grid_size, grid_size + 1, grid_step):
        glBegin(GL_LINES)
        glVertex3f(-grid_size, -down_offset, z)
        glVertex3f(grid_size, -down_offset, z)
        glEnd()
        
        
    
