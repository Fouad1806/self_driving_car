# Contains every presetting that I need and easily adjustable
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Self Driving Car Simulator')

        # Create a car instance
        self.car = Car(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

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

            # Draw everything
            self.display_surface.fill((255, 255, 255))
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Define the car
        self.image = pygame.image.load("car.png")
        self.image = pygame.transform.scale(self.image, (CAR_SIZE, CAR_SIZE))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed


game = Game()
game.run()

