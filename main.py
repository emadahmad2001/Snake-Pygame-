"""
    Snake Game
    CCT 211
    Assignment
    Emad Ahmad (1006469769)
"""
import random
import pygame


class Game:
    """ This class represents the Game. It contains all the game objects. """

    def __init__(self):
        """ Set up the game on creation. """

        # Initialize Pygame
        pygame.init()

        self.font_style = pygame.font.SysFont(name="chalkduster.ttf",
                                              size=25, bold=True)
        self.score_font = pygame.font.SysFont(name="chalkduster.ttf",
                                              size=25, bold=True)

        # --- Create the window
        # Set the height and width of the screen
        self.screen_width = 640
        self.screen_height = 480
        self.middle_x = self.screen_width // 6
        self.middle_y = self.screen_height // 3
        self.centre = [self.middle_x, self.middle_y]

        self.screen = pygame.display.set_mode(
            [self.screen_width, self.screen_height])

        # initialize the movement of the game
        self.snake_block = 10
        self.snake_speed = 15
        self.running = True

        pygame.display.set_caption('Snake Game by Emad')

    def update_score(self, score: int) -> None:
        """
        updates the score of the player and is called when food is eaten

        :param score: an integer value of your score prior to incrementation
        :return: None
        """
        current_score = self.score_font.render("Score: " + str(score),
                                               True,
                                               pygame.color.THECOLORS["green"])
        self.screen.blit(current_score, [0, 0])

    def update_snake(self, snake_block, snake_list) -> None:
        """
        visually updates a snake body when a food is eaten

        :param snake_block: the index of the snake bodu
        :param snake_list: List of snake bodies
        :return: None
        """
        for snake in snake_list:
            pygame.draw.rect(self.screen, pygame.color.THECOLORS["black"],
                             [snake[0], snake[1], snake_block, snake_block])

    def losing_message(self, s, colour):
        """
        renders and blits the message the player will see once they lose the game

        :param s: the message to be blit
        :param colour: the colour the message will be
        :return:
        """
        message = self.font_style.render(s, True, colour)
        self.screen.blit(message, self.centre)

    def poll(self):
        """
        processes all events
        :return: None
        """
        clock = pygame.time.Clock()
        x, y = self.screen_width / 2, self.screen_height / 2  # starting position
        delta_x, delta_y = 0, 0

        snakes = []
        current_length = 1

        apple_posx = random.randint(15, self.screen_width // 2)
        apple_posy = random.randint(15, self.screen_height // 2)

        lose = False

        while self.running:
            while lose:
                self.screen.fill(pygame.color.THECOLORS["white"])
                self.losing_message("Loser! Press any key to play again, or Q to quit",
                                    pygame.color.THECOLORS["red"])
                Game.update_score(self, score=current_length - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        lose = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.running = False
                            lose = False
                        else:
                            Game.poll(self)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        delta_y = -self.snake_block
                        delta_x = 0

                    elif event.key == pygame.K_DOWN:
                        delta_y = self.snake_block
                        delta_x = 0

                    elif event.key == pygame.K_RIGHT:
                        delta_x = self.snake_block
                        delta_y = 0

                    elif event.key == pygame.K_LEFT:
                        delta_x = -self.snake_block
                        delta_y = 0

            # player losing if snake goes outside the frame

            out_of_bounds = (x >= self.screen_width) or (x < 0) or \
                            (y >= self.screen_height) or (y < 0)
            if out_of_bounds:
                lose = True  # Game still runs but player loses

            x += delta_x
            y += delta_y
            self.screen.fill(pygame.color.THECOLORS["white"])
            pygame.draw.rect(self.screen, pygame.color.THECOLORS["red"],
                             [apple_posx, apple_posy, self.snake_block, self.snake_block])

            snake_head = [x, y]
            snakes.append(snake_head)

            if len(snakes) > current_length:
                del snakes[0]

            # Player loses if snake touches itself

            for snake_body in snakes[:-1]:
                if snake_body == snake_head:
                    lose = True  # Game still runs but player loses

            Game.update_snake(self, self.snake_block, snakes)
            Game.update_score(self, score=current_length - 1)

            pygame.display.update()

            if abs(x - apple_posx) < 6 and abs(y - apple_posy) < 6:
                apple_posx = random.randint(1, self.screen_width - self.snake_block)
                apple_posy = random.randint(1, self.screen_height - self.snake_block)
                current_length += 1

            clock.tick(self.snake_speed)

    def draw(self):
        """
        Draws frame
        :return: None
        """
        # Clear the screen
        self.screen.fill(pygame.color.THECOLORS['white'])

    def run(self):

        self.running = True
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while self.running:
            # --- Event processing and Game logic
            self.poll()

            # --- Draw a frame
            self.draw()

            # Update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit the frames per second
            clock.tick(60)


if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shuting down...")
    pygame.quit()
