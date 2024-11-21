import pygame


class Snake:
    def __init__(self, screen_width, screen_height, grid_size):
        self.grid_size = grid_size
        self.positions = [
            (screen_width // 2, screen_height // 2),
            (screen_width // 2 - grid_size, screen_height // 2),
            (screen_width // 2 - 2 * grid_size, screen_height // 2)
        ]
        self.direction = (1, 0)
        self.moving = False
        self.length = 3

    def change_direction(self, direction):
        if direction == "UP" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif direction == "DOWN" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif direction == "LEFT" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == "RIGHT" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def move(self):
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x * self.grid_size, head_y + delta_y * self.grid_size)
        self.positions = [new_head] + self.positions[:self.length - 1]

    def grow(self):
        self.length += 1

    def head_position(self):
        return self.positions[0]

    def check_collision(self, screen_width, screen_height):
        head_x, head_y = self.head_position()

        if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height:
            return True
        if len(self.positions) != len(set(self.positions)):
            return True
        return False

    def draw_snake(self, surface):
        start_color = (0, 255, 0)

        end_color = (0, 100, 0)
        delta_r = end_color[0] - start_color[0]
        delta_g = end_color[1] - start_color[1]
        delta_b = end_color[2] - start_color[2]

        radius = self.grid_size // 4

        for i, part in enumerate(self.positions):
            ratio = i / len(self.positions)
            color = (
                int(start_color[0] + ratio * delta_r),
                int(start_color[1] + ratio * delta_g),
                int(start_color[2] + ratio * delta_b)
            )
            rect = pygame.Rect(part[0], part[1], self.grid_size, self.grid_size)
            pygame.draw.rect(surface, color, rect, border_radius=radius)