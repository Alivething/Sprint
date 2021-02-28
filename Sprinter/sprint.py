from collections import deque, namedtuple
from random import randint

import pyxel

Point = namedtuple("Point", ["x", "y"])  # Convenience class for coordinates


#############
# Constants #
#############

COL_BACKGROUND = 3
COL_BODY = 11
COL_HEAD = 7
COL_DEATH = 8
COL_APPLE1 = 8
COL_APPLE2 = 9
COL_APPLE3 = 10

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 5

TEXT_PUSH = ["30 Pushups", "2 mins", "(N)EXT" , "(Q)UIT"]

TEXT_SIT = ["30 Situps", "2 mins", "(N)EXT" , "(Q)UIT"]

TEXT_JUMP = ["30 Starjumps", "2 mins", "(N)EXT" , "(Q)UIT"]

WIDTH = 50
HEIGHT = 60

HEIGHT_SCORE = pyxel.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)

START = Point(5, 5 + HEIGHT_SCORE)


###################
# The game itself #
###################


class Snake:
    """The class that sets up and runs the game."""

    def __init__(self):
        """Initiate pyxel, set up initial game variables, and run."""

        pyxel.init(WIDTH, HEIGHT, caption="Sprint!", fps=40)
        define_sound_and_music()
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Initiate key variables (direction, snake, apple, score, etc.)"""

        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)
        self.death = 0
        self.score = 0
        self.generate_apple1()
        self.generate_apple2()
        self.generate_apple3()

        pyxel.playm(0, loop=True)

    def resume(self):
        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)
        self.death = 0
        self.check_apple1()
        self.check_apple2()
        self.check_apple3()

        pyxel.playm(0, loop=True)
        
    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Updates the snake and checks for scoring/win condition."""

        if not self.death:
            self.update_direction()
            #self.update_snake()
            self.check_death()
            self.check_apple1()
            self.check_apple2()
            self.check_apple3()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_N):
            self.resume()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def update_direction(self):
        """Watch the keys and change direction."""

        if pyxel.btn(pyxel.KEY_UP):
            self.direction = UP
            self.update_snake()
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction = DOWN
            self.update_snake()
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.direction = LEFT
            self.update_snake()
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = RIGHT
            self.update_snake()
            

    def update_snake(self):
        """Move the snake based on the direction."""

        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x, old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        self.popped_point = self.snake.pop()

    def check_apple1(self):
        """Check whether the snake is on an apple."""

        if self.snake[0] == self.apple1:
            self.score += 1
            self.death = 21
            self.draw_push()
            #self.snake.append(self.popped_point)
            self.generate_apple1()

            pyxel.play(0, 0)

    def check_apple2(self):
        """Check whether the snake is on an apple."""

        if self.snake[0] == self.apple2:
            self.score += 1
            self.death = 22
            self.draw_sit()
            #self.snake.append(self.popped_point)
            self.generate_apple2()

            pyxel.play(0, 0)

    def check_apple3(self):
        """Check whether the snake is on an apple."""

        if self.snake[0] == self.apple3:
            self.score += 1
            self.death = 23
            self.draw_jump()
            #self.snake.append(self.popped_point)
            self.generate_apple3()

            pyxel.play(0, 0)

    def generate_apple1(self):
        """Generate an apple randomly."""
        snake_pixels = set(self.snake)

        self.apple1 = self.snake[0]
        while self.apple1 in snake_pixels:
            x = randint(0, WIDTH - 1)
            y = randint(HEIGHT_SCORE + 1, HEIGHT - 1)
            self.apple1 = Point(x, y)
            

    def generate_apple2(self):
        """Generate an apple randomly."""
        snake_pixels = set(self.snake)

        self.apple2 = self.snake[0]
        while self.apple2 in snake_pixels:
            x = randint(0, WIDTH - 3)
            y = randint(HEIGHT_SCORE + 3, HEIGHT - 3)
            self.apple2 = Point(x, y)

    def generate_apple3(self):
        """Generate an apple randomly."""
        snake_pixels = set(self.snake)

        self.apple3 = self.snake[0]
        while self.apple3 in snake_pixels:
            x = randint(0, WIDTH - 5)
            y = randint(HEIGHT_SCORE + 5, HEIGHT - 5)
            self.apple3 = Point(x, y)

    def check_death(self):
        """Check whether the snake has died (out of bounds or doubled up.)"""

        head = self.snake[0]
        if head.x < 0 or head.y <= HEIGHT_SCORE or head.x >= WIDTH or head.y >= HEIGHT:
            self.death_event()
        elif len(self.snake) != len(set(self.snake)):
            self.death_event()

    def death_event(self):
        """Kill the game (bring up end screen)."""
        self.death = 1  # Check having run into self
        pyxel.stop()
        pyxel.play(0, 1)
        

    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the background, snake, score, and apple OR the end screen."""

        if(self.death==0):
            pyxel.cls(col=COL_BACKGROUND)
            pyxel.rectb(0,6,WIDTH,HEIGHT-6,0)
            self.draw_snake()
            self.draw_score()
            pyxel.pset(self.apple1.x, self.apple1.y, col=COL_APPLE1)
            pyxel.pset(self.apple2.x, self.apple2.y, col=COL_APPLE2)
            pyxel.pset(self.apple3.x, self.apple3.y, col=COL_APPLE3)

        elif(self.death==1):
            self.draw_death()

        elif(self.death==21):
            self.draw_push()

        elif(self.death==22):
            self.draw_sit()

        elif(self.death==23):
            self.draw_jump()

    def draw_snake(self):
        """Draw the snake with a distinct head by iterating through deque."""
        for i, point in enumerate(self.snake):
            if i == 0:
                colour = COL_HEAD
            else:
                colour = COL_BODY
        pyxel.pset(point.x, point.y, col=colour)

    def draw_score(self):
        """Draw the score at the top."""

        score = "{:04}".format(self.score)
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
        pyxel.text(1, 1, score, COL_SCORE)

    def draw_death(self):
        """Draw a blank screen with some text."""

        pyxel.cls(col=COL_DEATH)
        display_text = TEXT_DEATH[:]
        display_text.insert(1, "{:04}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    def draw_push(self):
        """Draw a blank screen with some text."""

        pyxel.cls(col=COL_DEATH)
        display_text = TEXT_PUSH[:]
        display_text.insert(1, "{:04}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    def draw_jump(self):
        """Draw a blank screen with some text."""

        pyxel.cls(col=COL_DEATH)
        display_text = TEXT_JUMP[:]
        display_text.insert(1, "{:04}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    def draw_sit(self):
        """Draw a blank screen with some text."""

        pyxel.cls(col=COL_DEATH)
        display_text = TEXT_SIT[:]
        display_text.insert(1, "{:04}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Helper function for calcuating the start x value for centered text."""

        text_width = len(text) * char_width
        return (page_width - text_width) // 2


###########################
# Music and sound effects #
###########################


def define_sound_and_music():
    """Define sound and music."""

    # Sound effects
    pyxel.sound(0).set(
        note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
    )
    pyxel.sound(1).set(
        note="f3 b2 f2 b1  f1 f1 f1 f1",
        tone="p",
        volume=("4" * 4 + "4321"),
        effect=("n" * 7 + "f"),
        speed=9,
    )

    melody1 = (
        "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "e3 e3 e3 f3 d3 r c3 r"
        + ("r" * 8)
        + "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "b2 b2 b2 f3 d3 r c3 r"
        + ("r" * 8)
    )

    melody2 = (
        "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
        + "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
    )

    # Music
    pyxel.sound(2).set(
        note=melody1 * 2 + melody2 * 2,
        tone="s",
        volume=("3"),
        effect=("nnnsffff"),
        speed=20,
    )

    harmony1 = (
        "a1 a1 a1 b1  f1 f1 c2 c2"
        "c2 c2 c2 c2  g1 g1 b1 b1" * 3
        + "f1 f1 f1 f1 f1 f1 f1 f1 g1 g1 g1 g1 g1 g1 g1 g1"
    )
    harmony2 = (
        ("f1" * 8 + "g1" * 8 + "a1" * 8 + ("c2" * 7 + "d2")) * 3 + "f1" * 16 + "g1" * 16
    )

    pyxel.sound(3).set(
        note=harmony1 * 2 + harmony2 * 2, tone="t", volume="5", effect="f", speed=20
    )
    pyxel.sound(4).set(
        note=("f0 r a4 r  f0 f0 a4 r" "f0 r a4 r   f0 f0 a4 f0"),
        tone="n",
        volume="6622 6622 6622 6426",
        effect="f",
        speed=20,
    )

    pyxel.music(0).set([], [2], [3], [4])


Snake()
