
from typing import AbstractSet

import pddl.logic.base as logic

from planification_automatique.heuristic import Heuristic


class ManhattanDistanceHeuristic(Heuristic):
    """
    To compute the Manhattan distance between two states, 
    we need to calculate the sum of the distances between each tile in the current state 
    and its corresponding tile in the goal state. The distance between two tiles is calculated 
    as the sum of the absolute differences in their row and column positions.
    """
    def __init__(self):
        super().__init__()

    def __call__(self, state: AbstractSet[logic.Formula], goal: logic.Formula):
        return 1



def manhattan_distance(current_state, goal_state):
    # Create dictionaries to map each tile to its position in the states
    current_dict = {}
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            current_dict[current_state[i][j]] = (i, j)
            
    goal_dict = {}
    for i in range(len(goal_state)):
        for j in range(len(goal_state[i])):
            goal_dict[goal_state[i][j]] = (i, j)
            
    # Calculate the Manhattan distance for each tile
    distance = 0
    for tile in current_dict:
        current_pos = current_dict[tile]
        goal_pos = goal_dict[tile]
        distance += abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])
        
    # Return the total Manhattan distance
    return distance

# Example usage
goal_state = [['w', 'r', 'b'], ['w', 'o', 'b'], ['y', 'r', 'b'], ['y', 'o', 'b'], ['w', 'r', 'g'], ['w', 'o', 'g'], ['y', 'r', 'g'], ['y', 'o', 'g']]
current_state0 = [['o', 'b', 'y'], ['r', 'g', 'w'], ['y', 'r', 'b'], ['b', 'o', 'w'], ['y', 'o', 'g'], ['r', 'b', 'w'], ['w', 'o', 'g'], ['r', 'y', 'g']]
current_state1 = [['o', 'b', 'w'], ['o', 'b', 'w'], ['r', 'g', 'w'], ['r', 'b', 'w'], ['b', 'o', 'y'], ['b', 'r', 'y'], ['g', 'o', 'y'], ['g', 'r', 'y']]

distance0 = manhattan_distance(current_state0, goal_state)
distance1 = manhattan_distance(current_state1, goal_state)
print(distance0, distance1)
