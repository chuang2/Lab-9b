#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Charles Huang
"""

import random  # Import the random module for shuffling and random choices

# Parameters for the world and agents
world_size = (10, 10)  # Size of the world grid (10x10)
num_agents = 20  # Number of agents in the world
same_pref = 0.3  # Preference for similar neighbors (30%)
max_iter = 10  # Maximum number of iterations for the simulation

#1. create agent class

class Agent():
    def __init__(self, world, kind, same_pref):
        self.world = world  # The world the agent lives in
        self.kind = kind  # The type of the agent (e.g., 'red' or 'blue')
        self.same_pref = same_pref  # Preference for similar neighbors
        self.location = None  # Initial location of the agent (to be assigned later)

    def move(self):
        if not self.am_i_happy():  # Check if the agent is unhappy
            vacancies = self.world.find_vacant()  # Find all empty spots in the world
            if vacancies:  # If there are vacant spots
                new_loc = random.choice(vacancies)  # choose a random vacant spot
                self.world.grid[self.location] = None  # Vacate the current spot
                self.location = new_loc  # Move to the new spot
                self.world.grid[new_loc] = self  # Update the world grid with the new location

    def am_i_happy(self):
        neighbors = self.world.get_neighbors(self.location)  # Get all neighboring agents
        same_kind_neighbors = sum(1 for neighbor in neighbors if neighbor.kind == self.kind)  # Count same-kind neighbors
        if len(neighbors) == 0:  # If there are no neighbors
            return False  # The agent is unhappy
        return same_kind_neighbors / len(neighbors) >= self.same_pref  # Check if the proportion of same-kind neighbors meets the preference

#2. create World class

class World():
    def __init__(self, size, num_agents, same_pref):
        self.size = size  # Size of the world grid
        self.grid = {(i, j): None for i in range(size[0]) for j in range(size[1])}  # Initialize the grid with all positions empty
        self.agents = [Agent(self, kind='red' if i < num_agents // 2 else 'blue', same_pref=same_pref) for i in range(num_agents)]  # Create agents with 'red' or 'blue' kind
        self.init_world()  # Initialize the world with agents placed in it

    def init_world(self):
        locations = list(self.grid.keys())  # get all possible grid locations
        random.shuffle(locations)  # shuffle the locations 
        for agent, loc in zip(self.agents, locations[:len(self.agents)]):  # Assign a random location to each agent
            self.grid[loc] = agent  # place the agent on the grid
            agent.location = loc  # set agent location

    def find_vacant(self):
        return [loc for loc, agent in self.grid.items() if agent is None]  # Return a list of vacant spots on the grid

    def get_neighbors(self, loc):
        x, y = loc  # Get the x, y coordinates of the current location
        neighbors = [(x+i, y+j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)]  # Get all neighboring coordinates
        neighbors = [(i % self.size[0], j % self.size[1]) for i, j in neighbors]  # Wrap around edges of the grid 
        return [self.grid[n] for n in neighbors if self.grid[n] is not None]  # Return a list of non-empty neighboring agents

    def run(self, max_iter):
        for _ in range(max_iter):  # Run the simulation for a maximum number of iterations
            random.shuffle(self.agents)  # Shuffle agents randomly each iteration
            for agent in self.agents:  # For each agent
                agent.move()  # Attempt to move if unhappy
            if all(agent.am_i_happy() for agent in self.agents):  # Check if all agents are happy
                print('All agents are happy.')  # Print message if all agents are happy
                break  # Exit the loop if all agents are happy

#3. Initialize the world
world = World(world_size, num_agents, same_pref)  

#4. Run the loop

world.run(max_iter)  # Run the simulation
