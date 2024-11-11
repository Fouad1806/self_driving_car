# Contains every presetting that I need and easily adjustable
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Self Driving Car Simulator')
        
        # Load background image
        self.background = pygame.image.load("racetrack.jpg")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Create a car instance
        self.car = Car(self.background)

        # Sprite group to manage the car
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.car)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Update all sprites
            self.all_sprites.update()

            # Draw background first
            self.display_surface.blit(self.background, (0, 0))

            # Draw everything
            #self.display_surface.fill((255, 255, 255))
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

class Car(pygame.sprite.Sprite):
    def __init__(self, game_map):
        super().__init__()

        # Define the car
        self.original_image = pygame.image.load("car.png")
        self.original_image = pygame.transform.scale(self.original_image, (CAR_SIZE, CAR_SIZE))
        self.image = self.original_image  # The rotated image for display

        self.game_map = game_map

        self.rect = self.image.get_rect()
        self.rect.center = self.get_black_spawn_position()

        self.speed = 1
        self.angle = 0  # Initialize angle

    def rotate(self, angle):
        # Rotate the car and update the rect center to maintain position
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_black_spawn_position(self):
        width, height = self.game_map.get_size()
        max_attempts = 5000

        for attempt in range(max_attempts):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if self.is_black(x, y):
                print(f"Spawned on black pixel at ({x}, {y}) after {attempt} attempts")
                return x, y

        # Fallback: Warn and place near the center if no black pixel found
        print("Warning: Couldn't find a black pixel in the entire image. Placing at (width // 2, height // 2)")
        return width // 2, height // 2


    def is_black(self, x, y):
        # Get image dimensions
        width, height = self.game_map.get_size()

        # Check if (x, y) is within bounds
        if x < 0 or x >= width or y < 0 or y >= height:
            print(f"Out of bounds at ({x}, {y})")
            return False  # Treat out-of-bounds as non-black

        # Get the color of the pixel and print for debugging
        color = self.game_map.get_at((x, y))[:3]
        print(f"Checking color at ({x}, {y}): {color}")  # Print color for debugging

        # Return True if color is strictly black or near black (darker than (50, 50, 50))
        return all(c < 50 for c in color)  # Stricter thresh


    def can_move(self, direction):
        # Check specific pixels in the direction of movement
        if direction == 'left':
            return self.is_black(self.rect.left - self.speed, self.rect.centery)
        elif direction == 'right':
            return self.is_black(self.rect.right + self.speed, self.rect.centery)
        elif direction == 'up':
            return self.is_black(self.rect.centerx, self.rect.top - self.speed)
        elif direction == 'down':
            return self.is_black(self.rect.centerx, self.rect.bottom + self.speed)
        return False

    def update(self):
        keys = pygame.key.get_pressed()
        initial_position = self.rect.center
        moved = False  # Track if the car has successfully moved

        # Movement flags
        blocked_left = blocked_right = blocked_up = blocked_down = False

        # Check each direction and only move if the direction is clear
        if keys[pygame.K_LEFT] and self.can_move('left'):
            self.rect.x -= self.speed
            self.rotate(90)  # Face left
            moved = True
        elif keys[pygame.K_LEFT]:
            blocked_left = True

        if keys[pygame.K_RIGHT] and self.can_move('right'):
            self.rect.x += self.speed
            self.rotate(-90)  # Face right
            moved = True
        elif keys[pygame.K_RIGHT]:
            blocked_right = True

        if keys[pygame.K_UP] and self.can_move('up'):
            self.rect.y -= self.speed
            self.rotate(0)  # Face up
            moved = True
        elif keys[pygame.K_UP]:
            blocked_up = True

        if keys[pygame.K_DOWN] and self.can_move('down'):
            self.rect.y += self.speed
            self.rotate(180)  # Face down
            moved = True
        elif keys[pygame.K_DOWN]:
            blocked_down = True

        # Check if the car is in a non-track area and reset if so
        if not self.is_black(self.rect.centerx, self.rect.centery) and moved:
            print(f"Crash at position: {self.rect.center}")
            self.rect.center = initial_position

        # Detect if the car is completely stuck
        if not moved and (blocked_left or blocked_right or blocked_up or blocked_down):
            print("Car is completely stuck at position:", self.rect.center)



game = Game()
game.run()

