from typing import AbstractSet, Union, Dict, Tuple

import pddl.logic.base as logic
from pddl.logic import Predicate

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

    def __call__(self, state: AbstractSet[logic.Formula], goal: logic.Formula) -> float:
        state_positions = self.get_positions(state)
        goal_positions = self.get_positions(goal)

        distance = 0
        for tile, (i, j) in state_positions.items():
            goal_i, goal_j = goal_positions[tile]
            distance += abs(i - goal_i) + abs(j - goal_j)

        return distance

    def get_positions(self, state: Union[AbstractSet[logic.Formula], logic.Formula]) -> \
            Dict[str, Tuple[int, int]]:
        """
        Returns a dictionary mapping the name of each tile to its position in the board.
        """
        positions = {}

        if isinstance(state, logic.And):
            state = state.operands
        if isinstance(state, Predicate):
            state = [state]

        for i, row in enumerate(state):
            for j, tile in enumerate(row.terms):
                positions[f"{tile.name}"] = (i, j)
        return positions
