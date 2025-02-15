import os
import pickle

from settings import *
import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Game:
    def __init__(self, genomes, config, map_file, test_mode=False):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Self Driving Car Simulator')

        self.map_file = map_file
        self.map_image = pygame.image.load(self.map_file).convert()
        self.map_image = pygame.transform.scale(self.map_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.genomes = genomes
        self.config = config
        self.cars = []
        self.nets = []
        self.test_mode = test_mode

        # Create filenames for saving/loading based on the map
        base_name = os.path.splitext(os.path.basename(self.map_file))[0]
        self.saved_genome_file = f"{base_name}_best_genome.pkl"
        self.saved_start_position_file = f"{base_name}_start_position.pkl"

        if self.test_mode:
            self.load_best_car()
        else:
            self.initialize_cars()

    def load_best_car(self):
        if os.path.exists(self.saved_genome_file) and os.path.exists(self.saved_start_position_file):
            print("Loading best genome and start position for testing...")
            try:
                with open(self.saved_genome_file, "rb") as f:
                    best_genome = pickle.load(f)
                    print("Loaded genome:", best_genome)

                # Validate the loaded genome
                if not hasattr(best_genome, 'key') or not hasattr(best_genome, 'fitness'):
                    raise ValueError("Loaded genome is invalid. Missing required attributes.")

                with open(self.saved_start_position_file, "rb") as f:
                    start_position = pickle.load(f)
                    print("Loaded start position:", start_position)

                net = neat.nn.FeedForwardNetwork.create(best_genome, self.config)
                self.cars.append(Car(self.map_image, start_position, 90, net, best_genome))
            except Exception as e:
                print(f"Error loading saved data: {e}")
                sys.exit()
        else:
            print("No saved data found. Please train the model first.")
            sys.exit()

    def initialize_cars(self):
        for genome_id, genome in self.genomes:
            genome.fitness = 0.0
            net = neat.nn.FeedForwardNetwork.create(genome, self.config)
            self.nets.append(net)
            spawn_position = self.get_random_spawn()
            self.cars.append(Car(self.map_image, spawn_position, 90, net, genome))

    def get_random_spawn(self):
        while True:
            x = random.randint(0, WINDOW_WIDTH - 1)
            y = random.randint(0, WINDOW_HEIGHT - 1)
            if self.map_image.get_at((x, y))[:3] == (0, 0, 0):
                return [x, y]

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            still_alive = 0
            for i, car in enumerate(self.cars):
                if car.alive:
                    still_alive += 1
                    inputs = car.get_inputs()
                    outputs = car.net.activate(inputs)
                    car.update(outputs)
                    car.genome.fitness += car.calculate_reward()

            if still_alive == 0:
                break

            self.display_surface.blit(self.map_image, (0, 0))
            for car in self.cars:
                if car.alive:
                    car.draw(self.display_surface)

            pygame.display.update()
            clock.tick(60)

        if not self.test_mode:
            self.save_best_genome()

    def save_best_genome(self):
        try:
            best_car = max(self.cars, key=lambda car: car.genome.fitness)
            with open(self.saved_genome_file, "wb") as f:
                pickle.dump(best_car.genome, f)
                print("Genome successfully saved.")

            with open(self.saved_start_position_file, "wb") as f:
                pickle.dump(best_car.rect.center, f)
                print("Start position successfully saved.")
        except Exception as e:
            print(f"Error saving best genome: {e}")

class Car:
    def __init__(self, map_image, spawn_position, spawn_angle, net, genome):
        self.map_image = map_image
        self.net = net
        self.genome = genome

        self.image = pygame.image.load("car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (CAR_SIZE, CAR_SIZE))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=spawn_position)

        self.spawn_position = spawn_position
        self.spawn_angle = spawn_angle
        self.angle = spawn_angle
        self.alive = True
        self.speed = 2
        self.distance = 0
        self.time_alive = 0
        self.radars = []
        self.previous_positions = []
        self.no_progress_timer = 0
        self.last_fitness = 0
        self.rotation_sum = 0

    def reset(self):
        self.rect.center = self.spawn_position
        self.angle = self.spawn_angle
        self.image = self.original_image.copy()
        self.alive = True
        self.distance = 0
        self.time_alive = 0
        self.previous_positions = []
        self.no_progress_timer = 0
        self.last_fitness = 0
        self.rotation_sum = 0

    def rotate(self, angle):
        self.angle += angle
        self.rotation_sum += abs(angle)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def is_on_track(self, x, y):
        if 0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT:
            color = self.map_image.get_at((x, y))[:3]
            return all(c < 50 for c in color)
        return False

    def check_radar(self, degree):
        length = 0
        x = int(self.rect.centerx + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.rect.centery + math.sin(math.radians(360 - (self.angle + degree))) * length)

        while self.is_on_track(x, y) and length < 500:
            length += 1
            x = int(self.rect.centerx + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.rect.centery + math.sin(math.radians(360 - (self.angle + degree))) * length)

        self.radars.append(length)

    def get_inputs(self):
        self.radars = []
        for angle in [-135, -90, -45, 0, 45, 90, 135]:
            self.check_radar(angle)
        return [r / 500.0 for r in self.radars]

    def calculate_reward(self):
        if not self.is_on_track(self.rect.centerx, self.rect.centery):
            self.alive = False
            return -20

        current_position = (int(self.rect.centerx), int(self.rect.centery))
        if len(self.previous_positions) > 10:
            self.previous_positions.pop(0)
        self.previous_positions.append(current_position)

        if self.previous_positions.count(current_position) > 5:
            self.alive = False
            return -10

        if abs(self.genome.fitness - self.last_fitness) < 1:
            self.no_progress_timer += 1
        else:
            self.no_progress_timer = 0
        self.last_fitness = self.genome.fitness

        if self.no_progress_timer > 50:
            self.alive = False
            return -15

        if self.rotation_sum > 360 * 3:
            self.alive = False
            return -15

        return self.speed / 5 + sum(self.radars) / 2100.0

    def update(self, outputs):
        if not self.alive:
            return

        decision = outputs.index(max(outputs))

        if decision == 0:
            self.speed = min(self.speed + 0.5, 6)
        elif decision == 1:
            self.speed = max(self.speed - 0.5, 1)
        elif decision == 2:
            self.rotate(10)
        elif decision == 3:
            self.rotate(-10)

        self.rect.x += math.cos(math.radians(360 - self.angle)) * self.speed
        self.rect.y += math.sin(math.radians(360 - self.angle)) * self.speed

    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


best_fitness_per_gen = []
avg_fitness_per_gen = []


def eval_genomes(genomes, config):
    global best_fitness_per_gen, avg_fitness_per_gen

    fitness_values = []
    game = Game(genomes, config, MAP_FILE)
    game.run()

    for genome_id, genome in genomes:
        fitness_values.append(genome.fitness)

    best_fitness_per_gen.append(max(fitness_values))
    avg_fitness_per_gen.append(sum(fitness_values) / len(fitness_values))

def plot_fitness():
    plt.figure(figsize=(10, 6))
    plt.plot(best_fitness_per_gen, label="Best Fitness", marker="o")
    plt.plot(avg_fitness_per_gen, label="Average Fitness", linestyle="--")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness Over Generations")
    plt.legend()
    plt.savefig("fitness_plot.png")
    plt.close()

def run_neat(config_file):
    global MAP_FILE

    MAP_FILE = input("Enter the path to the map file (e.g., 'racetrack.jpg'): ")

    if not os.path.exists(MAP_FILE):
        print("Map file not found. Please provide a valid path.")
        sys.exit()

    if os.path.exists(f"{os.path.splitext(os.path.basename(MAP_FILE))[0]}_best_genome.pkl"):
        print("Running in test mode with saved genome.")
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file
        )
        game = Game([], config, MAP_FILE, test_mode=True)
        game.run()
    else:
        print("No saved genome found. Training from scratch.")
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file
        )
        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())
        population.add_reporter(neat.Checkpointer(5))

        winner = population.run(eval_genomes, 50)
        plot_fitness()
        print(f"Training complete. Best genome: {winner}")

if __name__ == "__main__":
    run_neat("config-feedforward.txt")