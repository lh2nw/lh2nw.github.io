from random import randint

WIDTH = 800
HEIGHT = 600

# Updated Actors based on your folder screenshots
plane = Actor("plane")
plane.pos = 100, 300

storm = Actor("stormcloud")
storm.pos = randint(800, 1600), randint(50, 200)

building = Actor("skyscraper")
building.pos = randint(800, 1600), 530  # Skyscrapers stay on the ground

# New scenery element
tree = Actor("tree")
tree.pos = randint(800, 1600), 530

up = False
game_over = False
score = 0
scores = []

# Update music to your new file
music.play("airplanesound")


def draw():
    screen.blit("background", (0, 0))
    plane.draw()
    storm.draw()
    building.draw()
    tree.draw()
    screen.draw.text("Score: " + str(score), (700, 5), color="black")

    if game_over:
        screen.draw.text("GAME OVER", center=(400, 300), color="red", fontsize=60)
        screen.draw.text("Final Score: " + str(score), center=(400, 350), color="black")


def update():
    global game_over, score

    if not game_over:
        # Smooth 'Lift' Logic
        if up:
            plane.y -= 4
            plane.angle = 15
        else:
            plane.y += 3
            plane.angle = -15

        # Move the world (Parallax effect)
        # Storms move fast, buildings/trees move slower
        storm.x -= 6
        building.x -= 3
        tree.x -= 3

        # Reset obstacles and increase score
        if storm.right < 0:
            storm.pos = randint(800, 1600), randint(50, 200)
            score += 1

        if building.right < 0:
            building.x = randint(800, 1600)
            score += 1

        if tree.right < 0:
            tree.x = randint(800, 1600)

        # Boundary and Collision checks
        if plane.top < 0 or plane.bottom > 600:
            game_over = True
            update_high_scores()

        if plane.colliderect(storm) or plane.colliderect(building):
            game_over = True
            update_high_scores()


# Keep your existing mouse and high-score functions here...
def on_mouse_down():
    global up
    up = True


def on_mouse_up():
    global up
    up = False

def update_high_scores():
    # You can leave this empty for now
    pass