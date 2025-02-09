from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

STONE_COLOR = (0, 0, 255)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Абстрактный метод."""
        pass


class Apple(GameObject):
    """Класс яблоко, унаследованный от базового класса."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Метод генерации случайного расположения яблока на игровом поле.
        В прекоде ошибка. Секций 640/20 = 32,
        индексация начинается с нуля,
        поэтому ячейка 32 выходит за пределы игрового поля,
        последняя должна быть 31
        """
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Метод прорисовки яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(Apple):
    """Класс камень, унаследованный от класса яблоко."""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """Класс змея, унаследованный от базового класса."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.lenght = 1

    def reset(self):
        """Метод сброса состояния змеи после проигрыша."""
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )
        self.next_direction = None
        screen.fill(
            BOARD_BACKGROUND_COLOR
        )

    def get_head_position(self):
        """Метод возвращает позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """
        Метод обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        head_position = self.get_head_position()
        head_x_position, head_y_position = self.direction
        new_head_position = (
            (head_position[0] + head_x_position * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + head_y_position * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        self.last = self.positions.pop()

    def draw(self):
        """Метод прорисовки змеи на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновляет направление змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Функция обработки нажатия клавиш управления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    stone = Stone()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()
        pygame.display.update()
        # Если змея укусила яблоко. Генерация нового расположения яблока.
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            snake.positions.append(snake.last)
            apple.randomize_position()
            stone.randomize_position()
        # Если длина змеи кратна 5, то появляется один камень.
        if snake.lenght % 5 == 0:
            stone.draw()
        # Если змея столкнулась с собой. Сброс состояния змеи и яблока.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
        # Если голова змеи столкнулась с камнем - проигрыш.
        if snake.get_head_position() == stone.position:
            snake.reset()
            apple.randomize_position()


if __name__ == '__main__':
    main()
