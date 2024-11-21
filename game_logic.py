import pygame
import time
from snake import Snake
from food import Food


def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    current_line_width = 0

    for word in words:
        word_surface = font.render(word, True, (255, 255, 255))
        word_width = word_surface.get_width()
        if current_line_width + word_width <= max_width:
            current_line.append(word)
            current_line_width += word_width + font.size(' ')[0]
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_line_width = word_width + font.size(' ')[0]
    lines.append(' '.join(current_line))
    return lines


def exit_game():
    pygame.quit()
    exit(0)


class Game:
    def __init__(self, username="", screen_width=600, screen_height=600, grid_size=20, skip_instructions=False):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.screen_width, self.screen_height, self.grid_size)
        self.food = Food(self.screen_width, self.screen_height, self.grid_size)
        self.running = True
        self.paused = False
        self.score = 0
        self.font = pygame.font.Font(None, 30)
        self.large_font = pygame.font.Font(None, 40)
        self.speed = 5
        self.username = username
        self.skip_instructions = skip_instructions
        self.username_input_active = not skip_instructions
        self.input_text = username if username else ""
        self.cursor_visible = True
        self.cursor_last_switch = time.time()
        self.buttons = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.username_input_active:
                    mouse_pos = event.pos
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            button["callback"]()
            elif event.type == pygame.KEYDOWN:
                if self.username_input_active:
                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip():
                            self.username = self.input_text
                            self.username_input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction("UP")
                        self.snake.moving = True
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("DOWN")
                        self.snake.moving = True
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("LEFT")
                        self.snake.moving = True
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("RIGHT")
                        self.snake.moving = True
                    elif event.key == pygame.K_SPACE:
                        self.snake.moving = not self.snake.moving

    def update(self):
        current_time = time.time()
        if current_time - self.cursor_last_switch > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_last_switch = current_time

        if self.snake.moving and not self.paused and not self.username_input_active:
            self.snake.move()
            if self.snake.head_position() == self.food.position:
                self.snake.grow()
                self.score += 1
                self.food.spawn_food(self.snake.positions)
            if self.snake.check_collision(self.screen_width, self.screen_height):
                self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.username_input_active:
            self.display_instructions_and_input()
        else:
            self.snake.draw_snake(self.screen)
            self.food.draw_food(self.screen)
            self.display_score()
        pygame.display.flip()

    def display_instructions_and_input(self):
        instructions = (
            "Welcome to the Snake Game!\n\n"
            "Instructions:\n"
            "1. Use UP, DOWN, LEFT, and RIGHT arrow keys to control the snake's direction.\n"
            "2. Eat the food (apple) to grow longer.\n"
            "3. Avoid colliding with the walls or the snake's own body.\n"
            "4. The game ends when the snake collides with itself or the boundaries.\n"
            "\nPress ENTER to submit your name."
        )

        wrapped_instructions = []
        for line in instructions.split('\n'):
            wrapped_instructions.extend(wrap_text(line, self.font, self.screen_width - 40))

        y_offset = 50
        for line in wrapped_instructions:
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, y_offset))
            y_offset += 30

        if self.cursor_visible:
            input_text_with_cursor = self.input_text + "|"
        else:
            input_text_with_cursor = self.input_text

        input_surface = self.large_font.render(f"Your Name: {input_text_with_cursor}", True, (255, 255, 255))
        input_rect = input_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(input_surface, input_rect)

    def display_score(self):
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def draw_button(self, text, x, y, callback):
        button_font = pygame.font.Font(None, 36)
        button_surface = button_font.render(text, True, (255, 255, 255))

        button_width = 200
        button_height = 50
        button_rect = button_surface.get_rect(center=(x, y))


        real_button_rect = pygame.Rect(0, 0, button_width, button_height)
        real_button_rect.center = button_rect.center

        pygame.draw.rect(self.screen, (0, 100, 200), real_button_rect)


        self.screen.blit(button_surface, button_surface.get_rect(center=real_button_rect.center))

        self.buttons.append({
            "rect": real_button_rect,
            "callback": callback
        })

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
        self.show_game_over()

    def show_game_over(self):
        self.buttons.clear()

        game_over_texts = [
            "Game Over!",
            f"{self.username}, your score is {self.score}.",
            ""
        ]

        y_offset = self.screen_height // 2 - 50

        text_surfaces = []
        for text in game_over_texts:
            surface = self.large_font.render(text, True, (255, 255, 255))
            rect = surface.get_rect(center=(self.screen_width // 2, y_offset))
            text_surfaces.append((surface, rect))
            y_offset += 50

        play_again_text = "Play Again"
        exit_text = "Exit"

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            button["callback"]()

            self.screen.fill((0, 0, 0))

            for surface, rect in text_surfaces:
                self.screen.blit(surface, rect)

            self.draw_button(play_again_text, self.screen_width // 2, self.screen_height // 2 + 100, self.restart_game)
            self.draw_button(exit_text, self.screen_width // 2, self.screen_height // 2 + 160, exit_game)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def restart_game(self):
        self.__init__(username=self.username, skip_instructions=True)
        self.run()