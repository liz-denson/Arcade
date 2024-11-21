
import random
import pygame
import os


class Food:
    def __init__(self, screen_width, screen_height, grid_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.position = None


        fruit_directory = os.path.join(os.path.dirname(__file__), 'fruit')
        self.images = [pygame.image.load(os.path.join(fruit_directory, img))
                       for img in os.listdir(fruit_directory)
                       if img.endswith('.png')]

        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.spawn_food([])

    def spawn_food(self, snake_positions):
        while True:
            x = random.randint(0, (self.screen_width // self.grid_size) - 1) * self.grid_size
            y = random.randint(0, (self.screen_height // self.grid_size) - 1) * self.grid_size
            new_position = (x, y)
            if all(abs(x - sx) >= self.grid_size * 5 or abs(y - sy) >= self.grid_size * 5 for sx, sy in
                   snake_positions):
                self.position = new_position
                break


        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.image = pygame.transform.scale(self.images[self.current_image_index], (self.grid_size, self.grid_size))

    def draw_food(self, surface):
        scaled_image = pygame.transform.scale(self.image, (self.grid_size, self.grid_size))
        surface.blit(scaled_image, self.position)
