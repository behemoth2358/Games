import pygame, sys, random, time

class Game:
    def __init__(self):
        status = pygame.init()

        if (status[1] > 0):
            print ("Had errors!")
            sys.exit()
        else:
            print ("Snake game started successfully!")

        pygame.display.set_caption('Snake')

        self.__surface = pygame.display.set_mode((720,460))
        self.__fps_controller = pygame.time.Clock()

        self.__snake_pos = [100,50]
        self.__snake_body = [[100, 50], [90, 50], [80, 50]]

        self.__food_pos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10];
        self.__food_spawn = True

        self.__direction = 'RIGHT'
        self.__change_direction_to = self.__direction

        self.__colors = self.__get_colors()

    def start(self):

        while (True):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                elif (event.type == pygame.KEYDOWN):
                    if (event.key in (pygame.K_RIGHT, ord('d'))):
                        self.__change_direction_to = 'RIGHT'
                    if (event.key in (pygame.K_LEFT, ord('a'))):
                        self.__change_direction_to = 'LEFT'
                    if (event.key in (pygame.K_UP, ord('w'))):
                        self.__change_direction_to = 'UP'
                    if (event.key in (pygame.K_DOWN, ord('s'))):
                        self.__change_direction_to = 'DOWN'
                    if (event.key == pygame.K_ESCAPE):
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # validation of direction
            if (self.__change_direction_to == 'RIGHT' and not self.__direction == 'LEFT'):
                self.__direction = 'RIGHT'
            if (self.__change_direction_to == 'LEFT' and not self.__direction == 'RIGHT'):
                self.__direction = 'LEFT'
            if (self.__change_direction_to == 'UP' and not self.__direction == 'DOWN'):
                self.__direction = 'UP'
            if (self.__change_direction_to == 'DOWN' and not self.__direction == 'UP'):
                self.__direction = 'DOWN'

            if (self.__direction == 'RIGHT'):
                self.__snake_pos[0] += 10
            if (self.__direction == 'LEFT'):
                self.__snake_pos[0] -= 10
            if (self.__direction == 'UP'):
                self.__snake_pos[1] -= 10
            if (self.__direction == 'DOWN'):
                self.__snake_pos[1] += 10

            # Snake body mechanism

            self.__snake_body.insert(0, list(self.__snake_pos))
            if (self.__snake_pos[0] == self.__food_pos[0] and self.__snake_pos[1] == self.__food_pos[1]):
                self.__food_spawn = False
            else:
                self.__snake_body.pop()

            if (self.__food_spawn == False):
                self.__food_pos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10];
                self.__food_spawn = True

            self.__surface.fill(self.__colors['white'])

            for pos in self.__snake_body:
                pygame.draw.rect(self.__surface, self.__colors['green'], pygame.Rect(pos[0], pos[1], 10, 10))

            pygame.draw.rect(self.__surface, self.__colors['brown'], pygame.Rect(self.__food_pos[0], self.__food_pos[1], 10, 10))

            self.__show_score()

            if (self.__snake_pos[0] > 710 or self.__snake_pos[0] < 0):
                self.__game_over()
            if (self.__snake_pos[1] > 450 or self.__snake_pos[1] < 0):
                self.__game_over()

            for block in self.__snake_body[1:]:
                if (self.__snake_pos[0] == block[0] and self.__snake_pos[1] == block[1]):
                    self.__game_over()

            pygame.display.flip()
            self.__fps_controller.tick(15)

    def __get_colors(self):
        colors_dict = {}

        colors_dict['red'] = pygame.Color(255, 0, 0)
        colors_dict['green'] = pygame.Color(0, 255, 0)
        colors_dict['black'] = pygame.Color(0, 0, 0)
        colors_dict['white'] = pygame.Color(255, 255, 255)
        colors_dict['brown'] = pygame.Color(165, 42, 42)

        return colors_dict

    def __game_over(self):

        game_over_font = pygame.font.SysFont('font', 72)
        game_over_surface = game_over_font.render('Game over!', True, self.__colors['red'])
        game_over_form = game_over_surface.get_rect()
        game_over_form.midtop = (360, 15)

        self.__surface.blit(game_over_surface, game_over_form)

        pygame.display.flip()
        time.sleep(3)
        sys.exit()

    def __show_score(self):
        score_font = pygame.font.SysFont('font', 24)
        score_surface = score_font.render('Score: ' + str(len(self.__snake_body)), True, self.__colors['red'])
        score_form = score_surface.get_rect()
        score_form.midtop = (80, 10)
        self.__surface.blit(score_surface, score_form)


if __name__ == "__main__":
    game = Game()
    game.start()
