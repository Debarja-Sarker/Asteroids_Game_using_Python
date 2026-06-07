from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math


W, H = 900, 600

ship_x, ship_y = 450, 300

bullets = []

asteroids = []

score = 0

def rad(deg):
    return deg * math.pi / 180.0

def reset_game():
    global ship_x, ship_y, bullets, asteroids, score

    ship_x, ship_y = W // 2, H // 2
    bullets = []
    asteroids = []
    score = 0

    for _ in range(8):
        asteroids.append({
            "x": random.randint(0, W),
            "y": random.randint(0, H),
            "vx": random.uniform(-2, 2),
            "vy": random.uniform(-2, 2),
            "r": random.randint(20, 50),
            "shape": []
        })

def generate_asteroid(cx, cy, r):
    pts = []
    for i in range(0, 360, 30):
        angle = rad(i)
        jitter = random.uniform(0.7, 1.3)

        x = cx + math.cos(angle) * r * jitter
        y = cy + math.sin(angle) * r * jitter
        pts.append((x, y))
    return pts

def check_ship_collision():
    global ship_x, ship_y

    for a in asteroids:
        dx = ship_x - a["x"]
        dy = ship_y - a["y"]
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < a["r"]:
            reset_game()
            return


def check_bullet_collision():
    global bullets, asteroids, score

    new_asteroids = []
    new_bullets = []

    for a in asteroids:
        hit = False

        for b in bullets:
            dx = b[0] - a["x"]
            dy = b[1] - a["y"]
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < a["r"]:
                hit = True
                score += 1
                break

        if not hit:
            new_asteroids.append(a)

    
    for b in bullets:
        new_bullets.append(b)

    asteroids = new_asteroids
    bullets = new_bullets


def draw_ship():
    glPushMatrix()
    glTranslatef(ship_x, ship_y, 0)

    glColor3f(0, 1, 0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(0, 15)
    glVertex2f(-10, -10)
    glVertex2f(10, -10)
    glEnd()

    glPopMatrix()

def draw_asteroids():
    glColor3f(1, 1, 1)
    for a in asteroids:
        glBegin(GL_LINE_LOOP)
        for p in a["shape"]:
            glVertex2f(p[0], p[1])
        glEnd()

def draw_bullets():
    glColor3f(1, 1, 1)  
    glBegin(GL_POINTS)
    for b in bullets:
        glVertex2f(b[0], b[1])
    glEnd()

def draw_score():
    glColor3f(1, 1, 0)
    glRasterPos2f(10, H - 20)
    text = f"Score: {score}"
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def update(value):
    global bullets

  
    new_bullets = []
    for x, y, vx, vy in bullets:
        x += vx
        y += vy

        if 0 <= x <= W and 0 <= y <= H:
            new_bullets.append((x, y, vx, vy))

    bullets = new_bullets

   
    for a in asteroids:
        a["x"] += a["vx"]
        a["y"] += a["vy"]

        if a["x"] < 0: a["x"] = W
        if a["x"] > W: a["x"] = 0
        if a["y"] < 0: a["y"] = H
        if a["y"] > H: a["y"] = 0

        a["shape"] = generate_asteroid(a["x"], a["y"], a["r"])

    check_bullet_collision()
    check_ship_collision()

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_ship()
    draw_asteroids()
    draw_bullets()
    draw_score()

    glutSwapBuffers()


def special_keys(key, x, y):
    global ship_x, ship_y

    speed = 8

    if key == GLUT_KEY_UP:
        ship_y += speed
    elif key == GLUT_KEY_DOWN:
        ship_y -= speed
    elif key == GLUT_KEY_LEFT:
        ship_x -= speed
    elif key == GLUT_KEY_RIGHT:
        ship_x += speed


def keyboard(key, x, y):
    global bullets, ship_x, ship_y

    if key == b' ':
        bullets.append((ship_x, ship_y, 0, 12))


def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W, 0, H)

    reset_game()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W, H)
glutCreateWindow(b"Asteroids Clone - Score + Destruction")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutTimerFunc(16, update, 0)

glutMainLoop()