# Self-Driving Car Simulator with NEAT Algorithm

## Overview
This project implements a self-driving car simulation using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm. The car is trained to navigate a racetrack by evolving a neural network through generations of reinforcement learning.

The simulation consists of multiple cars that learn how to drive using inputs from radar sensors detecting track boundaries. Over time, the best-performing car's genome is saved, allowing it to be tested on new tracks or reused for further improvements.

## Features
- **NEAT-based Evolutionary Training**: The AI evolves over generations, improving driving performance.
- **Radar Sensor System**: The car perceives the track through multiple radar angles.
- **Fitness Evaluation**: The AI is rewarded for staying on the track and penalized for crashing or repetitive movements.
- **Saving & Loading Models**: The best genome from training is saved and can be loaded for testing.
- **Graphical Visualization**: The simulation runs in a Pygame window, showing real-time movement.
- **Fitness Tracking**: A fitness plot is generated to visualize the progress over generations.

## Installation
### Prerequisites
Ensure you have the following dependencies installed:

```bash
pip install neat-python pygame matplotlib
```

### Clone the Repository
```bash
git clone https://github.com/yourusername/self-driving-car-neat.git
cd self-driving-car-neat
```

## Usage
### Training the AI
To train the AI on a track, run the following command:

```bash
python main.py
```

The script will ask for a map file (e.g., `racetrack.jpg`). If no pre-trained model exists, it will start training from scratch. The AI will evolve over multiple generations until an optimal driving behavior is achieved.

### Testing a Pre-trained Model
If a trained model exists (saved as `racetrack_best_genome.pkl`), you can test it by selecting the corresponding map file when prompted.

### Changing the Track
To train on a different track, replace or add a new map image in the project folder and use its filename when prompted.

## Project Structure
```
self-driving-car-neat/
│-- main.py                # Main script for training and testing
│-- settings.py            # Simulation settings and constants
│-- neat-checkpoint-*      # Checkpoints from training (optional)
│-- racetrack.jpg          # Default track image
│-- car.png                # Car sprite
│-- fitness_plot.png       # Generated fitness plot
│-- README.md              # Documentation
```

## NEAT Configuration (config-feedforward.txt)

This file controls the settings for the NEAT algorithm.

### Key Parameters:

pop_size = 50 → Number of cars per generation.

num_inputs = 7 → Number of radar sensor inputs.

num_outputs = 4 → Outputs: accelerate, brake, left, right.

num_hidden = 2 → Hidden layers in the neural network.

fitness_threshold = 700 → The fitness score required for the model to be considered "successful".

max_stagnation = 15 → Number of generations without improvement before species go extinct.

conn_add_prob = 0.6 → Probability of adding a connection during mutation.

node_add_prob = 0.4 → Probability of adding a new neuron.

max_nodes = 50 → Maximum allowed nodes in the network.

max_connections = 100 → Maximum allowed connections.

activation_options = tanh sigmoid relu → Activation functions used in the neural network.

## Troubleshooting
- **All species extinct error**: This means the NEAT algorithm failed to evolve useful behaviors. Try adjusting NEAT settings in `config-feedforward.txt`.
- **No track found (random spawning issue)**: Ensure the track is black on a white background. The car spawns on black pixels.
- **Monotonous movement or spinning**: Modify the reward/punishment system in `calculate_reward()` in `main.py`.


