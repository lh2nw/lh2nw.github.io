from random import randint
WIDTH = 800
HEIGHT = 600
mario = Actor("wario")
mario.pos = 400, 300
bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)
house = Actor("house")
house.pos = randint(800, 1600), 460
pipe = Actor("pipe")
pipe.pos = randint(800, 1600), 450
bird_up = True
up = False
game_over = False
score = 0
number_of_updates = 0

scores = []

def update_high_scores():
    global score, scores
    filename = r"./high-scores.txt"
    scores = []
    with open(filename, "r") as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if(score > int(high_score)):
                scores.append(str(score) + " ")
                score = int(high_score)
            else:
                scores.append(str(high_score) + " ")
    with open(filename, "w") as file:
        for high_score in scores:
            file.write(high_score)

def display_high_scores():
    screen.draw.text("HIGH SCORES", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + ". " + high_score, (350, y), color="black")
        y += 25
        position += 1

def draw():
    screen.blit("background", (0, 0))
    if not game_over:
        mario.draw()
        bird.draw()
        house.draw()
        pipe.draw()
        screen.draw.text("Score: " + str(score), (700, 5), color="black")
    else:
        display_high_scores()

def on_mouse_down():
    global up
    up = True
    mario.y -= 25

def on_mouse_up():
    global up
    up = False

def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True

music.play("mariomusic")

def update():
    global game_over, score, number_of_updates
    if not game_over:
        if not up:
            mario.y += 1
    if bird.x > 0:
        bird.x -= 4
        if number_of_updates == 9:
            flap()
            number_of_updates = 0
        else:
            number_of_updates += 1
    else:
        bird.x = randint(800, 1600)
        bird.y = randint(10, 200)
        score += 1
        number_of_updates = 0

    if house.right > 0:
        house.x -= 2
    else:
        house.x = randint(800, 1600)
        score += 1

    if pipe.right > 0:
        pipe.x -= 2
    else:
        pipe.x = randint(800, 1600)
        score += 1

    if mario.top < 0 or mario.bottom > 560:
        game_over = True
        update_high_scores()

    if mario.collidepoint(bird.x, bird.y) or \
        mario.collidepoint(house.x, house.y) or \
        mario.collidepoint(pipe.x, pipe.y):
            game_over = True
            update_high_scores()