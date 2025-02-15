# settings.py

import pygame
import sys
import random
import neat


# Window and Car Settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
CAR_SIZE = 50

# NEAT Settings
NEAT_CONFIG = {
     # General NEAT settings
    'fitness_criterion': 'max',
    'fitness_threshold': 500,
    'pop_size': 50,
    'reset_on_extinction': False,

    # Genome settings (defines the structure of neural networks)
    'num_inputs': 4,                # Number of sensors/input nodes for the car (adjust based on your setup)
    'num_outputs': 4,               # Number of movement outputs (left, right, up, down)
    'initial_connection': 'full',   # Start with a fully connected network
    'max_nodes': 100,               # Maximum number of nodes in the network
    'max_connections': 200,         # Maximum number of connections in the network

    # Node and connection mutation settings
    'node_add_prob': 0.2,           # Probability of adding a new node
    'node_delete_prob': 0.2,        # Probability of deleting an existing node
    'connection_add_prob': 0.5,     # Probability of adding a new connection
    'connection_delete_prob': 0.3,  # Probability of deleting an existing connection

    # Mutation rates
    'bias_mutate_rate': 0.7,
    'weight_mutate_rate': 0.8,      # Probability of mutating a weight
    'weight_replace_rate': 0.1,     # Probability of completely replacing a weight
    'weight_max_value': 5.0,        # Maximum value of a weight
    'weight_min_value': -5.0,       # Minimum value of a weight

    # Node activation settings
    'activation_default': 'tanh',
    'activation_mutate_rate': 0.1,
    'activation_options': ['tanh', 'sigmoid', 'relu'],  # Various activations for diverse learning

    # Compatibility and speciation settings
    'compatibility_threshold': 3.0,         # Threshold for dividing species
    'compatibility_disjoint_coefficient': 1.0,
    'compatibility_weight_coefficient': 0.5,

    # Stagnation settings
    'max_stagnation': 15,            # Maximum generations without fitness improvement before a species is extinct
    'species_elitism': 2,            # Number of top-performing genomes per species to keep

    # Crossover settings
    'crossover_prob': 0.75     
}
